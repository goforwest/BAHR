"""
Poet biographical database for metadata enhancement
Maps poet names to historical information (era, dates, region)
"""

POET_DATABASE = {
    # Pre-Islamic Era (500-622 CE)
    "امرؤ القيس": {
        "era": "Pre-Islamic",
        "era_dates": "500-622 CE",
        "poet_birth_year": "501 CE",
        "poet_death_year": "544 CE",
        "region": "Hijaz",
        "notes": "صاحب المعلقة الأولى، أشهر شعراء الجاهلية"
    },
    "عنترة بن شداد": {
        "era": "Pre-Islamic",
        "era_dates": "525-608 CE",
        "poet_birth_year": "525 CE",
        "poet_death_year": "608 CE",
        "region": "Hijaz",
        "notes": "صاحب المعلقة، فارس وشاعر"
    },
    "عنترة": {
        "era": "Pre-Islamic",
        "era_dates": "525-608 CE",
        "poet_birth_year": "525 CE",
        "poet_death_year": "608 CE",
        "region": "Hijaz",
        "notes": "صاحب المعلقة، فارس وشاعر"
    },
    "الشنفرى": {
        "era": "Pre-Islamic",
        "era_dates": "500-622 CE",
        "poet_birth_year": "550 CE",
        "poet_death_year": "525 BCE",  # Uncertain
        "region": "Hijaz",
        "notes": "صاحب لامية العرب، من شعراء الصعاليك"
    },
    "أبو ذؤيب الهذلي": {
        "era": "Pre-Islamic",
        "era_dates": "580-645 CE",
        "poet_birth_year": "580 CE",
        "poet_death_year": "645 CE",
        "region": "Hijaz",
        "notes": "من شعراء الهذليين، أدرك الإسلام"
    },
    "ميمون بن قيس": {
        "era": "Pre-Islamic",
        "era_dates": "570-629 CE",
        "poet_birth_year": "570 CE",
        "poet_death_year": "629 CE",
        "region": "Hijaz",
        "notes": "الأعشى، صناجة العرب"
    },

    # Early Islamic Era (622-661 CE)
    "جميل بثينة": {
        "era": "Umayyad",
        "era_dates": "660-750 CE",
        "poet_birth_year": "659 CE",
        "poet_death_year": "701 CE",
        "region": "Hijaz",
        "notes": "شاعر الغزل العذري"
    },

    # Umayyad Era (661-750 CE)
    "ابن الدمينة": {
        "era": "Umayyad",
        "era_dates": "661-750 CE",
        "poet_birth_year": "660 CE",
        "poet_death_year": "746 CE",
        "region": "Hijaz",
        "notes": "شاعر غزل عذري"
    },

    # Abbasid Era (750-1258 CE)
    "أبو نواس": {
        "era": "Abbasid",
        "era_dates": "750-1258 CE",
        "poet_birth_year": "756 CE",
        "poet_death_year": "814 CE",
        "region": "Iraq",
        "notes": "شاعر الخمر والمجون"
    },
    "أبو تمام": {
        "era": "Abbasid",
        "era_dates": "750-1258 CE",
        "poet_birth_year": "796 CE",
        "poet_death_year": "845 CE",
        "region": "Levant",
        "notes": "شاعر ومختار الحماسة"
    },
    "البحتري": {
        "era": "Abbasid",
        "era_dates": "750-1258 CE",
        "poet_birth_year": "821 CE",
        "poet_death_year": "897 CE",
        "region": "Levant",
        "notes": "من أعظم شعراء العصر العباسي"
    },
    "ابن الرومي": {
        "era": "Abbasid",
        "era_dates": "750-1258 CE",
        "poet_birth_year": "836 CE",
        "poet_death_year": "896 CE",
        "region": "Iraq",
        "notes": "شاعر التصوير الدقيق"
    },
    "أبو فراس الحمداني": {
        "era": "Abbasid",
        "era_dates": "750-1258 CE",
        "poet_birth_year": "932 CE",
        "poet_death_year": "968 CE",
        "region": "Levant",
        "notes": "شاعر الروميات"
    },
    "المتنبي": {
        "era": "Abbasid",
        "era_dates": "750-1258 CE",
        "poet_birth_year": "915 CE",
        "poet_death_year": "965 CE",
        "region": "Iraq",
        "notes": "أعظم شعراء العرب"
    },
    "أبو الطيب المتنبي": {
        "era": "Abbasid",
        "era_dates": "750-1258 CE",
        "poet_birth_year": "915 CE",
        "poet_death_year": "965 CE",
        "region": "Iraq",
        "notes": "أعظم شعراء العرب"
    },
    "أبو العلاء المعري": {
        "era": "Abbasid",
        "era_dates": "750-1258 CE",
        "poet_birth_year": "973 CE",
        "poet_death_year": "1057 CE",
        "region": "Levant",
        "notes": "رهين المحبسين، فيلسوف الشعراء"
    },
    "الإمام الشافعي": {
        "era": "Abbasid",
        "era_dates": "750-1258 CE",
        "poet_birth_year": "767 CE",
        "poet_death_year": "820 CE",
        "region": "Egypt",
        "notes": "إمام فقيه وشاعر حكيم"
    },
    "علي بن أبي طالب": {
        "era": "Early Islamic",
        "era_dates": "622-661 CE",
        "poet_birth_year": "601 CE",
        "poet_death_year": "661 CE",
        "region": "Hijaz",
        "notes": "الخليفة الرابع وأمير المؤمنين"
    },

    # Andalusian Era (711-1492 CE)
    "ابن زيدون": {
        "era": "Andalusian",
        "era_dates": "711-1492 CE",
        "poet_birth_year": "1003 CE",
        "poet_death_year": "1071 CE",
        "region": "Andalus",
        "notes": "شاعر الأندلس الأكبر"
    },

    # Mamluk Era (1250-1517 CE)
    "ابن الوردي": {
        "era": "Mamluk",
        "era_dates": "1250-1517 CE",
        "poet_birth_year": "1291 CE",
        "poet_death_year": "1349 CE",
        "region": "Levant",
        "notes": "صاحب اللامية المشهورة"
    },
    "ابن أبي الحديد": {
        "era": "Abbasid",
        "era_dates": "750-1258 CE",
        "poet_birth_year": "1190 CE",
        "poet_death_year": "1258 CE",
        "region": "Iraq",
        "notes": "شارح نهج البلاغة"
    },

    # Modern Era (1798-1950 CE)
    "أحمد شوقي": {
        "era": "Modern",
        "era_dates": "1798-1950 CE",
        "poet_birth_year": "1868 CE",
        "poet_death_year": "1932 CE",
        "region": "Egypt",
        "notes": "أمير الشعراء"
    },
    "حافظ إبراهيم": {
        "era": "Modern",
        "era_dates": "1798-1950 CE",
        "poet_birth_year": "1872 CE",
        "poet_death_year": "1932 CE",
        "region": "Egypt",
        "notes": "شاعر النيل"
    },
    "محمود سامي البارودي": {
        "era": "Modern",
        "era_dates": "1798-1950 CE",
        "poet_birth_year": "1839 CE",
        "poet_death_year": "1904 CE",
        "region": "Egypt",
        "notes": "رائد الشعر الحديث"
    },
    "إسماعيل صبري": {
        "era": "Modern",
        "era_dates": "1798-1950 CE",
        "poet_birth_year": "1854 CE",
        "poet_death_year": "1923 CE",
        "region": "Egypt",
        "notes": "شاعر مصري"
    },
}

