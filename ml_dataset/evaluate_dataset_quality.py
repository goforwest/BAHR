#!/usr/bin/env python3
"""
Arabic Prosody Dataset Quality Evaluation System
Senior Arabic NLP Researcher | Dataset Quality Engineer | ʿArūḍ Specialist

Comprehensive 7-phase evaluation following ARABIC_PROSODY_ML_DATASET_BLUEPRINT.md

Phases:
1. Dataset Normalization & Ingestion
2. Three-Level Deduplication (Exact/Fuzzy/Prosodic)
3. Cross-Meter Anomaly Detection
4. Poet Distribution Analysis
5. Metadata Validation
6. Report Generation
7. Deduplicated Dataset Production
"""

import json
import re
import hashlib
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Tuple, Set
from difflib import SequenceMatcher
import unicodedata

# ============================================================================
# PHASE 1: TEXT NORMALIZATION (Blueprint-Compliant)
# ============================================================================

class ArabicTextNormalizer:
    """Blueprint-compliant Arabic text normalization"""
    
    @staticmethod
    def normalize(text: str) -> str:
        """Apply all normalization rules from blueprint"""
        if not text:
            return ""
        
        # Remove tatweel/kashida
        text = text.replace('\u0640', '')
        
        # Normalize hamza forms
        text = re.sub('[إأآا]', 'ا', text)
        text = re.sub('[ئؤ]', 'ء', text)
        
        # Normalize alif maqsura and ya
        text = text.replace('ى', 'ي')
        
        # Normalize taa marbouta
        text = text.replace('ة', 'ه')
        
        # Remove all diacritics
        text = re.sub('[\u064B-\u065F]', '', text)  # Tashkeel
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove punctuation for comparison
        text = re.sub('[،؛؟!.:;,?!]', '', text)
        
        return text
    
    @staticmethod
    def get_fingerprint(text: str) -> str:
        """Generate normalized fingerprint for exact matching"""
        normalized = ArabicTextNormalizer.normalize(text)
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()
    
    @staticmethod
    def similarity(text1: str, text2: str) -> float:
        """Calculate fuzzy similarity between two texts"""
        norm1 = ArabicTextNormalizer.normalize(text1)
        norm2 = ArabicTextNormalizer.normalize(text2)
        return SequenceMatcher(None, norm1, norm2).ratio()


# ============================================================================
# PHASE 1: DATASET LOADER
# ============================================================================

class DatasetLoader:
    """Load and index all JSONL files"""
    
    def __init__(self, dataset_dir: str = "."):
        self.dataset_dir = Path(dataset_dir)
        self.verses = []
        self.normalizer = ArabicTextNormalizer()
        
    def load_all_batches(self) -> List[Dict]:
        """Load all JSONL files from dataset directory"""
        jsonl_files = sorted(self.dataset_dir.glob("*.jsonl"))
        
        print(f"{'='*70}")
        print(f"PHASE 1: DATASET NORMALIZATION & INGESTION")
        print(f"{'='*70}")
        print(f"Found {len(jsonl_files)} JSONL batch files")
        
        verse_count = 0
        for jsonl_file in jsonl_files:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    try:
                        verse = json.loads(line)
                        # Add normalized text and fingerprint
                        verse['normalized_text_eval'] = self.normalizer.normalize(verse.get('text', ''))
                        verse['fingerprint'] = self.normalizer.get_fingerprint(verse.get('text', ''))
                        verse['source_file'] = jsonl_file.name
                        verse['source_line'] = line_num
                        self.verses.append(verse)
                        verse_count += 1
                    except json.JSONDecodeError as e:
                        print(f"⚠️  JSON error in {jsonl_file.name}:{line_num}: {e}")
        
        print(f"✅ Loaded {verse_count} verses")
        print(f"✅ Applied blueprint normalization to all texts")
        print()
        return self.verses


# ============================================================================
# PHASE 2: THREE-LEVEL DEDUPLICATION
# ============================================================================

