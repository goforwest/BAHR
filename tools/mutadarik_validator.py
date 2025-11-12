#!/usr/bin/env python3
"""
المتدارك (al-Mutadārak) Annotation Validation Tool

Purpose: Validate candidate المتدارك verses before adding to golden set
Usage:
    python mutadarik_validator.py --verse "verse text" --tafail "فاعلن,فعلن,فاعلن,فاع"
    python mutadarik_validator.py --file candidate_verses.jsonl

Features:
- Tafʿīla pattern validation
- Ziḥāfāt compliance checking
- Disambiguation from الرجز
- Confidence scoring
- Comprehensive validation reports

Author: BAHR Detection Engine Team
Date: 2025-11-12
Version: 1.0
"""

import sys
import json
import argparse
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Add backend to path
sys.path.insert(0, '/home/user/BAHR/backend')

from app.core.prosody.meters import METERS_REGISTRY, AL_MUTADARIK, AL_RAJAZ
from app.core.prosody.detector_v2 import BahrDetectorV2
from app.core.prosody.zihafat import KHABN
from app.core.prosody.ilal import HADHF, QASR


class ValidationStatus(Enum):
    """Validation result status"""
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    NEEDS_REVIEW = "NEEDS_REVIEW"


@dataclass
class ValidationResult:
    """Comprehensive validation result for a single verse"""
    verse_id: str
    status: ValidationStatus
    is_valid_mutadarik: bool
    confidence: float
    errors: List[str]
    warnings: List[str]
    checks: Dict[str, bool]
    detected_meter: Optional[str]
    detected_pattern: Optional[str]
    confusion_risk: Dict[str, float]
    disambiguation_notes: str
    recommendations: List[str]

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        result['status'] = self.status.value
        return result

    def print_report(self):
        """Print human-readable validation report"""
        print("\n" + "="*80)
        print(f"VALIDATION REPORT: {self.verse_id}")
        print("="*80)

        # Status
        status_symbol = {
            ValidationStatus.PASSED: "✅",
            ValidationStatus.FAILED: "❌",
            ValidationStatus.WARNING: "⚠️",
            ValidationStatus.NEEDS_REVIEW: "🔍"
        }
        print(f"\nStatus: {status_symbol[self.status]} {self.status.value}")
        print(f"Valid المتدارك: {'YES' if self.is_valid_mutadarik else 'NO'}")
        print(f"Confidence: {self.confidence:.2%}")

        # Detected meter
        if self.detected_meter:
            print(f"\nDetected Meter: {self.detected_meter}")
            print(f"Pattern: {self.detected_pattern}")

        # Validation checks
        print("\nValidation Checks:")
        for check, passed in self.checks.items():
            symbol = "✓" if passed else "✗"
            print(f"  {symbol} {check}")

        # Errors
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")

        # Warnings
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")

        # Confusion risk
        if self.confusion_risk:
            print("\n🔍 CONFUSION RISK:")
            for meter, risk in sorted(self.confusion_risk.items(), key=lambda x: x[1], reverse=True):
                if risk > 0.3:  # Only show significant risks
                    print(f"  - {meter}: {risk:.1%}")

        # Disambiguation
        if self.disambiguation_notes:
            print("\n📝 DISAMBIGUATION NOTES:")
            print(f"  {self.disambiguation_notes}")

        # Recommendations
        if self.recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for rec in self.recommendations:
                print(f"  - {rec}")

        print("\n" + "="*80 + "\n")


