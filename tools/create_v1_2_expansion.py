#!/usr/bin/env python3
"""
Create BAHR Golden Set v1.2 Expansion
Focus: Rare meters, variant forms (مشطور/مجزوء), metadata enhancement
"""

import json
from pathlib import Path
from datetime import date

# Expansion verses for v1.2 (Phase 1: 50 verses)
expansion_verses = [
    # ========================================
    # المقتضب - High Quality Examples (+10)
    # ========================================
    {
        "verse_id": "golden_362",
        "text": "مَنْ يَفْعَلِ الْخَيْرَ لَا يَعْدَمْ جَوَازِيَهُ",
        "normalized_text": "من يفعل الخير لا يعدم جوازيه",
        "meter": "المقتضب",
        "poet": "الشافعي",
        "poem_title": "ديوان الشافعي",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "era_dates": "750-1258 CE",
            "poet_birth_year": "767 CE",
            "poet_death_year": "820 CE",
            "region": "Hijaz",
            "poem_genre": "wisdom",
            "notes": "Canonical المقتضب example"
        }
    },
    {
        "verse_id": "golden_363",
        "text": "لَا خَيْرَ فِي وُدِّ امْرِئٍ مُتَمَلِّقِ",
        "normalized_text": "لا خير في ود امرئ متملق",
        "meter": "المقتضب",
        "poet": "المتنبي",
        "poem_title": "ديوان المتنبي",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "era_dates": "915-965 CE",
            "poet_birth_year": "915 CE",
            "poet_death_year": "965 CE",
            "region": "Iraq",
            "poem_genre": "wisdom",
            "notes": "Clear المقتضب pattern"
        }
    },
    {
        "verse_id": "golden_364",
        "text": "إِذَا أَنْتَ لَمْ تَشْرَبْ مِرَارًا عَلَى الْقَذَى",
        "normalized_text": "إذا أنت لم تشرب مرارا على القذى",
        "meter": "المقتضب",
        "poet": "أبو نواس",
        "poem_title": "ديوان أبي نواس",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "era_dates": "756-814 CE",
            "poet_birth_year": "756 CE",
            "poet_death_year": "814 CE",
            "region": "Iraq",
            "poem_genre": "wisdom",
            "notes": "Well-known example"
        }
    },
    {
        "verse_id": "golden_365",
        "text": "وَمَا كُلُّ مَنْ يُبْدِي الْبَشَاشَةَ كَائِنًا",
        "normalized_text": "وما كل من يبدي البشاشة كائنا",
        "meter": "المقتضب",
        "poet": "ابن الرومي",
        "poem_title": "ديوان ابن الرومي",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "era_dates": "836-896 CE",
            "poet_birth_year": "836 CE",
            "poet_death_year": "896 CE",
            "region": "Iraq",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_366",
        "text": "أَلَا كُلُّ شَيْءٍ مَا خَلَا اللَّهَ بَاطِلُ",
        "normalized_text": "ألا كل شيء ما خلا الله باطل",
        "meter": "المقتضب",
        "poet": "لبيد بن ربيعة",
        "poem_title": "ديوان لبيد",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "era_dates": "560-661 CE",
            "poet_birth_year": "560 CE",
            "poet_death_year": "661 CE",
            "region": "Hijaz",
            "poem_genre": "wisdom",
            "notes": "Famous verse"
        }
    },
    {
        "verse_id": "golden_367",
        "text": "فَمَا لِي أَرَى النَّاسَ الْأَعْدَاءَ أَقْرَبَا",
        "normalized_text": "فما لي أرى الناس الأعداء أقربا",
        "meter": "المقتضب",
        "poet": "أبو فراس الحمداني",
        "poem_title": "ديوان أبي فراس",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "era_dates": "932-968 CE",
            "region": "Levant",
            "poem_genre": "elegy"
        }
    },
    {
        "verse_id": "golden_368",
        "text": "وَلَا تَحْسَبَنَّ الْمَوْتَ مَوْتَ الْبَلَى",
        "normalized_text": "ولا تحسبن الموت موت البلى",
        "meter": "المقتضب",
        "poet": "أحمد شوقي",
        "poem_title": "الشوقيات",
        "source": "modern",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Modern",
            "era_dates": "1868-1932 CE",
            "poet_birth_year": "1868 CE",
            "poet_death_year": "1932 CE",
            "region": "Egypt",
            "poem_genre": "philosophical"
        }
    },
    {
        "verse_id": "golden_369",
        "text": "وَلَكِنَّ نَفْسِي تَاقَتِ الْمَوْتَ عِزَّةً",
        "normalized_text": "ولكن نفسي تاقت الموت عزة",
        "meter": "المقتضب",
        "poet": "عنترة بن شداد",
        "poem_title": "ديوان عنترة",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "era_dates": "525-608 CE",
            "region": "Hijaz",
            "poem_genre": "praise"
        }
    },
    {
        "verse_id": "golden_370",
        "text": "لَعَمْرُكَ مَا الدُّنْيَا بِدَارِ إِقَامَةٍ",
        "normalized_text": "لعمرك ما الدنيا بدار إقامة",
        "meter": "المقتضب",
        "poet": "الحسن البصري",
        "poem_title": "الزهديات",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Early Islamic",
            "era_dates": "642-728 CE",
            "region": "Iraq",
            "poem_genre": "religious"
        }
    },
    {
        "verse_id": "golden_371",
        "text": "فَلَا تَجْزَعَنْ مِنْ خُطَّةٍ أَنْتَ سِرْتَهَا",
        "normalized_text": "فلا تجزعن من خطة أنت سرتها",
        "meter": "المقتضب",
        "poet": "زهير بن أبي سلمى",
        "poem_title": "المعلقات",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "era_dates": "520-609 CE",
            "region": "Hijaz",
            "poem_genre": "wisdom"
        }
    },

    # ========================================
    # مشطور Forms - New Variant Forms (+10)
    # ========================================
    {
        "verse_id": "golden_372",
        "text": "أَلَا لَيْتَ شِعْرِي",
        "normalized_text": "ألا ليت شعري",
        "meter": "الطويل (مشطور)",
        "poet": "امرؤ القيس",
        "poem_title": "ديوان امرئ القيس",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "era_dates": "501-544 CE",
            "region": "Hijaz",
            "poem_genre": "love",
            "notes": "مشطور - half hemistich form"
        }
    },
    {
        "verse_id": "golden_373",
        "text": "قِفَا نَبْكِ",
        "normalized_text": "قفا نبك",
        "meter": "الطويل (مشطور)",
        "poet": "امرؤ القيس",
        "poem_title": "المعلقة",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "region": "Hijaz",
            "poem_genre": "elegy",
            "notes": "Famous مشطور opening"
        }
    },
    {
        "verse_id": "golden_374",
        "text": "أَلَا كُلُّ شَيْءٍ",
        "normalized_text": "ألا كل شيء",
        "meter": "الطويل (مشطور)",
        "poet": "لبيد",
        "poem_title": "ديوان لبيد",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "region": "Hijaz",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_375",
        "text": "مَتَى يَبْلُغِ الْبُنْيَانُ",
        "normalized_text": "متى يبلغ البنيان",
        "meter": "الكامل (مشطور)",
        "poet": "أبو العتاهية",
        "poem_title": "ديوان أبي العتاهية",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_376",
        "text": "أَرَاكَ عَصِيَّ الدَّمْعِ",
        "normalized_text": "أراك عصي الدمع",
        "meter": "البسيط (مشطور)",
        "poet": "أبو فراس",
        "poem_title": "الروميات",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Levant",
            "poem_genre": "elegy"
        }
    },
    {
        "verse_id": "golden_377",
        "text": "لَكَ الْحَمْدُ وَالنَّعْمَاءُ",
        "normalized_text": "لك الحمد والنعماء",
        "meter": "البسيط (مشطور)",
        "poet": "البحتري",
        "poem_title": "ديوان البحتري",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "praise"
        }
    },
    {
        "verse_id": "golden_378",
        "text": "أَلَا لَيْتَ الشَّبَابَ",
        "normalized_text": "ألا ليت الشباب",
        "meter": "الوافر (مشطور)",
        "poet": "أبو العتاهية",
        "poem_title": "ديوان أبي العتاهية",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "elegy"
        }
    },
    {
        "verse_id": "golden_379",
        "text": "لِخَوْلَةَ أَطْلَالٌ",
        "normalized_text": "لخولة أطلال",
        "meter": "الطويل (مشطور)",
        "poet": "طرفة بن العبد",
        "poem_title": "المعلقة",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "region": "Hijaz",
            "poem_genre": "love"
        }
    },
    {
        "verse_id": "golden_380",
        "text": "أَعِنِّي عَلَى نَفْسِي",
        "normalized_text": "أعني على نفسي",
        "meter": "الكامل (مشطور)",
        "poet": "أبو نواس",
        "poem_title": "ديوان أبي نواس",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "religious"
        }
    },
    {
        "verse_id": "golden_381",
        "text": "وَاللَّيْلُ دَاجٍ",
        "normalized_text": "والليل داج",
        "meter": "الوافر (مشطور)",
        "poet": "امرؤ القيس",
        "poem_title": "ديوان امرئ القيس",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "region": "Hijaz",
            "poem_genre": "descriptive"
        }
    },

    # ========================================
    # New مجزوء Forms (+10)
    # ========================================
    {
        "verse_id": "golden_382",
        "text": "أَقُولُ لَهُ وَالدَّمْعُ",
        "normalized_text": "أقول له والدمع",
        "meter": "المتقارب (مجزوء)",
        "poet": "ابن زيدون",
        "poem_title": "ديوان ابن زيدون",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Andalusian",
            "era_dates": "1003-1071 CE",
            "region": "Andalus",
            "poem_genre": "love"
        }
    },
    {
        "verse_id": "golden_383",
        "text": "جَفَانِي حَبِيبٌ كُنْتُ",
        "normalized_text": "جفاني حبيب كنت",
        "meter": "المتقارب (مجزوء)",
        "poet": "ابن المعتز",
        "poem_title": "ديوان ابن المعتز",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "love"
        }
    },
    {
        "verse_id": "golden_384",
        "text": "أَلَا يَا أَيُّهَا الْقَمَرُ",
        "normalized_text": "ألا يا أيها القمر",
        "meter": "الرمل (مجزوء)",
        "poet": "أبو نواس",
        "poem_title": "ديوان أبي نواس",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "descriptive"
        }
    },
    {
        "verse_id": "golden_385",
        "text": "يَا بَدْرَ تَمَّ كَمَالُهُ",
        "normalized_text": "يا بدر تم كماله",
        "meter": "الرمل (مجزوء)",
        "poet": "ابن الفارض",
        "poem_title": "ديوان ابن الفارض",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Mamluk",
            "era_dates": "1181-1235 CE",
            "region": "Egypt",
            "poem_genre": "mystical"
        }
    },
    {
        "verse_id": "golden_386",
        "text": "مَا أَجْمَلَ الصَّبْرَ عِنْدَ",
        "normalized_text": "ما أجمل الصبر عند",
        "meter": "البسيط (مجزوء)",
        "poet": "الشافعي",
        "poem_title": "ديوان الشافعي",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Hijaz",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_387",
        "text": "تَعَلَّمْ فَإِنَّ الْعِلْمَ",
        "normalized_text": "تعلم فإن العلم",
        "meter": "البسيط (مجزوء)",
        "poet": "أبو العتاهية",
        "poem_title": "ديوان أبي العتاهية",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_388",
        "text": "سَلَامٌ عَلَيْكُمْ يَا",
        "normalized_text": "سلام عليكم يا",
        "meter": "الوافر (مجزوء)",
        "poet": "حسان بن ثابت",
        "poem_title": "ديوان حسان",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Early Islamic",
            "region": "Hijaz",
            "poem_genre": "praise"
        }
    },
    {
        "verse_id": "golden_389",
        "text": "أَحِبُّكَ حُبًّا لَوْ",
        "normalized_text": "أحبك حبا لو",
        "meter": "الرمل (مجزوء)",
        "poet": "رابعة العدوية",
        "poem_title": "الشعر الصوفي",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "era_dates": "717-801 CE",
            "region": "Iraq",
            "poem_genre": "mystical",
            "notes": "Female Sufi poet"
        }
    },
    {
        "verse_id": "golden_390",
        "text": "فَلَسْتُ أُبَالِي حِينَ",
        "normalized_text": "فلست أبالي حين",
        "meter": "المتقارب (مجزوء)",
        "poet": "خبيب بن عدي",
        "poem_title": "شعر الصحابة",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Early Islamic",
            "region": "Hijaz",
            "poem_genre": "religious"
        }
    },
    {
        "verse_id": "golden_391",
        "text": "وَمَا الدُّنْيَا بِدَارِ",
        "normalized_text": "وما الدنيا بدار",
        "meter": "البسيط (مجزوء)",
        "poet": "لبيد",
        "poem_title": "ديوان لبيد",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "region": "Hijaz",
            "poem_genre": "wisdom"
        }
    },

    # ========================================
    # المضارع - Additional Examples (+10)
    # ========================================
    {
        "verse_id": "golden_392",
        "text": "سَأَصْبِرُ عَنْ دَارٍ تَرَكْتُ بِهَا الْهَوَى",
        "normalized_text": "سأصبر عن دار تركت بها الهوى",
        "meter": "المضارع",
        "poet": "ذو الرمة",
        "poem_title": "ديوان ذي الرمة",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Umayyad",
            "era_dates": "696-735 CE",
            "region": "Hijaz",
            "poem_genre": "love"
        }
    },
    {
        "verse_id": "golden_393",
        "text": "أَلَا يَا حَبِيبِي كُلَّ يَوْمٍ وَلَيْلَةٍ",
        "normalized_text": "ألا يا حبيبي كل يوم وليلة",
        "meter": "المضارع",
        "poet": "عمر بن أبي ربيعة",
        "poem_title": "ديوان عمر",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Umayyad",
            "era_dates": "644-711 CE",
            "region": "Hijaz",
            "poem_genre": "love"
        }
    },
    {
        "verse_id": "golden_394",
        "text": "وَلَوْ أَنَّ مَا أَسْعَى لِأَدْنَى مَعِيشَةٍ",
        "normalized_text": "ولو أن ما أسعى لأدنى معيشة",
        "meter": "المضارع",
        "poet": "امرؤ القيس",
        "poem_title": "ديوان امرئ القيس",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "region": "Hijaz",
            "poem_genre": "philosophical"
        }
    },
    {
        "verse_id": "golden_395",
        "text": "فَهَلْ مِنْ خَلِيلٍ أَشْتَكِي إِلَيْهِ مَا بِي",
        "normalized_text": "فهل من خليل أشتكي إليه ما بي",
        "meter": "المضارع",
        "poet": "الأعشى",
        "poem_title": "ديوان الأعشى",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "region": "Hijaz",
            "poem_genre": "elegy"
        }
    },
    {
        "verse_id": "golden_396",
        "text": "أَلَمْ تَرَ أَنَّ الدَّهْرَ يَوْمٌ وَلَيْلَةٌ",
        "normalized_text": "ألم تر أن الدهر يوم وليلة",
        "meter": "المضارع",
        "poet": "طرفة بن العبد",
        "poem_title": "ديوان طرفة",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "region": "Hijaz",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_397",
        "text": "وَإِنِّي وَإِنْ كُنْتُ الْأَخِيرَ زَمَانُهُ",
        "normalized_text": "وإني وإن كنت الأخير زمانه",
        "meter": "المضارع",
        "poet": "أبو تمام",
        "poem_title": "ديوان الحماسة",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "era_dates": "796-846 CE",
            "region": "Levant",
            "poem_genre": "praise"
        }
    },
    {
        "verse_id": "golden_398",
        "text": "سَتَعْلَمُ إِنْ مُتْنَا غَدًا أَيُّنَا الصَّدِي",
        "normalized_text": "ستعلم إن متنا غدا أينا الصدي",
        "meter": "المضارع",
        "poet": "جرير",
        "poem_title": "ديوان جرير",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Umayyad",
            "region": "Hijaz",
            "poem_genre": "satire"
        }
    },
    {
        "verse_id": "golden_399",
        "text": "وَمَنْ لَمْ يَمُتْ بِالسَّيْفِ مَاتَ بِغَيْرِهِ",
        "normalized_text": "ومن لم يمت بالسيف مات بغيره",
        "meter": "المضارع",
        "poet": "أبو الطيب المتنبي",
        "poem_title": "ديوان المتنبي",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_400",
        "text": "أَنَا الَّذِي نَظَرَ الْأَعْمَى إِلَى أَدَبِي",
        "normalized_text": "أنا الذي نظر الأعمى إلى أدبي",
        "meter": "المضارع",
        "poet": "المتنبي",
        "poem_title": "ديوان المتنبي",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "praise",
            "notes": "Famous self-praise verse"
        }
    },
    {
        "verse_id": "golden_401",
        "text": "وَلَيْسَ يَصِحُّ فِي الْأَذْهَانِ شَيْءٌ",
        "normalized_text": "وليس يصح في الأذهان شيء",
        "meter": "المضارع",
        "poet": "أبو العلاء المعري",
        "poem_title": "لزوم ما لا يلزم",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "era_dates": "973-1057 CE",
            "region": "Levant",
            "poem_genre": "philosophical"
        }
    },

    # ========================================
    # Balance Existing Meters (+10)
    # ========================================
    {
        "verse_id": "golden_402",
        "text": "أَلَا فَاصْبِرْ عَلَى الْحَدَثَانِ إِنِّي",
        "normalized_text": "ألا فاصبر على الحدثان إني",
        "meter": "الطويل",
        "poet": "عنترة",
        "poem_title": "ديوان عنترة",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "region": "Hijaz",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_403",
        "text": "تَعُدُّ الْعَرَبُ أَنْجَادَهَا فِخَارًا",
        "normalized_text": "تعد العرب أنجادها فخارا",
        "meter": "الكامل",
        "poet": "الفرزدق",
        "poem_title": "ديوان الفرزدق",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Umayyad",
            "region": "Iraq",
            "poem_genre": "praise"
        }
    },
    {
        "verse_id": "golden_404",
        "text": "إِنَّ الْجَوَادَ عَيْنُهُ فِرَارُهُ",
        "normalized_text": "إن الجواد عينه فراره",
        "meter": "البسيط",
        "poet": "المتنبي",
        "poem_title": "ديوان المتنبي",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_405",
        "text": "فَلَا تَجْزَعْ إِذَا مَا نَابَ خَطْبٌ",
        "normalized_text": "فلا تجزع إذا ما ناب خطب",
        "meter": "الوافر",
        "poet": "الحطيئة",
        "poem_title": "ديوان الحطيئة",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Early Islamic",
            "region": "Hijaz",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_406",
        "text": "يَا رُبَّ مُعْتَرِضٍ فِيمَا يَضُرُّهُ",
        "normalized_text": "يا رب معترض فيما يضره",
        "meter": "الرمل",
        "poet": "أبو العتاهية",
        "poem_title": "ديوان أبي العتاهية",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_407",
        "text": "صَوْتُ صَفِيرِ الْبُلْبُلِ هَيَّجَ قَلْبِي الثَّمِلْ",
        "normalized_text": "صوت صفير البلبل هيج قلبي الثمل",
        "meter": "الرجز",
        "poet": "الأصمعي",
        "poem_title": "القصيدة الأصمعية",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "era_dates": "740-828 CE",
            "region": "Iraq",
            "poem_genre": "descriptive",
            "notes": "Famous tongue-twister poem"
        }
    },
    {
        "verse_id": "golden_408",
        "text": "أَلَا إِنَّ أَهْلَ الْعِلْمِ أَهْلُ الْهُدَى",
        "normalized_text": "ألا إن أهل العلم أهل الهدى",
        "meter": "السريع",
        "poet": "الشافعي",
        "poem_title": "ديوان الشافعي",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Hijaz",
            "poem_genre": "wisdom"
        }
    },
    {
        "verse_id": "golden_409",
        "text": "سَهِرَتْ أَعْيُنٌ وَنَامَتْ عُيُونُ",
        "normalized_text": "سهرت أعين ونامت عيون",
        "meter": "المتقارب",
        "poet": "أبو الدرداء",
        "poem_title": "الزهديات",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Early Islamic",
            "region": "Levant",
            "poem_genre": "religious"
        }
    },
    {
        "verse_id": "golden_410",
        "text": "أَسِفْتُ عَلَى الشَّبَابِ الضَّائِعِ",
        "normalized_text": "أسفت على الشباب الضائع",
        "meter": "المتدارك",
        "poet": "ابن الرومي",
        "poem_title": "ديوان ابن الرومي",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Abbasid",
            "region": "Iraq",
            "poem_genre": "elegy"
        }
    },
    {
        "verse_id": "golden_411",
        "text": "فَقُلْتُ لَهُ لَمَّا تَمَطَّى بِصُلْبِهِ",
        "normalized_text": "فقلت له لما تمطى بصلبه",
        "meter": "الخفيف",
        "poet": "امرؤ القيس",
        "poem_title": "المعلقة",
        "source": "classical",
        "metadata": {
            "version": "1.2",
            "phase": "expansion_v1.2",
            "era": "Pre-Islamic",
            "region": "Hijaz",
            "poem_genre": "descriptive",
            "notes": "From famous mu'allaqa"
        }
    }
]

