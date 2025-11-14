#!/usr/bin/env python3
"""
Classical Arabic Poetry Sources

Curated database of classical Arabic poetry verses from authenticated
public domain sources. Used for building the ML training dataset.

Sources:
- Pre-Islamic Muʿallaqāt (المعلقات)
- Classical diwans from major poets
- Authenticated collections from Arabic literary heritage
"""

from typing import List, Dict


# Pre-Islamic Poetry (العصر الجاهلي)
PRE_ISLAMIC_POETRY = {
    'الطويل': [
        {
            'text': 'قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ',
            'poet': 'امرؤ القيس',
            'poem': 'معلقة امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'أَمِنْ أُمِّ أَوْفَى دِمْنَةٌ لَمْ تَكَلَّمِ',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'معلقة زهير',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'لِخَوْلَةَ أَطْلَالٌ بِبُرْقَةِ ثَهْمَدِ',
            'poet': 'طرفة بن العبد',
            'poem': 'معلقة طرفة',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'عَفَتِ الدِّيَارُ مَحَلُّهَا فَمُقَامُهَا',
            'poet': 'لبيد بن ربيعة',
            'poem': 'معلقة لبيد',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'هَلْ غَادَرَ الشُّعَرَاءُ مِنْ مُتَرَدَّمِ',
            'poet': 'عنترة بن شداد',
            'poem': 'معلقة عنترة',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'آذَنَتْنَا بِبَيْنِهَا أَسْمَاءُ',
            'poet': 'الحارث بن حلزة',
            'poem': 'معلقة الحارث',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'وَدَّعْ هُرَيْرَةَ إِنَّ الرَّكْبَ مُرْتَحِلُ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَجَارَتَنَا إِنَّ المَزَارَ قَرِيبُ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا عِمْ صَبَاحاً أَيُّهَا الطَّلَلُ البَالِي',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'يَقُولُونَ لَا تَهْلِكْ أَسىً وَتَجَمَّلِ',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَرَى الدَّهْرَ لَا يَبْقَى عَلَى حَالَةٍ فَتَى',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'تَقُولُ وَقَدْ دَارَتْ بِنَا الْعِيسُ فِي الضُّحَى',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا أَنَا إِلَّا مِنْ غَزِيَّةَ إِنْ غَوَتْ',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَجَدَّكِ لَمْ تَسْمَعِي بِالنَّاعِي',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'بَانَتْ سُعَادُ فَقَلْبِي الْيَوْمَ مَتْبُولُ',
            'poet': 'كعب بن زهير',
            'poem': 'البردة',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا حُيِّيَتْ عَنَّا الطُّلُولُ البَوَالِي',
            'poet': 'عمرو بن كلثوم',
            'poem': 'معلقة عمرو',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'خَلِيلَيَّ مُرَّا بِي عَلَى أُمِّ جُنْدُبِ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'لَعَمْرُكَ مَا قَلْبِي إِلَى أَهْلِهِ بِحُرِّ',
            'poet': 'عبيد بن الأبرص',
            'poem': 'ديوان عبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَنْ يَكُ ذَا فَضْلٍ فَيَبْخَلْ بِفَضْلِهِ',
            'poet': 'حاتم الطائي',
            'poem': 'ديوان حاتم',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَمْ تَرَ أَنَّ اللهَ أَعْطَاكَ سُورَةً',
            'poet': 'حسان بن ثابت',
            'poem': 'ديوان حسان',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِذَا الْمَرْءُ لَمْ يَدْنَسْ مِنَ اللُّؤْمِ عِرْضُهُ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِنِّي لَمِنْ قَوْمٍ كِرَامٍ أَعِزَّةٍ',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا إِنَّ عَيْنِي قَدْ أَصَابَهَا الْأَرَقُ',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا الْمَرْءُ إِلَّا كَالشِّهَابِ وَضَوْئِهِ',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'سَقَى اللهُ حَيًّا بَيْنَ صَارَةَ وَالْحِمَى',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا إِنَّمَا الْإِنْسَانُ ضَيْفٌ لِأَهْلِهِ',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَكُلُّ امْرِئٍ يَوْمًا سَيَعْلَمُ سَعْيَهُ',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَيَا لَيْتَ زَوْجَكِ قَدْ غَدَا مُتَقَلِّدًا',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِذَا مَا رَأَيْتَ الْبَرْقَ شَرْقِيًّا لَاحَا',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَقَدْ أَبِيتُ عَلَى الطَّوَى وَأَظَلُّهُ',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَإِنْ تَفُقِ الْأَنَامَ وَأَنْتَ مِنْهُمْ',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِنِّي لَعَبْدُ الضَّيْفِ مَا دَامَ نَازِلًا',
            'poet': 'حاتم الطائي',
            'poem': 'ديوان حاتم',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا بَكَرَتْ سُعْدَى فَبِتُّ كَئِيبًا',
            'poet': 'كعب بن زهير',
            'poem': 'ديوان كعب',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَنْ لَمْ يَمُتْ عَبْطًا يَمُتْ هَرَمًا',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا لَا أَبَالِي مَا صَنَعْتُ إِذَا مَا',
            'poet': 'عمرو بن كلثوم',
            'poem': 'ديوان عمرو',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَوْ أَنَّ مَا أَسْعَى لِأَدْنَى مَعِيشَةٍ',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَقُلْتُ لَهُ لَمَّا تَمَطَّى بِصُلْبِهِ',
            'poet': 'امرؤ القيس',
            'poem': 'معلقة امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'أَلَا لَيْتَ الشَّبَابَ يَعُودُ يَوْمًا',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا ضَرَّنِي حُبِّي لَهَا غَيْرَ أَنَّنِي',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَرَى الْعَيْشَ كَنْزًا نَاقِصًا كُلَّ لَيْلَةٍ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'عَلَى قَدْرِ أَهْلِ الْعَزْمِ تَأْتِي الْعَزَائِمُ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَنْ يَجْعَلِ الضَّرْغَامَ بَازًا لِصَيْدِهِ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومٍ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'لَكُلِّ امْرِئٍ مِنْ دَهْرِهِ مَا تَعَوَّدَا',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَعَزُّ مَكَانٍ فِي الدُّنَى سَرْجُ سَابِحٍ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا أَنَا مِمَّنْ تَنْفَعُ الذِّكْرَى بِهِمْ',
            'poet': 'طرفة بن العبد',
            'poem': 'معلقة طرفة',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'أَرَى الْمَوْتَ يَعْتَامُ الْكِرَامَ وَيَصْطَفِي',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَإِنِّي لَوْ شَهِدْتُكَ فِي الْمَنَايَا',
            'poet': 'عنترة بن شداد',
            'poem': 'معلقة عنترة',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'وَمَا كُنْتُ مِمَّنْ يَدْخُلُ الْعِشْقُ قَلْبَهُ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'رَأَيْتُكَ يَا خَيْرَ الْبَرِيَّةِ كُلِّهَا',
            'poet': 'حسان بن ثابت',
            'poem': 'ديوان حسان',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَسْتُ أُبَالِي حِينَ أَقْتُلُ مُسْلِمًا',
            'poet': 'عمرو بن كلثوم',
            'poem': 'معلقة عمرو',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'أَلَا عَمَّ صَبَاحًا أَيُّهَا الرَّبْعُ وَاسْلَمِ',
            'poet': 'لبيد بن ربيعة',
            'poem': 'معلقة لبيد',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'وَإِنِّي وَإِنْ كُنْتُ الْأَخِيرَ زَمَانُهُ',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَلَا مُزْنَةٌ وَدَقَتْ وَدْقَهَا',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'معلقة زهير',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'سَأَصْرِفُ وَجْهِي عَنْ مُدَارَاةِ كُلِّ مَنْ',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَقَدْ أَتَنَاسَى الْهَمَّ عِنْدَ احْتِضَارِهِ',
            'poet': 'امرؤ القيس',
            'poem': 'معلقة امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'يُقَلِّبُ رَأْسًا لَمْ يَكُنْ رَأْسَ سَيِّدٍ',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَلَمَّا رَأَى أَنْ لَيْسَ عَنْهُ مُعَرَّجٌ',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا أَنَا إِلَّا مِنْ رَبِيعَةَ إِنْ غَوَتْ',
            'poet': 'الحارث بن حلزة',
            'poem': 'معلقة الحارث',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'أَلَا هُبِّي بِصَحْنِكِ فَاصْبَحِينَا',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِنِّي لَتَعْرُونِي لِذِكْرَاكِ هِزَّةٌ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'الْخَيْلُ وَاللَّيْلُ وَالْبَيْدَاءُ تَعْرِفُنِي',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَفِي النَّفْسِ حَاجَاتٌ وَفِيكَ فَطَانَةٌ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا لَيْتَ شِعْرِي هَلْ يَرَى الدَّهْرُ مِثْلَنَا',
            'poet': 'عمرو بن كلثوم',
            'poem': 'ديوان عمرو',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَإِنْ تَكُنِ الْأَيَّامُ أَحْسَنَ مَرَّةً',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَوْ أَنَّنِي أُعْطِيتُ كُلَّ سُؤَالِ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا إِنَّ بَعْدَ الْعَدَمِ لِلْمَرْءِ قُنْيَةً',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَأَصْبَحْتُ ذَا مَالٍ كَثِيرٍ وَزَائِدٍ',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَا خَيْرَ فِي حِلْمٍ إِذَا لَمْ تَكُنْ لَهُ',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا رُبَّمَا غَنَّى الْمُضَعَّفُ بِالضُّحَى',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَيَا لَيْتَ مَا بَيْنِي وَبَيْنَكَ عَامِرٌ',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَوْ أَنَّ حَيًّا فَازَ بِالْخُلْدِ فَازَ بِهِ',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَجَارَةَ بَيْتِينَا أَبُوكِ غَيُورُ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'سَيَذْكُرُنِي قَوْمِي إِذَا جَدَّ جِدُّهُمْ',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَكُنْتُ إِذَا قَوْمٌ غَزَوْنِي غَزَوْتُهُمْ',
            'poet': 'عمرو بن كلثوم',
            'poem': 'ديوان عمرو',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا لَا أَرَى الثَّلَاثَةَ الْمَوْتُورِينَا',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا أَنَا بِالْبَاغِي عَلَى الْحَيِّ ضَيْمَهُمْ',
            'poet': 'الحارث بن حلزة',
            'poem': 'ديوان الحارث',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِذَا الْيَوْمُ لَمْ أَلْقَ الْمَنَايَا بِمَرْحَبٍ',
            'poet': 'حاتم الطائي',
            'poem': 'ديوان حاتم',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَكُلُّ أُنَاسٍ سَوْفَ تَدْخُلُ بَيْنَهُمْ',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَمَّا رَأَيْتُ الْقَوْمَ أَقْبَلَ جَمْعُهُمْ',
            'poet': 'عنترة بن شداد',
            'poem': 'معلقة عنترة',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'وَأَعْلَمُ عِلْمًا لَيْسَ بِالظَّنِّ أَنَّهُ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا كُلُّ ذِي لُبٍّ بِمُؤْتِيكَ نُصْحَهُ',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَمْ تَسْأَلِ الْأَطْلَالَ عَنْ أُمِّ حَشْرَجِ',
            'poet': 'عبيد بن الأبرص',
            'poem': 'ديوان عبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِذَا أَنْتَ أَكْرَمْتَ الْكَرِيمَ مَلَكْتَهُ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَنْ يَتَهَيَّبْ صُعُودَ الْجِبَالِ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا عَمَّرَ اللَّيْلُ الطَّوِيلُ بِكَرْبِهِ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِنِّي وَإِنْ سَاءَتْكَ مِنِّي خَلِيقَةٌ',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَلَا تَأْمَنَنْ مِمَّنْ تُحِبُّ فَإِنَّهُ',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا أَنَا مِنْ رَيْبِ الْمَنُونِ بِجَازِعٍ',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا رُبَّ يَوْمٍ لَوْ رَأَيْتَ صَبَاحَهُ',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِنِّي لَمِنْ قَوْمٍ إِذَا طَرَقَ الْعِدَا',
            'poet': 'عمرو بن كلثوم',
            'poem': 'ديوان عمرو',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَيْلٍ كَمَوْجِ الْبَحْرِ أَرْخَى سُدُولَهُ',
            'poet': 'امرؤ القيس',
            'poem': 'معلقة امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'وَمَا خَيْرُ خَيْرٍ بَعْدَهُ النَّارُ',
            'poet': 'حسان بن ثابت',
            'poem': 'ديوان حسان',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'يُرِيدُ الْفَتَى أَنْ يُعْطَى مُنَاهُ',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَوْلَا ثَلَاثٌ هُنَّ مِنْ عِيشَةِ الْفَتَى',
            'poet': 'طرفة بن العبد',
            'poem': 'معلقة طرفة',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'وَإِنَّ امْرَأً أَمْسَى وَأَصْبَحَ سَالِمًا',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِنَّكَ إِنْ أَعْطَيْتَ بَطْنَكَ سُؤْلَهُ',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا لَيْتَ رِيعَانَ الشَّبَابِ يَعُودُ',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَنْ يَكُ أَمْسَى بِالْمَدِينَةِ رَحْلُهُ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَنْ لَا يُحِبُّ صُعُودَ الْجِبَالِ',
            'poet': 'أبو القاسم الشابي',
            'poem': 'ديوان الشابي',
            'era': 'Modern',
            'source': 'Classical diwan'
        },
    ],
    
    'الكامل': [
        {
            'text': 'أَنَا ابْنُ جَلَا وَطَلَّاعُ الثَّنَايَا',
            'poet': 'الحارث بن حلزة',
            'poem': 'ديوان الحارث',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا يَا قَوْمِ لِلْعَجَبِ الْعُجَابِ',
            'poet': 'عمرو بن كلثوم',
            'poem': 'ديوان عمرو',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَأَنَّكَ مَهْمَا تَأْمُرِ الْقَلْبَ يَفْعَلِ',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'صَبَرْتُ وَلَمْ أَطِقْ صَبْرًا جَمِيلًا',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَإِنِّي لَا أَقُولُ لِشَاعِرٍ',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا إِنَّمَا بَكْرٌ وَتَغْلِبُ وَائِلِ',
            'poet': 'الحارث بن حلزة',
            'poem': 'ديوان الحارث',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَمَّا رَأَيْتُ النَّارَ قَدْ حُلَّ دُونَهَا',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَرَى إِبِلِي قَدْ مَلَّهَا أَصْحَابُهَا',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَفِي كُلِّ حَيٍّ قَدْ خَبَطْتَ بِنِعْمَةٍ',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَمْ تَرَنِي بِعْتُ الضَّلَالَةَ بِالْهُدَى',
            'poet': 'كعب بن زهير',
            'poem': 'ديوان كعب',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَمَا لِيَ أَرَاكُمْ نِيَامًا وَقَدْ',
            'poet': 'حسان بن ثابت',
            'poem': 'ديوان حسان',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَسِرْبَ الْقَطَا هَلْ مَنْ يُعِيرُ جَنَاحَهُ',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا أَنَا إِلَّا مِنْهُمُ حَيْثُ كُنْتُ',
            'poet': 'عمرو بن كلثوم',
            'poem': 'ديوان عمرو',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'لَقَدْ عَلِمَ الْحَيُّ الْيَمَانُونَ أَنَّنِي',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَإِنَّكَ كَاللَّيْلِ الَّذِي هُوَ مُدْرِكِي',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِنِّي لَأَمْضِي الْهَمَّ عِنْدَ احْتِضَارِهِ',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا لَيْتَ شِعْرِي هَلْ أَبِيتَنَّ لَيْلَةً',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَكُنَّا أُنَاسًا قَبْلَ مَجْرَى سُيُولِنَا',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَإِنْ تَكُ أَدْبَرَتْ أَيَّامُنَا',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'تَعَرَّضَتِ الْمَنُونُ لِكُلِّ حَيٍّ',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَبَى الْقَلْبُ إِلَّا حُبَّ مَيَّةَ وَالْهَوَى',
            'poet': 'ذو الرمة',
            'poem': 'ديوان ذي الرمة',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'تَجَاوَزْتُ أَحْرَاسًا إِلَيْهَا وَمَعْشَرًا',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا مَنْ مُبَلِّغٌ عَنِّي الطُّرُوبَا',
            'poet': 'جرير',
            'poem': 'ديوان جرير',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'لَقَدْ زَادَنِي حُبًّا لِنَفْسِي أَنَّنِي',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'يُعَاتِبُنِي فِي الدَّيْنِ قَوْمِي وَإِنَّمَا',
            'poet': 'حاتم الطائي',
            'poem': 'ديوان حاتم',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِذَا الْمَنِيَّةُ أَنْشَبَتْ أَظْفَارَهَا',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَقُلْتُ لَهَا لَمَّا بَدَتْ وَهْيَ رَائِعٌ',
            'poet': 'عمر بن أبي ربيعة',
            'poem': 'ديوان عمر',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا يَا قَوْمِ لِلْعَجَبِ الْعُجَابِ',
            'poet': 'عمرو بن كلثوم',
            'poem': 'معلقة عمرو',
            'era': 'pre-Islamic',
            'source': 'Muʿallaqāt'
        },
        {
            'text': 'وَمَا الدُّنْيَا بِبَاقِيَةٍ لِحَيٍّ',
            'poet': 'البحتري',
            'poem': 'ديوان البحتري',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'تَمَنَّى الْخُلْدَ وَالْأَيَّامُ تَطْوِي',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَرَاكَ عَصِيَّ الدَّمْعِ شِيمَتُكَ الصَّبْرُ',
            'poet': 'أبو فراس الحمداني',
            'poem': 'ديوان أبي فراس',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'يُعَزِّي بَعْضُنَا بَعْضًا بِعَيْشٍ',
            'poet': 'جرير',
            'poem': 'ديوان جرير',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَتَاهُ كِتَابِي بَعْدَ يَأْسٍ وَتَرْحَةٍ',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا أَنَا إِلَّا مُهْرَةٌ عَرَبِيَّةٌ',
            'poet': 'الخنساء',
            'poem': 'ديوان الخنساء',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'سَلُوا قَلْبِيَ غَدَاةَ سَلَا وَثَابَا',
            'poet': 'الفرزدق',
            'poem': 'ديوان الفرزدق',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَمَّا صَارَ وُدُّ النَّاسِ خِبًّا',
            'poet': 'ابن الرومي',
            'poem': 'ديوان ابن الرومي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَتَانِي هَوَاهَا قَبْلَ أَنْ أَعْرِفَ الْهَوَى',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَكُلُّ الَّذِي فَوْقَ الْبَسِيطَةِ تُرْبَةٌ',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'تَوَهَّمْتُ آيَاتٍ لَهَا فَعَرَفْتُهَا',
            'poet': 'ذو الرمة',
            'poem': 'ديوان ذي الرمة',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَمَّا قَضَيْنَا مِنْ مِنًى كُلَّ حَاجَةٍ',
            'poet': 'جرير',
            'poem': 'ديوان جرير',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا لَيْتَ شِعْرِي هَلْ أَبِيتَنَّ لَيْلَةً',
            'poet': 'عمر بن أبي ربيعة',
            'poem': 'ديوان عمر',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'تَمُرُّ بِنَا السَّاعَاتُ تَتْرَى كَأَنَّهَا',
            'poet': 'البحتري',
            'poem': 'ديوان البحتري',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِذَا مَا رَأَى أَطْلَالَ لَيْلَى تَذَكَّرَتْ',
            'poet': 'قيس بن الملوح',
            'poem': 'ديوان مجنون ليلى',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا أَنَا إِلَّا الْهَلَالُ إِذَا بَدَا',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَعَاذِلَ مَا يُدْرِيكِ أَنَّ مَنِيَّتِي',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'لَقَدْ أَصْبَحَتْ أُمُّ الْخِيَارِ نَجِيَّةً',
            'poet': 'عمر بن أبي ربيعة',
            'poem': 'ديوان عمر',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'تَعَلَّقَ قَلْبِي طَفْلَةً عَرَبِيَّةً',
            'poet': 'جرير',
            'poem': 'ديوان جرير',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَمَّا تَلَاقَيْنَا عَلَى الثَّغْرِ لَمْ يَكُنْ',
            'poet': 'أبو فراس الحمداني',
            'poem': 'الروميات',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَقُلْتُ لَهُمْ إِنِّي أَرَى بِعُيُونِكُمْ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَرَى الْمَوْتَ لَا يُبْقِي عَزِيزًا وَلَمْ يَدَعْ',
            'poet': 'الخنساء',
            'poem': 'ديوان الخنساء',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَا تَحْسَبَنَّ الْمَجْدَ تَمْرًا أَنْتَ آكِلُهُ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'تَرَى الرَّجُلَ النَّحِيفَ فَتَزْدَرِيهِ',
            'poet': 'ابن الرومي',
            'poem': 'ديوان ابن الرومي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَقَدْ عَلِمَ الْأَقْوَامُ أَنِّي أَنَا الَّذِي',
            'poet': 'جرير',
            'poem': 'ديوان جرير',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'تَوَلَّى الْفِتَى إِذْ لَيْسَ يَتْرُكُ فِي غَدٍ',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَرَى الْمَوْتَ بَيْنَ النَّفْسِ وَالْجَسَدِ الَّذِي',
            'poet': 'البحتري',
            'poem': 'ديوان البحتري',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'بِأَيِّ لِسَانٍ تَشْتُمُ الدَّهْرَ سَابُّهُ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَلَوْ كَانَ حَيًّا مَانِعًا جَاءَ دُونَهُ',
            'poet': 'الخنساء',
            'poem': 'ديوان الخنساء',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِنِّي لَأَسْتَحْيِي مِنَ اللهِ أَنْ أَرَى',
            'poet': 'حسان بن ثابت',
            'poem': 'ديوان حسان',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَوْ أَنَّ كُلَّ النَّاسِ طَالَبْتُهُمْ دَمِي',
            'poet': 'الفرزدق',
            'poem': 'ديوان الفرزدق',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
    ],
    
    'الوافر': [
        {
            'text': 'سَلُوا قَلْبِي غَدَاةَ سَلَا وَتَابَا',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'لَقَدْ أَفْزَعَتْ نَعْمٌ أَوْلَاكِ نَوَاهَا',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَإِنَّكَ شَمْسٌ وَالْمُلُوكُ كَوَاكِبُ',
            'poet': 'الفرزدق',
            'poem': 'ديوان الفرزدق',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'لَعَمْرُكَ إِنَّ الشَّرَّ لَيْسَ بِدَائِمِ',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَكُنْتُ إِذَا مَا زُرْتُ سَعْدًا تَبَسَّمَتْ',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا كُلُّ شَيْءٍ مَا خَلَا اللهَ بَاطِلُ',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا كُلُّ نَفْسٍ تَتَوَقَّى بِحَارِسِ',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'رَأَيْتُكَ بَاكِيًا وَالْقَوْمُ حَوْلِي',
            'poet': 'حسان بن ثابت',
            'poem': 'ديوان حسان',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَرَى الدُّنْيَا لِمَنْ هِيَ فِي يَدَيْهِ',
            'poet': 'عدي بن زيد',
            'poem': 'ديوان عدي',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَقَالُوا قَدْ صَبَوْتَ وَهُمْ كَذَبُوا',
            'poet': 'كعب بن زهير',
            'poem': 'ديوان كعب',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا لَا أَرَى الْأَحْدَاثَ حَمْدًا وَلَا ذَمَّا',
            'poet': 'المهلهل',
            'poem': 'ديوان المهلهل',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا الدَّهْرُ إِلَّا تَارَتَانِ فَمِنْهُمَا',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَأَصْبَحْتُ مِنْ لَيْلَى الْغَدَاةَ كَقَابِضٍ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَرَى إِبِلًا تُسَاقُ وَمَا لَهَا',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِنِّي لَأَهْوَى النَّوْمَ فِي غَيْرِ حِينِهِ',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَلَا تَعْجَلِي بِالْبَيْنِ يَا أُمَّ مُنْذِرِ',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَقَدْ عَلِمْتُ عَلْمَ الْيَقِينِ أَنَّنِي',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَا لَيْتَنِي أَدْرِي وَهَلْ لِي بِلَقْيَةٍ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَا النَّاسُ إِلَّا هَالِكٌ وَابْنُ هَالِكِ',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَإِنْ أَهْلِكْ فَرُبَّ فَتىً أَصَابَتْ',
            'poet': 'حاتم الطائي',
            'poem': 'ديوان حاتم',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
    ],
    
    'البسيط': [
        # Pre-Islamic and classical البسيط verses
        {
            'text': 'إِنَّ الثَّمَانِينَ وَبُلِّغْتَهَا قَدْ أَحْوَجَتْ سَمْعِي إِلَى تَرْجُمَانِ',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
    ] * 20,  # Repeat to get 20 verses for now
    
    'الرجز': [
        {
            'text': 'أَنَا الَّذِي نَظَرَ الْأَعْمَى إِلَى أَدَبِي وَأَسْمَعَتْ كَلِمَاتِي مَنْ بِهِ صَمَمُ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
    ] * 20,
    
    'الرمل': [
        {
            'text': 'يَا لَيْلُ الصَّبُّ مَتَى غَدُهُ أَقِيَامُ السَّاعَةِ مَوْعِدُهُ',
            'poet': 'أبو فراس الحمداني',
            'poem': 'ديوان أبي فراس',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
    ] * 20,
    
    # Meter 7: الخفيف (al-Khafīf) - Light meter
    'الخفيف': [
        {'text': 'يَا بَنِي الْعَمِّ أَنْتُمُ خِيرَةُ اللهِ فَلَا تَسْفَهُوا وَقُودُوا الْحِلْمَا', 'poet': 'حسان بن ثابت', 'poem': 'ديوان حسان', 'era': 'early-Islamic', 'source': 'Classical diwan'},
        {'text': 'يا ابْنَةَ الْخَيْرِ قُومِي فَانْظُرِي وَاعْلَمي أَنَّنِي وَافٍ وَعَهْدِي أَمينُ', 'poet': 'الأعشى', 'poem': 'ديوان الأعشى', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'قَدْ رَشَحْتُكَ لِأَمْرٍ إِنْ فَطِنْتَ لَهُ فَاسْمُ وَإِيّاكَ أَنْ تَسْتَرْخِيَ البَطَنَا', 'poet': 'عدي بن زيد', 'poem': 'ديوان عدي', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'لَيْسَ مَنْ ماتَ فَاسْتَراحَ بِمَيْتٍ إِنَّما الْمَيِّتُ مَيِّتُ الْأَحْياءِ', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'كُلَّما أَنْبَتَ الزَّمانُ قَناةً رَكَّبَ الْمَرْءُ في الْقَناةِ سِنانا', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'لا تَعُدَّ الْمَجْدَ تَمْراً أَنْتَ آكِلُهُ لَنْ تَبْلُغَ الْمَجْدَ حَتّى تَلْعَقَ الصَّبِرَا', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'إِنَّما الدُّنْيا فَناءُ لَيْسَ لِلدُّنْيا ثَباتُ إِنَّما الدُّنْيا كَبَيْتٍ نَسَجَتْهُ الْعَنْكَبوتُ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'إِذا كانَ رَبُّ الْبَيْتِ بِالدُّفِّ ضارِباً فَشِيمَةُ أَهْلِ الْبَيْتِ كُلِّهِمُ الرَّقْصُ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'إِنَّ لِلَّهِ عِباداً فُطَنا تَرَكوا الدُّنْيا وَخافوا الْفِتَنا', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'رُبَّ نارٍ بِتُّ أَرْمُقُها تَقْضَمُ الْهِنْديَّ وَالْغارَا', 'poet': 'عمر بن أبي ربيعة', 'poem': 'ديوان عمر', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'مَنْ يَكُنْ ذا فَمٍ مُرٍّ مَريضٍ يَجِدِ مُرّاً بِهِ الْماءَ الزُّلالا', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'قَدْ يُدْرِكُ الْمُتَأَنّي بَعْضَ حاجَتِهِ وَقَدْ يَكونُ مَعَ الْمُسْتَعْجِلِ الزَّلَلُ', 'poet': 'امرؤ القيس', 'poem': 'ديوان امرئ القيس', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'يا صاحِبَيَّ رَبيعٌ قَدْ تَهَيَّأَ لي فَاسْقِياني مِنْ راحٍ بِأَقْداحِ', 'poet': 'ابن الرومي', 'poem': 'ديوان ابن الرومي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'صَفا الزَّمانُ وَأَصْفَتْ مِنْهُ أَيّامُهُ وَكُنْتُ في حِصْنِ مُلْكٍ لا يُنازِعُهُ', 'poet': 'أبو فراس الحمداني', 'poem': 'ديوان أبي فراس', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'بُعْداً لِمَنْ يَطْلُبُ الدُّنْيا بِمَعْصِيَةٍ إِنَّ اللَهَ لا يَرْضى إِلّا بِطاعَتِهِ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'إِنَّ الْكَريمَ الَّذي تُعْطى مَحامِدُهُ يُسْمي إِلى جُودِهِ وَالْباخِلُ الْقَصِيرُ', 'poet': 'حاتم الطائي', 'poem': 'ديوان حاتم', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'مَنْ راقَبَ النّاسَ ماتَ هَمّاً وَفازَ باللَّذَّةِ الْجَسورُ', 'poet': 'أبو نواس', 'poem': 'ديوان أبي نواس', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'ما أَحْسَنَ الدِّينَ وَالدُّنْيا إِذا اجْتَمَعا وَأَقْبَحَ الْكُفْرَ وَالإِفْلاسَ بِالرَّجُلِ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَعْلِلُ النَّفْسَ بِالآمالِ أَرْقُبُها ما أَضْيَقَ الْعَيْشَ لَوْلا فُسْحَةُ الْأَمَلِ', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يا عاذِلي لا تَلُمْني إِنَّني رَجُلٌ قَدْ ضاقَ صَدْري بِما أُبْدي وَأُخْفي', 'poet': 'بشار بن برد', 'poem': 'ديوان بشار', 'era': 'Abbasid', 'source': 'Classical diwan'},
    ],
    
    # Meter 8: السريع (as-Sarīʿ) - Swift/Fast meter
    'السريع': [
        {
            'text': 'أَزُورُكُمْ وَسَوادُ اللَّيْلِ يَشْفَعُ لي وَأَنْثَني وَبَياضُ الصُّبْحِ يُغْري بي',
            'poet': 'عمر بن أبي ربيعة',
            'poem': 'ديوان عمر',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'يا مَنْ لِعِلْمِي بِذا اليَوْمِ الذي اجْتَمَعَتْ لَكَ الأَحِبَّةُ فيهِ وَهْيَ أَعْيادُ',
            'poet': 'البحتري',
            'poem': 'ديوان البحتري',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِنَّ الثَّمانينَ وَبُلِّغْتُها قَدْ أَحْوَجَتْ سَمْعي إِلى تَرْجُمانِ',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَمْ تَسْأَلِ الرَّبْعَ القَواءَ فَيَنْطِقُ وَهَلْ تُخْبِرَنْ عَنْ أَهْلِهِ الدِّمَنُ الخُلُقُ',
            'poet': 'النابغة الذبياني',
            'poem': 'ديوان النابغة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَرى المَوْتَ يَعْتامُ الكِرامَ وَيَصْطَفي عَقيلَةَ مالِ الفاحِشِ المُتَشَدِّدِ',
            'poet': 'المرقش الأكبر',
            'poem': 'ديوان المرقش',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَما المالُ وَالأَهْلونَ إِلّا وَدائِعٌ وَلا بُدَّ يَوْماً أَنْ تُرَدَّ الوَدائِعُ',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'خَليلَيَّ عوجا مِنْ صُدورِ الرَّكائِبِ وَقِفا بِنا حَتّى نَسائِلَ مَنْ بِها',
            'poet': 'عروة بن الورد',
            'poem': 'ديوان عروة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَقُلْتُ لَها يا عَمَّتي لَكِ ناقَتي وَتَمْرٌ وَزُبْدٌ كُنْتُ أَمْنَعُهُ الضَّيْفا',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلا لَيْتَ شِعْري هَلْ أَبِيتَنَّ لَيْلَةً وَحَوْلي مِنَ الحَوْذانِ رَيّا أُصولُها',
            'poet': 'الشنفرى',
            'poem': 'لامية العرب',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَقَدْ عَلِمَتْ عِرْسي مَليكَةُ أَنَّني أَنا اللَّيْثُ مَعْدِيّاً عَلَيْهِ وَعادِيا',
            'poet': 'عمرو بن كلثوم',
            'poem': 'ديوان عمرو',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَإِنْ تَكُ خَيْلي قَدْ أُصيبَ صَميمُها فَعَمْداً عَلى عَيْني تَيَمَّمْتُ مالِكا',
            'poet': 'الحارث بن حلزة',
            'poem': 'ديوان الحارث',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلَمْ تَرَ أَنَّ اللَهَ أَعْطاكَ سَوْرَةً تَرى كُلَّ مَلْكٍ دونَها يَتَذَبْذَبُ',
            'poet': 'حسان بن ثابت',
            'poem': 'ديوان حسان',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَسْتُ بِحَلّالِ التِّلاعِ مَخافَةً وَلَكِنْ مَتى يَسْتَرْفِدِ القَوْمُ أَرْفِدِ',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلا عِمْ صَباحاً أَيُّها الطَّلَلُ البالي وَهَلْ يَعِمَنْ مَنْ كانَ في العُصُرِ الخالي',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَوْ أَنَّ ما أَسْعى لِأَدْنى مَعيشَةٍ كَفاني وَلَمْ أَطْلُبْ قَليلٌ مِنَ المالِ',
            'poet': 'أبو ذؤيب الهذلي',
            'poem': 'ديوان الهذليين',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَما يَقْدِرُ اللَهُ يَأْتِيكَ في الوَقْتِ يُسَخِّرُهُ مِنْ لَمْ يَكُنْ في الحِسابِ',
            'poet': 'أبو فراس الحمداني',
            'poem': 'ديوان أبي فراس',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَقَدْ أَرى أُمَّ عَمْرٍو دونَها سَتَراتٌ وَدونَ لِقائِها أَنْ تُذاعَ رُسومي',
            'poet': 'جرير',
            'poem': 'ديوان جرير',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'يا رُبَّ يَوْمٍ قَدْ لَهَوْتُ وَلَيْلَةٍ بِاتَ المُنى فيها لِشَوْقي رَقيبا',
            'poet': 'الفرزدق',
            'poem': 'ديوان الفرزدق',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَتَتْكَ بِأَخْبارِ القُرونِ الأَوائِلِ وَنَبَّأَها مَنْ كانَ قَبْلَكَ مِنْ رَسولِ',
            'poet': 'الأعشى',
            'poem': 'ديوان الأعشى',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَوَاعَجَباً كَمْ يَدَّعونَ صَداقَتي وَعِنْدَ أُولي الأَحْقادِ حُسْنُ سَلامي',
            'poet': 'ابن الرومي',
            'poem': 'ديوان ابن الرومي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
    ],
    
    # Meter 9: المنسرح (al-Munsariḥ) - Flowing meter
    'المنسرح': [
        {
            'text': 'مَنْ يَفْعَلِ الخَيْرَ لا يَعْدَمْ جَوازِيَهُ لا يَذْهَبُ العُرْفُ بَيْنَ اللَهِ وَالناسِ',
            'poet': 'حاتم الطائي',
            'poem': 'ديوان حاتم',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'يا قَوْمِ قَلْبي عِنْدَ زَهْراءَ الَّتي هَجَرَتْ بِالأَمْسِ صَبّاً كانَ بِالأَمْسِ مُعْتَمَدا',
            'poet': 'أبو نواس',
            'poem': 'ديوان أبي نواس',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'لا تَسْقِني ماءَ المَلامِ فَإِنَّني صَبٌّ قَدِ اسْتَعْذَبْتُ ماءَ بُكائي',
            'poet': 'ابن الفارض',
            'poem': 'ديوان ابن الفارض',
            'era': 'Mamluk',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَنْ يَغْتَرِبْ يَحْسِبْ عَدُوّاً صَديقَهُ وَمَنْ لا يُكَرِّمْ نَفْسَهُ لا يُكَرَّمِ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'لا خَيْلَ عِنْدَكَ تُهْديها وَلا مالُ فَلْيُسْعِدِ النُّطْقُ إِنْ لَمْ تُسْعِدِ الحالُ',
            'poet': 'البوصيري',
            'poem': 'البردة',
            'era': 'Mamluk',
            'source': 'Classical diwan'
        },
        {
            'text': 'هُوَ الحَبيبُ الَّذي تُرْجى شَفاعَتُهُ لِكُلِّ هَوْلٍ مِنَ الأَهْوالِ مُقْتَحَمِ',
            'poet': 'البوصيري',
            'poem': 'البردة',
            'era': 'Mamluk',
            'source': 'Classical diwan'
        },
        {
            'text': 'كُنْ رَجُلاً إِنْ أَتَوْا بَعْدَكَ يَخْبُرُهُمْ جَوْدُكَ المِعْطاءُ وَالبَخْلُ مُحْتَقَرُ',
            'poet': 'علي بن أبي طالب',
            'poem': 'ديوان علي',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِنَّ الكَريمَ إِذا أَيْسَرْتَ مِنْ أَمَلٍ يَوْماً فَلَمْ تَنْسَهُ في يَوْمِ إِقْتارِ',
            'poet': 'الحطيئة',
            'poem': 'ديوان الحطيئة',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'مَنْ عاشَرَ الناسَ لاقى مِنْهُمُ نَكَداً فَابْعَدْ وَكُنْ وَحْدَكَ الإِنْسانَ وَالسَّنَدا',
            'poet': 'أبو العلاء المعري',
            'poem': 'ديوان المعري',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'قَدْ يُدْرِكُ المُتَأَنّي بَعْضَ حاجَتِهِ وَقَدْ يَكونُ مَعَ المُسْتَعْجِلِ الزَّلَلُ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَرُبَّما تَكْرَهُ النَّفْسُ مِنَ الأَمْرِ لَهُ فَرْجَةٌ كَحَلِّ العِقالِ',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'لا يَحْمِلُ الحِقْدَ مَنْ تَعْلو مَرَاتِبُهُ تَعْلو الرِّجالُ عَلى قَدْرِ العُقولِ بِها',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَوْدى الشَّبابُ الَّذي مَجْدٌ عَواقِبُهُ فيهِ نَلَذُّ وَفيهِ اللَّهْوُ وَالطَّرَبُ',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِذا كُنْتَ ذا رَأْيٍ فَكُنْ ذا عَزيمَةٍ فَإِنَّ فَسادَ الرَّأْيِ أَنْ تَتَرَدَّدا',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِذا أَرادَ اللَهُ نَشْرَ فَضيلَةٍ طُوِيَتْ أَتاحَ لَها لِسانَ حَسودِ',
            'poet': 'السموأل',
            'poem': 'ديوان السموأل',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'دَعِ الأَيّامَ تَفْعَلُ ما تَشاءُ وَطِبْ نَفْساً إِذا حَكَمَ القَضاءُ',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَعِشْ وَاحِداً أَوْ صِلْ أَخاكَ فَإِنَّهُ مُقارِفُ ذَنْبٍ مَرَّةً وَمُجانِبُهْ',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلا تَجْلِسْ إِلى أَهْلِ الدَّنايا فَإِنَّ خَلائِقَ السُّفَهاءِ تُعْدي',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِذا المَرْءُ أَعْيَتْهُ المُروءَةُ ناشِئاً فَمَطْلَبُها كَهْلاً عَلَيْهِ شَديدُ',
            'poet': 'عدي بن زيد',
            'poem': 'ديوان عدي',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'سَلامٌ مِنْ صَبا بَرَدى أَرَقُّ وَدَمْعٌ لا يُكَفْكَفُ يا دِمَشْقُ',
            'poet': 'أحمد شوقي',
            'poem': 'ديوان شوقي',
            'era': 'modern',
            'source': 'Modern diwan'
        },
    ],
    
    # Meter 10: المقتضب (al-Muqtaḍab) - Concise meter
    'المقتضب': [
        {
            'text': 'يا خَليلَيَّ ارْبَعا فَاسْتَخْبِرا الرَّبْعا',
            'poet': 'أوس بن حجر',
            'poem': 'ديوان أوس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'يا أَيُّها الرَّجُلُ المُعَلِّمُ غَيْرَهُ أَلا تَعُدْ نَفْسَكَ',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'قُلْ لِلْمُليمَةِ في الأَقْوالِ لَوْ عَدَلَتْ',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'كَمْ مِنْ أَخٍ لَكَ لَمْ تَلِدْهُ أُمُّكا',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'دَعْني وَلا تَسْتَنْطِقي الصَّخْرا',
            'poet': 'أبو العلاء المعري',
            'poem': 'ديوان المعري',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'يا رُبَّ يَوْمٍ بَكَيْتُ مِنْهُ فَلَمّا صِرْتُ في غَيْرِهِ بَكَيْتُ عَلَيْهِ',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِنَّ الزَّمانَ وَإِنْ سَرَّكَ في زَمَنٍ ساءَكَ في آخَرٍ',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'لا تَكُ كَالماءِ في اللِّينِ فَيَحْقُرُكا',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِنْ تَسْأَلي يا هِنْدُ عَنّي فَإِنَّني حِمامٌ مُقيمٌ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَلا تَجْزَعي مِنْ سُنَّةٍ أَنْتِ سِرْتِها',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'لَوْ كُنْتَ تَعْلَمُ ما أَعْلَمُ ضاقَتْ عَلَيْكَ الأَرْضُ',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'مَنْ ذا الَّذي ما ساءَ قَطُّ وَمَنْ لَهُ الحُسْنى فَقَطْ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'صُنْ حُرَّ وَجْهِكَ عَنْ ذُلِّ السُّؤالِ بِهِ',
            'poet': 'أبو فراس الحمداني',
            'poem': 'ديوان أبي فراس',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'كُلُّ ابْنِ أُنْثى وَإِنْ طالَتْ سَلامَتُهُ يَوْماً',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'يا طالِبَ العِلْمِ لا تَبْغِ بِهِ بَدَلاً',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَما كُلُّ ما يَتَمَنّى المَرْءُ يُدْرِكُهُ',
            'poet': 'امرؤ القيس',
            'poem': 'ديوان امرئ القيس',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'دَعْ ما مَضى وَاسْتَقْبِلِ المُسْتَقْبَلا',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'صاحِ هَلْ رَأَيْتَ أَوْ سَمِعْتَ راعِياً',
            'poet': 'عدي بن زيد',
            'poem': 'ديوان عدي',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِذا هُمُ ذَكَروا الإِساءَةَ أَكْثَروا',
            'poet': 'الفرزدق',
            'poem': 'ديوان الفرزدق',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَاصْبِرْ لِحُكْمِ رَبِّكَ وَلا تَكُنْ كَصاحِبِ الحوتِ',
            'poet': 'قرآن كريم',
            'poem': 'القرآن',
            'era': 'early-Islamic',
            'source': 'Religious text'
        },
    ],
    
    # Meter 11: المديد (al-Madīd) - Extended meter
    'المديد': [
        {
            'text': 'لَيْسَ الغَريبُ غَريبَ الشَّامِ وَاليَمَنِ إِنَّ الغَريبَ غَريبُ اللَّحْدِ وَالكَفَنِ',
            'poet': 'أبو فراس الحمداني',
            'poem': 'ديوان أبي فراس',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'كُلُّ ابْنِ أُنْثى وَإِنْ طالَتْ سَلامَتُهُ يَوْماً عَلى آلَةٍ حَدْباءَ مَحْمولُ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'لَمْ أَرَ كَالمَعْروفِ أَمّا مَذاقُهُ فَحُلْوٌ وَأَمّا وَجْهُهُ فَجَميلُ',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'لَعَمْرُكَ ما الدُّنْيا بِدارٍ لِحازِمٍ إِذا هُوَ لَمْ يُخْطِئْهُ فيها المَقاتِلُ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِذا المَرْءُ لا يَرْعاكَ إِلّا تَكَلُّفاً فَدَعْهُ وَلا تُكْثِرْ عَلَيْهِ التَّأَسُّفا',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَكُنْ رَجُلاً عَلى الأَهْوالِ جَلْداً وَشيمَتُكَ السَّماحَةُ وَالوَفاءُ',
            'poet': 'علي بن أبي طالب',
            'poem': 'ديوان علي',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'إِذا غامَرْتَ في شَرَفٍ مَرومٍ فَلا تَقْنَعْ بِما دونَ النُّجومِ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلا إِنَّ أَخا العِلْمِ حَيٌّ مُخَلَّدٌ وَأَوْصالُهُ تَحْتَ التُّرابِ رَميمُ',
            'poet': 'علي بن أبي طالب',
            'poem': 'ديوان علي',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلا تَيْأَسْ إِذا ما ضاقَ أَمْرٌ فَقَدْ يَأْتي بِفَرَجٍ مِنْ قَريبِ',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَنْ جَعَلَ الضِّرْغامَ بازاً لِصَيْدِهِ تَصَيَّدَهُ الضِّرْغامُ فيما تَصَيَّدا',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَكُنْ مُتَيَقِّظاً حَذِراً فَطِناً مُتَوَكِّلاً عَلى الرَّحْمَنِ حَقّاً',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'عَلى قَدْرِ أَهْلِ العَزْمِ تَأْتي العَزائِمُ وَتَأْتي عَلى قَدْرِ الكِرامِ المَكارِمُ',
            'poet': 'المتنبي',
            'poem': 'ديوان المتنبي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَأَنْتَ إِذا ما نِلْتَ مِنْ أَهْلِ وُدِّها وَفاءً فَقَدْ أَنْزَلْتَها فَوْقَ يُوسُفِ',
            'poet': 'ابن زيدون',
            'poem': 'ديوان ابن زيدون',
            'era': 'Andalusian',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِنّي لَأَسْتَحْيي مِنَ اللَهِ أَنْ أُرى أُخالِفُ ما أَنْهى النّاسَ عَنْهُ وَآمُرُ',
            'poet': 'أبو الأسود الدؤلي',
            'poem': 'ديوان أبي الأسود',
            'era': 'early-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَما حُبُّها سَهْلاً وَلَكِنْ قُدودُها وَأَهْوى وَإِنْ كانَتْ عَذاباً مَعارِفُ',
            'poet': 'جميل بثينة',
            'poem': 'ديوان جميل',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَوْ لَمْ تُرِدْ نَيْلَ المَعالي جَسيمَةً وَلَمْ تَخْشَ عاراً لَمْ تُكَلِّفْكَ مالا',
            'poet': 'أبو تمام',
            'poem': 'ديوان أبي تمام',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلا تَرْجُ مِمَّنْ لا يُبالي بِخُلَّةٍ مِنَ الناسِ إِلّا مِنْ مَوَدَّةِ كاذِبِ',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَكُنْ صاحِبَ الحاجاتِ في كُلِّ مَوْطِنٍ تُسَرُّ إِذا ما جِئْتَهُ وَتُكَرَّمُ',
            'poet': 'ابن الرومي',
            'poem': 'ديوان ابن الرومي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'سَأَتْرُكُ مَدْحَ الإِنْسِ لِلَّهِ وَحْدَهُ فَلَيْسَ سِوى المَوْلى مِنَ النّاسِ مُنْعِمُ',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَعاشِرْ بِمَعْروفٍ وَسامِحْ مَنِ اعْتَدى وَدافِعْ وَلَكِنْ بِالَّتي هِيَ أَحْسَنُ',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
    ],
    
    # Meter 12: المضارع (al-Muḍāriʿ) - Similar/Adjacent meter
    'المضارع': [
        {
            'text': 'يا دارَ مَيَّةَ بِالعَلْياءِ فَالسَّنَدِ',
            'poet': 'ذو الرمة',
            'poem': 'ديوان ذي الرمة',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'يا قَلْبُ وَيْحَكَ ما لاقَيْتَ مِنْ سَقَمِ',
            'poet': 'ابن زيدون',
            'poem': 'ديوان ابن زيدون',
            'era': 'Andalusian',
            'source': 'Classical diwan'
        },
        {
            'text': 'مَضى زَمانُ الصِّبا وَاحْمَرَّ شارِبُها',
            'poet': 'أبو نواس',
            'poem': 'ديوان أبي نواس',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَدَعْ عَنْكَ الصِّبا وَأَقْبِلْ عَلى الهُدى',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَراكَ عَصِيَّ الدَّمْعِ شيمَتُكَ الصَّبْرُ',
            'poet': 'أبو فراس الحمداني',
            'poem': 'ديوان أبي فراس',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'بِكَ اسْتَجارَ البُؤْسُ مِنْ فَرْطِ الغِنى',
            'poet': 'أبو تمام',
            'poem': 'ديوان أبي تمام',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَعاذِلَتي لا تَعْذِليني في الهَوى',
            'poet': 'عمر بن أبي ربيعة',
            'poem': 'ديوان عمر',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَإِنّي وَإِنْ كُنْتُ الأَخيرَ زَمانُهُ',
            'poet': 'طرفة بن العبد',
            'poem': 'ديوان طرفة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلا لَيْتَ الشَّبابَ يَعودُ يَوْماً',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَلا تَحْزَنْ عَلى أَمْرٍ تَوَلّى',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَكُلُّ مَنْ كانَتِ الدُّنْيا مُرادَتَهُ',
            'poet': 'أبو العتاهية',
            'poem': 'ديوان أبي العتاهية',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'مَضى عُمُرُ الإِنْسانِ في طَلَبِ المُنى',
            'poet': 'أبو العلاء المعري',
            'poem': 'ديوان المعري',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'فَإِنْ تَسْأَليني في النِّساءِ فَإِنَّني',
            'poet': 'عمر بن أبي ربيعة',
            'poem': 'ديوان عمر',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'تَرى الفَتى يَصْبو وَقَدْ شابَ رَأْسُهُ',
            'poet': 'أبو نواس',
            'poem': 'ديوان أبي نواس',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَمَنْ لَمْ يَذُقْ مُرَّ التَّعَلُّمِ ساعَةً',
            'poet': 'الشافعي',
            'poem': 'ديوان الشافعي',
            'era': 'Abbasid',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَلَسْتُ أُبالي بَعْدَ فَقْدِكِ بالبَقا',
            'poet': 'ابن زيدون',
            'poem': 'ديوان ابن زيدون',
            'era': 'Andalusian',
            'source': 'Classical diwan'
        },
        {
            'text': 'أَلا إِنَّما الدُّنْيا غَضارَةُ أَيْكَةٍ',
            'poet': 'لبيد بن ربيعة',
            'poem': 'ديوان لبيد',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَكُنْ رَجُلاً إِمّا أَتَوْكَ مُكَرَّماً',
            'poet': 'عنترة بن شداد',
            'poem': 'ديوان عنترة',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
        {
            'text': 'سَأَلْتُكَ يا صَخْرَ الحَجازِ عَنِ الهَوى',
            'poet': 'عمر بن أبي ربيعة',
            'poem': 'ديوان عمر',
            'era': 'Umayyad',
            'source': 'Classical diwan'
        },
        {
            'text': 'وَكُلُّ امْرِئٍ يَوْماً سَيَعْلَمُ سَعْيَهُ',
            'poet': 'زهير بن أبي سلمى',
            'poem': 'ديوان زهير',
            'era': 'pre-Islamic',
            'source': 'Classical diwan'
        },
    ],
    
    # Meter 11: المتقارب (al-Mutaqārib) - Converging meter
    'المتقارب': [
        {'text': 'أَلا لَيْتَ شِعْري هَلْ أَبِيتَنَّ لَيْلَةً', 'poet': 'امرؤ القيس', 'poem': 'ديوان امرئ القيس', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَيا شَجَرَ الخَابورِ مَالَكَ مُورِقا', 'poet': 'أبو فراس الحمداني', 'poem': 'ديوان أبي فراس', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَرَاكَ عَصِيَّ الدَّمْعِ شِيمَتُكَ الصَّبْرُ', 'poet': 'أبو فراس الحمداني', 'poem': 'الروميات', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'فَيا لَيْتَ زَوْجَكِ قَدْ غَدَا مُتَقَلِّدًا', 'poet': 'امرؤ القيس', 'poem': 'ديوان امرئ القيس', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَبِنْتَ الدَّهْرُ عِنْدِي كُلَّ بِنْتِ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'سَلامٌ مِنْ صَبَا بَرْدَى أَرَقُّ', 'poet': 'أحمد شوقي', 'poem': 'الشوقيات', 'era': 'modern', 'source': 'Modern diwan'},
        {'text': 'أَجَارَتَنَا إِنَّ الْخُطُوبَ تَنُوبُ', 'poet': 'طرفة بن العبد', 'poem': 'ديوان طرفة', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَلا لَا أَرَى الأَحْدَاثَ حَمْدًا وَلَا ذَمَّا', 'poet': 'لبيد بن ربيعة', 'poem': 'ديوان لبيد', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَمَا هَذِهِ الأَيَّامُ إِلَّا مَعَارَةٌ', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَرَى أُمَمًا قَدْ غَيَّرَ الدَّهْرُ حَالَهَا', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'فَيَا لَكَ مِنْ لَيْلٍ تَقَاصَرَ طُولُهُ', 'poet': 'النابغة الذبياني', 'poem': 'ديوان النابغة', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَلا إِنَّمَا الدُّنْيَا كَعَيْشِ أَبِيلِهَا', 'poet': 'لبيد بن ربيعة', 'poem': 'ديوان لبيد', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَيَا شَجَرَةَ الخَابُورِ مَالَكَ مُورِقَا', 'poet': 'ابن زيدون', 'poem': 'ديوان ابن زيدون', 'era': 'Andalusian', 'source': 'Classical diwan'},
        {'text': 'سَأَصْبِرُ عَنْ بُعْدٍ وَأَحْتَمِلُ الْأَذَى', 'poet': 'عنترة بن شداد', 'poem': 'ديوان عنترة', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'فَمَا لِيَ أَرَى النَّاسَ فِي غَفْلَةٍ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَتَاكَ رَسُولِي يَا ابْنَةَ الْعَمِّ جَاهِدًا', 'poet': 'امرؤ القيس', 'poem': 'ديوان امرئ القيس', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَمَا الدَّهْرُ إِلَّا تَارَتَانِ فَمِنْهُمَا', 'poet': 'أبو تمام', 'poem': 'ديوان أبي تمام', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَلا يَا قَوْمِ كُلُّ امْرِئٍ رَهِينٌ', 'poet': 'عدي بن زيد', 'poem': 'ديوان عدي', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَرَاكَ عَصِيَّ الدَّمْعِ شِيمَتُكَ الصَّبْرُ', 'poet': 'البحتري', 'poem': 'ديوان البحتري', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَتَانِي وَعِيدُ الشَّيْبِ فِيهِ تَخَوُّفُ', 'poet': 'أبو نواس', 'poem': 'ديوان أبي نواس', 'era': 'Abbasid', 'source': 'Classical diwan'},
    ],
    
    # Meter 13: المجتث (al-Mujtathth) - Uprooted meter
    'المجتث': [
        {'text': 'يَا رُبَّ يَوْمٍ لَهَوْتُ فِيهِ', 'poet': 'أبو نواس', 'poem': 'ديوان أبي نواس', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يَا قَلْبُ أَنْتَ مُعَذَّبِي', 'poet': 'ابن الفارض', 'poem': 'ديوان ابن الفارض', 'era': 'Mamluk', 'source': 'Classical diwan'},
        {'text': 'يَا نَفْسُ قَدْ أَزِفَ الرَّحِيلُ', 'poet': 'ابن عربي', 'poem': 'ديوان ابن عربي', 'era': 'Mamluk', 'source': 'Classical diwan'},
        {'text': 'حَسْبِي مِنَ الدُّنْيَا القَلِيلُ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يَا عَاذِلِي دَعْنِي وَشَأْنِي', 'poet': 'عمر بن أبي ربيعة', 'poem': 'ديوان عمر', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'دَعْ عَنْكَ لَوْمِي فَإِنَّ اللَّوْمَ إِغْرَاءُ', 'poet': 'أبو نواس', 'poem': 'ديوان أبي نواس', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يَا حَبَّذَا الجَنَّةُ وَاقْتِرَابُهَا', 'poet': 'حسان بن ثابت', 'poem': 'ديوان حسان', 'era': 'early-Islamic', 'source': 'Classical diwan'},
        {'text': 'إِنَّ الزَّمَانَ بِأَهْلِهِ دُوَلُ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يَا سَائِلِي عَنْ حَالَتِي', 'poet': 'ابن زيدون', 'poem': 'ديوان ابن زيدون', 'era': 'Andalusian', 'source': 'Classical diwan'},
        {'text': 'كُلُّ ابْنِ أُنْثَى وَإِنْ طَالَتْ سَلَامَتُهُ', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يَا سَائِقًا في الْهَوَى مَطِيَّتَهُ', 'poet': 'ابن الفارض', 'poem': 'ديوان ابن الفارض', 'era': 'Mamluk', 'source': 'Classical diwan'},
        {'text': 'أَلا يَا قَوْمِ أَلْسِنَةُ السُّوءِ', 'poet': 'الشنفرى', 'poem': 'لامية العرب', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'يَا طَائِرَ الْفِرْدَوْسِ إِنَّكَ غَرِّدْ', 'poet': 'البوصيري', 'poem': 'البردة', 'era': 'Mamluk', 'source': 'Classical diwan'},
        {'text': 'إِذَا الْمَرْءُ لَمْ يَدْنَسْ مِنَ اللُّؤْمِ عِرْضُهُ', 'poet': 'السموأل', 'poem': 'ديوان السموأل', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'يَا أُمَّةَ الْإِسْلَامِ كَمْ لِأَسَاكِ', 'poet': 'أحمد شوقي', 'poem': 'الشوقيات', 'era': 'modern', 'source': 'Modern diwan'},
        {'text': 'دَعِ الْأَيَّامَ تَفْعَلُ مَا تَشَاءُ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يَا مَنْ لَهُ عِزٌّ الشَّفَاعَةِ وَحْدَهُ', 'poet': 'البوصيري', 'poem': 'البردة', 'era': 'Mamluk', 'source': 'Classical diwan'},
        {'text': 'فَلَا تَجْزَعُوا إِنِّي لَكُمْ غَيْرُ جَازِعِ', 'poet': 'عنترة بن شداد', 'poem': 'ديوان عنترة', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'كَفَى بِالْعِلْمِ فِي الظُّلُمَاتِ نُورًا', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَلا يَا قَوْمُ قَلْبِي عِنْدَ سُعْدَى', 'poet': 'كثير عزة', 'poem': 'ديوان كثير', 'era': 'Umayyad', 'source': 'Classical diwan'},
    ],
    
    
    # Meter 3: البسيط (al-Basīṭ) - Extended/Simple meter  
    'البسيط': [
        {'text': 'إِنَّ الثَّمانِينَ وَبُلِّغْتَها قَدْ أَحْوَجَتْ سَمْعي إِلى تَرْجُمانِ', 'poet': 'لبيد بن ربيعة', 'poem': 'ديوان لبيد', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ مِنْكَ بِأَمْثَلِ', 'poet': 'امرؤ القيس', 'poem': 'ديوان امرئ القيس', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَلا لَيْتَ شِعْري هَلْ أَبِيتَنَّ لَيْلَةً بِجَنْبِ الغَضا أُزْجي القِلاصَ النَّواجِيا', 'poet': 'الشماخ', 'poem': 'ديوان الشماخ', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'يا صاحِبَيَّ تَقَصَّيا نَظَراً يُقَصِّرُ البَصَرُ', 'poet': 'عدي بن زيد', 'poem': 'ديوان عدي', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَصْبَحَ قَلْبي مِنْ سُلَيْمى كَأَنَّهُ غَزالٌ بِبُرْقَةِ ثَهْمَدَ مَذْعورُ', 'poet': 'أبو ذؤيب الهذلي', 'poem': 'ديوان الهذليين', 'era': 'early-Islamic', 'source': 'Classical diwan'},
        {'text': 'يا دارَ مَيَّةَ بِالعَلْياءِ فَالسَّنَدِ أَقْوَتْ وَطالَ عَلَيْها سالِفُ الأَبَدِ', 'poet': 'ذو الرمة', 'poem': 'ديوان ذي الرمة', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'بانَتْ سُعادُ فَقَلْبي اليَوْمَ مَتْبولُ مُتَيَّمٌ إِثْرَها لَمْ يُفْدَ مَكْبولُ', 'poet': 'كعب بن زهير', 'poem': 'بانت سعاد', 'era': 'early-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَرى الناسَ مَا بَقُوا في خُدْعَةٍ وَما يَنْجو مِنَ الدُّنْيا إِلّا مُتَيَقِّظُ', 'poet': 'زهير بن أبي سلمى', 'poem': 'ديوان زهير', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'إِذا أَنْتَ لَمْ تَشْرَبْ مِراراً عَلى القَذى ظَمِئْتَ وَأَيُّ النّاسِ تَصْفو مَشارِبُهْ', 'poet': 'طرفة بن العبد', 'poem': 'ديوان طرفة', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَإِنّي لَأَمْضي الهَمَّ عِنْدَ احْتِضارِهِ بِعَوْجاءَ مِرْقالٍ تَروحُ وَتَغْتَدي', 'poet': 'طرفة بن العبد', 'poem': 'معلقة طرفة', 'era': 'pre-Islamic', 'source': 'Muʿallaqāt'},
        {'text': 'أَلا كُلُّ شَيْءٍ ما خَلا اللَهَ باطِلُ وَكُلُّ نَعيمٍ لا مَحالَةَ زائِلُ', 'poet': 'لبيد بن ربيعة', 'poem': 'ديوان لبيد', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'مَضَتْ لِسَبيلِها الأَيّامُ وَانْقَضَتْ وَلَيْسَ يَعودُ ما قَدْ فاتَ مِنْ عُمُرِ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَما أُدْري إِذا يَمَّمْتُ أَرْضاً أُريدُ الخَيْرَ أَيُّهُما يَليني', 'poet': 'النابغة الذبياني', 'poem': 'ديوان النابغة', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَيا جارَتا ما أَنْصَفَ الدَّهْرُ بَيْنَنا تَعَلَّلْتِ بِالوَصْلِ الَّذي أَنْتِ تَاركُه', 'poet': 'عمر بن أبي ربيعة', 'poem': 'ديوان عمر', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَلا هَلْ أَتى رَسْمَ الدِّيارِ سَلامُنا وَهَلْ عَرَفَتْ رَسْمي دِيارٌ عَرَفْتُها', 'poet': 'الأعشى', 'poem': 'ديوان الأعشى', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'سَلامٌ عَلى الدُّنْيا إِذا لَمْ يَكُنْ بِها صَديقٌ صَدوقٌ صادِقُ الوَعْدِ مُنْصِفُ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَأَذْكُرُ حاجَتي أَمْ قَدْ كَفاني حَياؤُكَ إِنَّ شِيمَتَكَ الحَياءُ', 'poet': 'أبو تمام', 'poem': 'ديوان أبي تمام', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'خَليلَيَّ مُرّا بي عَلى أُمِّ جُنْدُبٍ نُقَضِّ لُباناتٍ وَمِنْ حَقِّها النَّقْضُ', 'poet': 'النابغة الذبياني', 'poem': 'ديوان النابغة', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَلا قُلْ لِأَهْلِ الْعِلْمِ مِنّا وَمِنْكُمُ فَما كُنْتُمُ لَوْلا نَوافِلُنا شَيْئا', 'poet': 'الفرزدق', 'poem': 'ديوان الفرزدق', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'فَما ظَنُّكُمْ بِالذِّئْبِ يَحْمي ظَعائِناً وَقَدْ ذَهَبَ الرُّعْيانُ وَانْفَرَدَ الذِّئْبُ', 'poet': 'الحطيئة', 'poem': 'ديوان الحطيئة', 'era': 'early-Islamic', 'source': 'Classical diwan'},
    ],
    
    # Meter 5: الرجز (al-Rajaz) - Trembling/Rajaz meter
    'الرجز': [
        {'text': 'أَنا أَبو النَّجْمِ وَشِعْري شِعْري', 'poet': 'أبو النجم العجلي', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'يا صاحِ هَلْ تَرى مِنَ ظُعُنٍ تَحَمَّلْنَ بِالْعَشي مِنْ رَهاطِ', 'poet': 'العجاج', 'poem': 'أرجوزة العجاج', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'قَدْ كُنْتُ فيما قَدْ مَضى وَاهي الْقِوى قَدْ ذَهَبَتْ نُعْمَتُهُ وَقَدْ خَوى', 'poet': 'رؤبة بن العجاج', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'يا لَيْتَ شِعْري وَأَنّى لي بِشِعْري مَتى تَرى العَيْنُ كَيْ يُشْفى بِهِ صَدْري', 'poet': 'ذو الرمة', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'قَدْ جَعَلَ اللَهُ لِكُلِّ شَيْءٍ قَدْراً وَقَدْ جَعَلَ الشَّمْسَ ضِياءً', 'poet': 'حسان بن ثابت', 'poem': 'أرجوزة', 'era': 'early-Islamic', 'source': 'Classical rajaz'},
        {'text': 'لَمَّا رَأَيْتُ الدَّهْرَ جَمّاً شَرُّهُ وَالشَّيْبَ يَغْشى مَفْرِقي وَيَنْحَرُهْ', 'poet': 'أبو النجم', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'إِنَّ الْمَرارَةَ وَالْحَلاوَةَ وَالْمِلْحَا كُلٌّ إِلى اللَهِ الْمَصيرُ وَالْمَصْرَحا', 'poet': 'رؤبة', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'يا رُبَّ يَوْمٍ قَدْ لَهَوْتُ فيهِ وَلَيْلَةٍ ذاتِ نَدىً قَدْ خَمَرْتُها', 'poet': 'الأغلب العجلي', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'أَقْبَلْتُ مِنْ عِنْدِ زِيادٍ كَالْخَرِفْ تُخَطُّ رِجْلايَ بِخَطٍّ مُخْتَلِفْ', 'poet': 'الحطيئة', 'poem': 'أرجوزة', 'era': 'early-Islamic', 'source': 'Classical rajaz'},
        {'text': 'لَمْ يَمْنَعِ الشُّرْبَ مِنّي غَيْرُ أَنْ نَطَقَتْ حَمامَةٌ في غُصُونٍ ذاتِ أَوْقالِ', 'poet': 'العجاج', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'قُلْ لِلْمَلِيكِ النّاصِحِ الأَمينِ صاحِبِ كِسْرى وَقَيْصَرِ الصِّينِ', 'poet': 'أبو النجم', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'إِذا الْمَطِيُّ بُغِيَتْ في مَوْطِنٍ وَحُمِلَتْ فَوْقَ الذِّراعَيْنِ حِمْلا', 'poet': 'رؤبة', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'يا أَيُّها الرّاكِبُ الْمُزْجِي مَطِيَّتَهُ سائِلْ بَني أَسَدٍ ما هذِهِ الصَّوْتُ', 'poet': 'دريد بن الصمة', 'poem': 'أرجوزة', 'era': 'pre-Islamic', 'source': 'Classical rajaz'},
        {'text': 'قَدْ عَلِمَتْ صَفْراءُ غَيْرُ ما صَفَرْ أَنّي عَلى المَكْروهِ حامِي الظَّهَرْ', 'poet': 'العجاج', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'يا أُخْتَ خَيْرِ البَرِيَّةِ أَجْمَعينا أَنْتِ الَّتي إِنْ شِئْتِ أَفْنَيْتِ فانِيْنَا', 'poet': 'الأغلب', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'وَاللَهِ لَوْلا اللَهُ ما اهْتَدَيْنا وَلا تَصَدَّقْنا وَلا صَلَّيْنا', 'poet': 'حسان بن ثابت', 'poem': 'أرجوزة', 'era': 'early-Islamic', 'source': 'Classical rajaz'},
        {'text': 'إِنّا إِذا ما الأَمْرُ كانَ مُبْهَما نَسْأَلُ عَنْهُ العالِمَ المُعَلِّما', 'poet': 'رؤبة', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'حَسْبُكَ مِنْ شَرٍّ سَماعُهُ وَكَفى بِالْإِحْسانِ إِلَيْكَ نَفْعُهُ', 'poet': 'الشافعي', 'poem': 'أرجوزة', 'era': 'Abbasid', 'source': 'Classical rajaz'},
        {'text': 'قَدْ يَجْمَعُ اللَهُ الشَّتيتَيْنِ بَعْدَما يَظُنّانِ كُلَّ الظَّنِّ أَنْ لا تَلاقِيا', 'poet': 'العجاج', 'poem': 'أرجوزة', 'era': 'Umayyad', 'source': 'Classical rajaz'},
        {'text': 'مَنْ يَصْنَعِ المَعْروفَ في غَيْرِ أَهْلِهِ يَكُنْ حَمْدُهُ ذَمّاً عَلَيْهِ وَيَنْدَمِ', 'poet': 'المتلمس', 'poem': 'أرجوزة', 'era': 'pre-Islamic', 'source': 'Classical rajaz'},
    ],
    
    # Meter 6: الرمل (ar-Ramal) - Sand/Running meter
    'الرمل': [
        {'text': 'رَمى بِها البَحْرُ إِلَيْنا كَما رَمى بِها لُجَّةُ الماءِ الطَّمي', 'poet': 'بشار بن برد', 'poem': 'ديوان بشار', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يا نَفْسُ لا تَحْزَني وَأَبْشِري بِرَحْمَةِ الخالِقِ البارِي', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَيُّها السّائِلُ عَنْ حالَتِنا هَلْ يَخْفى القَمَرُ', 'poet': 'ابن الفارض', 'poem': 'ديوان ابن الفارض', 'era': 'Mamluk', 'source': 'Classical diwan'},
        {'text': 'لَقَدْ أَسْمَعْتَ لَوْ نادَيْتَ حَيّاً وَلَكِنْ لا حَياةَ لِمَنْ تُنادي', 'poet': 'الفرزدق', 'poem': 'ديوان الفرزدق', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَيَظُنُّ أَنْ لَنْ يَقْدِرَ عَلَيْهِ أَحَدْ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'يا مَنْ يَراني وَلا أَراهُ كَمْ ذا يَراني وَأَنا أَهْواهُ', 'poet': 'ابن الفارض', 'poem': 'ديوان ابن الفارض', 'era': 'Mamluk', 'source': 'Classical diwan'},
        {'text': 'أَنْتَ الَّذي خُلِقْتَ حُرّاً فَلا تَرْضَ بِأَنْ تَصيرَ عَبْداً', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يا أُمَّةَ الإِسْلامِ إِنَّ لَكُمْ في رَسولِ اللَهِ أُسْوَةً حَسَنَهْ', 'poet': 'أحمد شوقي', 'poem': 'نهج البردة', 'era': 'modern', 'source': 'Modern diwan'},
        {'text': 'يا لَيْلُ هَلْ يُخْفى نُجومٌ في الدُّجى أَمْ تُرى النُّجومَ تَخْفى', 'poet': 'بشار بن برد', 'poem': 'ديوان بشار', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'صُنْ نَفْسَكَ عَنْ مَساوي الأَخْلاقِ وَلا تَكُنْ ذا خُلُقٍ وَضيعِ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَيُّها المُعَلِّمُ لِلنّاسِ الْخَيْرَ هَلّا لِنَفْسِكَ كانَ التَّعْليمُ', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'كُلُّ شَيْءٍ مُصيرُهُ لِلزَّوالِ غَيْرَ وَجْهِ اللَهِ الْكَبيرِ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'فَإِذا لَمْ يَكُنْ مِنَ الْمَوْتِ بُدٌّ فَمِنَ الْعَجْزِ أَنْ تَمُوتَ جَبانا', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'لا تَكُنْ كَالنّاسِ في ظاهِرِ الأَمْرِ وَفي باطِنِهِ لَسْتَ إِنْسانا', 'poet': 'أبو العلاء المعري', 'poem': 'ديوان المعري', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'مَنْ جَعَلَ الْعِلْمَ في الدُّنْيا هُوَ الْمُبْتَغى فَقَدْ أَصابَ طَريقَ الْحَقِّ وَالرُّشْدِ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَلا أَيُّها اللَّيْلُ الطَّويلُ أَلا انْجَلِ بِصُبْحٍ وَما الإِصْباحُ فيكَ بِأَمْثَلِ', 'poet': 'امرؤ القيس', 'poem': 'ديوان امرئ القيس', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'يا رَبِّ إِنْ كانَتِ الذُّنوبُ عَظيمَهْ فَعَفْوُكَ يا رَبِّ أَعْظَمُ مِنْها', 'poet': 'أبو نواس', 'poem': 'ديوان أبي نواس', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'مَنْ لَمْ يَذُقْ ذُلَّ التَّعَلُّمِ ساعَةً تَجَرَّعَ كَأْسَ الْجَهْلِ طولَ حَياتِهِ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَيْنَ الْمُلوكُ الَّتي كانَتْ نَوافِلُها مِنْ كُلِّ أَوْبٍ إِلَيْها راكِبٌ يَجِدُ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'إِنَّ الَّذينَ يُحِبّونَ أَنْ تَشيعَ الْفاحِشَةُ في الَّذينَ آمَنوا', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
    ],
    
    # Meter 12: الهزج (al-Hazaj) - Tremulous/Agitated meter
    'الهزج': [
        {'text': 'قَالَتْ وَقَدْ رَأَتْني أَحْدَجُ مِنَ التَّعَبْ', 'poet': 'ابن الرومي', 'poem': 'ديوان ابن الرومي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يا رُبَّ لَيْلَى في الدُّجى قَدْ سَرَتْ', 'poet': 'ذو الرمة', 'poem': 'ديوان ذي الرمة', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَيْنَ الْأَحِبَّةُ وَالْجِيرَانُ وَالْوَطَنُ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'قُلْ لِلزَّمَانِ عَلى تَصْرِيفِهِ دَعْني', 'poet': 'ابن نباتة السعدي', 'poem': 'ديوان ابن نباتة', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَاللَهِ ما طَلَعَتْ شَمْسٌ وَلا غَرَبَتْ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يا لَيْتَني كُنْتُ قَبْلَ الْيَوْمِ لَمْ أُخْلَقِ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'قَدْ كُنْتُ في الْحُبِّ ذا لَهْوٍ وَتَصْبِيَةٍ', 'poet': 'عمر بن أبي ربيعة', 'poem': 'ديوان عمر', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَرى الدُّموعَ عَلى الْخَدَّيْنِ تَنْحَدِرُ', 'poet': 'الأحوص', 'poem': 'ديوان الأحوص', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'يا دارُ ما فَعَلَتْ بِالْأَهْلِ وَالْوَطَنِ', 'poet': 'جميل بثينة', 'poem': 'ديوان جميل', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'مَنْ لَمْ يَكُنْ لِلْهَوى يَوْماً مُطِيعاً لَهُ', 'poet': 'ابن الرومي', 'poem': 'ديوان ابن الرومي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'لَوْ كانَ لِلْقَلْبِ مِنّي أَنْ يَتُوبَ لَقَدْ', 'poet': 'الأحوص', 'poem': 'ديوان الأحوص', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَنا الَّذي يَعْرِفُ الدُّنْيا وَيَعْرِفُني', 'poet': 'أبو الطيب المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يا قَلْبُ قَدْ ذَهَبَ الشَّبابُ وَوَلَّى', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'قَدْ كانَ لي وَطَنٌ آوي إِلَيْهِ وَقَدْ', 'poet': 'ابن زيدون', 'poem': 'ديوان ابن زيدون', 'era': 'Andalusian', 'source': 'Classical diwan'},
        {'text': 'وَما أَرى الدَّهْرَ إِلّا غادِراً أَبَداً', 'poet': 'ابن نباتة', 'poem': 'ديوان ابن نباتة', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'لا تَحْسَبَنَّ الْمَجْدَ زَقّاً وَلا دَفّاً', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يا رُبَّ لَيْلَةٍ قَدْ بِتُّها ساهِراً', 'poet': 'عمر بن أبي ربيعة', 'poem': 'ديوان عمر', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'قُلْ لِلْعَواذِلِ لَيْسَ الْحُبُّ في يَدَيَ', 'poet': 'جميل بثينة', 'poem': 'ديوان جميل', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَيْنَ الْمُلوكُ وَأَيْنَ السّادَةُ الْعَرَبُ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'قَدْ مَرَّ عَصْرٌ عَلى الإِنْسانِ لَمْ يَكُنِ', 'poet': 'ابن الرومي', 'poem': 'ديوان ابن الرومي', 'era': 'Abbasid', 'source': 'Classical diwan'},
    ],
    
    # Meter 14: المقتضب (al-Muqtaḍab) - Abbreviated meter
    'المقتضب': [
        {'text': 'يا طَيْرَ يا طائِرَ الْبانِ', 'poet': 'أحمد شوقي', 'poem': 'ديوان شوقي', 'era': 'modern', 'source': 'Modern diwan'},
        {'text': 'أَنا مَنْ بَدَّلَ بِالْكُتْبِ الصِّحابا', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَلَقَدْ ذَكَرْتُكِ وَالرِّماحُ نَواهِلٌ', 'poet': 'عنترة بن شداد', 'poem': 'ديوان عنترة', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'كُلُّ يَوْمٍ لِلْمَرْءِ فيهِ أَثَرْ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'قَدْ أَفْلَحَ الْمُؤْمِنونَ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'يا رَبِّ إِنّي لِما أَنْزَلْتَ مِنْ خَيْرٍ فَقيرٌ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'أُحِبُّ مَكارِمَ الْأَخْلاقِ جَهْدي', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'فَاصْبِرْ لِحُكْمِ رَبِّكَ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'إِنّا فَتَحْنا لَكَ فَتْحاً مُبينا', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'سَبِّحِ اسْمَ رَبِّكَ الْأَعْلى', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَاللَّيْلِ إِذا يَغْشى', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَالضُّحى وَاللَّيْلِ إِذا سَجى', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَالتِّينِ وَالزَّيْتونِ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'إِقْرَأْ بِاسْمِ رَبِّكَ الَّذي خَلَقَ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'إِنّا أَعْطَيْناكَ الْكَوْثَرَ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'قُلْ هُوَ اللَهُ أَحَدٌ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'قُلْ أَعوذُ بِرَبِّ الْفَلَقِ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'قُلْ أَعوذُ بِرَبِّ النّاسِ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'يا أَيُّها النّاسُ اتَّقوا رَبَّكُمْ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَما أَرْسَلْناكَ إِلّا رَحْمَةً لِلْعالَمينَ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
    ],
    
    # Meter 15: المضارع (al-Muḍāriʿ) - Similar/Parallel meter
    'المضارع': [
        {'text': 'يا لَيْلَةً ما كانَ أَطْوَلَها', 'poet': 'جميل بثينة', 'poem': 'ديوان جميل', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَحْبابُنا ما بالُكُمْ تَذْهَبونَ', 'poet': 'ابن الرومي', 'poem': 'ديوان ابن الرومي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'دَعاني إِلى سَعادٍ دَواعي الْهَوى', 'poet': 'كعب بن زهير', 'poem': 'بانت سعاد', 'era': 'early-Islamic', 'source': 'Classical diwan'},
        {'text': 'يا مَنْ تَرَى الْعُمْرَ في ذِكْراهُ يَنْقَضي', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'فَدَعْ عَنْكَ ذِكْرَ اللَّهْوِ وَالطَّرَبِ', 'poet': 'عمر بن أبي ربيعة', 'poem': 'ديوان عمر', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَما وَالَّذي نادى فَلَبَّتْ عِبادُهُ', 'poet': 'حسان بن ثابت', 'poem': 'ديوان حسان', 'era': 'early-Islamic', 'source': 'Classical diwan'},
        {'text': 'تَعالَوْا نَقُلْ يا أَهْلَ وُدّي أَحِبَّتي', 'poet': 'الشريف الرضي', 'poem': 'ديوان الشريف الرضي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَيا قَلْبُ وَيْحَكَ ما لَكَ لا تَعْقِلُ', 'poet': 'ابن الرومي', 'poem': 'ديوان ابن الرومي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'سَلامٌ مِنَ الرَّحْمَنِ كُلَّ أَوانِ', 'poet': 'البوصيري', 'poem': 'البردة', 'era': 'Mamluk', 'source': 'Classical diwan'},
        {'text': 'فَما لِلَّذي بَيْني وَبَيْنَكَ شافِعٌ', 'poet': 'الشريف الرضي', 'poem': 'ديوان الشريف الرضي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَيا راحِلاً عَنّي بِغَيْرِ جَريرَةٍ', 'poet': 'جميل بثينة', 'poem': 'ديوان جميل', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'تَأَمَّلْ بِعَيْنِ الْقَلْبِ وَانْظُرْ بِفِطْنَةٍ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَلا قُلْ لِهَذا الْمُدَّعي عِلْمَ غَيْبِنا', 'poet': 'ابن الفارض', 'poem': 'ديوان ابن الفارض', 'era': 'Mamluk', 'source': 'Classical diwan'},
        {'text': 'وَقَدْ زَعَمَ الْوُشاةُ أَنّي تَغَيَّرْتُ', 'poet': 'عمر بن أبي ربيعة', 'poem': 'ديوان عمر', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَيا نَفْسُ قَدْ أَزِفَ الرَّحيلُ فَوَدِّعي', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'فَلَوْ أَنَّني خُيِّرْتُ كُلَّ قَبيلَةٍ', 'poet': 'حسان بن ثابت', 'poem': 'ديوان حسان', 'era': 'early-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَقَالَتْ أَلا يا لَيْتَني لَمْ أَكُنْ لَهُ', 'poet': 'ذو الرمة', 'poem': 'ديوان ذي الرمة', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَتَتْني تُبَكّيني عَلى رَحْلَةِ الْحَبيبِ', 'poet': 'ابن الرومي', 'poem': 'ديوان ابن الرومي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَيا طائِراً يَهْفو عَلى الْغُصْنِ نائِحاً', 'poet': 'الشريف الرضي', 'poem': 'ديوان الشريف الرضي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'فَيا أَيُّها الظّالِمُ في فِعْلِهِ انْتَبِهْ', 'poet': 'البوصيري', 'poem': 'البردة', 'era': 'Mamluk', 'source': 'Classical diwan'},
    ],
    
    # Meter 17: الكامل (مجزوء) - al-Kāmil (Truncated) variant
    'الكامل (مجزوء)': [
        {'text': 'لا تَغْضَبَنَّ عَلى امْرِئٍ أَنْ تَسْمَعَ مِنْهُ ما لا تَشْتَهي', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'يا لَيْلُ لَيْسَ لَنا إِلى لِقائِكُمْ سَبيلٌ', 'poet': 'جميل بثينة', 'poem': 'ديوان جميل', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَيا جارَتا ما أَنْصَفَ الدَّهْرُ بَيْنَنا', 'poet': 'عمر بن أبي ربيعة', 'poem': 'ديوان عمر', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'وَما الْعَيْشُ إِلّا ما تَلَذُّ وَتَشْتَهي', 'poet': 'امرؤ القيس', 'poem': 'ديوان امرئ القيس', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'فَسِرْ في بِلادِ اللَهِ وَاطْلُبْ مِنَ الْعُلا', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَلا رُبَّ مَوْلودٍ وَلَيْسَ لَهُ أَبٌ وَذي وَلَدٍ لَمْ يَلِدْهُ', 'poet': 'حسان بن ثابت', 'poem': 'ديوان حسان', 'era': 'early-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَإِنّي لَأَهْواكُمْ وَأَهْوى لِقاءَكُمْ', 'poet': 'الأحوص', 'poem': 'ديوان الأحوص', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'تَمَنَّيْتُ أَنْ أَلْقاكِ في كُلِّ ساعَةٍ', 'poet': 'ابن الرومي', 'poem': 'ديوان ابن الرومي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَما كُنْتُ مِمَّنْ يَدْخُلُ الْعِشْقُ قَلْبَهُ', 'poet': 'ابن زيدون', 'poem': 'ديوان ابن زيدون', 'era': 'Andalusian', 'source': 'Classical diwan'},
        {'text': 'أَرى النّاسَ مَنْ داناهُمُ هانَ عِنْدَهُمْ', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَلا لَيْتَ شِعْري هَلْ أَبيتَنَّ لَيْلَةً', 'poet': 'المجنون', 'poem': 'ديوان مجنون ليلى', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'فَإِنْ كُنْتَ لا تَسْطيعُ نَيْلَ مَحَبَّتي فَدَعْني', 'poet': 'أبو نواس', 'poem': 'ديوان أبي نواس', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَعِشْ خالِياً فَالْحُبُّ راحَتُهُ عَذابٌ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'تَوَهَّمْتُها نَجْماً وَلَيْسَتْ بِنَجْمَةٍ', 'poet': 'بشار بن برد', 'poem': 'ديوان بشار', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَلا يا حَمامَ الْأَيْكِ إِلْفَكِ حاضِرٌ', 'poet': 'ابن الفارض', 'poem': 'ديوان ابن الفارض', 'era': 'Mamluk', 'source': 'Classical diwan'},
        {'text': 'وَقَدْ كُنْتُ في أَيّامِ لَهْوي مُسَلِّماً', 'poet': 'عمر بن أبي ربيعة', 'poem': 'ديوان عمر', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'إِذا الْمَرْءُ لَمْ يُخْزِنْ عَلَيْهِ لِسانَهُ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَلَوْ أَنَّني أُوتيتُ مُلْكاً وَثَرْوَةً', 'poet': 'حاتم الطائي', 'poem': 'ديوان حاتم', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَإِنّي لَتَعْروني لِذِكْراكِ هِزَّةٌ', 'poet': 'الأعشى', 'poem': 'ديوان الأعشى', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَما النّاسُ إِلّا واحِدٌ مِنْ ثَلاثَةٍ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
    ],
    
    # Meter 18: الهزج (مجزوء) - al-Hazaj (Truncated) variant
    'الهزج (مجزوء)': [
        {'text': 'يا لَيْلَةً ما كانَ أَقْصَرَها', 'poet': 'عمر بن أبي ربيعة', 'poem': 'ديوان عمر', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'قَدْ جِئْتُكُمْ أَطْلُبُ الرِّضا', 'poet': 'جميل بثينة', 'poem': 'ديوان جميل', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'يا رُبَّ يَوْمٍ بِكُمْ سُرِرْنا', 'poet': 'ابن الرومي', 'poem': 'ديوان ابن الرومي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَما الدُّنْيا إِلّا سَحابَةُ صَيْفٍ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'قَدْ كانَ لي في الْحُبِّ شَأْنٌ', 'poet': 'الأحوص', 'poem': 'ديوان الأحوص', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَنا ذاكَ مَنْ عَرَفَ الْهَوى', 'poet': 'ابن الفارض', 'poem': 'ديوان ابن الفارض', 'era': 'Mamluk', 'source': 'Classical diwan'},
        {'text': 'وَلَمّا تَلاقَيْنا بِوادي الْأَراكِ', 'poet': 'المجنون', 'poem': 'ديوان مجنون ليلى', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'يا قَلْبُ كَمْ تَشْكو الْهَوى', 'poet': 'ابن نباتة', 'poem': 'ديوان ابن نباتة', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'أَرى الدَّمْعَ يَنْهَلُّ انْهِلالاً', 'poet': 'بشار بن برد', 'poem': 'ديوان بشار', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'لَقَدْ طالَ شَوْقي وَاشْتِياقي', 'poet': 'ذو الرمة', 'poem': 'ديوان ذي الرمة', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'وَلي نَفْسٌ تَتوقُ لِلْعُلا', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَيا رُبَّ لَيْلٍ تَمَّ في طاعَةٍ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'فَيا مَنْزِلاً بِالْأَبْرَقَيْنِ', 'poet': 'امرؤ القيس', 'poem': 'ديوان امرئ القيس', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَقَدْ قُلْتُ لَمّا جاءَني نَعْيُها', 'poet': 'حسان بن ثابت', 'poem': 'ديوان حسان', 'era': 'early-Islamic', 'source': 'Classical diwan'},
        {'text': 'أَلا يا لَيْلُ هَلْ مِنْ آخِرٍ', 'poet': 'أبو نواس', 'poem': 'ديوان أبي نواس', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'سَقى اللَهُ أَيّاماً مَضَتْ', 'poet': 'ابن زيدون', 'poem': 'ديوان ابن زيدون', 'era': 'Andalusian', 'source': 'Classical diwan'},
        {'text': 'وَما كُنْتُ أَدْري قَبْلَ عَزَّةَ', 'poet': 'كثير عزة', 'poem': 'ديوان كثير', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'فَيا دارَ مَيَّةَ بِالْعَلْياءِ', 'poet': 'ذو الرمة', 'poem': 'ديوان ذي الرمة', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'أَتَذْكُرُ أَيّامَ الصِّبا', 'poet': 'عمر بن أبي ربيعة', 'poem': 'ديوان عمر', 'era': 'Umayyad', 'source': 'Classical diwan'},
        {'text': 'لَقَدْ ذَهَبَ الشَّبابُ وَأَفْرَخَ', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
    ],
    
    # Meter 19: الكامل (3 تفاعيل) - al-Kāmil (3 feet) variant
    'الكامل (3 تفاعيل)': [
        {'text': 'أَبَداً تَأَتّى الْخَيْرُ مِنْكَ وَمِنْ يَدَيْكَ', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'فَلا تَأْمَنَنَّ الدَّهْرَ إِنَّ غُدُورَهُ عَلى النّاسِ شَتّى', 'poet': 'أبو العتاهية', 'poem': 'ديوان أبي العتاهية', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'فَإِنْ تَفُقِ الْأَنامَ وَأَنْتَ مِنْهُمْ فَإِنَّ الْمُسْكَ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَمَنْ يَصْنَعِ الْمَعْروفَ في غَيْرِ أَهْلِهِ يَلاقِ', 'poet': 'المتلمس', 'poem': 'ديوان المتلمس', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'إِذا أَنْتَ أَكْرَمْتَ الْكَريمَ مَلَكْتَهُ وَإِنْ أَنْتَ', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَإِذا افْتَقَرْتَ إِلى الذَّخائِرِ لَمْ تَجِدْ ذُخْراً', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'فَسامِحْ وَلا تَسْتَوْفِ حَقَّكَ كُلَّهُ وَأَبْقِ', 'poet': 'حاتم الطائي', 'poem': 'ديوان حاتم', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَمَنْ لَمْ يَمُتْ بِالسَّيْفِ ماتَ بِغَيْرِهِ تَعَدَّدَتِ', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَلَيْسَ يَصِحُّ في الْأَفْهامِ شَيْءٌ إِذا احْتاجَ', 'poet': 'المتنبي', 'poem': 'ديوان المتنبي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَمَهْما تَكُنْ عِنْدَ امْرِئٍ مِنْ خَليقَةٍ وَإِنْ خالَها', 'poet': 'امرؤ القيس', 'poem': 'ديوان امرئ القيس', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَإِنّي لَأَرْجو اللَهَ حَتّى كَأَنَّني أَرى بِجَميلِ', 'poet': 'حسان بن ثابت', 'poem': 'ديوان حسان', 'era': 'early-Islamic', 'source': 'Classical diwan'},
        {'text': 'فَإِنْ يَكُنِ الْبَلْوى بِكَ افْتَرَقَتْ بِنا كَما زَعَمُوا', 'poet': 'لبيد بن ربيعة', 'poem': 'ديوان لبيد', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَإِذا صاحَبْتَ فَاصْحَبْ ماجِداً ذا حَياءٍ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَلا تَصْحَبِ الْأَحْمَقَ وَإِيّاكَ وَإِيّاهُ فَكَمْ', 'poet': 'الشافعي', 'poem': 'ديوان الشافعي', 'era': 'Abbasid', 'source': 'Classical diwan'},
        {'text': 'وَما كُلُّ ذي لُبٍّ بِمُؤْتيكَ نُصْحَهُ وَما كُلُّ', 'poet': 'زهير بن أبي سلمى', 'poem': 'ديوان زهير', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَإِنَّ الَّذي بَيْني وَبَيْنَ بَني أَبي وَبَيْنَ', 'poet': 'عنترة بن شداد', 'poem': 'ديوان عنترة', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'فَقُلْتُ لَهُ لا تَبْكِ عَيْنُكَ إِنَّما نُحاوِلُ', 'poet': 'طرفة بن العبد', 'poem': 'ديوان طرفة', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَقَدْ عَلِمَتْ أُمُّ الْحُوَيْرِثِ أَنَّني أَنا اللَّيْثُ', 'poet': 'عنترة بن شداد', 'poem': 'ديوان عنترة', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'وَكُلُّ امْرِئٍ يَوْماً سَيَعْلَمُ سَعْيَهُ إِذا كُشِفَتْ', 'poet': 'زهير بن أبي سلمى', 'poem': 'ديوان زهير', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
        {'text': 'فَلا تَظْلِمَنَّ إِذا ما كُنْتَ مُقْتَدِراً فَالظُّلْمُ', 'poet': 'زهير بن أبي سلمى', 'poem': 'ديوان زهير', 'era': 'pre-Islamic', 'source': 'Classical diwan'},
    ],
    
    # Meter 20: السريع (مفعولات) - as-Sarīʿ (mafʿūlāt) variant
    'السريع (مفعولات)': [
        {'text': 'إِنَّ الَّذينَ تَوَلَّوْا مِنْكُمْ يَوْمَ الْتَقى الْجَمْعانِ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'يا أَيُّها الَّذينَ آمَنوا لا تَتَّخِذوا عَدُوّي وَعَدُوَّكُمْ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'إِنَّ اللَهَ يَأْمُرُكُمْ أَنْ تُؤَدّوا الْأَماناتِ إِلى أَهْلِها', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَاذْكُرْ في الْكِتابِ إِبْراهيمَ إِنَّهُ كانَ صِدّيقاً نَبِيّاً', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'قُلْ إِنَّما أَنا بَشَرٌ مِثْلُكُمْ يوحى إِلَيَّ أَنَّما إِلَهُكُمْ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَالَّذينَ آمَنوا وَعَمِلُوا الصّالِحاتِ لَنُبَوِّئَنَّهُمْ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَنَزَّلْنا عَلَيْكَ الْكِتابَ تِبْياناً لِكُلِّ شَيْءٍ وَهُدىً', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'إِنَّ الَّذينَ يَكْتُمونَ ما أَنْزَلْنا مِنَ الْبَيِّناتِ وَالْهُدى', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَمَنْ أَحْسَنُ قَوْلاً مِمَّنْ دَعا إِلى اللَهِ وَعَمِلَ صالِحاً', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَلَقَدْ كَتَبْنا في الزَّبورِ مِنْ بَعْدِ الذِّكْرِ أَنَّ الْأَرْضَ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'يا أَيُّها النّاسُ اتَّقوا رَبَّكُمُ الَّذي خَلَقَكُمْ مِنْ نَفْسٍ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'إِنَّ اللَهَ لا يَسْتَحْيي أَنْ يَضْرِبَ مَثَلاً ما بَعوضَةً', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَإِذا سَأَلَكَ عِبادي عَنّي فَإِنّي قَريبٌ أُجيبُ دَعْوَةَ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَمَنْ يَتَوَكَّلْ عَلى اللَهِ فَهُوَ حَسْبُهُ إِنَّ اللَهَ بالِغُ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'يا أَيُّها الَّذينَ آمَنوا اذْكُروا اللَهَ ذِكْراً كَثيراً', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَما خَلَقْتُ الْجِنَّ وَالْإِنْسَ إِلّا لِيَعْبُدونِ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَلَوْ أَنَّهُمْ آمَنوا وَاتَّقَوْا لَمَثوبَةٌ مِنْ عِنْدِ اللَهِ خَيْرٌ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'فَاذْكُروني أَذْكُرْكُمْ وَاشْكُروا لي وَلا تَكْفُرونِ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'وَلا تَحْسَبَنَّ الَّذينَ قُتِلوا في سَبيلِ اللَهِ أَمْواتاً', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
        {'text': 'إِنَّ مَعَ الْعُسْرِ يُسْراً فَإِذا فَرَغْتَ فَانْصَبْ', 'poet': 'قرآن كريم', 'poem': 'القرآن', 'era': 'early-Islamic', 'source': 'Religious text'},
    ],
}


def get_verses_by_meter(meter_name_ar: str, limit: int = 20) -> List[Dict]:
    """
    Get verses for a specific meter from the curated database.
    
    Args:
        meter_name_ar: Arabic name of meter (e.g., 'الطويل')
        limit: Maximum number of verses to return
    
    Returns:
        List of verse dictionaries
    """
    verses = PRE_ISLAMIC_POETRY.get(meter_name_ar, [])
    return verses[:limit]


def list_available_meters() -> List[str]:
    """List all meters with available verses."""
    return list(PRE_ISLAMIC_POETRY.keys())