class MutadarikValidator:
    """Validator for المتدارك verses"""

    # Valid tafāʿīl for المتدارك
    VALID_TAFAIL = {
        "فاعلن": "/o//o",      # Base form
        "فعلن": "///o",        # After khabn
        "فاع": "/o/",          # After ḥadhf
        "فاعل": "/o///",       # After qaṣr
        "فعل": "///",          # After khabn + ḥadhf (rare)
    }

    # Expected tafʿīla count
    EXPECTED_TAFAIL_COUNT = 4

    def __init__(self):
        """Initialize validator with detection engine"""
        self.detector = BahrDetectorV2()
        # Access patterns from detector's pattern cache
        self.mutadarik_patterns = self.detector.pattern_cache.get(16, set())  # المتدارك ID = 16
        self.rajaz_patterns = self.detector.pattern_cache.get(5, set())  # الرجز ID = 5

    def validate(
        self,
        verse_id: str,
        text: str,
        expected_tafail: List[str],
        phonetic_pattern: Optional[str] = None
    ) -> ValidationResult:
        """
        Validate a candidate المتدارك verse

        Args:
            verse_id: Unique verse identifier
            text: Original Arabic text
            expected_tafail: List of expected tafāʿīl (e.g., ["فاعلن", "فعلن", "فاعلن", "فاع"])
            phonetic_pattern: Optional phonetic pattern (will be detected if not provided)

        Returns:
            ValidationResult with comprehensive validation information
        """
        errors = []
        warnings = []
        checks = {}
        recommendations = []
        confusion_risk = {}

        # Check 1: Tafʿīla count
        checks["tafail_count"] = len(expected_tafail) == self.EXPECTED_TAFAIL_COUNT
        if not checks["tafail_count"]:
            errors.append(
                f"Invalid tafʿīla count: expected {self.EXPECTED_TAFAIL_COUNT}, "
                f"got {len(expected_tafail)}"
            )

        # Check 2: Valid tafāʿīl
        invalid_tafail = [t for t in expected_tafail if t not in self.VALID_TAFAIL]
        checks["valid_tafail"] = len(invalid_tafail) == 0
        if not checks["valid_tafail"]:
            errors.append(
                f"Invalid tafāʿīl found: {invalid_tafail}. "
                f"Valid tafāʿīl for المتدارك: {list(self.VALID_TAFAIL.keys())}"
            )

        # Check 3: Ziḥāfāt compliance (positions 1-3: khabn only)
        checks["zihafat_compliance"] = self._check_zihafat_compliance(expected_tafail)
        if not checks["zihafat_compliance"]:
            warnings.append(
                "Non-standard ziḥāfāt detected. المتدارك only allows خبن in positions 1-3."
            )

        # Check 4: ʿIlal compliance (position 4: ḥadhf or qaṣr only)
        checks["ilal_compliance"] = self._check_ilal_compliance(expected_tafail)
        if not checks["ilal_compliance"]:
            warnings.append(
                "Non-standard ʿilal detected. المتدارك only allows حذف or قصر in final position."
            )

        # Check 5: Pattern matching
        if phonetic_pattern is None and checks["valid_tafail"]:
            # Generate pattern from tafāʿīl
            phonetic_pattern = "".join(self.VALID_TAFAIL[t] for t in expected_tafail)

        detected_meter = None
        detected_pattern = None
        confidence = 0.0

        if phonetic_pattern:
            # Run detection
            results = self.detector.detect(phonetic_pattern, top_k=5)

            if results:
                detected_meter = results[0].meter_name_ar
                detected_pattern = results[0].matched_pattern
                confidence = results[0].confidence

                # Check if top detection is المتدارك
                checks["pattern_match"] = detected_meter == "المتدارك"

                if not checks["pattern_match"]:
                    errors.append(
                        f"Pattern does NOT match المتدارك. Detected: {detected_meter} "
                        f"(confidence: {results[0].confidence:.2%})"
                    )

                # Build confusion risk
                for result in results:
                    confusion_risk[result.meter_name_ar] = result.confidence
            else:
                checks["pattern_match"] = False
                errors.append("Pattern does not match any known meter")
        else:
            checks["pattern_match"] = False
            errors.append("Cannot validate pattern - phonetic pattern not provided or invalid tafāʿīl")

        # Check 6: Disambiguation from الرجز
        disambiguation_notes = self._disambiguate_mutadarik_vs_rajaz(
            phonetic_pattern, expected_tafail, confusion_risk
        )

        # Check for high الرجز confusion
        rajaz_risk = confusion_risk.get("الرجز", 0.0)
        checks["rajaz_disambiguation"] = rajaz_risk < 0.5 or detected_meter == "المتدارك"

        if rajaz_risk > 0.7 and detected_meter != "المتدارك":
            errors.append(
                f"HIGH CONFUSION RISK with الرجز (risk: {rajaz_risk:.1%}). "
                "This verse may actually be الرجز, not المتدارك."
            )
        elif rajaz_risk > 0.4:
            warnings.append(
                f"Moderate confusion risk with الرجز (risk: {rajaz_risk:.1%}). "
                "Recommend expert review for disambiguation."
            )

        # Overall validation status
        all_checks_passed = all(checks.values())
        has_errors = len(errors) > 0
        has_warnings = len(warnings) > 0

        if all_checks_passed and not has_errors:
            status = ValidationStatus.PASSED
            is_valid = True
            recommendations.append("✅ Verse is valid for golden set inclusion")
        elif has_errors:
            status = ValidationStatus.FAILED
            is_valid = False
            recommendations.append("❌ Verse MUST NOT be added to golden set")
            recommendations.append("Fix errors before re-submission")
        elif has_warnings:
            status = ValidationStatus.NEEDS_REVIEW
            is_valid = False
            recommendations.append("⚠️  Verse requires expert review before inclusion")
            recommendations.append("Address warnings and obtain 2+ expert confirmations")
        else:
            status = ValidationStatus.WARNING
            is_valid = False
            recommendations.append("🔍 Review recommended before final approval")

        # Confidence threshold check
        if confidence < 0.85 and status == ValidationStatus.PASSED:
            status = ValidationStatus.NEEDS_REVIEW
            warnings.append(
                f"Low confidence ({confidence:.2%}). Recommend expert verification."
            )
            recommendations.append("Obtain expert confirmation due to low confidence")

        return ValidationResult(
            verse_id=verse_id,
            status=status,
            is_valid_mutadarik=is_valid,
            confidence=confidence,
            errors=errors,
            warnings=warnings,
            checks=checks,
            detected_meter=detected_meter,
            detected_pattern=detected_pattern,
            confusion_risk=confusion_risk,
            disambiguation_notes=disambiguation_notes,
            recommendations=recommendations
        )

    def _check_zihafat_compliance(self, tafail: List[str]) -> bool:
        """
        Check if ziḥāfāt comply with المتدارك rules
        Positions 1-3: Only خبن (فاعلن → فعلن) allowed
        """
        # For positions 1-3, only base form (فاعلن) or khabn form (فعلن) allowed
        for i, tafila in enumerate(tafail[:3]):  # First 3 positions
            if tafila not in ["فاعلن", "فعلن"]:
                return False
        return True

    def _check_ilal_compliance(self, tafail: List[str]) -> bool:
        """
        Check if ʿilal comply with المتدارك rules
        Position 4: Only حذف (فاعلن → فاع) or قصر (فاعلن → فاعل) allowed
        """
        if len(tafail) < 4:
            return True  # Skip if not enough tafāʿīl

        final_tafila = tafail[3]
        # Final position can be: فاعلن (base), فعلن (khabn), فاع (ḥadhf), فاعل (qaṣr), فعل (khabn+ḥadhf)
        valid_final = ["فاعلن", "فعلن", "فاع", "فاعل", "فعل"]
        return final_tafila in valid_final

    def _disambiguate_mutadarik_vs_rajaz(
        self,
        phonetic_pattern: Optional[str],
        tafail: List[str],
        confusion_risk: Dict[str, float]
    ) -> str:
        """
        Generate disambiguation notes explaining why this is المتدارك and not الرجز
        """
        notes = []

        # Count-based disambiguation
        if len(tafail) == 4:
            notes.append(
                f"✓ Tafʿīla count = {len(tafail)} (المتدارك uses 4 تفاعيل, "
                "الرجز typically uses 3)"
            )
        elif len(tafail) == 3:
            notes.append(
                f"⚠ Tafʿīla count = {len(tafail)} - AMBIGUOUS. Could be الرجز. "
                "Verify tafʿīla types."
            )

        # Tafʿīla type analysis
        has_فاعلن = "فاعلن" in tafail or "فعلن" in tafail
        has_مستفعلن_indicator = len(tafail) == 3  # Rough heuristic

        if has_فاعلن:
            notes.append(
                "✓ Tafāʿīl match فاعلن pattern (characteristic of المتدارك)"
            )

        # Confusion risk analysis
        rajaz_risk = confusion_risk.get("الرجز", 0.0)
        mutadarik_risk = confusion_risk.get("المتدارك", 0.0)

        if mutadarik_risk > rajaz_risk:
            notes.append(
                f"✓ Detection confidence: المتدارك ({mutadarik_risk:.1%}) > "
                f"الرجز ({rajaz_risk:.1%})"
            )
        elif rajaz_risk > mutadarik_risk:
            notes.append(
                f"⚠ WARNING: Detection suggests الرجز ({rajaz_risk:.1%}) > "
                f"المتدارك ({mutadarik_risk:.1%}). REVIEW REQUIRED."
            )

        # Pattern analysis
        if phonetic_pattern and len(phonetic_pattern) == 16:
            notes.append(
                f"✓ Pattern length = {len(phonetic_pattern)} syllables "
                "(matches 4×فاعلن structure)"
            )

        return " | ".join(notes) if notes else "No disambiguation notes available"

    def validate_batch(self, verses: List[Dict]) -> List[ValidationResult]:
        """
        Validate multiple verses from JSONL format

        Args:
            verses: List of verse dictionaries with keys:
                    - verse_id, text, expected_tafail, phonetic_pattern (optional)

        Returns:
            List of ValidationResult objects
        """
        results = []
        for verse in verses:
            result = self.validate(
                verse_id=verse.get("verse_id", "unknown"),
                text=verse.get("text", ""),
                expected_tafail=verse.get("expected_tafail", []),
                phonetic_pattern=verse.get("phonetic_pattern")
            )
            results.append(result)
        return results