class DeduplicationAnalyzer:
    """Three-level duplicate detection system"""
    
    def __init__(self, verses: List[Dict]):
        self.verses = verses
        self.duplicates = {
            'exact': [],
            'fuzzy': [],
            'prosodic': []
        }
        self.normalizer = ArabicTextNormalizer()
    
    def analyze(self) -> Dict:
        """Run all three deduplication levels"""
        print(f"{'='*70}")
        print(f"PHASE 2: THREE-LEVEL DEDUPLICATION ANALYSIS")
        print(f"{'='*70}")
        
        self._detect_exact_duplicates()
        self._detect_fuzzy_duplicates()
        self._detect_prosodic_duplicates()
        
        return self.duplicates
    
    def _detect_exact_duplicates(self):
        """Level A: Exact text duplication"""
        print("Level A: Exact-text duplication detection...")
        fingerprint_map = defaultdict(list)
        
        for idx, verse in enumerate(self.verses):
            fp = verse['fingerprint']
            fingerprint_map[fp].append(idx)
        
        exact_count = 0
        for fp, indices in fingerprint_map.items():
            if len(indices) > 1:
                verses_group = [self.verses[i] for i in indices]
                self.duplicates['exact'].append({
                    'type': 'exact',
                    'count': len(indices),
                    'verse_ids': [v['verse_id'] for v in verses_group],
                    'text': verses_group[0]['text'],
                    'normalized': verses_group[0]['normalized_text_eval'],
                    'meters': [v.get('meter_id') for v in verses_group],
                    'poets': [v.get('poet') for v in verses_group],
                    'sources': [v['source_file'] for v in verses_group],
                    'indices': indices
                })
                exact_count += len(indices) - 1  # Duplicates = total - 1
        
        print(f"  Found {len(self.duplicates['exact'])} exact duplicate groups")
        print(f"  Total redundant verses: {exact_count}")
        print()
    
    def _detect_fuzzy_duplicates(self):
        """Level B: Fuzzy similarity detection (≥90%)"""
        print("Level B: Fuzzy-similarity detection (≥90% threshold)...")
        
        threshold = 0.90
        checked_pairs = set()
        fuzzy_count = 0
        
        for i, verse1 in enumerate(self.verses):
            for j, verse2 in enumerate(self.verses[i+1:], i+1):
                pair_key = (min(i, j), max(i, j))
                if pair_key in checked_pairs:
                    continue
                
                # Skip if already exact duplicate
                if verse1['fingerprint'] == verse2['fingerprint']:
                    continue
                
                similarity = self.normalizer.similarity(verse1['text'], verse2['text'])
                
                if similarity >= threshold:
                    self.duplicates['fuzzy'].append({
                        'type': 'fuzzy',
                        'similarity': similarity,
                        'verse_ids': [verse1['verse_id'], verse2['verse_id']],
                        'texts': [verse1['text'], verse2['text']],
                        'meters': [verse1.get('meter_id'), verse2.get('meter_id')],
                        'poets': [verse1.get('poet'), verse2.get('poet')],
                        'sources': [verse1['source_file'], verse2['source_file']],
                        'indices': [i, j]
                    })
                    checked_pairs.add(pair_key)
                    fuzzy_count += 1
        
        print(f"  Found {len(self.duplicates['fuzzy'])} fuzzy duplicate pairs")
        print()
    
    def _detect_prosodic_duplicates(self):
        """Level C: Prosodic pattern duplication"""
        print("Level C: Prosodic-pattern duplication detection...")
        
        # Group by tafāʿīl sequence
        prosodic_map = defaultdict(list)
        
        for idx, verse in enumerate(self.verses):
            prosody = verse.get('prosody_precomputed', {})
            tafail = tuple(prosody.get('tafail_sequence', []))
            
            if tafail:
                prosodic_map[tafail].append(idx)
        
        prosodic_count = 0
        for tafail_seq, indices in prosodic_map.items():
            if len(indices) > 1:
                # Check for semantic similarity within same prosodic pattern
                for i in range(len(indices)):
                    for j in range(i+1, len(indices)):
                        v1 = self.verses[indices[i]]
                        v2 = self.verses[indices[j]]
                        
                        # Skip if same meter (expected to have same pattern)
                        if v1.get('meter_id') == v2.get('meter_id'):
                            continue
                        
                        # Check semantic similarity
                        sim = self.normalizer.similarity(v1['text'], v2['text'])
                        if sim >= 0.70:  # Lower threshold for prosodic
                            self.duplicates['prosodic'].append({
                                'type': 'prosodic',
                                'similarity': sim,
                                'tafail_sequence': list(tafail_seq),
                                'verse_ids': [v1['verse_id'], v2['verse_id']],
                                'texts': [v1['text'], v2['text']],
                                'meters': [v1.get('meter_id'), v2.get('meter_id')],
                                'poets': [v1.get('poet'), v2.get('poet')],
                                'indices': [indices[i], indices[j]]
                            })
                            prosodic_count += 1
        
        print(f"  Found {len(self.duplicates['prosodic'])} prosodic duplicates")
        print()


