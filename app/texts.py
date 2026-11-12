"""All words shown by the application, in every language it offers.

To add a language: add it to LANGUAGES and give every key in TEXT a value for it.
Bhojpuri and Awadhi fall back to Hindi for crop, season and district names.
"""

LANGUAGES = {"en": "English", "hi": "हिन्दी", "ur": "اردو", "bho": "भोजपुरी", "awa": "अवधी"}
RIGHT_TO_LEFT = {"ur"}
FALLBACK = {"bho": "hi", "awa": "hi"}

TEXT = {
    "title": {"en": "KrishiDrishti", "hi": "कृषि दृष्टि", "ur": "کرشی درشٹی", "bho": "कृषि दृष्टि", "awa": "कृषि दृष्टि"},
    "tagline": {
        "en": "Which crop can earn you more this season? Uttar Pradesh",
        "hi": "इस मौसम में कौन सी फसल ज़्यादा कमाई दे सकती है? उत्तर प्रदेश",
        "ur": "اس موسم میں کون سی فصل زیادہ کمائی دے سکتی ہے؟ اتر پردیش",
        "bho": "ए मौसम में कवन फसल जादा कमाई दे सकेले? उत्तर प्रदेश",
        "awa": "यहि मौसम मा कउन फसल जादा कमाई दै सकत है? उत्तर प्रदेश",
    },
    "language": {"en": "Language", "hi": "भाषा", "ur": "زبان", "bho": "भाषा", "awa": "भाषा"},
    "how_title": {"en": "How to use", "hi": "कैसे इस्तेमाल करें", "ur": "استعمال کا طریقہ", "bho": "कइसे इस्तेमाल करीं", "awa": "कइसे इस्तेमाल करी"},
    "how_1": {
        "en": "Choose your district and the season.",
        "hi": "अपना ज़िला और मौसम चुनें।",
        "ur": "اپنا ضلع اور موسم چنیں۔",
        "bho": "आपन जिला आ मौसम चुनीं।",
        "awa": "आपन जिला अउर मौसम चुनौ।",
    },
    "how_2": {
        "en": "Enter your land size and say if you can water the field.",
        "hi": "अपनी ज़मीन का आकार भरें और बताएँ कि खेत में सिंचाई हो सकती है या नहीं।",
        "ur": "اپنی زمین کا رقبہ بھریں اور بتائیں کہ کھیت میں آبپاشی ہو سکتی ہے یا نہیں۔",
        "bho": "आपन जमीन के नाप भरीं आ बताईं कि खेत में सिंचाई हो सकेला कि ना।",
        "awa": "आपन जमीन कै नाप भरौ अउर बताओ कि खेत मा सिंचाई होइ सकत है कि नाहीं।",
    },
    "how_3": {
        "en": "Press the green button to see the best crops.",
        "hi": "सबसे अच्छी फसलें देखने के लिए हरा बटन दबाएँ।",
        "ur": "بہترین فصلیں دیکھنے کے لیے ہرا بٹن دبائیں۔",
        "bho": "सबसे बढ़िया फसल देखे खातिर हरियर बटन दबाईं।",
        "awa": "सबसे नीक फसल देखै खातिर हरियर बटन दबाओ।",
    },
    "farm_title": {"en": "Your farm", "hi": "आपका खेत", "ur": "آپ کا کھیت", "bho": "रउआ के खेत", "awa": "आपन खेत"},
    "district": {"en": "District", "hi": "ज़िला", "ur": "ضلع", "bho": "जिला", "awa": "जिला"},
    "season": {"en": "Season", "hi": "मौसम", "ur": "موسم", "bho": "मौसम", "awa": "मौसम"},
    "land": {"en": "Land size", "hi": "ज़मीन का आकार", "ur": "زمین کا رقبہ", "bho": "जमीन के नाप", "awa": "जमीन कै नाप"},
    "unit": {"en": "Unit", "hi": "इकाई", "ur": "اکائی", "bho": "इकाई", "awa": "इकाई"},
    "acre": {"en": "Acre", "hi": "एकड़", "ur": "ایکڑ", "bho": "एकड़", "awa": "एकड़"},
    "hectare": {"en": "Hectare", "hi": "हेक्टेयर", "ur": "ہیکٹیئر", "bho": "हेक्टेयर", "awa": "हेक्टेयर"},
    "water": {
        "en": "Can you water this field? (tubewell, canal or pump)",
        "hi": "क्या इस खेत में सिंचाई हो सकती है? (ट्यूबवेल, नहर या पंप)",
        "ur": "کیا اس کھیت میں آبپاشی ہو سکتی ہے؟ (ٹیوب ویل، نہر یا پمپ)",
        "bho": "का ए खेत में सिंचाई हो सकेला? (ट्यूबवेल, नहर भा पंप)",
        "awa": "का यहि खेत मा सिंचाई होइ सकत है? (ट्यूबवेल, नहर या पंप)",
    },
    "yes": {"en": "Yes", "hi": "हाँ", "ur": "ہاں", "bho": "हँ", "awa": "हाँ"},
    "no": {"en": "No", "hi": "नहीं", "ur": "نہیں", "bho": "ना", "awa": "नाहीं"},
    "more": {
        "en": "More details (optional, gives a better answer)",
        "hi": "और जानकारी (ज़रूरी नहीं, पर जवाब बेहतर होगा)",
        "ur": "مزید معلومات (ضروری نہیں، مگر جواب بہتر ہوگا)",
        "bho": "अउरी जानकारी (जरूरी नइखे, बाकिर जवाब बढ़िया होई)",
        "awa": "अउर जानकारी (जरूरी नाहीं, मुला जवाब नीक होई)",
    },
    "own_crop": {
        "en": "A crop you already grow in this season",
        "hi": "इस मौसम में जो फसल आप पहले से उगाते हैं",
        "ur": "اس موسم میں جو فصل آپ پہلے سے اگاتے ہیں",
        "bho": "ए मौसम में जवन फसल रउआ पहिले से उगावेनी",
        "awa": "यहि मौसम मा जउन फसल आप पहिले से उगावत हौ",
    },
    "none": {"en": "None", "hi": "कोई नहीं", "ur": "کوئی نہیں", "bho": "कवनो ना", "awa": "कउनो नाहीं"},
    "own_yield": {
        "en": "How much do you usually get? (quintal per acre)",
        "hi": "आम तौर पर कितनी पैदावार मिलती है? (क्विंटल प्रति एकड़)",
        "ur": "عام طور پر کتنی پیداوار ملتی ہے؟ (کوئنٹل فی ایکڑ)",
        "bho": "आम तौर पर केतना पैदावार मिलेला? (क्विंटल प्रति एकड़)",
        "awa": "आम तौर पर केतनी पैदावार मिलत है? (क्विंटल प्रति एकड़)",
    },
    "soil_card": {
        "en": "If your Soil Health Card says so, tick:",
        "hi": "अगर आपके मृदा स्वास्थ्य कार्ड में लिखा है, तो निशान लगाएँ:",
        "ur": "اگر آپ کے سوائل ہیلتھ کارڈ میں لکھا ہے تو نشان لگائیں:",
        "bho": "अगर रउआ के मृदा स्वास्थ्य कार्ड में लिखल बा, त निशान लगाईं:",
        "awa": "अगर आपके मृदा स्वास्थ्य कार्ड मा लिखा है, तौ निशान लगाओ:",
    },
    "saline": {"en": "Salty soil (saline)", "hi": "खारी मिट्टी (लवणीय)", "ur": "کھاری مٹی (شور)", "bho": "खारा माटी (लवणीय)", "awa": "खारी माटी (लवणीय)"},
    "alkaline": {"en": "Usar soil (alkaline)", "hi": "ऊसर मिट्टी (क्षारीय)", "ur": "اوسر مٹی (کلر)", "bho": "ऊसर माटी (क्षारीय)", "awa": "ऊसर माटी (क्षारीय)"},
    "button": {"en": "Show best crops", "hi": "सबसे अच्छी फसलें दिखाएँ", "ur": "بہترین فصلیں دکھائیں", "bho": "सबसे बढ़िया फसल देखाईं", "awa": "सबसे नीक फसल देखाओ"},
    "result_title": {"en": "Best crops for you", "hi": "आपके लिए सबसे अच्छी फसलें", "ur": "آپ کے لیے بہترین فصلیں", "bho": "रउआ खातिर सबसे बढ़िया फसल", "awa": "आपके खातिर सबसे नीक फसल"},
    "profit": {"en": "Expected profit", "hi": "अनुमानित मुनाफ़ा", "ur": "متوقع منافع", "bho": "अनुमानित मुनाफा", "awa": "अनुमानित मुनाफा"},
    "on_land": {"en": "on your {size} {unit}", "hi": "आपके {size} {unit} पर", "ur": "آپ کے {size} {unit} پر", "bho": "रउआ के {size} {unit} पर", "awa": "आपके {size} {unit} पर"},
    "bad_year": {"en": "Bad year", "hi": "खराब साल", "ur": "خراب سال", "bho": "खराब साल", "awa": "खराब साल"},
    "good_year": {"en": "Good year", "hi": "अच्छा साल", "ur": "اچھا سال", "bho": "बढ़िया साल", "awa": "नीक साल"},
    "tag_safe": {
        "en": "Profit likely even in a bad year",
        "hi": "खराब साल में भी मुनाफ़े की उम्मीद",
        "ur": "خراب سال میں بھی منافع کی امید",
        "bho": "खराब साल में भी मुनाफा के उम्मीद",
        "awa": "खराब साल मा भी मुनाफा कै उम्मीद",
    },
    "tag_risk": {
        "en": "Can lose money in a bad year",
        "hi": "खराब साल में घाटा हो सकता है",
        "ur": "خراب سال میں نقصان ہو سکتا ہے",
        "bho": "खराब साल में घाटा हो सकेला",
        "awa": "खराब साल मा घाटा होइ सकत है",
    },
    "less_certain": {
        "en": "This estimate is less certain",
        "hi": "यह अनुमान कम पक्का है",
        "ur": "یہ اندازہ کم پکا ہے",
        "bho": "ई अनुमान कम पक्का बा",
        "awa": "ई अनुमान कम पक्का है",
    },
    "note_rare": {
        "en": "Few farmers in your district grow this. Check seed and buyers first.",
        "hi": "आपके ज़िले में कम किसान इसे उगाते हैं। पहले बीज और ख़रीदार का पता करें।",
        "ur": "آپ کے ضلع میں کم کسان اسے اگاتے ہیں۔ پہلے بیج اور خریدار کا پتا کریں۔",
        "bho": "रउआ के जिला में कम किसान एकरा के उगावेलें। पहिले बीज आ खरीदार के पता करीं।",
        "awa": "आपके जिला मा कम किसान एहिका उगावत हैं। पहिले बीज अउर खरीदार कै पता करौ।",
    },
    "note_water": {
        "en": "This crop needs watering.",
        "hi": "इस फसल को सिंचाई चाहिए।",
        "ur": "اس فصل کو آبپاشی چاہیے۔",
        "bho": "ए फसल के सिंचाई चाहीं।",
        "awa": "यहि फसल का सिंचाई चाही।",
    },
    "note_saline": {
        "en": "This crop does poorly in salty soil.",
        "hi": "यह फसल खारी मिट्टी में अच्छी नहीं होती।",
        "ur": "یہ فصل کھاری مٹی میں اچھی نہیں ہوتی۔",
        "bho": "ई फसल खारा माटी में बढ़िया ना होला।",
        "awa": "ई फसल खारी माटी मा नीक नाहीं होत।",
    },
    "note_alkaline": {
        "en": "This crop does poorly in usar soil.",
        "hi": "यह फसल ऊसर मिट्टी में अच्छी नहीं होती।",
        "ur": "یہ فصل اوسر مٹی میں اچھی نہیں ہوتی۔",
        "bho": "ई फसल ऊसर माटी में बढ़िया ना होला।",
        "awa": "ई फसल ऊसर माटी मा नीक नाहीं होत।",
    },
    "note_old": {
        "en": "Yield figures for this crop are a few years old.",
        "hi": "इस फसल की पैदावार के आँकड़े कुछ साल पुराने हैं।",
        "ur": "اس فصل کی پیداوار کے اعداد کچھ سال پرانے ہیں۔",
        "bho": "ए फसल के पैदावार के आँकड़ा कुछ साल पुरान बा।",
        "awa": "यहि फसल कै पैदावार कै आँकड़ा कुछ साल पुरान हैं।",
    },
    "no_result": {
        "en": "We do not have enough price information to rank crops for this choice.",
        "hi": "इस चुनाव के लिए फसलों की तुलना करने लायक भाव की जानकारी हमारे पास नहीं है।",
        "ur": "اس انتخاب کے لیے فصلوں کا موازنہ کرنے لائق بھاؤ کی معلومات ہمارے پاس نہیں ہے۔",
        "bho": "ए चुनाव खातिर फसल के तुलना करे लायक भाव के जानकारी हमनी लगे नइखे।",
        "awa": "यहि चुनाव खातिर फसल कै तुलना करै लायक भाव कै जानकारी हमरे पास नाहीं है।",
    },
    "all_crops": {"en": "See all crops", "hi": "सभी फसलें देखें", "ur": "تمام فصلیں دیکھیں", "bho": "सगरी फसल देखीं", "awa": "सब फसल देखौ"},
    "col_crop": {"en": "Crop", "hi": "फसल", "ur": "فصل", "bho": "फसल", "awa": "फसल"},
    "col_remark": {"en": "Remark", "hi": "टिप्पणी", "ur": "تبصرہ", "bho": "टिप्पणी", "awa": "टिप्पणी"},
    "remark_no_water": {
        "en": "Not suitable: needs watering",
        "hi": "ठीक नहीं: सिंचाई चाहिए",
        "ur": "مناسب نہیں: آبپاشی چاہیے",
        "bho": "ठीक नइखे: सिंचाई चाहीं",
        "awa": "ठीक नाहीं: सिंचाई चाही",
    },
    "remark_no_price": {
        "en": "No price information yet",
        "hi": "भाव की जानकारी अभी नहीं है",
        "ur": "بھاؤ کی معلومات ابھی نہیں ہے",
        "bho": "भाव के जानकारी अबहीं नइखे",
        "awa": "भाव कै जानकारी अबहीं नाहीं है",
    },
    "read_title": {"en": "How to read this", "hi": "इसे कैसे समझें", "ur": "اسے کیسے سمجھیں", "bho": "एकरा के कइसे समझीं", "awa": "एहिका कइसे समझी"},
    "read_1": {
        "en": "Profit is the money from selling the crop minus the cost of growing it, for your land size.",
        "hi": "मुनाफ़ा = फसल बेचने से मिला पैसा घटा उगाने का ख़र्च, आपकी ज़मीन के हिसाब से।",
        "ur": "منافع = فصل بیچنے سے ملا پیسہ منفی اگانے کا خرچ، آپ کی زمین کے حساب سے۔",
        "bho": "मुनाफा = फसल बेचे से मिलल पइसा में से उगावे के खर्चा घटा के, रउआ के जमीन के हिसाब से।",
        "awa": "मुनाफा = फसल बेचे से मिला पइसा मा से उगावै कै खर्चा घटाइ कै, आपकी जमीन के हिसाब से।",
    },
    "read_2": {
        "en": "In 8 years out of 10, the profit should fall between the bad-year and the good-year figure.",
        "hi": "10 में से 8 साल मुनाफ़ा खराब साल और अच्छे साल के आँकड़ों के बीच रहना चाहिए।",
        "ur": "10 میں سے 8 سال منافع خراب سال اور اچھے سال کے اعداد کے درمیان رہنا چاہیے۔",
        "bho": "10 में से 8 साल मुनाफा खराब साल आ बढ़िया साल के आँकड़ा के बीच रहे के चाहीं।",
        "awa": "10 मा से 8 साल मुनाफा खराब साल अउर नीक साल के आँकड़ा के बीच रहै का चाही।",
    },
    "read_3": {
        "en": "These are averages for your district, not a promise for your field. Talk to your Krishi Vigyan Kendra before deciding.",
        "hi": "ये आपके ज़िले के औसत हैं, आपके खेत के लिए वादा नहीं। फ़ैसला करने से पहले अपने कृषि विज्ञान केंद्र से बात करें।",
        "ur": "یہ آپ کے ضلع کے اوسط ہیں، آپ کے کھیت کے لیے وعدہ نہیں۔ فیصلہ کرنے سے پہلے اپنے کرشی وگیان کیندر سے بات کریں۔",
        "bho": "ई रउआ के जिला के औसत बा, रउआ के खेत खातिर वादा ना। फैसला करे से पहिले आपन कृषि विज्ञान केंद्र से बात करीं।",
        "awa": "ई आपके जिला कै औसत हैं, आपके खेत खातिर वादा नाहीं। फैसला करै से पहिले आपन कृषि विज्ञान केंद्र से बात करौ।",
    },
    "footer": {
        "en": "Prototype for learning and testing. Yield estimate for 2025-26, price and cost for 2026-27.",
        "hi": "यह सीखने और परखने के लिए बना नमूना है। पैदावार का अनुमान 2025-26 का, भाव और ख़र्च 2026-27 के।",
        "ur": "یہ سیکھنے اور آزمانے کے لیے بنا نمونہ ہے۔ پیداوار کا اندازہ 2025-26 کا، بھاؤ اور خرچ 2026-27 کے۔",
        "bho": "ई सीखे आ परखे खातिर बनल नमूना बा। पैदावार के अनुमान 2025-26 के, भाव आ खर्चा 2026-27 के।",
        "awa": "ई सीखै अउर परखै खातिर बना नमूना है। पैदावार कै अनुमान 2025-26 कै, भाव अउर खर्चा 2026-27 कै।",
    },
}