def main():
    """Command-line interface for validator"""
    parser = argparse.ArgumentParser(
        description="Validate المتدارك verses before adding to golden set"
    )
    parser.add_argument(
        "--verse",
        help="Verse text (Arabic)"
    )
    parser.add_argument(
        "--tafail",
        help="Expected tafāʿīl (comma-separated, e.g., 'فاعلن,فعلن,فاعلن,فاع')"
    )
    parser.add_argument(
        "--pattern",
        help="Optional phonetic pattern (e.g., '/o//o///o/o//o/o/')"
    )
    parser.add_argument(
        "--file",
        help="Path to JSONL file with candidate verses"
    )
    parser.add_argument(
        "--output",
        help="Output path for validation results (JSON)"
    )

    args = parser.parse_args()

    validator = MutadarikValidator()

    if args.file:
        # Batch validation from file
        print(f"Loading verses from: {args.file}")
        verses = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f:
                verses.append(json.loads(line))

        print(f"Validating {len(verses)} verses...")
        results = validator.validate_batch(verses)

        # Print reports
        for result in results:
            result.print_report()

        # Summary
        passed = sum(1 for r in results if r.status == ValidationStatus.PASSED)
        failed = sum(1 for r in results if r.status == ValidationStatus.FAILED)
        needs_review = sum(1 for r in results if r.status == ValidationStatus.NEEDS_REVIEW)

        print("\n" + "="*80)
        print("BATCH VALIDATION SUMMARY")
        print("="*80)
        print(f"Total verses: {len(results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"🔍 Needs review: {needs_review}")
        print("="*80 + "\n")

        # Save results if output specified
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump([r.to_dict() for r in results], f, ensure_ascii=False, indent=2)
            print(f"Results saved to: {args.output}")

    elif args.verse and args.tafail:
        # Single verse validation
        tafail_list = args.tafail.split(',')
        result = validator.validate(
            verse_id="cli_verse",
            text=args.verse,
            expected_tafail=tafail_list,
            phonetic_pattern=args.pattern
        )
        result.print_report()

        # Save if output specified
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
            print(f"Result saved to: {args.output}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