# Genre classification for unknown/generic verses
GENRE_BY_KEYWORDS = {
    "حكمة": ["حكمة", "wisdom", "صبر", "دهر", "زمان", "علم"],
    "غزل": ["حبيب", "ليلة", "هوى", "فؤاد", "وصل"],
    "فخر": ["مجد", "عز", "سرج", "فارس", "بطل"],
    "رثاء": ["موت", "زمن مضى", "بكى", "أسف"],
    "وصف": ["نار", "صبح", "دهر", "مزن", "طلل"],
    "مدح": ["ممدوح", "كريم", "جواد", "ماجد"],
}

def get_poet_metadata(poet_name):
    """Get metadata for a poet, with fallback for unknown poets"""
    # Direct match
    if poet_name in POET_DATABASE:
        return POET_DATABASE[poet_name].copy()

    # Partial match (e.g., "المتنبي" vs "أبو الطيب المتنبي")
    for key in POET_DATABASE:
        if poet_name in key or key in poet_name:
            return POET_DATABASE[key].copy()

    # Unknown poet - return generic classical era
    return {
        "era": "classical",
        "era_dates": "500-1258 CE",
        "poet_birth_year": "Unknown",
        "poet_death_year": "Unknown",
        "region": "Unknown",
        "notes": "شاعر غير معروف"
    }

def infer_genre(text, source, notes):
    """Infer genre from verse text, source, or notes"""
    combined_text = f"{text} {source} {notes}".lower()

    for genre, keywords in GENRE_BY_KEYWORDS.items():
        if any(keyword in combined_text for keyword in keywords):
            return genre

    # Default
    return "general"