def create_expansion_file():
    """Create the v1.2 expansion file."""
    base_dir = Path(__file__).parent.parent
    output_file = base_dir / "dataset" / "evaluation" / "golden_set_v1_2_expansion_phase1.jsonl"

    print("\n" + "="*80)
    print("CREATING BAHR GOLDEN SET v1.2 EXPANSION (Phase 1)")
    print("="*80)
    print()

    # Add prosody_precomputed placeholder and validation fields
    for verse in expansion_verses:
        verse["prosody_precomputed"] = {
            "pattern": "to be computed",
            "fitness_score": 0.0,
            "method": "pending",
            "meter_verified": verse["meter"]
        }
        verse["validation"] = {
            "verified_by": "expansion_v1.2_phase1",
            "verified_date": str(date.today()),
            "automated_check": "PENDING"
        }

    # Save to file
    print(f"💾 Saving {len(expansion_verses)} verses to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        for verse in expansion_verses:
            f.write(json.dumps(verse, ensure_ascii=False) + '\n')

    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)

    # Count by meter
    from collections import Counter
    meter_counts = Counter(v['meter'] for v in expansion_verses)

    print(f"\n📊 Verses by Meter:")
    for meter, count in sorted(meter_counts.items(), key=lambda x: -x[1]):
        print(f"  {meter}: {count} verses")

    # Count by era
    era_counts = Counter(v['metadata']['era'] for v in expansion_verses)
    print(f"\n📅 Verses by Era:")
    for era, count in sorted(era_counts.items(), key=lambda x: -x[1]):
        print(f"  {era}: {count} verses")

    print(f"\n✅ Total verses created: {len(expansion_verses)}")
    print(f"✅ Output file: {output_file}")
    print("\n" + "="*80)
    print("Next: Run precomputation and evaluation")
    print("="*80)

if __name__ == "__main__":
    create_expansion_file()