# ============================================================================
# PHASE 3: CROSS-METER ANOMALY DETECTION
# ============================================================================

class CrossMeterAnalyzer:
    """Detect verses appearing in multiple meters"""
    
    def __init__(self, verses: List[Dict]):
        self.verses = verses
        self.anomalies = []
    
    def analyze(self) -> List[Dict]:
        """Detect cross-meter verse repetition"""
        print(f"{'='*70}")
        print(f"PHASE 3: CROSS-METER ANOMALY DETECTION")
        print(f"{'='*70}")
        
        fingerprint_meter_map = defaultdict(set)
        
        for verse in self.verses:
            fp = verse['fingerprint']
            meter_id = verse.get('meter_id')
            fingerprint_meter_map[fp].add((meter_id, verse['verse_id']))
        
        for fp, meter_verse_set in fingerprint_meter_map.items():
            meters = {m for m, _ in meter_verse_set}
            if len(meters) > 1:
                verse_ids = [v for _, v in meter_verse_set]
                # Find one example
                example = next(v for v in self.verses if v['fingerprint'] == fp)
                self.anomalies.append({
                    'fingerprint': fp,
                    'text': example['text'],
                    'meters': sorted(meters),
                    'verse_ids': verse_ids,
                    'count': len(meter_verse_set)
                })
        
        print(f"Found {len(self.anomalies)} verses appearing in multiple meters")
        print()
        return self.anomalies


# ============================================================================
# PHASE 4: POET DISTRIBUTION ANALYSIS
# ============================================================================

class PoetDistributionAnalyzer:
    """Analyze poet representation and detect imbalances"""
    
    def __init__(self, verses: List[Dict]):
        self.verses = verses
        self.distribution = {}
        self.imbalances = []
    
    def analyze(self) -> Dict:
        """Calculate poet distribution per meter"""
        print(f"{'='*70}")
        print(f"PHASE 4: POET DISTRIBUTION ANALYSIS")
        print(f"{'='*70}")
        
        meter_poet_counts = defaultdict(lambda: defaultdict(int))
        meter_totals = defaultdict(int)
        
        for verse in self.verses:
            meter_id = verse.get('meter_id')
            poet = verse.get('poet', 'Unknown')
            meter_poet_counts[meter_id][poet] += 1
            meter_totals[meter_id] += 1
        
        # Detect imbalances (>5% tolerance)
        tolerance = 0.05
        
        for meter_id, poet_counts in meter_poet_counts.items():
            total = meter_totals[meter_id]
            self.distribution[meter_id] = {}
            
            for poet, count in poet_counts.items():
                percentage = count / total
                self.distribution[meter_id][poet] = {
                    'count': count,
                    'percentage': percentage
                }
                
                if percentage > tolerance:
                    self.imbalances.append({
                        'meter_id': meter_id,
                        'poet': poet,
                        'count': count,
                        'percentage': percentage,
                        'total_verses': total,
                        'threshold_exceeded': percentage - tolerance
                    })
        
        print(f"Analyzed {len(meter_poet_counts)} meters")
        print(f"Found {len(self.imbalances)} poet imbalances exceeding 5% threshold")
        print()
        return self.distribution


# ============================================================================
# PHASE 5: METADATA VALIDATION
# ============================================================================

class MetadataValidator:
    """Validate tafāʿīl, poet attribution, era, and source metadata"""
    
    def __init__(self, verses: List[Dict]):
        self.verses = verses
        self.errors = []
    
    def analyze(self) -> List[Dict]:
        """Validate all metadata fields"""
        print(f"{'='*70}")
        print(f"PHASE 5: METADATA VALIDATION")
        print(f"{'='*70}")
        
        required_fields = ['verse_id', 'text', 'meter_id', 'poet', 'prosody_precomputed']
        
        for idx, verse in enumerate(self.verses):
            # Check required fields
            for field in required_fields:
                if field not in verse or not verse[field]:
                    self.errors.append({
                        'verse_id': verse.get('verse_id', f'index_{idx}'),
                        'error_type': 'missing_field',
                        'field': field,
                        'source': verse.get('source_file')
                    })
            
            # Validate prosody structure
            prosody = verse.get('prosody_precomputed', {})
            if 'tafail_sequence' not in prosody or not prosody['tafail_sequence']:
                self.errors.append({
                    'verse_id': verse.get('verse_id'),
                    'error_type': 'invalid_tafail',
                    'message': 'Missing or empty tafāʿīl sequence',
                    'source': verse.get('source_file')
                })
            
            # Check confidence score
            if prosody.get('confidence', 0) < 0.95:
                self.errors.append({
                    'verse_id': verse.get('verse_id'),
                    'error_type': 'low_confidence',
                    'confidence': prosody.get('confidence'),
                    'source': verse.get('source_file')
                })
        
        print(f"Found {len(self.errors)} metadata validation errors")
        print()
        return self.errors


