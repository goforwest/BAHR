#!/usr/bin/env python3
"""
Arabic Poetry Dataset Collector

Web-based collection, validation, and JSONL export of classical Arabic poetry
according to ARABIC_PROSODY_ML_DATASET_BLUEPRINT.md specifications.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import time

# For web scraping (will be used to fetch real poetry)
try:
    import requests
    from bs4 import BeautifulSoup
    WEB_ENABLED = True
except ImportError:
    WEB_ENABLED = False
    print("Warning: requests/bs4 not installed. Web collection disabled.")

from prosody_validator import ProsodyValidator, ArabicTextNormalizer, get_meter_info


@dataclass
class VerseData:
    """Complete verse data structure matching blueprint schema."""
    verse_id: str
    text: str
    normalized_text: str
    meter_id: int
    meter: str
    meter_en: str
    poet: str
    source: str
    source_type: str
    timestamp: str
    prosody_precomputed: Dict
    metadata: Dict
    ml_features: Dict


class ArabicPoetryCollector:
    """Collects and validates Arabic poetry from web sources."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.validator = ProsodyValidator()
        self.normalizer = ArabicTextNormalizer()
        self.verse_cache = set()  # For deduplication
        
    def collect_from_aldiwan(self, meter_name_ar: str, limit: int = 50) -> List[Dict]:
        """
        Collect verses from Aldiwan.net (Arabic poetry database).
        
        Note: This is a template. Actual implementation requires
        understanding Aldiwan's structure and respecting robots.txt.
        """
        if not WEB_ENABLED:
            return []
        
        verses = []
        
        # Aldiwan meter mapping (approximate)
        meter_urls = {
            'الطويل': 'taweel',
            'الكامل': 'kamel',
            'البسيط': 'baseet',
            'الوافر': 'wafer',
            'الرجز': 'rajaz',
            'الرمل': 'ramal',
            'الخفيف': 'khafeef',
            'السريع': 'saree',
            'المديد': 'madeed',
            'المنسرح': 'munsareh',
            'المتقارب': 'mutakareb',
            'الهزج': 'hazaj',
        }
        
        if meter_name_ar not in meter_urls:
            print(f"Warning: {meter_name_ar} not in Aldiwan meter mapping")
            return []
        
        # Example URL (adjust based on actual site structure)
        base_url = f"https://www.aldiwan.net/meter/{meter_urls[meter_name_ar]}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Academic Research Bot; Poetry Dataset)',
                'Accept-Language': 'ar,en;q=0.9'
            }
            
            response = requests.get(base_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find verse elements (this is hypothetical - adjust to actual HTML)
            verse_elements = soup.find_all('div', class_='verse-container', limit=limit)
            
            for elem in verse_elements:
                verse_text = elem.find('p', class_='verse-text')
                poet_elem = elem.find('span', class_='poet-name')
                
                if verse_text and poet_elem:
                    text = verse_text.get_text(strip=True)
                    poet = poet_elem.get_text(strip=True)
                    
                    verses.append({
                        'text': text,
                        'poet': poet,
                        'source': 'aldiwan.net'
                    })
            
            # Be respectful - rate limit
            time.sleep(2)
            
        except Exception as e:
            print(f"Error fetching from Aldiwan: {e}")
        
        return verses
    
    def collect_from_adab(self, meter_name_ar: str, limit: int = 50) -> List[Dict]:
        """
        Collect from adab.com or similar classical poetry archives.
        """
        if not WEB_ENABLED:
            return []
        
        # Placeholder - implement based on actual site structure
        print(f"Collecting from Adab.com for meter: {meter_name_ar}")
        return []
    
    def search_classical_diwans(self, meter_id: int, limit: int = 50) -> List[Dict]:
        """
        Search for classical poetry from known public domain sources.
        
        This would integrate with:
        - Al-Warraq digital library
        - Archive.org Arabic manuscripts
        - Other authenticated sources
        """
        # Placeholder for actual implementation
        print(f"Searching classical diwans for meter ID: {meter_id}")
        return []
    
    def validate_and_annotate(self, raw_verse: Dict, meter_id: int) -> Optional[VerseData]:
        """
        Validate verse against meter and create full annotation.
        
        Args:
            raw_verse: Dict with 'text', 'poet', 'source' keys
            meter_id: Target meter ID
        
        Returns:
            Fully annotated VerseData or None if validation fails
        """
        text = raw_verse.get('text', '').strip()
        
        # Deduplication check
        text_hash = hash(text)
        if text_hash in self.verse_cache:
            return None
        
        # Validate prosody
        is_valid, confidence, analysis = self.validator.validate_verse(text, meter_id)
        
        if not is_valid or confidence < 0.90:
            return None
        
        # Get meter info
        meter_info = get_meter_info(meter_id)
        if not meter_info:
            return None
        
        # Generate verse ID
        meter_abbr = self._get_meter_abbreviation(meter_info.name_en)
        source_abbr = self._get_source_abbreviation(raw_verse.get('source', 'unknown'))
        seq_num = len(self.verse_cache) + 1
        verse_id = f"{meter_abbr}_{source_abbr}_{seq_num:04d}"
        
        # Normalize text
        normalized = self.normalizer.normalize(text)
        
        # Extract metadata
        poet = raw_verse.get('poet', 'مجهول')
        source_type = raw_verse.get('source', 'web_collection')
        
        # Compute ML features
        ml_features = self._compute_ml_features(text, normalized, analysis)
        
        # Build prosody precomputed
        prosody = {
            'pattern_phonetic': analysis.get('pattern_phonetic', ''),
            'tafail_sequence': analysis.get('tafail_sequence', []),
            'tafail_patterns': self._extract_tafail_patterns(analysis),
            'zihafat': [],  # Would be populated by full prosody engine
            'ilal': [],
            'confidence': confidence,
            'engine_version': 'ML_Dataset_Validator v1.0'
        }
        
        # Build metadata
        metadata = {
            'poem_title': raw_verse.get('poem_title', ''),
            'era': self._infer_era(poet),
            'genre': raw_verse.get('genre', ''),
            'original_source': source_type,
            'verification_status': 'validated',
            'diacritization_source': 'original' if self._has_diacritics(text) else 'partial',
            'notes': ''
        }
        
        # Create timestamp
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Build complete verse data
        verse_data = VerseData(
            verse_id=verse_id,
            text=text,
            normalized_text=normalized,
            meter_id=meter_id,
            meter=meter_info.name_ar,
            meter_en=meter_info.name_en,
            poet=poet,
            source='classical',  # Adjust based on actual source
            source_type=source_type,
            timestamp=timestamp,
            prosody_precomputed=prosody,
            metadata=metadata,
            ml_features=ml_features
        )
        
        # Add to cache
        self.verse_cache.add(text_hash)
        
        return verse_data
    
    def _compute_ml_features(self, text: str, normalized: str, analysis: Dict) -> Dict:
        """Compute ML features according to blueprint."""
        # Count diacritics
        harakat_pattern = r'[\u064B-\u064F\u0650\u0651\u0652]'
        harakat_count = len(re.findall(harakat_pattern, text))
        
        # Count sukun
        sakin_count = text.count('\u0652')
        
        # Word count
        word_count = len(normalized.split())
        
        # Pattern length
        pattern = analysis.get('pattern_phonetic', '')
        pattern_length = len(pattern)
        
        return {
            'pattern_length': pattern_length,
            'harakat_count': harakat_count,
            'sakin_count': sakin_count,
            'mutaharrik_count': harakat_count - sakin_count,
            'word_count': word_count,
            'syllable_pattern': pattern,
            'tafail_count': len(analysis.get('tafail_sequence', [])),
            'zihafat_count': 0,
            'has_ilal': False,
            'pattern_diversity': 0.5  # Placeholder
        }
    
    def _extract_tafail_patterns(self, analysis: Dict) -> List[str]:
        """Extract individual tafīlah patterns."""
        # Placeholder - would extract from full analysis
        return []
    
    def _get_meter_abbreviation(self, meter_en: str) -> str:
        """Generate short meter abbreviation."""
        abbr_map = {
            'al-Ṭawīl': 'tawil',
            'al-Kāmil': 'kamil',
            'al-Basīṭ': 'basit',
            'al-Wāfir': 'wafir',
            'al-Rajaz': 'rajaz',
            'ar-Ramal': 'ramal',
            'al-Khafīf': 'khafif',
            'as-Sarīʿ': 'sari',
            'al-Madīd': 'madid',
            'al-Munsariḥ': 'munsarih',
            'al-Mutaqārib': 'mutaqarib',
            'al-Hazaj': 'hazaj',
            'al-Mujtathth': 'mujtath',
            'al-Muqtaḍab': 'muqtadab',
            'al-Muḍāriʿ': 'mudari',
            'al-Mutadārik': 'mutadarik',
        }
        return abbr_map.get(meter_en, meter_en.lower().replace('-', '').replace('al', ''))
    
    def _get_source_abbreviation(self, source: str) -> str:
        """Generate source abbreviation."""
        return source.replace('.', '').replace('www', '').replace('net', '')[:8]
    
    def _has_diacritics(self, text: str) -> bool:
        """Check if text contains diacritics."""
        return bool(re.search(r'[\u064B-\u0652]', text))
    
    def _infer_era(self, poet: str) -> str:
        """Infer historical era from poet name (simplified)."""
        # This is a placeholder - in production, use a poet database
        classical_poets = ['امرؤ القيس', 'عنترة', 'الحارث', 'طرفة', 'لبيد']
        if any(name in poet for name in classical_poets):
            return 'pre-Islamic'
        return 'classical'
    
    def export_to_jsonl(self, verses: List[VerseData], meter_name: str, batch_num: int = 1) -> Path:
        """
        Export verses to JSONL file.
        
        Args:
            verses: List of VerseData objects
            meter_name: Meter name (Arabic)
            batch_num: Batch number
        
        Returns:
            Path to output file
        """
        # Clean meter name for filename
        meter_clean = meter_name.replace(' ', '_').replace('(', '').replace(')', '')
        filename = f"{meter_clean}_batch_{batch_num:03d}.jsonl"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for verse in verses:
                verse_dict = asdict(verse)
                json_line = json.dumps(verse_dict, ensure_ascii=False, separators=(',', ':'))
                f.write(json_line + '\n')
        
        print(f"✓ Exported {len(verses)} verses to: {filepath}")
        return filepath
    
    def collect_batch(self, meter_id: int, batch_size: int = 20) -> List[VerseData]:
        """
        Collect a batch of validated verses for a specific meter.
        
        Args:
            meter_id: Meter ID (1-20)
            batch_size: Number of verses to collect
        
        Returns:
            List of validated VerseData objects
        """
        meter_info = get_meter_info(meter_id)
        if not meter_info:
            print(f"Error: Invalid meter ID {meter_id}")
            return []
        
        print(f"\n📚 Collecting batch for meter: {meter_info.name_ar} ({meter_info.name_en})")
        print(f"   Target: {batch_size} verses")
        
        validated_verses = []
        
        # Try multiple sources
        raw_verses = []
        
        # Source 1: Aldiwan
        print("   Searching Aldiwan.net...")
        raw_verses.extend(self.collect_from_aldiwan(meter_info.name_ar, limit=batch_size * 3))
        
        # Source 2: Adab
        print("   Searching Adab.com...")
        raw_verses.extend(self.collect_from_adab(meter_info.name_ar, limit=batch_size * 2))
        
        # Source 3: Classical diwans
        print("   Searching classical sources...")
        raw_verses.extend(self.search_classical_diwans(meter_id, limit=batch_size * 2))
        
        print(f"   Found {len(raw_verses)} candidate verses")
        
        # Validate and annotate
        print("   Validating...")
        for raw_verse in raw_verses:
            if len(validated_verses) >= batch_size:
                break
            
            verse_data = self.validate_and_annotate(raw_verse, meter_id)
            if verse_data:
                validated_verses.append(verse_data)
        
        print(f"   ✓ Validated {len(validated_verses)} verses")
        
        return validated_verses


def main():
    """Main entry point for dataset collection."""
    print("=" * 80)
    print("Arabic Prosody ML Dataset Collection Tool")
    print("=" * 80)
    
    output_dir = Path(__file__).parent
    collector = ArabicPoetryCollector(output_dir)
    
    # List available meters
    print("\nAvailable meters:")
    from prosody_validator import list_all_meters
    meters = list_all_meters()
    for i, meter in enumerate(meters, 1):
        print(f"  {meter['id']:2d}. {meter['name_ar']:20s} ({meter['name_en']})")
    
    print("\n" + "=" * 80)
    print("Ready to begin collection.")
    print("=" * 80)


if __name__ == '__main__':
    main()