SEASONS = {
    "Kharif": {"en": "Kharif (sown June-July)", "hi": "खरीफ़ (बुवाई जून-जुलाई)", "ur": "خریف (بوائی جون-جولائی)"},
    "Rabi": {"en": "Rabi (sown October-November)", "hi": "रबी (बुवाई अक्टूबर-नवंबर)", "ur": "ربیع (بوائی اکتوبر-نومبر)"},
    "Summer": {"en": "Zaid / Summer (sown March-April)", "hi": "ज़ायद / गर्मी (बुवाई मार्च-अप्रैल)", "ur": "زائد / گرمی (بوائی مارچ-اپریل)"},
    "Whole Year": {"en": "Whole year", "hi": "पूरा साल", "ur": "پورا سال"},
}

CROPS = {
    "Arhar/Tur": {"en": "Arhar (Tur)", "hi": "अरहर", "ur": "ارہر"},
    "Bajra": {"en": "Bajra", "hi": "बाजरा", "ur": "باجرا"},
    "Banana": {"en": "Banana", "hi": "केला", "ur": "کیلا"},
    "Barley": {"en": "Barley (Jau)", "hi": "जौ", "ur": "جَو"},
    "Coriander": {"en": "Coriander", "hi": "धनिया", "ur": "دھنیا"},
    "Cotton(lint)": {"en": "Cotton", "hi": "कपास", "ur": "کپاس"},
    "Dry chillies": {"en": "Dry chillies", "hi": "सूखी मिर्च", "ur": "سوکھی مرچ"},
    "Garlic": {"en": "Garlic", "hi": "लहसुन", "ur": "لہسن"},
    "Ginger": {"en": "Ginger", "hi": "अदरक", "ur": "ادرک"},
    "Gram": {"en": "Gram (Chana)", "hi": "चना", "ur": "چنا"},
    "Groundnut": {"en": "Groundnut", "hi": "मूँगफली", "ur": "مونگ پھلی"},
    "Guar seed": {"en": "Guar", "hi": "ग्वार", "ur": "گوار"},
    "Jowar": {"en": "Jowar", "hi": "ज्वार", "ur": "جوار"},
    "Linseed": {"en": "Linseed (Alsi)", "hi": "अलसी", "ur": "السی"},
    "Maize": {"en": "Maize", "hi": "मक्का", "ur": "مکئی"},
    "Masoor": {"en": "Masoor (Lentil)", "hi": "मसूर", "ur": "مسور"},
    "Moong(Green Gram)": {"en": "Moong", "hi": "मूँग", "ur": "مونگ"},
    "Onion": {"en": "Onion", "hi": "प्याज़", "ur": "پیاز"},
    "Peas & beans (Pulses)": {"en": "Peas (Matar)", "hi": "मटर", "ur": "مٹر"},
    "Potato": {"en": "Potato", "hi": "आलू", "ur": "آلو"},
    "Rapeseed & Mustard": {"en": "Mustard (Sarson)", "hi": "सरसों", "ur": "سرسوں"},
    "Rice": {"en": "Paddy (Rice)", "hi": "धान", "ur": "دھان"},
    "Sannhamp": {"en": "Sunn hemp (Sanai)", "hi": "सनई", "ur": "سنئی"},
    "Sesamum": {"en": "Sesame (Til)", "hi": "तिल", "ur": "تل"},
    "Small millets": {"en": "Small millets", "hi": "छोटे मोटे अनाज", "ur": "چھوٹے موٹے اناج"},
    "Soyabean": {"en": "Soyabean", "hi": "सोयाबीन", "ur": "سویابین"},
    "Sugarcane": {"en": "Sugarcane", "hi": "गन्ना", "ur": "گنا"},
    "Sunflower": {"en": "Sunflower", "hi": "सूरजमुखी", "ur": "سورج مکھی"},
    "Sweet potato": {"en": "Sweet potato", "hi": "शकरकंद", "ur": "شکرقند"},
    "Tobacco": {"en": "Tobacco", "hi": "तंबाकू", "ur": "تمباکو"},
    "Turmeric": {"en": "Turmeric", "hi": "हल्दी", "ur": "ہلدی"},
    "Urad": {"en": "Urad", "hi": "उड़द", "ur": "اُڑد"},
    "Wheat": {"en": "Wheat", "hi": "गेहूँ", "ur": "گندم"},
}