# ============================================================================
# PHASE 6: REPORT GENERATION
# ============================================================================

class ReportGenerator:
    """Generate comprehensive quality evaluation report"""
    
    def __init__(self, verses, duplicates, anomalies, distribution, imbalances, errors):
        self.verses = verses
        self.duplicates = duplicates
        self.anomalies = anomalies
        self.distribution = distribution
        self.imbalances = imbalances
        self.errors = errors
    
    def generate(self, output_file: str = "DATASET_QUALITY_EVALUATION_REPORT.md"):
        """Generate markdown report"""
        print(f"{'='*70}")
        print(f"PHASE 6: REPORT GENERATION")
        print(f"{'='*70}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_report_content())
        
        print(f"✅ Report generated: {output_file}")
        print()
        return output_file
    
    def _generate_report_content(self) -> str:
        """Generate report markdown content"""
        report = []
        
        # Header
        report.append("# Arabic Prosody Dataset Quality Evaluation Report\n")
        report.append(f"**Evaluation Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**Evaluator:** Senior Arabic NLP Researcher | Dataset Quality Engineer | ʿArūḍ Specialist\n")
        report.append(f"**Dataset Size:** {len(self.verses)} verses\n")
        report.append(f"**Methodology:** 7-Phase Blueprint-Compliant Evaluation\n\n")
        report.append("---\n\n")
        
        # Executive Summary
        report.append("## Executive Summary\n\n")
        exact_dups = len(self.duplicates['exact'])
        fuzzy_dups = len(self.duplicates['fuzzy'])
        prosodic_dups = len(self.duplicates['prosodic'])
        total_redundant = sum(d['count']-1 for d in self.duplicates['exact'])
        
        report.append(f"- **Total Verses Evaluated:** {len(self.verses)}\n")
        report.append(f"- **Exact Duplicates:** {exact_dups} groups ({total_redundant} redundant verses)\n")
        report.append(f"- **Fuzzy Duplicates:** {fuzzy_dups} pairs (≥90% similarity)\n")
        report.append(f"- **Prosodic Duplicates:** {prosodic_dups} pairs\n")
        report.append(f"- **Cross-Meter Anomalies:** {len(self.anomalies)} verses\n")
        report.append(f"- **Poet Imbalances:** {len(self.imbalances)} cases (>5% threshold)\n")
        report.append(f"- **Metadata Errors:** {len(self.errors)} issues\n\n")
        
        unique_verses = len(self.verses) - total_redundant
        report.append(f"**Recommended Dataset Size After Deduplication:** {unique_verses} verses\n\n")
        report.append("---\n\n")
        
        # Phase 2 Results
        report.append("## Phase 2: Deduplication Analysis\n\n")
        report.append("### Level A: Exact Duplicates\n\n")
        
        if self.duplicates['exact']:
            for i, dup in enumerate(self.duplicates['exact'][:10], 1):
                report.append(f"**Group {i}:** {dup['count']} copies\n")
                report.append(f"- Text: `{dup['text'][:100]}...`\n")
                report.append(f"- Verse IDs: {', '.join(dup['verse_ids'])}\n")
                report.append(f"- Meters: {dup['meters']}\n")
                report.append(f"- Poets: {set(dup['poets'])}\n")
                report.append(f"- **Root Cause:** Same verse used multiple times in batch collection\n")
                report.append(f"- **Action:** Keep 1 copy, remove {dup['count']-1} duplicates\n\n")
            
            if len(self.duplicates['exact']) > 10:
                report.append(f"*...and {len(self.duplicates['exact'])-10} more duplicate groups*\n\n")
        else:
            report.append("✅ No exact duplicates found\n\n")
        
        # Fuzzy duplicates
        report.append("### Level B: Fuzzy Duplicates (≥90% similarity)\n\n")
        if self.duplicates['fuzzy']:
            for i, dup in enumerate(self.duplicates['fuzzy'][:5], 1):
                report.append(f"**Pair {i}:** {dup['similarity']:.2%} similarity\n")
                report.append(f"- Verse IDs: {', '.join(dup['verse_ids'])}\n")
                report.append(f"- Text 1: `{dup['texts'][0][:80]}...`\n")
                report.append(f"- Text 2: `{dup['texts'][1][:80]}...`\n")
                report.append(f"- **Action:** Review manually, likely remove one\n\n")
            
            if len(self.duplicates['fuzzy']) > 5:
                report.append(f"*...and {len(self.duplicates['fuzzy'])-5} more fuzzy pairs*\n\n")
        else:
            report.append("✅ No fuzzy duplicates found\n\n")
        
        # Prosodic duplicates
        report.append("### Level C: Prosodic Duplicates\n\n")
        if self.duplicates['prosodic']:
            for i, dup in enumerate(self.duplicates['prosodic'][:5], 1):
                report.append(f"**Pair {i}:** {dup['similarity']:.2%} similarity, identical tafāʿīl\n")
                report.append(f"- Tafāʿīl: {' + '.join(dup['tafail_sequence'])}\n")
                report.append(f"- Meters: {dup['meters']}\n")
                report.append(f"- **Action:** Review for semantic uniqueness\n\n")
        else:
            report.append("✅ No prosodic duplicates found\n\n")
        
        report.append("---\n\n")
        
        # Phase 3 Results
        report.append("## Phase 3: Cross-Meter Anomalies\n\n")
        if self.anomalies:
            for i, anom in enumerate(self.anomalies[:10], 1):
                report.append(f"**Anomaly {i}:** Verse in {len(anom['meters'])} meters\n")
                report.append(f"- Text: `{anom['text'][:100]}...`\n")
                report.append(f"- Meters: {anom['meters']}\n")
                report.append(f"- Verse IDs: {', '.join(anom['verse_ids'])}\n")
                report.append(f"- **Root Cause:** Verse assigned to multiple meters incorrectly\n")
                report.append(f"- **Action:** Keep in correct meter only, remove from others\n\n")
        else:
            report.append("✅ No cross-meter anomalies found\n\n")
        
        report.append("---\n\n")
        
        # Phase 4 Results
        report.append("## Phase 4: Poet Distribution Analysis\n\n")
        if self.imbalances:
            for imb in self.imbalances[:15]:
                report.append(f"- **Meter {imb['meter_id']}:** Poet `{imb['poet']}` = {imb['percentage']:.1%} ")
                report.append(f"({imb['count']}/{imb['total_verses']} verses, ")
                report.append(f"exceeds threshold by {imb['threshold_exceeded']:.1%})\n")
        else:
            report.append("✅ All meters have balanced poet distribution\n\n")
        
        report.append("\n---\n\n")
        
        # Phase 5 Results
        report.append("## Phase 5: Metadata Validation\n\n")
        if self.errors:
            error_types = Counter(e['error_type'] for e in self.errors)
            for error_type, count in error_types.most_common():
                report.append(f"- **{error_type}:** {count} occurrences\n")
        else:
            report.append("✅ No metadata errors found\n\n")
        
        report.append("\n---\n\n")
        
        # Recommendations
        report.append("## Recommendations\n\n")
        report.append("### Immediate Actions\n\n")
        report.append(f"1. **Remove {total_redundant} exact duplicate verses**\n")
        report.append(f"2. **Review and resolve {len(self.duplicates['fuzzy'])} fuzzy duplicate pairs**\n")
        report.append(f"3. **Correct {len(self.anomalies)} cross-meter anomalies**\n")
        report.append(f"4. **Address {len(self.imbalances)} poet imbalance cases**\n")
        report.append(f"5. **Fix {len(self.errors)} metadata validation errors**\n\n")
        
        report.append("### Expected Outcomes\n\n")
        report.append(f"- **Clean Dataset Size:** ~{unique_verses} unique verses\n")
        report.append(f"- **Quality Improvement:** Remove {(total_redundant/len(self.verses)*100):.1f}% redundancy\n")
        report.append(f"- **Meter Balance:** Ensure ≥95 unique verses per meter\n")
        report.append(f"- **Poet Diversity:** <5% concentration per poet per meter\n\n")
        
        return ''.join(report)


# ============================================================================
# PHASE 7: DEDUPLICATED DATASET PRODUCTION
# ============================================================================

class DatasetDeduplicator:
    """Produce clean deduplicated dataset"""
    
    def __init__(self, verses, duplicates):
        self.verses = verses
        self.duplicates = duplicates
        self.keep_indices = set()
    
    def deduplicate(self) -> List[Dict]:
        """Remove duplicates and produce clean dataset"""
        print(f"{'='*70}")
        print(f"PHASE 7: DEDUPLICATED DATASET PRODUCTION")
        print(f"{'='*70}")
        
        # Mark all verses as keep initially
        self.keep_indices = set(range(len(self.verses)))
        
        # Remove exact duplicates (keep first occurrence)
        for dup_group in self.duplicates['exact']:
            indices = dup_group['indices']
            # Keep first, remove rest
            for idx in indices[1:]:
                self.keep_indices.discard(idx)
        
        # Filter verses
        clean_verses = [v for i, v in enumerate(self.verses) if i in self.keep_indices]
        
        print(f"Original dataset: {len(self.verses)} verses")
        print(f"Removed: {len(self.verses) - len(clean_verses)} duplicates")
        print(f"Clean dataset: {len(clean_verses)} verses")
        print()
        
        return clean_verses
    
    def export_batches(self, verses: List[Dict], output_dir: str = "deduplicated", batch_size: int = 50):
        """Export deduplicated dataset in batches"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Group by meter
        meter_verses = defaultdict(list)
        for verse in verses:
            meter_id = verse.get('meter_id')
            meter_verses[meter_id].append(verse)
        
        total_files = 0
        for meter_id, meter_verse_list in sorted(meter_verses.items()):
            meter_name = meter_verse_list[0].get('meter', f'meter_{meter_id}')
            
            # Split into batches
            for batch_num, i in enumerate(range(0, len(meter_verse_list), batch_size), 1):
                batch = meter_verse_list[i:i+batch_size]
                filename = f"{meter_name}_deduped_batch_{batch_num:03d}.jsonl"
                filepath = output_path / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    for verse in batch:
                        # Remove evaluation fields
                        clean_verse = {k: v for k, v in verse.items() 
                                     if k not in ['normalized_text_eval', 'fingerprint', 'source_file', 'source_line']}
                        f.write(json.dumps(clean_verse, ensure_ascii=False) + '\n')
                
                total_files += 1
        
        print(f"✅ Exported {total_files} deduplicated batch files to {output_dir}/")
        print()


# ============================================================================
# MAIN EVALUATION PIPELINE
# ============================================================================

def main():
    """Execute full 7-phase evaluation"""
    print("\n")
    print("="*70)
    print("ARABIC PROSODY DATASET QUALITY EVALUATION")
    print("Senior Arabic NLP Researcher | Dataset Quality Engineer")
    print("="*70)
    print("\n")
    
    # Phase 1: Load dataset
    loader = DatasetLoader()
    verses = loader.load_all_batches()
    
    # Phase 2: Deduplication analysis
    dedup_analyzer = DeduplicationAnalyzer(verses)
    duplicates = dedup_analyzer.analyze()
    
    # Phase 3: Cross-meter anomalies
    cross_meter = CrossMeterAnalyzer(verses)
    anomalies = cross_meter.analyze()
    
    # Phase 4: Poet distribution
    poet_analyzer = PoetDistributionAnalyzer(verses)
    distribution = poet_analyzer.analyze()
    
    # Phase 5: Metadata validation
    validator = MetadataValidator(verses)
    errors = validator.analyze()
    
    # Phase 6: Generate report
    reporter = ReportGenerator(verses, duplicates, anomalies, distribution, 
                               poet_analyzer.imbalances, errors)
    report_file = reporter.generate()
    
    # Phase 7: Produce deduplicated dataset
    deduplicator = DatasetDeduplicator(verses, duplicates)
    clean_verses = deduplicator.deduplicate()
    deduplicator.export_batches(clean_verses)
    
    print("="*70)
    print("EVALUATION COMPLETE")
    print("="*70)
    print(f"✅ Report: {report_file}")
    print(f"✅ Deduplicated dataset: deduplicated/")
    print(f"✅ Original: {len(verses)} verses → Clean: {len(clean_verses)} verses")
    print("="*70)
    print()

if __name__ == '__main__':
    main()
