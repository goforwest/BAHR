#!/usr/bin/env python3
"""
Seed database with reference data for BAHR prosody analysis.

This script populates the database with:
- 16 classical Arabic meters (بحور)
- 8 base prosodic feet (تفاعيل)

Usage:
    python scripts/seed_database.py

Environment:
    Requires DATABASE_URL environment variable or uses default:
    postgresql://bahr:bahr_dev_password@localhost:5432/bahr_dev

Features:
    - Idempotent: Safe to run multiple times
    - Uses upsert logic (insert if not exists)
    - Provides detailed console output
    - Transaction-based for atomicity
"""

import os
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.models import Meter, Tafila, MeterType

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://bahr:bahr_dev_password@localhost:5432/bahr_dev"
)

# ============================================================================
# بَحُور الشِعْر العَرَبِي - 16 Classical Arabic Meters
# ============================================================================

BAHRS_DATA = [
    {
        "name": "الطويل",
        "english_name": "al-Tawil",
        "base_pattern": "فعولن مفاعيلن فعولن مفاعيلن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 2,
        "syllable_count": 48,
        "foot_pattern": ["فَعُولُنْ", "مَفَاعِيلُنْ", "فَعُولُنْ", "مَفَاعِيلُنْ"],
        "frequency_rank": 1,
        "usage_count": 0,
        "difficulty_score": 2.5,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["امرؤ القيس", "عنترة بن شداد", "المتنبي"],
        "description_ar": "أشهر البحور وأكثرها استخداماً في الشعر العربي، يمتاز بالفخامة والجزالة",
        "description_en": "Most popular meter in Arabic poetry, characterized by grandeur and eloquence",
        "example_verses": [
            {
                "text": "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ",
                "poet": "امرؤ القيس",
                "source": "معلقة امرؤ القيس"
            }
        ],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "المديد",
        "english_name": "al-Madid",
        "base_pattern": "فاعلاتن فاعلن فاعلاتن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 3,
        "syllable_count": 44,
        "foot_pattern": ["فَاعِلَاتُنْ", "فَاعِلُنْ", "فَاعِلَاتُنْ"],
        "frequency_rank": 9,
        "usage_count": 0,
        "difficulty_score": 3.0,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["البحتري", "أبو نواس"],
        "description_ar": "بحر رقيق عذب، مناسب للغزل والوصف",
        "description_en": "A gentle meter, suitable for love poetry and description",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "البسيط",
        "english_name": "al-Basit",
        "base_pattern": "مستفعلن فاعلن مستفعلن فاعلن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 2,
        "syllable_count": 48,
        "foot_pattern": ["مُسْتَفْعِلُنْ", "فَاعِلُنْ", "مُسْتَفْعِلُنْ", "فَاعِلُنْ"],
        "frequency_rank": 3,
        "usage_count": 0,
        "difficulty_score": 2.5,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["جرير", "الفرزدق"],
        "description_ar": "بحر واسع الانتشار، يصلح للفخر والحماسة",
        "description_en": "Widely used meter, suitable for pride and enthusiasm",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "الوافر",
        "english_name": "al-Wafir",
        "base_pattern": "مفاعلتن مفاعلتن فعولن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 2,
        "syllable_count": 46,
        "foot_pattern": ["مُفَاعَلَتُنْ", "مُفَاعَلَتُنْ", "فَعُولُنْ"],
        "frequency_rank": 4,
        "usage_count": 0,
        "difficulty_score": 2.0,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["أبو فراس الحمداني", "أحمد شوقي"],
        "description_ar": "بحر موسيقي جميل، كثير الاستعمال في العصر الحديث",
        "description_en": "Musical meter, frequently used in modern poetry",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "الكامل",
        "english_name": "al-Kamil",
        "base_pattern": "متفاعلن متفاعلن متفاعلن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 1,
        "syllable_count": 48,
        "foot_pattern": ["مُتَفَاعِلُنْ", "مُتَفَاعِلُنْ", "مُتَفَاعِلُنْ"],
        "frequency_rank": 2,
        "usage_count": 0,
        "difficulty_score": 2.0,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["البحتري", "أبو تمام", "محمود درويش"],
        "description_ar": "ثاني أشهر البحور، متوازن وسهل الحفظ",
        "description_en": "Second most popular meter, balanced and easy to memorize",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "الهزج",
        "english_name": "al-Hazaj",
        "base_pattern": "مفاعيلن مفاعيلن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 3,
        "syllable_count": 32,
        "foot_pattern": ["مَفَاعِيلُنْ", "مَفَاعِيلُنْ"],
        "frequency_rank": 12,
        "usage_count": 0,
        "difficulty_score": 3.5,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["ابن الرومي"],
        "description_ar": "بحر خفيف رشيق، يصلح للغناء",
        "description_en": "Light and graceful meter, suitable for singing",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "الرجز",
        "english_name": "al-Rajaz",
        "base_pattern": "مستفعلن مستفعلن مستفعلن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 1,
        "syllable_count": 48,
        "foot_pattern": ["مُسْتَفْعِلُنْ", "مُسْتَفْعِلُنْ", "مُسْتَفْعِلُنْ"],
        "frequency_rank": 5,
        "usage_count": 0,
        "difficulty_score": 1.5,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["العجاج", "رؤبة"],
        "description_ar": "بحر سهل بسيط، استخدم كثيراً في الأرجوزات التعليمية",
        "description_en": "Simple meter, widely used in educational poetry (urjuza)",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "الرمل",
        "english_name": "ar-Ramal",
        "base_pattern": "فاعلاتن فاعلاتن فاعلاتن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 2,
        "syllable_count": 48,
        "foot_pattern": ["فَاعِلَاتُنْ", "فَاعِلَاتُنْ", "فَاعِلَاتُنْ"],
        "frequency_rank": 6,
        "usage_count": 0,
        "difficulty_score": 2.0,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["أبو نواس", "نزار قباني"],
        "description_ar": "بحر سلس رقيق، مناسب للغزل والرثاء",
        "description_en": "Smooth meter, suitable for love and elegy poetry",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "السريع",
        "english_name": "as-Sari'",
        "base_pattern": "مستفعلن مستفعلن فاعلن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 3,
        "syllable_count": 44,
        "foot_pattern": ["مُسْتَفْعِلُنْ", "مُسْتَفْعِلُنْ", "فَاعِلُنْ"],
        "frequency_rank": 8,
        "usage_count": 0,
        "difficulty_score": 3.0,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["أبو العلاء المعري"],
        "description_ar": "بحر سريع الإيقاع، مناسب للحماسة",
        "description_en": "Fast-paced meter, suitable for enthusiastic poetry",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "المنسرح",
        "english_name": "al-Munsarih",
        "base_pattern": "مستفعلن مفعولات مفتعلن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 4,
        "syllable_count": 46,
        "foot_pattern": ["مُسْتَفْعِلُنْ", "مَفْعُولَاتُ", "مُفْتَعِلُنْ"],
        "frequency_rank": 10,
        "usage_count": 0,
        "difficulty_score": 3.5,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["المتنبي"],
        "description_ar": "بحر منساب سلس، قليل الاستعمال",
        "description_en": "Flowing meter, rarely used",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "الخفيف",
        "english_name": "al-Khafif",
        "base_pattern": "فاعلاتن مستفعلن فاعلاتن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 2,
        "syllable_count": 48,
        "foot_pattern": ["فَاعِلَاتُنْ", "مُسْتَفْعِلُنْ", "فَاعِلَاتُنْ"],
        "frequency_rank": 7,
        "usage_count": 0,
        "difficulty_score": 2.5,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["أبو العتاهية", "صلاح عبد الصبور"],
        "description_ar": "بحر خفيف الوزن، مناسب للموشحات",
        "description_en": "Light meter, suitable for muwashshah poetry",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "المضارع",
        "english_name": "al-Mudari'",
        "base_pattern": "مفاعيلن فاعلاتن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 4,
        "syllable_count": 32,
        "foot_pattern": ["مَفَاعِيلُنْ", "فَاعِلَاتُنْ"],
        "frequency_rank": 15,
        "usage_count": 0,
        "difficulty_score": 4.0,
        "origin_period": "العصر الجاهلي",
        "famous_poets": [],
        "description_ar": "بحر نادر الاستعمال، يضارع الهزج",
        "description_en": "Rarely used meter, similar to al-Hazaj",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "المقتضب",
        "english_name": "al-Muqtadab",
        "base_pattern": "مفعولات مستفعلن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 4,
        "syllable_count": 32,
        "foot_pattern": ["مَفْعُولَاتُ", "مُسْتَفْعِلُنْ"],
        "frequency_rank": 14,
        "usage_count": 0,
        "difficulty_score": 4.0,
        "origin_period": "العصر الجاهلي",
        "famous_poets": [],
        "description_ar": "بحر قليل الاستخدام",
        "description_en": "Rarely used meter",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "المجتث",
        "english_name": "al-Mujtathth",
        "base_pattern": "مستفعلن فاعلاتن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 4,
        "syllable_count": 32,
        "foot_pattern": ["مُسْتَفْعِلُنْ", "فَاعِلَاتُنْ"],
        "frequency_rank": 13,
        "usage_count": 0,
        "difficulty_score": 4.0,
        "origin_period": "العصر الجاهلي",
        "famous_poets": [],
        "description_ar": "بحر نادر، مجتث من البسيط",
        "description_en": "Rare meter, derived from al-Basit",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "المتقارب",
        "english_name": "al-Mutaqarib",
        "base_pattern": "فعولن فعولن فعولن فعولن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 2,
        "syllable_count": 32,
        "foot_pattern": ["فَعُولُنْ", "فَعُولُنْ", "فَعُولُنْ", "فَعُولُنْ"],
        "frequency_rank": 11,
        "usage_count": 0,
        "difficulty_score": 2.0,
        "origin_period": "العصر الجاهلي",
        "famous_poets": ["أبو فراس", "ابن زيدون"],
        "description_ar": "بحر متقارب التفعيلات، سهل الحفظ",
        "description_en": "Meter with similar feet, easy to memorize",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
    {
        "name": "المتدارك",
        "english_name": "al-Mutadarik",
        "base_pattern": "فاعلن فاعلن فاعلن فاعلن",
        "pattern_type": MeterType.CLASSICAL,
        "complexity_level": 3,
        "syllable_count": 32,
        "foot_pattern": ["فَاعِلُنْ", "فَاعِلُنْ", "فَاعِلُنْ", "فَاعِلُنْ"],
        "frequency_rank": 16,
        "usage_count": 0,
        "difficulty_score": 3.0,
        "origin_period": "اكتشفه الأخفش",
        "famous_poets": [],
        "description_ar": "البحر السادس عشر، أضافه الأخفش لبحور الخليل",
        "description_en": "16th meter, added by al-Akhfash to al-Khalil's meters",
        "example_verses": [],
        "is_active": True,
        "is_classical": True
    },
]

# ============================================================================
# التَفَاعِيل - 8 Base Prosodic Feet
# ============================================================================

TAFAIL_DATA = [
    {
        "name_ar": "فَعُولُنْ",
        "name_en": "fa'ūlun",
        "pattern": "//0/0",
        "arabic_notation": "ب ب ه ب ه",
        "syllable_structure": "CVCCVC",
        "syllable_count": 3,
        "long_syllables": 2,
        "short_syllables": 1,
        "common_variations": [
            {"name": "فَعُولُ", "type": "حذف"},
            {"name": "فَعُو", "type": "قطع"}
        ],
        "used_in_meters": ["الطويل", "المتقارب"],
        "usage_frequency": 0.95,
        "example_words": ["كَتَبْنَا", "قَرَأْتُمْ"],
        "description": "من أكثر التفاعيل استخداماً، تتكون من سبب ثقيل ووتد مجموع"
    },
    {
        "name_ar": "مَفَاعِيلُنْ",
        "name_en": "mafā'īlun",
        "pattern": "///0/0",
        "arabic_notation": "ب ب ب ه ب ه",
        "syllable_structure": "CVCVCCVC",
        "syllable_count": 4,
        "long_syllables": 2,
        "short_syllables": 2,
        "common_variations": [
            {"name": "مَفَاعِلُنْ", "type": "قبض"},
            {"name": "مَفَاعِيلُ", "type": "حذف"}
        ],
        "used_in_meters": ["الطويل", "الهزج", "المضارع"],
        "usage_frequency": 0.90,
        "example_words": ["مُسَافِرُونَ"],
        "description": "تفعيلة سباعية، تتكون من ثلاثة أسباب ووتد مجموع"
    },
    {
        "name_ar": "فَاعِلُنْ",
        "name_en": "fā'ilun",
        "pattern": "//0/0",
        "arabic_notation": "ب ب ه ب ه",
        "syllable_structure": "CVCCVC",
        "syllable_count": 3,
        "long_syllables": 2,
        "short_syllables": 1,
        "common_variations": [
            {"name": "فَعِلُنْ", "type": "خبن"},
            {"name": "فَاعِلْ", "type": "قطع"}
        ],
        "used_in_meters": ["المديد", "البسيط", "السريع", "المتدارك"],
        "usage_frequency": 0.88,
        "example_words": ["عَالِمُونَ"],
        "description": "تفعيلة خماسية شائعة جداً"
    },
    {
        "name_ar": "مُتَفَاعِلُنْ",
        "name_en": "mutafā'ilun",
        "pattern": "////0/0",
        "arabic_notation": "ب ب ب ب ه ب ه",
        "syllable_structure": "CVCVCVCVC",
        "syllable_count": 4,
        "long_syllables": 2,
        "short_syllables": 2,
        "common_variations": [
            {"name": "مُتَفَاعِلْ", "type": "حذف"},
            {"name": "مُتْفَاعِلُنْ", "type": "إضمار"}
        ],
        "used_in_meters": ["الكامل"],
        "usage_frequency": 0.92,
        "example_words": ["مُتَعَلِّمُونَ"],
        "description": "تفعيلة الكامل الأساسية"
    },
    {
        "name_ar": "مُسْتَفْعِلُنْ",
        "name_en": "mustaf'ilun",
        "pattern": "/0//0/0",
        "arabic_notation": "ب ه ب ب ه ب ه",
        "syllable_structure": "CVCCVCVC",
        "syllable_count": 4,
        "long_syllables": 3,
        "short_syllables": 1,
        "common_variations": [
            {"name": "مُتَفْعِلُنْ", "type": "خبن"},
            {"name": "مَفَاعِلُنْ", "type": "طي"}
        ],
        "used_in_meters": ["الرجز", "البسيط", "السريع", "المنسرح", "الخفيف"],
        "usage_frequency": 0.85,
        "example_words": ["مُسْتَمِعُونَ"],
        "description": "من أكثر التفاعيل مرونة في التغييرات"
    },
    {
        "name_ar": "مَفْعُولَاتُ",
        "name_en": "maf'ūlātu",
        "pattern": "/0/0//0",
        "arabic_notation": "ب ه ب ه ب ب ه",
        "syllable_structure": "CVCCVCCV",
        "syllable_count": 4,
        "long_syllables": 2,
        "short_syllables": 2,
        "common_variations": [
            {"name": "مَفْعُولُ", "type": "حذف"},
            {"name": "فَعُولَاتُ", "type": "قبض"}
        ],
        "used_in_meters": ["المنسرح", "المقتضب"],
        "usage_frequency": 0.60,
        "example_words": ["مَكْتُوبَاتٌ"],
        "description": "تفعيلة تبدأ بوتد مفروق"
    },
    {
        "name_ar": "فَاعِلَاتُنْ",
        "name_en": "fā'ilātun",
        "pattern": "///0/0",
        "arabic_notation": "ب ب ب ه ب ه",
        "syllable_structure": "CVCVCCVC",
        "syllable_count": 4,
        "long_syllables": 2,
        "short_syllables": 2,
        "common_variations": [
            {"name": "فَعِلَاتُنْ", "type": "خبن"},
            {"name": "فَاعِلَاتُ", "type": "حذف"}
        ],
        "used_in_meters": ["الرمل", "المديد", "الخفيف", "المجتث", "المضارع"],
        "usage_frequency": 0.87,
        "example_words": ["عَامِلَاتٌ"],
        "description": "تفعيلة سباعية شائعة في بحور متعددة"
    },
    {
        "name_ar": "مُفَاعَلَتُنْ",
        "name_en": "mufā'alatun",
        "pattern": "////0/0",
        "arabic_notation": "ب ب ب ب ه ب ه",
        "syllable_structure": "CVCVCVCVC",
        "syllable_count": 4,
        "long_syllables": 2,
        "short_syllables": 2,
        "common_variations": [
            {"name": "مُفَاعَلْتُنْ", "type": "عصب"},
            {"name": "مُفَاعَتُنْ", "type": "عقل"}
        ],
        "used_in_meters": ["الوافر"],
        "usage_frequency": 0.75,
        "example_words": ["مُسَابَقَاتٌ"],
        "description": "تفعيلة الوافر الأساسية"
    },
]


def seed_database():
    """Seed the database with reference data."""
    print("=" * 80)
    print("🌱 BAHR Database Seeding Script")
    print("=" * 80)
    
    # Create engine and session
    print(f"\n📡 Connecting to database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # ====================================================================
        # Seed البحور (Meters)
        # ====================================================================
        print("\n" + "=" * 80)
        print("📚 Seeding البحور (Arabic Meters)")
        print("=" * 80)
        
        meters_inserted = 0
        meters_skipped = 0
        
        for bahr_data in BAHRS_DATA:
            existing = session.query(Meter).filter_by(name=bahr_data["name"]).first()
            
            if existing:
                print(f"⏭️  Skipping '{bahr_data['name']}' (already exists)")
                meters_skipped += 1
            else:
                meter = Meter(**bahr_data)
                session.add(meter)
                print(f"✅ Inserted '{bahr_data['name']}' ({bahr_data['english_name']})")
                meters_inserted += 1
        
        session.commit()
        print(f"\n📊 Meters Summary: {meters_inserted} inserted, {meters_skipped} skipped")
        
        # ====================================================================
        # Seed التفاعيل (Prosodic Feet)
        # ====================================================================
        print("\n" + "=" * 80)
        print("📚 Seeding التفاعيل (Prosodic Feet)")
        print("=" * 80)
        
        tafail_inserted = 0
        tafail_skipped = 0
        
        for tafila_data in TAFAIL_DATA:
            existing = session.query(Tafila).filter_by(name_ar=tafila_data["name_ar"]).first()
            
            if existing:
                print(f"⏭️  Skipping '{tafila_data['name_ar']}' (already exists)")
                tafail_skipped += 1
            else:
                tafila = Tafila(**tafila_data)
                session.add(tafila)
                print(f"✅ Inserted '{tafila_data['name_ar']}' ({tafila_data['name_en']})")
                tafail_inserted += 1
        
        session.commit()
        print(f"\n📊 Tafa'il Summary: {tafail_inserted} inserted, {tafail_skipped} skipped")
        
        # ====================================================================
        # Final Summary
        # ====================================================================
        total_meters = session.query(Meter).count()
        total_tafail = session.query(Tafila).count()
        
        print("\n" + "=" * 80)
        print("✨ Database Seeding Complete!")
        print("=" * 80)
        print(f"📈 Total Meters in database: {total_meters}/16")
        print(f"📈 Total Tafa'il in database: {total_tafail}/8")
        
        if total_meters == 16 and total_tafail == 8:
            print("\n🎉 Success! All reference data is now in the database.")
        else:
            print(f"\n⚠️  Warning: Expected 16 meters and 8 tafa'il, but found {total_meters} and {total_tafail}")
        
        print("=" * 80)
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Error during seeding: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
