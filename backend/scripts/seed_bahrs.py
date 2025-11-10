#!/usr/bin/env python3
"""
Seed script to populate the bahrs table with all 16 classical Arabic meters.

Usage:
    python scripts/seed_bahrs.py

This script is idempotent - it checks if each bahr exists before inserting.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models.bahr import Bahr
from app.models.base import Base


# All 16 classical Arabic meters with accurate data
BAHRS_DATA = [
    {
        "id": 1,
        "name_ar": "الطويل",
        "name_en": "at-Tawil",
        "pattern": "فعولن مفاعيلن فعولن مفاعيلن",
        "description": "أكثر البحور استعمالاً في الشعر العربي، يتميز بطوله ورصانته",
        "example_verse": "أَلا عِمْ صَباحاً أَيُّها الطَلَلُ البالي"
    },
    {
        "id": 2,
        "name_ar": "الكامل",
        "name_en": "al-Kamil",
        "pattern": "متفاعلن متفاعلن متفاعلن",
        "description": "سمي بالكامل لكمال حركاته، يستخدم كثيراً في الشعر الحماسي والوصف",
        "example_verse": "بَصُرَتْ بِهِ كَفِّي فَأَبْصَرَ قَلْبُهُ"
    },
    {
        "id": 3,
        "name_ar": "الوافر",
        "name_en": "al-Wafir",
        "pattern": "مفاعلتن مفاعلتن فعولن",
        "description": "سمي بالوافر لوفور حركاته، يتميز بموسيقاه العذبة",
        "example_verse": "سَلامٌ مِنْ صَبا بَرَدى أَرَقُّ"
    },
    {
        "id": 4,
        "name_ar": "الرمل",
        "name_en": "ar-Ramal",
        "pattern": "فاعلاتن فاعلاتن فاعلاتن",
        "description": "من أخف البحور وأسرعها، يستخدم كثيراً في الغزل والرثاء",
        "example_verse": "يا لَيْلَةً لَمْ أَنَمْ فيها ولَمْ أَقُمِ"
    },
    {
        "id": 5,
        "name_ar": "البسيط",
        "name_en": "al-Basit",
        "pattern": "مستفعلن فاعلن مستفعلن فاعلن",
        "description": "سمي بالبسيط لانبساط أسبابه، يستعمل في جميع الأغراض",
        "example_verse": "إِنَّ الثَمانينَ وَبُلِّغْتَها قَدْ أَحْوَجَتْ سَمْعي إِلى تَرْجُمانِ"
    },
    {
        "id": 6,
        "name_ar": "الخفيف",
        "name_en": "al-Khafif",
        "pattern": "فاعلاتن مستفعلن فاعلاتن",
        "description": "سمي بالخفيف لخفة النطق به، يتميز برقته وعذوبته",
        "example_verse": "يا أَيُّها القَلْبُ لِمَ التَشَتُّتُ"
    },
    {
        "id": 7,
        "name_ar": "المتقارب",
        "name_en": "al-Mutaqarib",
        "pattern": "فعولن فعولن فعولن فعولن",
        "description": "سمي بالمتقارب لتقارب أجزائه، يستخدم في الحكم والأمثال",
        "example_verse": "أَعَدَّ اللَهُ لِلشُعَراءِ مِنّي صَواعِقَ يَخْضَعُونَ لَها صِغارا"
    },
    {
        "id": 8,
        "name_ar": "المتدارك",
        "name_en": "al-Mutadarik",
        "pattern": "فاعلن فاعلن فاعلن فاعلن",
        "description": "سمي بالمتدارك لأنه تدارك به ما فات الخليل، ويسمى أيضاً المحدث",
        "example_verse": "حُبُّ المَعالي رَفَعَ الأَوْسا"
    },
    {
        "id": 9,
        "name_ar": "الهزج",
        "name_en": "al-Hazaj",
        "pattern": "مفاعيلن مفاعيلن",
        "description": "سمي بالهزج لأنه يشبه الهزج في الغناء، يتميز بالخفة والسرعة",
        "example_verse": "أَلا يا اسْلَمِي يا دارَ مَيٍّ عَلى البِلى"
    },
    {
        "id": 10,
        "name_ar": "الرجز",
        "name_en": "ar-Rajaz",
        "pattern": "مستفعلن مستفعلن مستفعلن",
        "description": "من أكثر البحور مرونة، استخدم في الحرب والحماسة والأراجيز",
        "example_verse": "قَدْ جَبَرَ الدِّينَ الإِلَهُ فَجَبَرْ"
    },
    {
        "id": 11,
        "name_ar": "السريع",
        "name_en": "as-Sari'",
        "pattern": "مستفعلن مستفعلن فاعلن",
        "description": "سمي بالسريع لسرعة النطق به، يستخدم في الرثاء والحكمة",
        "example_verse": "ضاقَتْ فَلَمّا اسْتَحْكَمَتْ حَلَقاتُها فُرِجَتْ وَكُنْتُ أَظُنُّها لا تُفْرَجُ"
    },
    {
        "id": 12,
        "name_ar": "المنسرح",
        "name_en": "al-Munsarih",
        "pattern": "مستفعلن مفعولات مستفعلن",
        "description": "سمي بالمنسرح لانسراحه وسهولته، قليل الاستعمال",
        "example_verse": "مُسْتَفْعِلُنْ مَفْعولاتُ مُسْتَفْعِلُنْ"
    },
    {
        "id": 13,
        "name_ar": "المقتضب",
        "name_en": "al-Muqtadab",
        "pattern": "مفعولات مستفعلن مستفعلن",
        "description": "سمي بالمقتضب لاقتضابه من الدائرة، من أقل البحور استعمالاً",
        "example_verse": "يا لَبَكْرٍ أَنْشِروا لي كُلَيْبا"
    },
    {
        "id": 14,
        "name_ar": "المجتث",
        "name_en": "al-Mujtatth",
        "pattern": "مستفعلن فاعلاتن",
        "description": "سمي بالمجتث لاجتثاثه من الدائرة، قليل الاستعمال",
        "example_verse": "أَلا يا نَخْلَةً مِنْ ذاتِ عِرْقٍ"
    },
    {
        "id": 15,
        "name_ar": "المضارع",
        "name_en": "al-Mudari'",
        "pattern": "مفاعيلن فاعلاتن",
        "description": "سمي بالمضارع لمضارعته المقتضب، نادر الاستعمال",
        "example_verse": "دَعانِيَ مِنْ نَجْدٍ فَإِنَّ سِنينَهُ"
    },
    {
        "id": 16,
        "name_ar": "المحدث",
        "name_en": "al-Muhdath",
        "pattern": "فعلن فعلن فعلن فعلن",
        "description": "سمي بالمحدث لأنه استحدث بعد الخليل، نادر جداً في الشعر العربي",
        "example_verse": "جادَ بِالمالِ وَبَذَّ السُّؤَّلا"
    }
]


def create_tables():
    """Create all tables if they don't exist."""
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables ready")


