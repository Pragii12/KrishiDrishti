"""All words shown by the application, in every language it offers.

To add a language: add it to LANGUAGES and give the keys in TEXT a value for it.
A key with no Bhojpuri or Awadhi value is shown in Hindi; crop, season and district names too.
"""

LANGUAGES = {"en": "English", "hi": "हिन्दी", "ur": "اردو", "bho": "भोजपुरी", "awa": "अवधी"}
RIGHT_TO_LEFT = {"ur"}
FALLBACK = {"bho": "hi", "awa": "hi"}

TEXT = {
    "title": {"en": "KrishiDrishti", "hi": "कृषि दृष्टि", "ur": "کرشی درشٹی", "bho": "कृषि दृष्टि", "awa": "कृषि दृष्टि"},
    "tagline": {
        "en": "Crop advice suited to your land · Uttar Pradesh",
        "hi": "आपकी ज़मीन के हिसाब से फसल सलाह · उत्तर प्रदेश",
        "ur": "آپ کی زمین کے حساب سے فصل مشورہ · اتر پردیش",
        "bho": "रउआ के जमीन के हिसाब से फसल सलाह · उत्तर प्रदेश",
        "awa": "आपकी जमीन के हिसाब से फसल सलाह · उत्तर प्रदेश",
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
        "en": "Choose acre or hectare and say if you can water the field.",
        "hi": "एकड़ या हेक्टेयर चुनें और बताएँ कि खेत में सिंचाई हो सकती है या नहीं।",
        "ur": "ایکڑ یا ہیکٹیئر چنیں اور بتائیں کہ کھیت میں آبپاشی ہو سکتی ہے یا نہیں۔",
        "bho": "एकड़ चाहे हेक्टेयर चुनीं आ बताईं कि खेत में सिंचाई हो सकेला कि ना।",
        "awa": "एकड़ या हेक्टेयर चुनौ अउर बताओ कि खेत मा सिंचाई होइ सकत है कि नाहीं।",
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
    "unit": {"en": "Show figures for one", "hi": "आँकड़े किसके हिसाब से दिखाएँ", "ur": "اعداد کس کے حساب سے دکھائیں",
             "bho": "आँकड़ा केकरा हिसाब से देखाईं", "awa": "आँकड़ा केहिके हिसाब से देखाई"},
    "per_unit": {"en": "per {unit}", "hi": "प्रति {unit}", "ur": "فی {unit}", "bho": "प्रति {unit}", "awa": "प्रति {unit}"},
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
    "yield_line": {
        "en": "Expected yield: <b>{amount}</b> quintal per {unit}",
        "hi": "अनुमानित उपज: <b>{amount}</b> क्विंटल प्रति {unit}",
        "ur": "متوقع پیداوار: <b>{amount}</b> کوئنٹل فی {unit}",
        "bho": "अनुमानित उपज: <b>{amount}</b> क्विंटल प्रति {unit}",
        "awa": "अनुमानित उपज: <b>{amount}</b> क्विंटल प्रति {unit}",
    },
    "col_yield": {
        "en": "Expected yield (quintal per {unit})",
        "hi": "अनुमानित उपज (क्विंटल प्रति {unit})",
        "ur": "متوقع پیداوار (کوئنٹل فی {unit})",
        "bho": "अनुमानित उपज (क्विंटल प्रति {unit})",
        "awa": "अनुमानित उपज (क्विंटल प्रति {unit})",
    },
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
        "en": "Profit is the money from selling the crop minus the cost of growing it, for one acre or one hectare.",
        "hi": "मुनाफ़ा = फसल बेचने से मिला पैसा घटा उगाने का ख़र्च, एक एकड़ या एक हेक्टेयर के हिसाब से।",
        "ur": "منافع = فصل بیچنے سے ملا پیسہ منفی اگانے کا خرچ، ایک ایکڑ یا ایک ہیکٹیئر کے حساب سے۔",
        "bho": "मुनाफा = फसल बेचे से मिलल पइसा में से उगावे के खर्चा घटा के, एक एकड़ चाहे एक हेक्टेयर के हिसाब से।",
        "awa": "मुनाफा = फसल बेचे से मिला पइसा मा से उगावै कै खर्चा घटाइ कै, एक एकड़ या एक हेक्टेयर के हिसाब से।",
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

TEXT.update({
    "strip": {"en": "Crop advisory for the farmers of Uttar Pradesh", "hi": "उत्तर प्रदेश के किसानों के लिए फसल सलाह",
              "ur": "اتر پردیش کے کسانوں کے لیے فصل مشورہ"},
    "nav_home": {"en": "Home", "hi": "मुख्य पृष्ठ", "ur": "مرکزی صفحہ"},
    "nav_crops": {"en": "Find Best Crop", "hi": "सबसे अच्छी फसल जानें", "ur": "بہترین فصل جانیں"},
    "nav_schemes": {"en": "Farmer Schemes", "hi": "किसान योजनाएँ", "ur": "کسان اسکیمیں"},
    "hero_title": {"en": "Find the crop best suited to your land",
                   "hi": "जानें, आपकी ज़मीन के लिए कौन सी फसल सबसे ठीक है",
                   "ur": "جانیں، آپ کی زمین کے لیے کون سی فصل سب سے موزوں ہے"},
    "hero_text": {"en": "Tell us your district, season and whether you can water the field. KrishiDrishti suggests the crops that suit your farm best.",
                  "hi": "अपना ज़िला, मौसम और सिंचाई की सुविधा बताएँ। कृषि दृष्टि आपके खेत के लिए सबसे उपयुक्त फसलें सुझाता है।",
                  "ur": "اپنا ضلع، موسم اور آبپاشی کی سہولت بتائیں۔ کرشی درشٹی آپ کے کھیت کے لیے سب سے موزوں فصلیں تجویز کرتا ہے۔"},
    "btn_crops": {"en": "Find the best crop", "hi": "सबसे अच्छी फसल जानें", "ur": "بہترین فصل جانیں"},
    "btn_schemes": {"en": "See farmer schemes", "hi": "किसान योजनाएँ देखें", "ur": "کسان اسکیمیں دیکھیں"},
    "stat_districts": {"en": "Districts of Uttar Pradesh", "hi": "उत्तर प्रदेश के ज़िले", "ur": "اتر پردیش کے اضلاع"},
    "stat_years": {"en": "Years of farm records studied", "hi": "साल के खेती के आँकड़े", "ur": "سال کے زرعی اعداد"},
    "stat_languages": {"en": "Languages", "hi": "भाषाएँ", "ur": "زبانیں"},
    "about_title": {"en": "What is KrishiDrishti?", "hi": "कृषि दृष्टि क्या है?", "ur": "کرشی درشٹی کیا ہے؟"},
    "about_text": {"en": "KrishiDrishti is a crop advisory tool. It studies past government records of crop yield, mandi prices, weather, soil and the cost of cultivation, and suggests the crops that suit your land in the coming season.",
                   "hi": "कृषि दृष्टि फसल सलाह का एक साधन है। यह पैदावार, मंडी भाव, मौसम, मिट्टी और खेती के ख़र्च के पुराने सरकारी आँकड़ों का अध्ययन करके बताता है कि आने वाले मौसम में आपकी ज़मीन के लिए कौन सी फसलें उपयुक्त हैं।",
                   "ur": "کرشی درشٹی فصل مشورے کا ایک آلہ ہے۔ یہ پیداوار، منڈی بھاؤ، موسم، مٹی اور کھیتی کے خرچ کے پرانے سرکاری اعداد کا مطالعہ کر کے بتاتا ہے کہ آنے والے موسم میں آپ کی زمین کے لیے کون سی فصلیں موزوں ہیں۔"},
    "works_title": {"en": "How it works", "hi": "यह कैसे काम करता है", "ur": "یہ کیسے کام کرتا ہے"},
    "works_1_title": {"en": "You tell us about your farm", "hi": "आप अपने खेत के बारे में बताते हैं", "ur": "آپ اپنے کھیت کے بارے میں بتاتے ہیں"},
    "works_1_text": {"en": "District, season and whether you can water the field.",
                     "hi": "ज़िला, मौसम और सिंचाई हो सकती है या नहीं।",
                     "ur": "ضلع، موسم اور آبپاشی ہو سکتی ہے یا نہیں۔"},
    "works_2_title": {"en": "The computer studies past years", "hi": "कंप्यूटर पिछले सालों का अध्ययन करता है", "ur": "کمپیوٹر پچھلے سالوں کا مطالعہ کرتا ہے"},
    "works_2_text": {"en": "It estimates the yield, the selling price and the cost of every crop.",
                     "hi": "यह हर फसल की पैदावार, बिक्री भाव और ख़र्च का अनुमान लगाता है।",
                     "ur": "یہ ہر فصل کی پیداوار، فروخت بھاؤ اور خرچ کا اندازہ لگاتا ہے۔"},
    "works_3_title": {"en": "You see the three best crops", "hi": "आपको तीन सबसे अच्छी फसलें दिखती हैं", "ur": "آپ کو تین بہترین فصلیں دکھتی ہیں"},
    "works_3_text": {"en": "With the expected profit in a bad year and in a good year.",
                     "hi": "ख़राब साल और अच्छे साल के अनुमानित मुनाफ़े के साथ।",
                     "ur": "خراب سال اور اچھے سال کے متوقع منافع کے ساتھ۔"},
    "warn_title": {"en": "Please note: treat this as a suggestion", "hi": "कृपया ध्यान दें: इसे एक सुझाव मानें",
                   "ur": "براہ کرم توجہ دیں: اسے ایک مشورہ سمجھیں", "bho": "ध्यान दीं: एकरा के एगो सुझाव मानीं",
                   "awa": "ध्यान देव: एहिका एक सुझाव मानौ"},
    "warn_text": {"en": "These figures are estimates for your knowledge and information. Treat them as a suggestion, and make your final decision with your own experience and the advice of your Krishi Vigyan Kendra or agriculture officer.",
                  "hi": "ये आँकड़े आपकी जानकारी के लिए अनुमान हैं। इन्हें एक सुझाव मानें और आख़िरी फ़ैसला अपने अनुभव तथा कृषि विज्ञान केंद्र या कृषि अधिकारी की सलाह से करें।",
                  "ur": "یہ اعداد آپ کی معلومات کے لیے اندازے ہیں۔ انہیں ایک مشورہ سمجھیں اور آخری فیصلہ اپنے تجربے اور کرشی وگیان کیندر یا زرعی افسر کے مشورے سے کریں۔",
                  "bho": "ई आँकड़ा रउआ के जानकारी खातिर अनुमान बा। एकरा के एगो सुझाव मानीं आ आखिरी फैसला आपन अनुभव आ कृषि विज्ञान केंद्र भा कृषि अधिकारी के सलाह से करीं।",
                  "awa": "ई आँकड़ा आपकी जानकारी खातिर अनुमान हैं। इनका एक सुझाव मानौ अउर आखिरी फैसला आपन अनुभव अउर कृषि विज्ञान केंद्र या कृषि अधिकारी कै सलाह से करौ।"},
    "year_title": {"en": "What do bad year and good year mean?", "hi": "ख़राब साल और अच्छा साल का क्या मतलब है?",
                   "ur": "خراب سال اور اچھا سال کا کیا مطلب ہے؟", "bho": "खराब साल आ बढ़िया साल के का मतलब बा?",
                   "awa": "खराब साल अउर नीक साल कै का मतलब है?"},
    "year_bad": {"en": "The rain is poor, pests attack, or the mandi price falls. Your profit may drop to about this amount.",
                 "hi": "बारिश कम हो, कीट लग जाएँ या मंडी भाव गिर जाए। तब मुनाफ़ा घटकर लगभग इतना रह सकता है।",
                 "ur": "بارش کم ہو، کیڑے لگ جائیں یا منڈی بھاؤ گر جائے۔ تب منافع گھٹ کر تقریباً اتنا رہ سکتا ہے۔",
                 "bho": "बरखा कम होखे, कीड़ा लाग जाव भा मंडी भाव गिर जाव। तब मुनाफा घट के लगभग एतना रह सकेला।",
                 "awa": "बरखा कम होय, कीड़ा लागि जाय या मंडी भाव गिरि जाय। तब मुनाफा घटि कै लगभग एतना रहि सकत है।"},
    "year_good": {"en": "The weather is kind, the crop is healthy and the mandi price is high. Your profit may rise to about this amount.",
                  "hi": "मौसम साथ दे, फसल अच्छी हो और मंडी भाव ऊँचा मिले। तब मुनाफ़ा बढ़कर लगभग इतना हो सकता है।",
                  "ur": "موسم ساتھ دے، فصل اچھی ہو اور منڈی بھاؤ اونچا ملے۔ تب منافع بڑھ کر تقریباً اتنا ہو سکتا ہے۔",
                  "bho": "मौसम साथ देव, फसल बढ़िया होखे आ मंडी भाव ऊँच मिले। तब मुनाफा बढ़ के लगभग एतना हो सकेला।",
                  "awa": "मौसम साथ देय, फसल नीक होय अउर मंडी भाव ऊँच मिलै। तब मुनाफा बढ़ि कै लगभग एतना होइ सकत है।"},
    "year_between": {"en": "Most years (about 8 out of 10) fall between these two. The big number on each card is what to expect in a normal year.",
                     "hi": "ज़्यादातर साल (10 में से लगभग 8) इन दोनों के बीच रहते हैं। हर कार्ड की बड़ी संख्या सामान्य साल का अनुमान है।",
                     "ur": "زیادہ تر سال (10 میں سے تقریباً 8) ان دونوں کے درمیان رہتے ہیں۔ ہر کارڈ کا بڑا عدد عام سال کا اندازہ ہے۔",
                     "bho": "जादातर साल (10 में से लगभग 8) ए दुनो के बीच रहेला। हर कार्ड के बड़का संख्या सामान्य साल के अनुमान बा।",
                     "awa": "जादातर साल (10 मा से लगभग 8) इन दूनौ के बीच रहत हैं। हर कार्ड कै बड़ी संख्या सामान्य साल कै अनुमान है।"},
    "schemes_title": {"en": "Government schemes for farmers", "hi": "किसानों के लिए सरकारी योजनाएँ", "ur": "کسانوں کے لیے سرکاری اسکیمیں"},
    "scheme_more": {"en": "Click to know more", "hi": "और जानने के लिए क्लिक करें", "ur": "مزید جاننے کے لیے کلک کریں"},
    "image_source": {"en": "Image", "hi": "चित्र", "ur": "تصویر"},
    "scheme_benefit": {"en": "What you get", "hi": "आपको क्या मिलता है", "ur": "آپ کو کیا ملتا ہے"},
    "scheme_who": {"en": "Who can apply", "hi": "कौन आवेदन कर सकता है", "ur": "کون درخواست دے سکتا ہے"},
    "scheme_how": {"en": "How to apply", "hi": "आवेदन कैसे करें", "ur": "درخواست کیسے دیں"},
    "scheme_visit": {"en": "Go to the official website", "hi": "आधिकारिक वेबसाइट पर जाएँ", "ur": "سرکاری ویب سائٹ پر جائیں"},
    "scheme_back": {"en": "Back to all schemes", "hi": "सभी योजनाओं पर वापस", "ur": "تمام اسکیموں پر واپس"},
    "schemes_note": {"en": "Amounts and rules change. Always confirm on the official website, and never pay anyone to apply.",
                     "hi": "रक़म और नियम बदलते रहते हैं। हमेशा आधिकारिक वेबसाइट पर पुष्टि करें, और आवेदन के लिए किसी को पैसे न दें।",
                     "ur": "رقم اور قواعد بدلتے رہتے ہیں۔ ہمیشہ سرکاری ویب سائٹ پر تصدیق کریں، اور درخواست کے لیے کسی کو پیسے نہ دیں۔"},
})


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
    """The crop's name in the chosen language; the Hindi name is added where the language is not written in Devanagari."""
    if crop not in CROPS:
        return crop
    name = pick(CROPS[crop], lang)
    return name if lang in ("hi", "bho", "awa") else f"{name} · {CROPS[crop]['hi']}"


def season_name(season: str, lang: str) -> str:
    return pick(SEASONS[season], lang) if season in SEASONS else season


def district_name(district: str, lang: str) -> str:
    title = district.title()
    if lang in ("hi", "bho", "awa") and district in DISTRICTS_HI:
        return f"{DISTRICTS_HI[district]} ({title})"
    return title