DISTRICTS_HI = {
    "Agra": "आगरा", "Aligarh": "अलीगढ़", "Allahabad": "प्रयागराज (इलाहाबाद)", "Ambedkar nagar": "अंबेडकर नगर",
    "Amethi": "अमेठी", "Amroha": "अमरोहा", "Auraiya": "औरैया", "Azamgarh": "आज़मगढ़", "Baghpat": "बागपत",
    "Bahraich": "बहराइच", "Ballia": "बलिया", "Balrampur": "बलरामपुर", "Banda": "बाँदा", "Barabanki": "बाराबंकी",
    "Bareilly": "बरेली", "Basti": "बस्ती", "Bijnor": "बिजनौर", "Budaun": "बदायूँ", "Bulandshahr": "बुलंदशहर",
    "Chandauli": "चंदौली", "Chitrakoot": "चित्रकूट", "Deoria": "देवरिया", "Etah": "एटा", "Etawah": "इटावा",
    "Faizabad": "अयोध्या (फ़ैज़ाबाद)", "Farrukhabad": "फ़र्रुख़ाबाद", "Fatehpur": "फ़तेहपुर", "Firozabad": "फ़िरोज़ाबाद",
    "Gautam buddha nagar": "गौतम बुद्ध नगर", "Ghaziabad": "ग़ाज़ियाबाद", "Ghazipur": "ग़ाज़ीपुर", "Gonda": "गोंडा",
    "Gorakhpur": "गोरखपुर", "Hamirpur": "हमीरपुर", "Hapur": "हापुड़", "Hardoi": "हरदोई", "Hathras": "हाथरस",
    "Jalaun": "जालौन", "Jaunpur": "जौनपुर", "Jhansi": "झाँसी", "Kannauj": "कन्नौज", "Kanpur dehat": "कानपुर देहात",
    "Kanpur nagar": "कानपुर नगर", "Kasganj": "कासगंज", "Kaushambi": "कौशाम्बी", "Kheri": "लखीमपुर खीरी",
    "Kushi nagar": "कुशीनगर", "Lalitpur": "ललितपुर", "Lucknow": "लखनऊ", "Maharajganj": "महराजगंज", "Mahoba": "महोबा",
    "Mainpuri": "मैनपुरी", "Mathura": "मथुरा", "Mau": "मऊ", "Meerut": "मेरठ", "Mirzapur": "मिर्ज़ापुर",
    "Moradabad": "मुरादाबाद", "Muzaffarnagar": "मुज़फ़्फ़रनगर", "Pilibhit": "पीलीभीत", "Pratapgarh": "प्रतापगढ़",
    "Rae bareli": "रायबरेली", "Rampur": "रामपुर", "Saharanpur": "सहारनपुर", "Sambhal": "संभल",
    "Sant kabeer nagar": "संत कबीर नगर", "Sant ravidas nagar": "भदोही (संत रविदास नगर)", "Shahjahanpur": "शाहजहाँपुर",
    "Shamli": "शामली", "Shravasti": "श्रावस्ती", "Siddharth nagar": "सिद्धार्थनगर", "Sitapur": "सीतापुर",
    "Sonbhadra": "सोनभद्र", "Sultanpur": "सुल्तानपुर", "Unnao": "उन्नाव", "Varanasi": "वाराणसी",
}


def pick(table: dict, lang: str) -> str:
    """The entry of `table` for the language, falling back to Hindi (dialects) and then English."""
    if lang in table:
        return table[lang]
    return table.get(FALLBACK.get(lang, "en"), table["en"])


def t(key: str, lang: str, **values) -> str:
    return pick(TEXT[key], lang).format(**values)


def crop_name(crop: str, lang: str) -> str:
    return pick(CROPS[crop], lang) if crop in CROPS else crop


def season_name(season: str, lang: str) -> str:
    return pick(SEASONS[season], lang) if season in SEASONS else season


def district_name(district: str, lang: str) -> str:
    title = district.title()
    if lang in ("hi", "bho", "awa") and district in DISTRICTS_HI:
        return f"{DISTRICTS_HI[district]} ({title})"
    return title