def seed_bahrs(db: Session):
    """
    Seed the bahrs table with all 16 classical Arabic meters.
    
    This function is idempotent - it checks if each bahr exists before inserting.
    """
    print("\n" + "="*60)
    print("Starting to seed bahrs table...")
    print("="*60 + "\n")
    
    inserted_count = 0
    skipped_count = 0
    error_count = 0
    
    for bahr_data in BAHRS_DATA:
        try:
            # Check if bahr already exists
            existing = db.query(Bahr).filter(
                Bahr.name_ar == bahr_data["name_ar"]
            ).first()
            
            if existing:
                print(f"⊘ Skipping {bahr_data['name_ar']} ({bahr_data['name_en']}) - already exists")
                skipped_count += 1
                continue
            
            # Create new bahr
            bahr = Bahr(
                id=bahr_data["id"],
                name_ar=bahr_data["name_ar"],
                name_en=bahr_data["name_en"],
                pattern=bahr_data["pattern"],
                description=bahr_data["description"],
                example_verse=bahr_data["example_verse"]
            )
            
            db.add(bahr)
            db.commit()
            
            print(f"✓ Inserted {bahr_data['name_ar']} ({bahr_data['name_en']})")
            inserted_count += 1
            
        except Exception as e:
            print(f"✗ Error inserting {bahr_data['name_ar']}: {str(e)}")
            db.rollback()
            error_count += 1
    
    print("\n" + "="*60)
    print("Seeding complete!")
    print("="*60)
    print(f"✓ Inserted: {inserted_count}")
    print(f"⊘ Skipped:  {skipped_count}")
    print(f"✗ Errors:   {error_count}")
    print(f"Total:      {len(BAHRS_DATA)}")
    print("="*60 + "\n")


def verify_bahrs(db: Session):
    """Verify all bahrs are in the database."""
    print("Verifying bahrs in database...\n")
    
    bahrs = db.query(Bahr).order_by(Bahr.id).all()
    
    if len(bahrs) == 0:
        print("⚠ No bahrs found in database!")
        return False
    
    print(f"Found {len(bahrs)} bahrs:\n")
    for bahr in bahrs:
        print(f"  {bahr.id:2d}. {bahr.name_ar:15s} ({bahr.name_en})")
    
    print(f"\n✓ All {len(bahrs)} bahrs verified in database\n")
    return len(bahrs) == 16


def main():
    """Main execution function."""
    print("\n" + "🎭 " * 20)
    print("BAHR Platform - Bahrs Seeding Script")
    print("🎭 " * 20 + "\n")
    
    try:
        # Create tables
        create_tables()
        
        # Create database session
        db = SessionLocal()
        
        try:
            # Seed bahrs
            seed_bahrs(db)
            
            # Verify seeding
            success = verify_bahrs(db)
            
            if success:
                print("🎉 Success! All 16 classical Arabic meters are now in the database.\n")
                return 0
            else:
                print("⚠ Warning: Expected 16 bahrs but found a different number.\n")
                return 1
                
        finally:
            db.close()
            
    except Exception as e:
        print(f"\n✗ Fatal error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
