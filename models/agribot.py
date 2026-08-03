


import re

class AgriBot:
    def __init__(self):
        # Intent classification keywords
        self.keywords = {
            "greetings": [
                r"\b(hello|hi|hey|namaste|vanakkam|namaskara|halo|pranam|namaskar|salaam)\b"
            ],
            "disease_id": [
                r"affect.*tomato", r"leaves.*yellow", r"brown.*spots", r"white.*powder", r"black.*spots",
                r"curling", r"dry.*edges", r"fungal.*bacterial", r"virus", r"contagious", r"how.*serious"
            ],
            "disease_symptoms": [
                r"symptom.*early.*blight", r"symptom.*late.*blight", r"sign.*bacterial.*wilt",
                r"powdery.*mildew", r"leaf.*rust", r"root.*rot", r"mosaic.*virus"
            ],
            "disease_treatment": [
                r"treat.*leaf.*spot", r"medicine", r"fungicide", r"pesticide", r"natural.*cure",
                r"how.*often.*spray", r"recovery", r"recover", r"mix.*pesticides"
            ],
            "disease_prevention": [
                r"prevent", r"stop.*spread", r"sanitize.*tools", r"remove.*infected", r"inspect"
            ],
            "crop_info": [
                r"grow.*tomato", r"grow.*rice", r"cultivate.*maize", r"wheat.*farming",
                r"grow.*paddy", r"sandy.*soil.*crop", r"less.*water.*crop", r"summer.*crop", r"best.*crop"
            ],
            "fertilizer": [
                r"fertilizer.*tomato", r"urea", r"organic.*chemical", r"compost",
                r"what.*is.*npk", r"increase.*flowering", r"fruit.*size", r"excess.*fertilizer"
            ],
            "soil": [
                r"test.*soil", r"soil.*ph", r"ph.*rice", r"soil.*fertility",
                r"hard.*soil", r"salinity", r"nutrients.*lacking"
            ],
            "irrigation": [
                r"water.*tomato", r"drip.*irrigation", r"sprinkler", r"overwatering",
                r"water.*maize", r"stop.*irrigation"
            ],
            "pest_control": [
                r"aphid", r"caterpillar", r"insect.*eating", r"pest.*control",
                r"safe.*pesticide", r"whitefl", r"stem.*borer", r"neem.*oil"
            ],
            "weather": [
                r"rain.*spread", r"spray.*before.*rain", r"temperature.*tomato",
                r"humidity", r"drought", r"climate", r"weather",
                r"मौसम|बारिश|तापमान|हवामान|ಮಳೆ|ತಾಪಮಾನ|వాతావరణం|వర్షం|ఉష్ణోగ్రత|வானிலை|மழை|வெப்பநிலை|കാലാവസ്ഥ|ചൂട്|rain|temp|weather|humidity|climate|forecast"
            ],
            "organic_farming": [
                r"start.*organic", r"organic.*fertilizer", r"organic.*pesticide",
                r"compost.*preparation", r"vermicompost", r"cow.*dung", r"biofertilizer", r"green.*manure"
            ],
            "seeds": [
                r"best.*seed", r"hybrid.*local", r"certified", r"seed.*treatment",
                r"germination", r"not.*germinating", r"seed.*storage"
            ],
            "harvesting": [
                r"harvest.*tomato", r"mature.*crop.*sign", r"harvest.*time",
                r"spoilage", r"post-harvest", r"storage.*temp"
            ],
            "nutrition": [
                r"nitrogen.*deficiency", r"potassium.*deficiency", r"magnesium.*deficiency",
                r"calcium.*deficiency", r"zinc.*deficiency", r"micronutrient", r"macronutrient"
            ],
            "fruit_problems": [
                r"fruit.*crack", r"fruit.*drop", r"fruit.*small", r"flower.*drop", r"fruit.*setting", r"ripening"
            ],
            "leaf_problems": [
                r"curling", r"edges.*brown", r"wilting", r"holes.*leaves", r"sticky.*leaves", r"white.*patches", r"purple.*leaves"
            ],
            "best_practices": [
                r"farming.*practice", r"crop.*rotation", r"intercropping", r"mulching", r"weed.*control", r"sustainable", r"precision"
            ],
            "greenhouse": [
                r"greenhouse", r"polyhouse", r"suitable.*greenhouse", r"greenhouse.*temp"
            ],
            "hydroponics": [
                r"hydroponic", r"soilless", r"nutrient.*solution", r"hydroponic.*cost"
            ],
            "schemes": [
                r"scheme", r"subsidy", r"subsidies", r"insurance", r"loan", r"pm.*kisan"
            ],
            "equipment": [
                r"tractor", r"rotavator", r"sprayer", r"power.*tiller", r"drone.*spray", r"seed.*drill"
            ],
            "livestock": [
                r"cow.*feed", r"goat.*farming", r"poultry", r"dairy", r"vaccination"
            ],
            "market": [
                r"profitable.*crop", r"high.*demand", r"export", r"increase.*profit", r"market.*timing", r"storage.*price"
            ],
            "seasonal": [
                r"kharif", r"rabi", r"zaid", r"summer.*crop", r"monsoon.*crop", r"winter.*crop", r"crop.*calendar"
            ],
            "safety": [
                r"safety", r"pesticide.*safe", r"harvest.*after.*spray", r"protective.*gear", r"first.*aid", r"safe.*storage"
            ],
            "follow_up": [
                r"why.*disease", r"severity", r"spread.*other.*plants", r"dangerous",
                r"what.*do.*first", r"eat.*fruit", r"come.*back", r"isolate.*plant"
            ],
            "general": [
                r"integrated.*farming", r"ipm", r"manure.*fertilizer", r"fungicide.*pesticide", r"insecticide.*herbicide"
            ]
        }

        # Comprehensive response database
        self.responses = {
            "en": {
                "greetings": "Hello! I am AgriBot, your personal virtual Agronomist. I can guide you on crop cultivation (Tomato, Chilli, Paddy, Mango, Coconut, etc.), soil testing, NPK calculations, organic farming, disease treatments, and government schemes. How can I help you today?",
                "disease_id": "🌱 **Disease Identification Guide**:\n- **Yellow leaves**: Usually indicates Nitrogen deficiency or waterlogging. If yellowing shows wavy margins, it could be a bacterial blight.\n- **Brown/Black spots**: Typical of fungal spots (like Early Blight in Tomato or Anthracnose in Mango).\n- **White powdery patches**: Powdery Mildew, common during warm, humid days.\n- **Leaf curling**: Usually viral, carried by whiteflies or thrips. Spray Neem oil (2%) or Imidacloprid (0.5ml/L) to control the insect vector.\n- Upload a picture in our **Leaf Scanner** page for a detailed OpenCV pixel analysis!",
                "disease_symptoms": "🔬 **Common Disease Symptoms**:\n1. **Early Blight**: Target-like brown concentric rings on older lower leaves first.\n2. **Bacterial Wilt**: Leaves wilt and droop rapidly while remaining green. Stems exude a milky white slime when cut and placed in water.\n3. **Powdery Mildew**: Superficial white-to-grey powdery fungal sheets on leaf tops, flowers, and tender shoots.\n4. **Mosaic Virus**: Mottled yellow-and-green mosaic patches, crinkling, and stunted dwarf stems.",
                "disease_treatment": "🧪 **Crop Disease Treatments**:\n- **Fungal spots (Blight/Mildew)**: Spray Mancozeb (2g/L), Hexaconazole (1ml/L), or Copper Oxychloride (3g/L).\n- **Bacterial infections**: Spray Streptocycline (0.1g/L) mixed with Copper Oxychloride (2g/L).\n- **Organic treatment**: Spray Neem Seed Kernel Extract (NSKE 5%) or dilute milk whey. Prune leaves within 30cm of soil to reduce humidity.\n- **Recovery**: Infected leaves won't turn green again, but new shoots will recover in 7-14 days after proper spray.",
                "disease_prevention": "🛡️ **Disease Prevention & Sanitization**:\n1. **Pruning**: Prune lower diseased foliage to prevent soil splash infections.\n2. **Sanitize Tools**: Wipe secateurs and sickles with 70% isopropyl alcohol or bleach solution between plants.\n3. **Crop Inspection**: Inspect crops twice a week, paying close attention to lower leaf bases.\n4. **Removal**: Immediately rogue out and burn virus-infected plants to prevent vector transmission.",
                "crop_info": "🌾 **Crop Cultivation Insights**:\n- **Tomato**: Best grown in well-drained loamy soils (pH 6.0-6.8). Takes 110-140 days. Avoid waterlogging.\n- **Paddy/Rice**: Requires clayey/loamy soil. Needs abundant water. Grows in 120-150 days. Ideal pH is 5.5-6.5.\n- **Maize/Corn**: Requires sandy loam or loamy soil. Sensitive to waterlogging. Needs 90-120 days.\n- **Wheat**: Rabi winter crop. Requires cool climate and loam soils.\n- **Sandy soils**: Suitable for tuber crops, melons, cashew, and coconut if irrigated.",
                "fertilizer": "🧪 **Fertilizer & NPK Application**:\n- **NPK**: Nitrogen (N) for green leafy growth; Phosphorus (P) for root and flower setting; Potassium (K) for fruit size, weight, and disease resistance.\n- **Urea (46% N)**: Apply in splits (basal, tillering, flowering). Avoid applying Urea during active disease outbreaks as soft vegetative growth attracts pests.\n- **Organic Compost**: Apply decomposed farmyard manure (FYM) to improve soil structure and water-holding capacity.\n- **Excess Fertilizer**: Causes leaf burn, salt accumulation, and weak stems. Always irrigate immediately after applying chemical fertilizers.",
                "soil": "🪵 **Soil Management & Testing**:\n- **Soil Test**: Collect soil in a V-shape up to 15cm depth from 5-10 different points in your field, mix them, discard half until 500g remains, and send to a lab.\n- **Soil pH**: Ideal pH for most crops is 6.0-7.0. For paddy, 5.5-6.5. \n- **Acidic Soils**: Add Agricultural Lime or Dolomite to raise pH.\n- **Saline/Salty Soils**: Apply Gypsum (Calcium Sulfate), flush fields with clean water, and grow green manures.",
                "irrigation": "💧 **Water & Irrigation Guide**:\n- **Tomatoes**: Drip irrigation is best (2-3 liters/day per plant). Avoid overhead sprinklers which keep leaves wet and spread fungal spores.\n- **Drip Irrigation**: Saves up to 60% water, delivers water directly to roots, and prevents weed growth.\n- **Overwatering**: Leads to root rot (damping-off) due to lack of oxygen in root zones.\n- **Pre-Harvest Dry Period**: Stop irrigation 10-14 days before harvest for Paddy and Onions to improve shelf-life and drying.",
                "pest_control": "🐛 **Pest Control Methods**:\n- **Aphids/Thrips**: Spray soapy water or Neem Oil (2% with emulsifier). For chemical control, spray Imidacloprid (0.5ml/L).\n- **Caterpillars**: Spray Bacillus thuringiensis (Bt) formulation (2g/L) or spinosad.\n- **Whiteflies**: Hang Yellow Sticky Traps at crop canopy levels to capture them. Spray Acetamiprid.\n- **Stem Borer**: Apply Carbofuran granules in soil or spray Chlorantraniliprole.",
                "weather": "🌦️ **Weather-Aware Agriculture**:\n- **Rain Spills**: Heavy rains splash fungal spores from soil onto crop leaves, spreading diseases. Avoid spraying pesticides if rain is expected within 3 hours.\n- **Humidity**: Relative humidity >80% encourages fungal spore germination. Increase crop spacing to improve aeration.\n- **Drought Crops**: Millets, Sorghum, Cowpea, and Cashew survive water stress well.",
                "organic_farming": "🌿 **Organic Farming & Compost**:\n- **Compost**: Layer dry brown leaves (carbon) and green waste/cow dung (nitrogen), keep moist (50% moisture), and turn every 15 days.\n- **Vermicompost**: Uses earthworms to digest organic waste, yielding nutrient-rich castings.\n- **Cow Dung**: Enriches soil microbiology and adds organic carbon.\n- **Biofertilizers**: Azotobacter (fixes nitrogen) and PSB (Phosphorus Solubilizing Bacteria).",
                "seeds": "🌱 **Seed Treatment & Germination**:\n- **Seed Treatment**: Treat seeds with Trichoderma viride (4g/kg) or Carbendazim (2g/kg) before sowing to prevent root rot.\n- **Germination Failures**: Caused by sowing seeds too deep (>2cm), waterlogged soil (suffocates seeds), or dry soil.\n- **Hybrid vs Local**: Hybrid seeds offer higher yields but cannot be re-saved for next season; local seeds are resilient and free.",
                "harvesting": "🧺 **Harvesting & Post-Harvest Storage**:\n- **Tomatoes**: Harvest at 'breaker stage' (pinkish-yellow) for long-distance transport, or fully red for local sale.\n- **Paddy**: Harvest when 80% of panicles turn golden brown and grain moisture is around 20%.\n- **Grain Storage**: Dry grains under sun until moisture is below 14% to prevent storage mold and weevils.",
                "nutrition": "🍂 **Plant Deficiencies & Nutrition**:\n- **Nitrogen (N)**: Older lower leaves turn uniform pale yellow. Stunted growth.\n- **Potassium (K)**: Leaf margins look scorched/brown (marginal necrosis), weak stems.\n- **Magnesium (Mg)**: Interveinal chlorosis (leaves turn yellow between veins, veins remain green) on older leaves.\n- **Calcium (Ca)**: Blossom-end rot in tomatoes (black leathery bottom on fruits). Apply Calcium Nitrate.",
                "fruit_problems": "🍅 **Fruit & Flower Problems**:\n- **Tomato Cracking**: Caused by irregular watering (heavy rains/watering after a dry spell). Keep soil moisture consistent.\n- **Fruit/Flower Dropping**: Caused by high temperatures (above 35°C), nitrogen overdose, or moisture stress.\n- **Poor Fruit Setting**: Lack of pollinators. Shake tomato plants gently in midday to assist self-pollination.",
                "leaf_problems": "🍃 **Leaf Anomalies**:\n- **Curling Upward**: Virus (carried by whiteflies) or thrips feeding. \n- **Holes in Leaves**: Chewing pests (caterpillars/beetles). Spray Bt or Neem Seed Kernel Extract.\n- **Sticky Leaves**: Caused by honeydew excreted by aphids or mealybugs. Spray water jets followed by Neem oil.",
                "best_practices": "🚜 **Sustainable Farming Best Practices**:\n- **Crop Rotation**: Alternate cereals (like paddy) with legumes (like cowpea) to rebuild soil nitrogen.\n- **Mulching**: Cover soil with straw or plastic sheet to retain moisture, suppress weed growth, and regulate temperature.\n- **Intercropping**: Grow companion crops (e.g. Marigolds in Tomatoes) to naturally repel nematodes and pests.",
                "greenhouse": "🏠 **Greenhouse & Polyhouse Cultivation**:\n- Controlled environmental agriculture allows off-season cultivation of high-value crops (bell peppers, dutch roses, cucumbers).\n- **Advantages**: Protects from pests, heavy rains, and scorching sun. Saves water.\n- **Crops**: Exotic vegetables and floriculture.",
                "hydroponics": "💧 **Hydroponics (Soilless Farming)**:\n- **What it is**: Growing plants in water containing dissolved mineral nutrient solutions (using media like coco-peat or clay balls).\n- **Advantages**: 90% water saving, faster growth, zero soil-borne diseases, vertical stacking.\n- **Suitable crops**: Lettuce, spinach, strawberries, herbs, and tomatoes.",
                "schemes": "🏛️ **Government Subsidies & Schemes**:\n- **PM-Kisan**: Income support of ₹6,000/year to farmer families in three installments.\n- **Drip Irrigation Subsidy**: PMKSY scheme provides 50% to 90% subsidy depending on farmer category.\n- **Crop Insurance**: PM Fasal Bima Yojana offers low premium insurance against weather disasters.",
                "equipment": "⚙️ **Agricultural Machinery**:\n- **Rotavator**: Used for seedbed preparation by breaking soil clods.\n- **Seed Drill**: Sows seeds at uniform depth and spacing, saving labor.\n- **Drone Spraying**: Highly efficient pesticide spraying, reduces chemical contact and saves 90% water compared to manual pumps.",
                "livestock": "🐄 **Livestock & Dairy Management**:\n- **Cow Feed**: Balanced ration should include green fodder (napier grass/maize), dry fodder (paddy straw), and concentrate feed.\n- **Vaccinations**: FMD (Foot and Mouth Disease) vaccine should be given twice a year. Deworm animals regularly.\n- **Dairy/Poultry**: Ensure cross-ventilation, dry bedding, and clean drinking water.",
                "market": "📈 **Market Profitability & Timing**:\n- **High-Demand Crops**: Broccoli, color bell peppers, baby corn, ginger, garlic, papaya, and dragonfruit.\n- **Better Prices**: Avoid selling immediately at harvest peak when market is flooded. Dry and store grains in warehouses, or utilize cold storage for onions/potatoes.",
                "seasonal": "📅 **Indian Crop Seasons**:\n- **Kharif (Monsoon: June-Oct)**: Rice, Maize, Cotton, Soybeans, Tur.\n- **Rabi (Winter: Nov-April)**: Wheat, Mustard, Barley, Chickpea.\n- **Zaid (Summer: March-June)**: Watermelon, Cucumber, Bitter gourd, Moong.",
                "safety": "🦺 **Pesticide Safety & Pre-Harvest Intervals (PHI)**:\n- **Safety**: Wear mask, gloves, and protective clothing. Never spray against the wind.\n- **Pre-Harvest Interval (PHI)**: The mandatory waiting period between pesticide spray and harvest (usually 7 to 14 days) to ensure safe pesticide residues.\n- **First Aid**: In case of skin contact, wash immediately with plenty of soap and running water.",
                "follow_up": "⚠️ **Leaf Diagnosis Follow-up Actions**:\n1. **Isolation**: If leaf scanner detects viral leaf curl or systemic wilt, isolate or rogue out the plant immediately.\n2. **Pruning**: Cut away heavily spotted leaves to stop spores from splashing onto healthy foliage.\n3. **Application**: Apply the recommended organic or chemical treatment promptly. Fungal spots spread exponentially during wet weather.",
                "general": "📚 **Agricultural Terminology**:\n- **IPM (Integrated Pest Management)**: Combining biological, cultural, mechanical, and chemical tools to manage pests below damage threshold.\n- **Manure vs Fertilizer**: Manure is organic and improves soil health; chemical fertilizers are inorganic concentrates supplying specific NPK elements."
            },
            "kn": {
                "greetings": "ನಮಸ್ಕಾರ! ನಾನು ಅಗ್ರಿಬಾಟ್, ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಕೃಷಿ ಸಲಹೆಗಾರ. ಬೆಳೆ ಬೇಸಾಯ (ಟೊಮೇಟೊ, ಮೆಣಸಿನಕಾಯಿ, ಭತ್ತ, ಮಾವು, ತೆಂಗು ಇತ್ಯಾದಿ), ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ, NPK ಲೆಕ್ಕಾಚಾರ, ಸಾವಯವ ಕೃಷಿ, ರೋಗ ತಡೆಗಟ್ಟುವಿಕೆ ಮತ್ತು ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ನಾನು ಮಾಹಿತಿ ನೀಡಬಲ್ಲೆ. ಇಂದು ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ?",
                "disease_id": "🌱 **ರೋಗ ಪತ್ತೆ ಮಾಹಿತಿ**:\n- **ಎಲೆಗಳು ಹಳದಿಯಾಗುವುದು**: ಸಾರಜನಕದ (Nitrogen) ಕೊರತೆ ಅಥವಾ ನೀರು ನಿಲ್ಲುವುದರಿಂದ ಆಗುತ್ತದೆ.\n- **ಕಂದು/ಕಪ್ಪು ಕಲೆಗಳು**: ಸಾಮಾನ್ಯವಾಗಿ ಶಿಲೀಂಧ್ರ ರೋಗ (ಟೊಮೇಟೊದಲ್ಲಿ ಅರ್ಲಿ ಬ್ಲೈಟ್ ಅಥವಾ ಮಾವಿನಲ್ಲಿ ಆಂಥ್ರಾಕ್ನೋಸ್).\n- **ಬಿಳಿ ಪುಡಿ ಕಲೆಗಳು**: ಬೂದಿ ರೋಗ (Powdery Mildew).\n- **ಎಲೆ ಮುದುಡುವುದು**: ವೈರಸ್ ರೋಗ. ಬಿಳಿ ನೊಣ ಅಥವಾ ನುಸಿಗಳಿಂದ ಹರಡುತ್ತದೆ. ಎಲೆ ಸ್ಕ್ಯಾನರ್ ಪುಟದಲ್ಲಿ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ ವಿಶ್ಲೇಷಿಸಿ!",
                "disease_symptoms": "🔬 **ಪ್ರಮುಖ ರೋಗ ಲಕ್ಷಣಗಳು**:\n1. **ಅರ್ಲಿ ಬ್ಲೈಟ್**: ಕೆಳಗಿನ ಹಳೆಯ ಎಲೆಗಳ ಮೇಲೆ ಕಂದು ಬಣ್ಣದ ವೃತ್ತಾಕಾರದ ಕಲೆಗಳು ಕಾಣಿಸಿಕೊಳ್ಳುತ್ತವೆ.\n2. **ಬ್ಯಾಕ್ಟೀರಿಯಾ ಒಣಗು ರೋಗ**: ಗಿಡ ಹಸಿರಾಗಿದ್ದಾಗಲೇ ಬೇಗನೆ ಒಣಗುತ್ತದೆ.\n3. **ಬೂದಿ ರೋಗ**: ಎಲೆ ಮತ್ತು ಚಿಗುರುಗಳ ಮೇಲೆ ಬಿಳಿ ಬಣ್ಣದ ಪುಡಿ ಹರಡಿಕೊಳ್ಳುತ್ತದೆ.\n4. **ಮೊಸಾಯಿಕ್ ವೈರಸ್**: ಎಲೆಗಳು ಹಸಿರು ಮತ್ತು ಹಳದಿ ಬಣ್ಣದ ಕಲೆಗಳೊಂದಿಗೆ ಮುದುಡಿಕೊಳ್ಳುತ್ತವೆ.",
                "disease_treatment": "🧪 **ರೋಗಗಳಿಗೆ ಚಿಕಿತ್ಸೆಗಳು**:\n- **ಶಿಲೀಂಧ್ರ ರೋಗಗಳು**: ಮ್ಯಾಂಕೋಜೆಬ್ (2 ಗ್ರಾಂ/ಲೀ) ಅಥವಾ ಹೆಕ್ಸಾಕೊನಜೋಲ್ (1 ಮಿಲಿ/ಲೀ) ಸಿಂಪಡಿಸಿ.\n- **ಬ್ಯಾಕ್ಟೀರಿಯಾ ರೋಗಗಳು**: ಸ್ಟ್ರೆಪ್ಟೋಸೈಕ್ಲಿನ್ (0.1 ಗ್ರಾಂ/ಲೀ) ಜೊತೆಗೆ ತಾಮ್ರದ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ (2 ಗ್ರಾಂ/ಲೀ) ಮಿಶ್ರಣ ಮಾಡಿ ಸಿಂಪಡಿಸಿ.\n- **ಸಾವಯವ ಚಿಕಿತ್ಸೆ**: ಶೇ. 5 ರಷ್ಟು ಬೇವಿನ ಹಿಂಡಿ ಕಷಾಯ ಅಥವಾ ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಿಸಿ.",
                "disease_prevention": "🛡️ **ರೋಗ ತಡೆಗಟ್ಟುವಿಕೆ**:\n1. ರೋಗ ಪೀಡಿತ ಕೆಳಗಿನ ಎಲೆಗಳನ್ನು ಕತ್ತರಿಸಿ ತೆಗೆಯಿರಿ.\n2. ಕೃಷಿ ಉಪಕರಣಗಳನ್ನು ಶೇ. 70 ರಷ್ಟು ಆಲ್ಕೋಹಾಲ್ ಅಥವಾ ಬ್ಲೀಚಿಂಗ್ ದ್ರಾವಣದಿಂದ ಸ್ವಚ್ಛಗೊಳಿಸಿ.\n3. ವೈರಸ್ ಪೀಡಿತ ಗಿಡಗಳನ್ನು ಬೇರು ಸಮೇತ ಕಿತ್ತು ಸುಟ್ಟು ಹಾಕಿ.",
                "crop_info": "🌾 **ಬೆಳೆ ಮಾಹಿತಿ**:\n- **ಟೊಮೇಟೊ**: ಮರಳು ಮಿಶ್ರಿತ ಜೇಡಿಮಣ್ಣು ಉತ್ತಮ. ಬೆಳೆಯ ಅವಧಿ 110-140 ದಿನಗಳು.\n- **ಭತ್ತ**: ಜೇಡಿಮಣ್ಣು ಸೂಕ್ತ. ಹೆಚ್ಚು ನೀರು ಬೇಕು. ಅವಧಿ 120-150 ದಿನಗಳು.\n- **ಮೆಕ್ಕೆಜೋಳ**: ನೀರು ಸುಲಭವಾಗಿ ಬಸಿದುಹೋಗುವ ಮಣ್ಣು ಬೇಕು. ಅವಧಿ 90-120 ದಿನಗಳು.",
                "fertilizer": "🧪 **ರಸಗೊಬ್ಬರ ಮತ್ತು NPK ಮಾಹಿತಿ**:\n- **NPK**: ಸಾರಜನಕ (N) ಹಸಿರು ಬೆಳವಣಿಗೆಗೆ, ರಂಜಕ (P) ಬೇರು ಮತ್ತು ಹೂಬಿಡಲು, ಪೊಟ್ಯಾಷಿಯಂ (K) ಹಣ್ಣಿನ ಗಾತ್ರ ಮತ್ತು ರೋಗ ನಿರೋಧಕ ಶಕ್ತಿಗಾಗಿ.\n- **ಯೂರಿಯಾ**: ಕಂತುಗಳಲ್ಲಿ ನೀಡಿ. ರೋಗ ಬಂದಾಗ ಯೂರಿಯಾ ಬಳಕೆ ಕಡಿಮೆ ಮಾಡಿ.",
                "soil": "🪵 **ಮಣ್ಣು ಮತ್ತು ಫಲವತ್ತತೆ**:\n- **ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ**: ಹೊಲದ ಬೇರೆ ಬೇರೆ ಭಾಗಗಳಿಂದ 15 ಸೆಂ.ಮೀ ಆಳದ ಮಣ್ಣು ಸಂಗ್ರಹಿಸಿ ಪರೀಕ್ಷಾ ಕೇಂದ್ರಕ್ಕೆ ಕಳುಹಿಸಿ.\n- **ಆಮ್ಲೀಯ ಮಣ್ಣು**: ಮಣ್ಣಿಗೆ ಸುಣ್ಣ (Lime) ಅಥವಾ ಡಾಲಮೈಟ್ ಸೇರಿಸಿ pH ಮಟ್ಟವನ್ನು ಸುಧಾರಿಸಿ.",
                "irrigation": "💧 **ನೀರಾವರಿ ಗೈಡ್**:\n- **ಹನಿ ನೀರಾವರಿ (Drip)**: ಶೇ. 60 ರಷ್ಟು ನೀರನ್ನು ಉಳಿಸುತ್ತದೆ. ನೇರವಾಗಿ ಬೇರುಗಳಿಗೆ ನೀರು ತಲುಪಿಸುತ್ತದೆ.\n- **ಹೆಚ್ಚು ನೀರು ಹಾಯಿಸುವುದು**: ಬೇರು ಕೊಳೆಯುವಿಕೆಗೆ ಕಾರಣವಾಗುತ್ತದೆ.",
                "pest_control": "🐛 **ಕೀಟ ನಿಯಂತ್ರಣ**:\n- **ನುಸಿ/ಗಿಡಹೇನು**: ಬೇವಿನ ಎಣ್ಣೆ (2%) ಸಿಂಪಡಿಸಿ. ಅಥವಾ ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ (0.5 ಮಿಲಿ/ಲೀ) ಬಳಸಿ.\n- **ಕಾಂಡ ಕೊರಕ**: ಕಾರ್ಬೋಫ್ಯುರಾನ್ ಹರಳುಗಳನ್ನು ಮಣ್ಣಿಗೆ ಸೇರಿಸಿ.",
                "weather": "🌦️ **ಹವಾಮಾನ ಮತ್ತು ಕೃಷಿ**:\n- ಮಳೆ ಬರುವ ಮುನ್ಸೂಚನೆ ಇದ್ದರೆ ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಬೇಡಿ.\n- ಗಾಳಿಯಲ್ಲಿ ತೇವಾಂಶ ಹೆಚ್ಚಿದ್ದಾಗ ಶಿಲೀಂಧ್ರ ರೋಗಗಳು ವೇಗವಾಗಿ ಹರಡುತ್ತವೆ.",
                "organic_farming": "🌿 **ಸಾವಯವ ಕೃಷಿ**:\n- ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ, ಕಾಂಪೋಸ್ಟ್, ಎರೆಹುಳು ಗೊಬ್ಬರ (Vermicompost) ಬಳಸಿ ಮಣ್ಣಿನ ಫಲವತ್ತತೆ ಹೆಚ್ಚಿಸಿ.\n- ಜೈವಿಕ ಗೊಬ್ಬರಗಳಾದ ಅಜೋಟೋಬ್ಯಾಕ್ಟರ್ ಮತ್ತು ಪಿ.ಎಸ್.ಬಿ ಬಳಸಿ.",
                "seeds": "🌱 **ಬೀಜೋಪಚಾರ**:\n- ಬಿತ್ತುವ ಮುನ್ನ ಬೀಜಗಳಿಗೆ ಟ್ರೈಕೋಡರ್ಮಾ ಬಿಳಿ ಅಥವಾ ಕಾರ್ಬೆಂಡಾಜಿಮ್ ಹಚ್ಚಿ ಉಪಚರಿಸಿ.\n- ಹೈಬ್ರಿಡ್ ಬೀಜಗಳು ಹೆಚ್ಚು ಇಳುವರಿ ನೀಡುತ್ತವೆ ಆದರೆ ಇವುಗಳನ್ನು ಮುಂದಿನ ವರ್ಷ ಬಿತ್ತನೆಗೆ ಬಳಸಲು ಬರುವುದಿಲ್ಲ.",
                "harvesting": "🧺 **ಕಟಾವು ಮತ್ತು ಶೇಖರಣೆ**:\n- ಭತ್ತವನ್ನು ತೆನೆಗಳು ಶೇ. 80 ರಷ್ಟು ಬಂಗಾರದ ಬಣ್ಣಕ್ಕೆ ತಿರುಗಿದಾಗ ಕಟಾವು ಮಾಡಿ.\n- ಧಾನ್ಯಗಳನ್ನು ಶೇಖರಿಸುವ ಮುನ್ನ ತೇವಾಂಶ ಶೇ. 14 ಕ್ಕಿಂತ ಕಡಿಮೆ ಇರುವಂತೆ ಬಿಸಿಲಿನಲ್ಲಿ ಒಣಗಿಸಿ.",
                "nutrition": "🍂 **ಪೋಷಕಾಂಶಗಳ ಕೊರತೆ ಲಕ್ಷಣಗಳು**:\n- **ಸಾರಜನಕ ಕೊರತೆ**: ಕೆಳಗಿನ ಹಳೆಯ ಎಲೆಗಳು ಹಳದಿಯಾಗುತ್ತವೆ.\n- **ಪೊಟ್ಯಾಷಿಯಂ ಕೊರತೆ**: ಎಲೆಯ ಅಂಚುಗಳು ಕಂದು ಬಣ್ಣಕ್ಕೆ ತಿರುಗಿ ಒಣಗಿದಂತೆ ಕಾಣುತ್ತವೆ.",
                "fruit_problems": "🍅 **ಹಣ್ಣು ಮತ್ತು ಹೂವಿನ ಸಮಸ್ಯೆಗಳು**:\n- **ಟೊಮೇಟೊ ಹಣ್ಣು ಬಿರುಕು ಬಿಡುವುದು**: ಮಣ್ಣಿನ ತೇವಾಂಶದಲ್ಲಿ ಏರುಪೇರಾಗುವುದರಿಂದ ಆಗುತ್ತದೆ. ನಿಯಮಿತ ನೀರು ನೀಡಿ.\n- **ಹೂವು ಉದುರುವುದು**: ಅತಿಯಾದ ತಾಪಮಾನ ಅಥವಾ ನೀರಿನ ಕೊರತೆಯಿಂದ ಆಗುತ್ತದೆ.",
                "leaf_problems": "🍃 **ಎಲೆಯ ಸಮಸ್ಯೆಗಳು**:\n- ಎಲೆಗಳ ಮೇಲೆ ರಂಧ್ರಗಳಿದ್ದರೆ ಕೀಟಗಳು ತಿನ್ನುತ್ತಿವೆ ಎಂದರ್ಥ. ಬೇವಿನ ಎಣ್ಣೆ ಅಥವಾ ಬಿಟಿ ಸಿಂಪಡಿಸಿ.",
                "best_practices": "🚜 **ಉತ್ತಮ ಕೃಷಿ ಪದ್ಧತಿಗಳು**:\n- **ಬೆಳೆ ಸರದ ಬದಲಾವಣೆ (Crop Rotation)**: ಮಣ್ಣಿನ ನೈಸರ್ಗಿಕ ಶಕ್ತಿ ಉಳಿಸಲು ಪ್ರತಿ ವರ್ಷ ಬೇರೆ ಬೆಳೆ ಬೆಳೆಯಿರಿ.\n- **ಹೊದಿಕೆ ಹಾಕುವಿಕೆ (Mulching)**: ಮಣ್ಣಿನಲ್ಲಿ ತೇವಾಂಶ ಕಾಪಾಡಲು ಪ್ಲಾಸ್ಟಿಕ್ ಅಥವಾ ಒಣ ಹುಲ್ಲಿನ ಹೊದಿಕೆ ಬಳಸಿ.",
                "greenhouse": "🏠 **ಹಸಿರುಮನೆ ಕೃಷಿ**: ತಾಪಮಾನ ನಿಯಂತ್ರಿಸಿ ಆಫ್-ಸೀಸನ್ ಬೆಳೆಗಳನ್ನು ಬೆಳೆಯಲು ಸಹಕಾರಿ.",
                "hydroponics": "💧 **ಹೈಡ್ರೋಪೋನಿಕ್ಸ್**: ಮಣ್ಣಿಲ್ಲದೆ ಕೇವಲ ಪೋಷಕಾಂಶಯುಕ್ತ ನೀರಿನ ಸಹಾಯದಿಂದ ಬೆಳೆ ಬೆಳೆಯುವ ತಂತ್ರಜ್ಞಾನ.",
                "schemes": "🏛️ **ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು**:\n- **ಪಿಎಂ-ಕಿಸಾನ್**: ರೈತರಿಗೆ ವಾರ್ಷಿಕ ₹6,000 ಧನಸಹಾಯ.\n- **ಹನಿ ನೀರಾವರಿ ಸಹಾಯಧನ**: ಸಣ್ಣ ಮತ್ತು ಅತಿಸಣ್ಣ ರೈತರಿಗೆ ಶೇ. 90 ರವರೆಗೆ ಸಬ್ಸಿಡಿ ದೊರೆಯುತ್ತದೆ.",
                "equipment": "⚙️ **ಕೃಷಿ ಉಪಕರಣಗಳು**: ಡ್ರೋನ್ ಸಿಂಪಡಣೆಯು ಕೀಟನಾಶಕಗಳ ಬಳಕೆಯನ್ನು ಕಡಿಮೆ ಮಾಡುತ್ತದೆ ಮತ್ತು ಸಮಯ ಉಳಿಸುತ್ತದೆ.",
                "livestock": "🐄 **ಪಶುಸಂಗೋಪನೆ**: ಹಸುಗಳಿಗೆ ಹಸಿರು ಮೇವು ಮತ್ತು ಹಿಂಡಿ ನೀಡಿ. ವರ್ಷಕ್ಕೆ ಎರಡು ಬಾರಿ ಕಾಲುಬಾಯಿ ಜ್ವರಕ್ಕೆ ಲಸಿಕೆ ಹಾಕಿಸಿ.",
                "market": "📈 **ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿ**: ಸುಗ್ಗಿ ಕಾಲದಲ್ಲಿ ಬೆಲೆ ಕಡಿಮೆಯಿದ್ದಾಗ ಧಾನ್ಯಗಳನ್ನು ಗೋದಾಮಿನಲ್ಲಿ ಸಂಗ್ರಹಿಸಿಟ್ಟು ನಂತರ ಮಾರಾಟ ಮಾಡಿ.",
                "seasonal": "📅 **ಬೆಳೆ ಹಂಗಾಮುಗಳು**: ಮುಂಗಾರು (ಖಾರಿಫ್ - ಜೂನ್‌ನಿಂದ ಅಕ್ಟೋಬರ್), ಹಿಂಗಾರು (ರಬಿ - ನವೆಂಬರ್‌ನಿಂದ ಏಪ್ರಿಲ್), ಬೇಸಿಗೆ (ಜೈದ್).",
                "safety": "🦺 **ಸುರಕ್ಷತೆ**: ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸುವಾಗ ಮಾಸ್ಕ್ ಮತ್ತು ಕೈಗವಸುಗಳನ್ನು ಧರಿಸಿ. ಮಕ್ಕಳಿಂದ ದೂರವಿಡಿ.",
                "follow_up": "⚠️ **ರೋಗ ಪತ್ತೆಯ ನಂತರದ ಕ್ರಮಗಳು**: ರೋಗ ತೀವ್ರವಾಗಿದ್ದರೆ ಗಿಡವನ್ನು ತಕ್ಷಣ ಪ್ರತ್ಯೇಕಿಸಿ ಶಿಫಾರಸು ಮಾಡಿದ ಔಷಧಿ ಸಿಂಪಡಿಸಿ.",
                "general": "📚 **ಸಾಮಾನ್ಯ ಕೃಷಿ ಪ್ರಶ್ನೆಗಳು**: ಸಾವಯವ ಗೊಬ್ಬರಗಳು ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಸುಧಾರಿಸುತ್ತವೆ, ರಾಸಾಯನಿಕ ಗೊಬ್ಬರಗಳು ಕೇವಲ ಗಿಡಗಳಿಗೆ ಆಹಾರ ನೀಡುತ್ತವೆ."
            },
            "ml": {
                "greetings": "നമസ്കാരം! ഞാൻ അഗ്രിബോട്ട് ആണ്, നിങ്ങളുടെ കൃഷി സഹായി. വിവിധ വിളകൾ (തക്കാളി, മുളക്, നെല്ല്, മാവ്, തെങ്ങ്), വളപ്രയോഗം, രോഗനിർണ്ണയം, കീടനিয়ന്ത്രണം, സർക്കാർ ആനുകൂല്യങ്ങൾ എന്നിവയെക്കുറിച്ച് ഞാൻ പറഞ്ഞുതരാം. ഇന്ന് ഞാൻ നിങ്ങൾക്ക് എങ്ങനെയാണ് സഹായിക്കേണ്ടത്?",
                "disease_id": "🌱 **രോഗനിർണ്ണയ വിവരങ്ങൾ**:\n- **ഇലകൾ മഞ്ഞളിക്കുന്നത്**: നൈട്രജന്റെ കുറവ് അല്ലെങ്കിൽ വെള്ളക്കെട്ട് കാരണം സംഭവിക്കുന്നു.\n- **തവിട്ട്/കറുപ്പ് പാടുകൾ**: കുമിൾ രോഗലക്ഷണങ്ങൾ (തക്കാളിയിലെ കരിച്ചിൽ, മാവിലെ കൊളരോഗം).\n- **ഇല ചുരുളൽ**: വൈറസ് രോഗം (വെള്ളീച്ച പരത്തുന്നത്). ഇല സ്കാനർ ഉപയോഗിച്ച് ഫോട്ടോ അപ്‌ലോഡ് ചെയ്ത് പരിശോധിക്കൂ!",
                "disease_symptoms": "🔬 **പ്രധാന രോഗലക്ഷണങ്ങൾ**:\n1. **അർലി ബ്ലൈറ്റ്**: താഴത്തെ പഴയ ഇലകളിൽ തവിട്ടുനിറത്തിലുള്ള വളയങ്ങൾ കാണുന്നു.\n2. **ബാക്ടീരിയൽ വാട്ടം**: ചെടി പെട്ടെന്ന് വാടിപ്പോകും.\n3. **പൗഡറി മിൽഡ്യൂ**: ഇലകളിൽ വെളുത്ത പൊടി പറ്റിപ്പിടിച്ചതുപോലെ കാണപ്പെടുന്നു.",
                "disease_treatment": "🧪 **രോഗചികിത്സാ രീതികൾ**:\n- **കുമിൾ രോഗങ്ങൾക്ക്**: മാങ്കോസെബ് (2g/L) അല്ലെങ്കിൽ ഹെക്സാകൊണസോൾ (1ml/L) തളിക്കുക.\n- **ബാക്ടീരിയൽ രോഗങ്ങൾക്ക്**: സ്ട്രെപ്റ്റോസൈക്ലിൻ (0.1g/L) പച്ചക്കറികളിൽ പ്രയോഗിക്കുക.\n- **جൈവരീതി**: 2% വേപ്പെണ്ണ-വെളുത്തുള്ളി മിശ്രിതം തളിക്കുക.",
                "disease_prevention": "🛡️ **രോഗപ്രതിരോധം**:\n1. രോഗം ബാധിച്ച താഴത്തെ ഇലകൾ മുറിച്ചു മാറ്റുക.\n2. കർഷക ഉപകരണങ്ങൾ അണുമുക്തമാക്കുക.\n3. virus ബാധിച്ച ചെടികൾ വേരോടെ പിഴുതു മാറ്റുക.",
                "crop_info": "🌾 **വിള വിവരങ്ങൾ**:\n- **തക്കാളി**: നല്ല നീർവാർച്ചയുള്ള മണ്ണ് വേണം. വിളവെടുപ്പ് സമയം 110-140 ദിവസങ്ങൾ.\n- **நெല്**: കളിമണ്ണും ധാരാളം വെള്ളവും വേണം. വിളവെടുപ്പ് സമയം 120-150 ദിവസങ്ങൾ.\n- **ചോളം**: വെള്ളക്കെട്ടില്ലാത്ത മണ്ണ് ആവശ്യമാണ്.",
                "fertilizer": "🧪 **വളപ്രയോഗവും NPK യും**:\n- **NPK**: നൈട്രജൻ (N) ഇലകളുടെ വളർച്ചയ്ക്ക്, ഫോസ്ഫറസ് (P) വേരുകൾക്കും പൂക്കൾക്കും, പൊട്ടാസ്യം (K) രോഗപ്രതിരോധത്തിനും കായഫലത്തിനും.\n- **യൂറിയ**: ഘട്ടങ്ങളായി പ്രയോഗിക്കുക. രോഗമുള്ളപ്പോൾ നൈട്രജൻ വളങ്ങൾ കുറയ്ക്കുക.",
                "soil": "🪵 **മണ്ണ് പരിശോധന**:\n- മണ്ണിലെ പുളിരസം (pH) അളക്കുക. നെല്ലിന് 5.5-6.5 pH ആണ് നല്ലത്.\n- അമ്ലത്വമുള്ള മണ്ണിൽ കുമ്മായം അല്ലെങ്കിൽ ഡോളമൈറ്റ് ചേർക്കുക.",
                "irrigation": "💧 **നനയ്ക്കൽ രീതികൾ**:\n- തക്കാളിക്ക് തുള്ളിനന (Drip irrigation) ആണ് ഏറ്റവും അനുയോജ്യം. ഇലകൾ നനയുന്നത് രോഗങ്ങൾ പടർത്തും.\n- അമിതമായി നനയ്ക്കുന്നത് വേരഴുകൽ രോഗത്തിന് കാരണമാകും.",
                "pest_control": "🐛 **കീടനിയന്ത്രണം**:\n- **ഇലപ്പേൻ/മുഞ്ഞ**: വേപ്പെണ്ണ മിശ്രിതം അല്ലെങ്കിൽ ഇമിഡാക്ലോപ്രിഡ് (0.5ml/L) പ്രയോഗിക്കുക.\n- **തണ്ടുതുരപ്പൻ**: തണ്ടിൽ കാണുന്ന പുഴുക്കളെ നശിപ്പിച്ച് വേപ്പധിഷ്ഠിത കീടനാശിനി തളിക്കുക.",
                "weather": "🌦️ **കാലാവസ്ഥയും കൃഷിയും**:\n- മഴ പെയ്യാൻ സാധ്യതയുള്ളപ്പോൾ കീടനാശിനി തളിക്കരുത്.\n- അന്തരീക്ഷ ഈർപ്പം കൂടുമ്പോൾ കുമിൾ രോഗങ്ങൾ വർദ്ധിക്കും.",
                "organic_farming": "🌿 **ജൈവകൃഷി**:\n- ചാണകം, കമ്പോസ്റ്റ്, എരവളങ്ങൾ എന്നിവ ഉപയോഗിക്കുക.\n- സ്യൂഡോമോണാസ്, ട്രൈക്കോഡെർമ തുടങ്ങിയ ജൈവനിയന്ത്രണ മാർഗ്ഗങ്ങൾ ഉപയോഗിക്കുക.",
                "seeds": "🌱 **വിത്തുചികിത്സ**:\n- വിതയ്ക്കുന്നതിന് മുമ്പ് സ്യൂഡോമോണാസ് ലായനിയിൽ വിത്ത് മുക്കി വെക്കുന്നത് രോഗങ്ങളെ ചെറുക്കാൻ സഹായിക്കും.",
                "harvesting": "🧺 **വിളവെടുപ്പ്**:\n- നെല്ല് 80% സ്വർണ്ണനിറമാകുമ്പോൾ വിളവെടുക്കുക. സംഭരിക്കുന്നതിന് മുൻപ് വിത്ത് നന്നായി ഉണക്കുക.",
                "nutrition": "🍂 **പോഷകക്കുറവ്**:\n- നൈട്രജൻ കുറഞ്ഞാൽ ഇലകൾ മഞ്ഞനിറമാകും, പൊട്ടാസ്യം കുറഞ്ഞാൽ ഇലകളുടെ അരികുകൾ കരിഞ്ഞുണങ്ങും.",
                "fruit_problems": "🍅 **കായഫല പ്രശ്നങ്ങൾ**:\n- തക്കാളി വിണ്ടു കീറുന്നത് ജലസേചനത്തിലെ വ്യതിയാനം മൂലമാണ്. തുള്ളിനന വഴി ഇത് തടയാം.",
                "leaf_problems": "🍃 **ഇല രോഗങ്ങൾ**:\n- ഇലകളിൽ ദ്വാരങ്ങൾ കാണുന്നത് പുഴുക്കൾ തിന്നുന്നത് കൊണ്ടാണ്. ബിടി കീടനാശിനി തളിക്കുക.",
                "best_practices": "🚜 **കർഷക രീതികൾ**:\n- വിളവിന്യാസം (Crop rotation) മണ്ണിലെ പോഷകങ്ങൾ നിലനിർത്താൻ സഹായിക്കുന്നു.\n- പുതയിടൽ (Mulching) മണ്ണിലെ ഈർപ്പം നിലനിർത്താൻ സഹായിക്കുന്നു.",
                "greenhouse": "🏠 **ഹരിതഗൃഹ കൃഷി**: കാലാവസ്ഥ വ്യതിയാനങ്ങളിൽ നിന്നും വിളകളെ സംരക്ഷിക്കാൻ സഹായിക്കുന്നു.",
                "hydroponics": "💧 **ഹൈഡ്രോപോണിക്സ്**: മണ്ണില്ലാതെ പോഷകങ്ങൾ അടങ്ങിയ ജലത്തിൽ ചെടികൾ വളർത്തുന്ന രീതി.",
                "schemes": "🏛️ **സർക്കാർ ആനുകൂല്യങ്ങൾ**:\n- **പി.എം കിസാൻ**: കർഷകർക്ക് പ്രതിവർഷം ₹6,000 ധനസഹായം ലഭിക്കുന്നു.\n- തുള്ളിനനയ്ക്ക് 90% വരെ സബ്‌സിഡി ലഭ്യമാണ്.",
                "equipment": "⚙️ **കാർഷിക യന്ത്രങ്ങൾ**: ഡ്രോൺ വഴിയുള്ള മരുന്ന് തളിക്കൽ വെള്ളവും കീടനാശിനിയും ലാഭിക്കാൻ സഹായിക്കുന്നു.",
                "livestock": "🐄 **ക്ഷീരവികസനം**: പശുക്കൾക്ക് പച്ചപ്പുല്ലും സമീകൃതാഹാരവും നൽകുക. കുളമ്പുരോഗത്തിന് ലക്സിൻ എടുക്കുക.",
                "market": "📈 **വിപണനം**: ഉൽപ്പന്നങ്ങൾ ഉണക്കി സംഭരിച്ച് വില കൂടുമ്പോൾ വിൽക്കുക.",
                "seasonal": "📅 **കൃഷി കലണ്ടർ**: മൺസൂൺ വിളകൾ (ഖാരിഫ്), മഞ്ഞുകാല വിളകൾ (റബി), വേനൽക്കാല വിളകൾ (സെയ്ദ്).",
                "safety": "🦺 **സുരക്ഷ**: കീടനാശിനി പ്രയോഗിക്കുമ്പോൾ മാസ്കും ഗ്ലൗസും ധരിക്കുക. കാറ്റിന് എതിരായി തളിക്കരുത്.",
                "follow_up": "⚠️ **രോഗനിർണ്ണയശേഷമുള്ള പടികൾ**: കുമിൾ ബാധിച്ച ഇലകൾ നശിപ്പിച്ച് കളഞ്ഞ് ബാധയുള്ള ഭാഗങ്ങളിൽ മരുന്ന് തളിക്കുക.",
                "general": "📚 **കാർഷിക പദാവലി**: ജൈവവളങ്ങൾ മണ്ണിന്റെ ഘടന മെച്ചപ്പെടുത്തുമ്പോൾ രാസവളങ്ങൾ പോഷകങ്ങൾ പെട്ടെന്ന് ലഭ്യമാക്കുന്നു."
            },
            "hi": {
                "greetings": "नमस्ते! मैं एग्रीबॉट हूँ, आपका व्यक्तिगत कृषि सलाहकार। मैं आपको फसल खेती (टमाटर, मिर्च, धान, आम, नारियल आदि), मिट्टी परीक्षण, एनपीके गणना, जैविक खेती, रोग उपचार और सरकारी योजनाओं पर मार्गदर्शन दे सकता हूँ। मैं आपकी कैसे मदद कर सकता हूँ?",
                "disease_id": "🌱 **रोग पहचान गाइड**:\n- **पीली पत्तियाँ**: आमतौर पर नाइट्रोजन की कमी या जलभराव का संकेत है।\n- **भूरी/काली चित्तियाँ**: फंगल संक्रमण (जैसे टमाटर में अगेती झुलसा/अर्ली ब्लाइट या आम में एन्थ्रेक्नोस)।\n- **सफेद पाउडर**: पाउडर जैसी फफूंदी (पाउडरी मिल्ड्यू)।\n- **पत्तियों का मुड़ना**: वायरल संक्रमण। विस्तृत विश्लेषण के लिए लीफ स्कैनर का उपयोग करें!",
                "disease_symptoms": "🔬 **प्रमुख लक्षण**:\n1. **अर्ली ब्लाइट**: निचली पुरानी पत्तियों पर गोलाकार छल्ले।\n2. **बैक्टीरियल विल्ट (उकठा)**: पत्तियां हरी रहते हुए ही तेजी से मुरझा जाती हैं।\n3. **पाउडरी मिल्ड्यू**: पत्ती की ऊपरी सतह पर सफेद चूर्ण की परत।",
                "disease_treatment": "🧪 **फसलों के रोग उपचार**:\n- **फंगल रोग**: मैनकोजेब (2g/L) या हेक्साकोनाज़ोल (1ml/L) का छिड़काव करें।\n- **बैक्टीरियल संक्रमण**: कॉपर ऑक्सीक्लोराइड (2g/L) के साथ स्ट्रेप्टोसाइक्लिन (0.1g/L) मिलाएं।\n- **जैविक**: 5% नीम के बीज का काढ़ा (NSKE) छिड़कें।",
                "disease_prevention": "🛡️ **रोग नियंत्रण**:\n1. निचली रोगग्रस्त पत्तियों को काटें।\n2. औजारों को सैनिटाइज करें।\n3. वायरस से संक्रमित पौधों को उखाड़कर जला दें।",
                "crop_info": "🌾 **फसल की जानकारी**:\n- **टमाटर**: बलुई दोमट मिट्टी (pH 6.0-6.8) सर्वोत्तम है। अवधि 110-140 दिन।\n- **धान**: दोमट/चिकनी मिट्टी, भरपूर पानी की आवश्यकता। अवधि 120-150 दिन।\n- **मक्का**: जलभराव के प्रति संवेदनशील। अवधि 90-120 दिन।",
                "fertilizer": "🧪 **उर्वरक और एनपीके**:\n- **NPK**: नाइट्रोजन (N) हरियाली के लिए, फास्फोरस (P) जड़ों और फूलों के लिए, पोटेशियम (K) फल के आकार और रोग प्रतिरोधक क्षमता के लिए।\n- **यूरिया**: किस्तों में डालें। संक्रमण के दौरान यूरिया कम करें।",
                "soil": "🪵 **मिट्टी परीक्षण और स्वास्थ्य**:\n- **मिट्टी जांच**: खेत के अलग-अलग हिस्सों से 15 सेमी गहराई की मिट्टी लेकर जांच के लिए भेजें।\n- **अम्लीय मिट्टी**: पीएच सुधारने के लिए चूना (Lime) या डोलोमाइट मिलाएं।",
                "irrigation": "💧 **जलापूर्ति गाइड**:\n- टमाटर के लिए ड्रिप (टपक) सिंचाई सर्वोत्तम है।\n- अधिक सिंचाई से जड़ें सड़ने लगती हैं (डैम्पिंग-ऑफ)।",
                "pest_control": "🐛 **कीट नियंत्रण**:\n- **चेपा/थ्रिप्स**: नीम का तेल (2%) छिड़कें। रासायनिक के लिए इमिडाक्लोप्रिड (0.5ml/L) का प्रयोग करें।\n- **तन्ना छेदक**: मिट्टी में कार्बोफ्यूरान डालें।",
                "weather": "🌦️ **मौसम और खेती**:\n- यदि 3 घंटे के भीतर बारिश की संभावना हो, तो कीटनाशक छिड़काव से बचें।\n- उच्च आर्द्रता से फंगल रोग तेजी से फैलते हैं।",
                "organic_farming": "🌿 **जैविक खेती**:\n- गोबर खाद, कम्पोस्ट और केंचुआ खाद (Vermicompost) का उपयोग करें।\n- एजोटोबैक्टर और पीएसबी जैसे जैव उर्वरक डालें।",
                "seeds": "🌱 **बीजोपचार**:\n- बोने से पहले बीजों को ट्राइकोडेर्मा (4g/kg) या कार्बेन्डाजिम (2g/kg) से उपचारित करें।",
                "harvesting": "🧺 **कटाई और भंडारण**:\n- टमाटरों को लंबी दूरी के परिवहन के लिए 'ब्रेकर चरण' (पीला-गुलाबी) में तोड़ें।\n- अनाज को भंडारण से पहले धूप में सुखाएं (नमी 14% से कम)।",
                "nutrition": "🍂 **पोषण की कमी**:\n- **नाइट्रोजन की कमी**: पुरानी पत्तियां समान रूप से पीली पड़ जाती हैं।\n- **पोटेशियम की कमी**: पत्तियों के किनारे झुलसे/भूरे दिखाई देते हैं।",
                "fruit_problems": "🍅 **फलों की समस्याएं**:\n- **टमाटर फटना**: अनियमित सिंचाई के कारण। मिट्टी में नमी का स्तर समान रखें।",
                "leaf_problems": "🍃 **पत्तियों की समस्याएं**:\n- पत्तियों में छिद्र होना कीड़ों के खाने का संकेत है। नीम का तेल या बीटी स्प्रे करें।",
                "best_practices": "🚜 **उन्नत कृषि पद्धतियां**:\n- **फसल चक्र (Crop Rotation)**: मिट्टी की उर्वरता बनाए रखने के लिए फसलें बदल-बदल कर बोएं।\n- **मल्चिंग**: नमी बचाने के लिए प्लास्टिक या पुआल से जमीन ढकें।",
                "greenhouse": "🏠 **ग्रीनहाउस खेती**: नियंत्रित वातावरण में ऑफ-सीजन सब्जियां उगाने की तकनीक.",
                "hydroponics": "💧 **हाइड्रोपोनिक्स**: बिना मिट्टी के पोषक तत्वों से भरपूर पानी में पौधे उगाने की प्रणाली।",
                "schemes": "🏛️ **सरकारी योजनाएं**:\n- **पीएम-किसान**: किसानों को सालाना ₹6,000 की वित्तीय सहायता।\n- **सिंचाई सब्सिडी**: ड्रिप सिंचाई पर 90% तक की छूट।",
                "equipment": "⚙️ **कृषि उपकरण**: रोटावेटर मिट्टी को भुरभुरा बनाता है। ड्रोन छिड़काव से रसायन और पानी की बचत होती है।",
                "livestock": "🐄 **पशुपालन**: गायों को संतुलित आहार दें। खुरपका-मुँहपका (FMD) रोग का टीका वर्ष में दो बार लगवाएं।",
                "market": "📈 **बाजार भाव**: अनाज सुखाकर गोदाम में रखें और सही दाम मिलने पर बेचें।",
                "seasonal": "📅 **फसल चक्र**: खरीफ (मानसून: धान, मक्का), रबी (शीतकाल: गेहूं, सरसों), जायद (गर्मी: तरबूज, ककड़ी)।",
                "safety": "🦺 **छिड़काव सुरक्षा**: छिड़काव के दौरान मास्क, दस्ताने पहनें और कभी भी हवा के विपरीत दिशा में न छिड़कें।",
                "follow_up": "⚠️ **रोग उपचार कदम**: संक्रमित पौधों को तुरंत अलग करें और अनुशंसित दवाओं का छिड़काव शुरू करें।",
                "general": "📚 **सामान्य शब्दावली**: जैविक खाद मिट्टी का स्वास्थ्य सुधारती है जबकि रासायनिक खाद तुरंत एनपीके प्रदान करती है।"
            },
            "te": {
                "greetings": "നമസ്കാരം! నేను అగ్రిబాట్, మీ వ్యక్తిగత వ్యవసాయ సలహాదారుని. పంట సాగు (టమోటా, మిర్చి, వరి, మామిడి, కొబ్బరి మొదలైనవి), మట్టి పరీక్షలు, NPK లెಕ್ಕలు, సేంద్రీయ వ్యవసాయం, తెగుళ్ల నివారణ మరియు ప్రభుత్వ పథకాలపై నేను మీకు సమాచారం ఇవ్వగలను. ఈ రోజు నేను మీకు ఎలా సహాయపడగలను?",
                "disease_id": "🌱 **తెగుళ్ల గుర్తింపు**:\n- **ఆకులు పసుపు రంగులోకి మారడం**: నత్రజని (Nitrogen) లోపం లేదా నీరు నిలవడం వల్ల జరుగుతుంది.\n- **గోధుమ/నలుపు మచ్చలు**: శిలీంధ్ర వ్యాధి (టమోటాలో ఆకు మాడు తెగులు లేదా మామిడిలో మచ్చ తెగులు).\n- **తెల్లటి పొడి మచ్చలు**: బూడిద తెగులు (Powdery Mildew).\n- **ఆకులు ముడుచుకుపోవడం**: వైరస్ వ్యాధి (తెల్ల దోమ ద్వారా వ్యాప్తి). లీఫ్ స్కానర్ ఉపయోగించి ఫోటో అప్లోడ్ చేయండి!",
                "disease_symptoms": "🔬 **ప్రధాన తెగుళ్ల లక్షణాలు**:\n1. **ಅರ್ಲಿ ಬ್ಲೈಟ್**: ಕಿಂದಿ ಪಾತ ಆಕುಲಪೈ ವಲಯಾಕಾರಪು ಗೋಧುಮ ರಂಗು ಮಚ್ಚಲು.\n2. **బ్యాక్టీరియల్ వడల తెగులు**: మొక్క పచ్చగా ఉన్నప్పుడే వేగంగా ఎండిపోతుంది.\n3. **ಬೂಡಿದ ತೆಗುಲು**: ಆಕುಲಪೈ ತೆಲ್ಲಟಿ ಬೂಡಿದ ವಂಟಿ ಪೊಡಿ ಪರಚುಕುಂಟುಂದಿ.",
                "disease_treatment": "🧪 **తెగుళ్ల నివారణ చర్యలు**:\n- **శిలీంధ్ర వ్యాధులు**: మ్యాంకోజెబ్ (2g/L) లేదా హెక్సాకొనజోల్ (1ml/L) పిచికారీ చేయండి.\n- **బ్యాక్టీరియా వ్యాధులు**: కాపర్ ఆక్సిక్లోరైడ్ (2g/L) మరియు స్ట్రెప్టోసైక్లిన్ (0.1g/L) కలపండి.\n- **సేంద్రీయ చికిత్స**: 5% వేప గింజల కషాయం పిచికారీ చేయండి.",
                "disease_prevention": "🛡️ **తెగుళ్ల నివారణ**:\n1. తెగులు సోకిన కింది ఆకులను కత్తిరించి నాశనం చేయండి.\n2. వ్యవసాయ పనిముట్లను ఆల్కహాల్ తో శుభ్రం చేయండి.\n3. వైరస్ సోకిన మొక్కలను పీకి తగులబెట్టండి.",
                "crop_info": "🌾 **పంటల సమాచారం**:\n- **టమోటా**: లోమీ నేలలు (pH 6.0-6.8) అనుకూలం. పంట కాలం 110-140 రోజులు.\n- **వరి**: నల్లరేగడి/లోమీ నేలలు, ఎక్కువ నీరు అవసరం. పంట కాలం 120-150 రోజులు.\n- **మొక్కజొన్న**: నేలలు అవసరం. పంట కాలం 90-120 రోజులు.",
                "fertilizer": "🧪 **ఎరువులు మరియు NPK**:\n- **NPK**: నత్రజని (N) ఆకుల ఎదుగుదలకు, భాస్వరం (P) వేర్లు మరియు పూతకు, పొటాషియం (K) కాయ సైజు మరియు తెగుళ్ల నిరోధకతకు.\n- **యూరియా**: దఫాలుగా వేయండి. తెగులు ఉన్నప్పుడు యూరియా వాడకం తగ్గించండి.",
                "soil": "🪵 **మట్టి పరీక్షలు**:\n- **మట్టి పరీక్ష**: పొలంలో 15 సెం.మీ లోతు నుండి మట్టిని సేకరించి పరీక్షా కేంద్రానికి పంపండి.\n- **ఆమ్ల గుణం గల నేలలు**: నేలలో సున్నం లేదా డోలమైట్ కలిపి pH ని సవరించండి.",
                "irrigation": "💧 **నీటి యాజమాన్యం**:\n- టమోటాలకు బిందు సేద్యం (Drip) అత్యంత అనుకూలం. ఆకులు తడిస్తే శిలీంధ్ర తెగుళ్లు వ్యాపిస్తాయి.\n- ఎక్కువ నీరు పెడితే వేరుకుళ్లు తెగులు వస్తుంది.",
                "pest_control": "🐛 **కీటక నివారణ**:\n- **పేనుబంక/తామర పురుగులు**: వేపనూనె (2%) పిచికారీ చేయండి. రసాయన చికిత్సకు ఇమిడాక్లోప్రిడ్ (0.5ml/L) వాడండి.\n- **కాండం తొలిచే పురుగు**: కార్బోఫ్యూరాన్ గుళికలు నేలలో వేయండి.",
                "weather": "🌦️ **వాతావరణం మరియు వ్యవసాయం**:\n- వర్షం పడే సూచన ఉంటే పురుగు మందులు పిచికారీ చేయవద్దు.\n- గాలిలో తేమ ఎక్కువగా ఉన్నప్పుడు బూజు తెగుళ్లు వేగంగా వ్యాపిస్తాయి.",
                "organic_farming": "🌿 **సేంద్రీయ వ్యవసాయం**:\n- పశువుల ఎరువు, వర్মীకంపోస్ట్, పచ్చిరొట్ట ఎరువులను వాడండి.\n- అజటోబాక్టర్ మరియు పి.ಎಸ್.ಬಿ వంటి జీవ ఎరువులను ఉపయోగించండి.",
                "seeds": "🌱 **విత్తన శుద్ధి**:\n- విత్తే ಮುನ್ನು ವಿತ್ತನಾಳಕು ಟ್ರೈಕೋಡರ್ಮಾ ವಿರಿಡಿ (4g/kg) ಲೇದಾ ಕಾರ್ಬಂಡಿಜಮ್ (2g/kg) ತೋ ವಿತ್ತನ ಶುದ್ಧಿ ಚೇಯಂಡಿ.",
                "harvesting": "🧺 **కోత మరియు నిల్వ**:\n- టమోటాలను రవాణా కోసం 'బ్రేకర్ దశ' (పసుపు-గులాబీ రంగు) లో కోయండి.\n- ధాన్యాలను నిల్వ చేసే ಮುನ್ನು ఎండబెట్టి తేమ శాతాన్ని 14% కన్నా తక్కువకు తీసుకురండి.",
                "nutrition": "🍂 **పోషకాల లోపాలు**:\n- **నత్రజని లోపం**: కింది ఆకులు పసుపు రంగులోకి మారిపోతాయి.\n- **పొటాషియం లోపం**: ఆకుల అంచులు కాలిపోయినట్లు గోధుమ రంగులోకి మారుతాయి.",
                "fruit_problems": "🍅 **కాయల సమస్యలు**:\n- **టమోటాలు పగలడం**: నీటి సరఫరాలో హెచ్చుతగ్గుల వల్ల జరుగుతుంది. తేమ సమానంగా ఉంచండి.",
                "leaf_problems": "🍃 **ఆకుల సమస్యలు**:\n- ఆకులపై రంధ్రాలు ఉంటే పురుగులు తింటున్నాయని అర్థం. బిటి పిచికారీ చేయండి.",
                "best_practices": "🚜 **పంట పద్ధతులు**:\n- **పంట మార్పిడి (Crop Rotation)**: నేల సారాన్ని కాపాడటానికి ఏటా పంటను మార్చండి.\n- **మల్చింగ్**: తేమను కాపాడటానికి ప్లాస్టిక్ లేదా ఎండుగడ్డి పరచండి.",
                "greenhouse": "🏠 **గ్రీన్ హౌస్ సాగు**: ఉష్ణోగ్రత నియంత్రించి అకాల పంటలను పండించే విధానం.",
                "hydroponics": "💧 **హైడ్రోపోనిక్స్**: మట్టి లేకుండా కేవలం ఖనిజ లవణాల నీటిలో పంటలు పండించే పద్ధతి.",
                "schemes": "🏛️ **ప్రభుత్వ పథకాలు**:\n- **పీఎం-కిసాన్**: రైతులకు ఏడాదికి ₹6,000 ఆర్థిక సహాయం.\n- **బిందు సేద్యం సబ్సిడీ**: మైక్రో ఇరిగేషన్ పై 90% వరకు రాయితీ లభిస్తుంది.",
                "equipment": "⚙️ **వ్యవసాయ పరికరాలు**: రోటవేటర్ నేలను మెత్తగా చేస్తుంది. డ్రోన్ ద్వారా మందు పిచికారీ చేయడం వల్ల నీరు, మందు ఆదా అవుతాయి.",
                "livestock": "🐄 **పశుగ్రాసం**: ఆవులకు సమతుల్య ఆహారం ఇవ్వండి. గాలికుంటు వ్యాధి (FMD) నివారణకు ఏడాదికి రెండు సార్లు టీకాలు వేయించండి.",
                "market": "📈 **మార్కెట్ ధరలు**: పంట కోసిన వెంటనే తక్కువ ధరకు అమ్మకుండా నిల్వ చేసి, ధర పెరిగినప్పుడు అమ్మండి.",
                "seasonal": "📅 **వ్యవసాయ కాలాలు**: ఖరీఫ్ (వానకాలం: వరి, మొక్కజొన్న), రబీ (యాసంగి: గోధుమలు, ఆవాలు), జైద్ (వేసవి).",
                "safety": "🦺 **రక్షణ చర్యలు**: మందు పిచికారీ చేసేటప్పుడు మాస్క్, గ్లౌస్ ధరించండి. గాలి వీచే దిశలోనే పిచికారీ చేయండి.",
                "follow_up": "⚠️ **తెగులు గుర్తింపు తదుపరి చర్యలు**: తెగులు సోకిన మొక్కలను వేరుచేసి వెంటనే తగిన మందును పిచికారీ చేయండి.",
                "general": "📚 **వ్యవసాయ పదజాలం**: సేంద్రీయ ఎరువు నేల ఆరోగ్యాన్ని పెంచుతుంది, రసాయన ఎరువులు పంటకు తక్షణ ఆహారాన్ని అందిస్తాయి."
            },
            "ta": {
                "greetings": "வணக்கம்! நான் அக்ரிபாட், உங்கள் தனிப்பட்ட விவசாய உதவியாளர். தக்காளி, மிளகாய், நெல், மாம்பழம், தென்னை சாகுபடி, மண் பரிசோதனை, NPK அளவுகள், இயற்கை விவசாயம் மற்றும் அரசு திட்டங்கள் குறித்து நான் உங்களுக்கு வழிகாட்டுவேன். இன்று உங்களுக்கு நான் எவ்வாறு உதவ வேண்டும்?",
                "disease_id": "🌱 **நோய் கண்டறிதல் வழிகாட்டி**:\n- **மஞ்சள் இலைகள்**: பொதுவாக நைட்ரஜன் பற்றாக்குறை அல்லது தேங்கிய நீர்.\n- **பழுப்பு/கருப்பு புள்ளிகள்**: பூஞ்சை நோய் (தக்காளியில் கருகல் நோய் அல்லது மாம்பழத்தில் ஆந்த்ராக்னோஸ்).\n- **வெள்ளை மாவு போன்ற புள்ளிகள்**: சாம்பல் நோய் (Powdery Mildew).\n- **இலை சுருட்டல்**: வைரஸ் நோய். இலை ஸ்கேனர் பக்கத்தில் புகைப்படம் பதிவேற்றி கண்டறியவும்!"
            }
        }
        
        # Add rest of Tamil mapping programmatically/directly
        self.responses["ta"].update({
            "disease_symptoms": "🔬 **முக்கிய நோய்களின் அறிகுறிகள்**:\n1. **அர்லி பிளைட்**: கீழ் இலைகளில் வளைய வடிவ பழுப்பு நிற புள்ளிகள்.\n2. **பாக்டீரியா வாடல்**: இலைகள் பச்சையாக இருக்கும்போதே செடி வாடிவிடும்.\n3. **சாம்பல் நோய்**: இலைகளில் வெள்ளை நிற சாம்பல் படிந்திருக்கும்.",
            "disease_treatment": "🧪 **நோய்களுக்கான சிகிச்சைகள்**:\n- **பூஞ்சை நோய்கள்**: மேன்கோசெப் (2g/L) அல்லது ஹெக்சாகோனசோல் (1ml/L) தெளிக்கவும்.\n- **பாக்டீரியா நோய்கள்**: காப்பர் ஆக்ஸிகுளோரைடுடன் (2g/L) ஸ்ட்ரெப்டோமைசின் (0.1g/L) கலந்து தெளிக்கவும்.\n- **இயற்கை முறை**: 5% வேப்பங்கொட்டை கரைசல் தெளிக்கவும்.",
            "disease_prevention": "🛡️ **நோய் தடுப்பு முறைகள்**:\n1. பாதிக்கப்பட்ட கீழ் இலைகளை வெட்டி அழிக்கவும்.\n2. விவசாய கருவிகளை அணுநீக்கம் செய்யவும்.\n3. வைரஸ் தாக்கிய செடிகளை வேரோடு பிடுங்கி எரிக்கவும்.",
            "crop_info": "🌾 **பயிர்கள் பற்றிய தகவல்கள்**:\n- **தக்காளி**: மணல் கலந்த வண்டல் மண் (pH 6.0-6.8) சிறந்தது. சாகுபடி காலம் 110-140 நாட்கள்.\n- **நெல்**: களிமண் மற்றும் அதிக நீர் தேவை. சாகுபடி காலம் 120-150 நாட்கள்.\n- **சோளம்**: நீர் தேங்காத மண் தேவை. சாகுபடி காலம் 90-120 நாட்கள்.",
            "fertilizer": "🧪 **உரங்கள் மற்றும் NPK**:\n- **NPK**: நைட்ரஜன் (N) இலைகளின் வளர்ச்சிக்கும், பாஸ்பரஸ் (P) வேர்கள் மற்றும் பூக்களுக்கும், பொட்டாசியம் (K) பழங்களின் அளவிற்கும் நோய் எதிர்ப்பு சக்திக்கும்.\n- **யூரியா**: தவணை முறையில் போடவும். நோய் இருக்கும்போது யூரியாவை குறைக்கவும்.",
            "soil": "🪵 **மண் பரிசோதனை**:\n- **மண் பரிசோதனை**: நிலத்தின் 15 செ.மீ ஆழத்திலிருந்து மண் எடுத்து பரிசோதனைக்கு அனுப்பவும்.\n- **அமில மண்**: மண்ணிற்கு சுண்ணாம்பு அல்லது டோலமைட் சேர்த்து pH அளவை சீராக்கவும்.",
            "irrigation": "💧 **நீர் மேலாண்மை**:\n- தக்காளிக்கு சொட்டு நீர் பாசனம் (Drip) சிறந்தது. இலைகளில் நீர் பட்டால் பூஞ்சை பரவும்.\n- அதிக நீர் பாய்ச்சினால் வேரழுகல் நோய் ஏற்படும்.",
            "pest_control": "🐛 **பூச்சி கட்டுப்பாடு**:\n- **இலைப்பேன்கள்/அசுவினி**: வேப்பெண்ணெய் (2%) தெளிக்கவும். இரசாயன முறைக்கு இமிடாக்குளோபிரிட் (0.5ml/L) தெளிக்கவும்.\n- **தண்டு துளைப்பான்**: கார்போபியூரான் குருணை உரத்தை மண்ணில் இடவும்.",
            "weather": "🌦️ **வானிலை மற்றும் விவசாயம்**:\n- மழை பெய்யும் வாய்ப்பு இருந்தால் பூச்சிக்கொல்லி தெளிக்க வேண்டாம்.\n- காற்றில் ஈரப்பதம் அதிகரிக்கும் போது பூஞ்சை நோய்கள் விரைவாக பரவும்.",
            "organic_farming": "🌿 **இயற்கை விவசாயம்**:\n- தொழு உரம், மண்புழு உரம் (Vermicompost) மற்றும் பசுந்தாள் உரங்களை பயன்படுத்தவும்.\n- அசோஸ்பைரில்லம் மற்றும் பி.எஸ்.比 உயிர் உரங்களை பயன்படுத்தவும்.",
            "seeds": "🌱 **விதை நேர்த்தி**:\n- விதைக்கும் முன் விதைகளை டிரைக்கோடெர்மா விரிடி (4g/kg) அல்லது கார்பென்டாசிம் (2g/kg) கொண்டு விதை நேர்த்தி செய்யவும்.",
            "harvesting": "🧺 **அறுவடை மற்றும் சேமிப்பு**:\n- தக்காளியை 'பிரேக்கர் நிலையில்' (மஞ்சள்-இளஞ்சிவப்பு நிறம்) அறுவடை செய்யவும்.\n- தானியங்களை சேமிக்கும் முன் வெயிலில் உலர்த்தி ஈரப்பதம் 14% க்கும் குறைவாக இருப்பதை உறுதி செய்யவும்.",
            "nutrition": "🍂 **சத்து குறைபாடுகள்**:\n- **நைட்ரஜன் குறைபாடு**: கீழ் இலைகள் மஞ்சள் நிறமாக மாறும்.\n- **பொட்டாசியம் குறைபாடு**: இலைகளின் ஓரங்கள் கருகியவாறு பழுப்பு நிறமாக மாறும்.",
            "fruit_problems": "🍅 **பழங்களின் பிரச்சனைகள்**:\n- **தக்காளி வெடிப்பு**: சீரற்ற நீர் பாய்ச்சுவதால் ஏற்படும். மண்ணின் ஈரப்பதத்தை சீராக வைக்கவும்.",
            "leaf_problems": "🍃 **இலை பிரச்சனைகள்**:\n- இலைகளில் துளைகள் இருந்தால் புழுக்கள் தின்கிறது என்று பொருள். பிடி தெளிக்கவும்.",
            "best_practices": "🚜 **விவசாய முறைகள்**:\n- **பயிர் சுழற்சி (Crop Rotation)**: மண் வளத்தை காக்க ஆண்டிற்கு ஒருமுறை பயிரை மாற்றவும்.\n- **மூடாக்கு (Mulching)**: ஈரப்பதத்தை காக்க பிளாஸ்டிக் அல்லது காய்ந்த புற்களை கொண்டு மூடவும்.",
            "greenhouse": "🏠 **பசுமைக்குடில் சாகுபடி**: தட்பவெப்ப நிலையை கட்டுப்படுத்தி பருவம் அல்லாத பயிர்களை விளைவிக்கும் முறை.",
            "hydroponics": "💧 **ஹைட்ரோபோனிக்സ്**: மண் இல்லாமல் தண்ணீரில் மட்டுமே ஊட்டச்சத்துக்களை கரைத்து பயிர் வளர்க்கும் முறை.",
            "schemes": "🏛️ **அரசு திட்டங்கள்**:\n- **பிஎம்-கிசான்**: விவசாயிகளுக்கு ஆண்டுக்கு ₹6,000 நிதியுதவி.\n- சொட்டு நீர் பாசனத்திற்கு 90% வரை மானியம் வழங்கப்படுகிறது.",
            "equipment": "⚙️ **விவசாய கருவிகள்**: ரோட்டவேட்டர் மண்ணை மென்மையாக்குகிறது. ட்ரோன் மூலம் மருந்து தெளிப்பது நீர் மற்றும் மருந்தை மிச்சப்படுத்துகிறது.",
            "livestock": "🐄 **கால்நடை வளர்ப்பு**: பசுக்களுக்கு சமச்சீர் தீவனம் வழங்குங்கள். கோமாரி நோய்க்கு ஆண்டுக்கு இருமுறை தடுப்பூசி போடுங்கள்.",
            "market": "📈 **சந்தை நிலவரம்**: அறுவடையின் போது விற்காமல் சேமித்து வைத்து, விலை உயரும் போது விற்பனை செய்யவும்.",
            "seasonal": "📅 **பயிர் பருவங்கள்**: காரிஃப் (மழைக்காலம்: நெல், சோளம்), ரபி (குளிர்காலம்: கோதுமை, கடுகு), சையத் (கோடைகாலம்).",
            "safety": "🦺 **பாதுகாப்பு**: பூச்சிக்கொல்லி தெளிக்கும் போது முகமூடி மற்றும் கையுறைகளை அணியுங்கள். காற்றின் திசையிலேயே தெளிக்கவும்.",
            "follow_up": "⚠️ **விளக்கம் கண்டறிந்த பின்**: பாதிக்கப்பட்ட செடியை தனியாக பிரித்து வைத்து பரிந்துரைக்கப்பட்ட மருந்தை தெளிக்கவும்.",
            "general": "📚 **விளக்கக் குறிப்புகள்**: இயற்கை உரங்கள் மண் வளத்தை கூட்டுகிறது, இரசாயன உரங்கள் பயிருக்கு உடனடி சத்தை தருகிறது."
        })

    def respond(self, message, lang="en"):
        lang = lang.lower().strip()
        if lang not in self.responses:
            lang = "en"

        message_clean = message.lower().strip()
        message_no_punct = re.sub(r'[?.,!:]', '', message_clean).strip()
        
        # Direct localized question to intent mapping (lowercase keys)
        direct_mapping = {
            # English
            "what causes this fungal infection": "disease_id",
            "how to prevent fungal spores from spreading": "disease_prevention",
            "which chemical fungicide is best": "disease_treatment",
            "what virus causes this disease": "disease_id",
            "how to control the insect vectors spreading it": "pest_control",
            "should i destroy the infected crop": "disease_prevention",
            "how does bacterial blight spread": "disease_id",
            "what bactericide spray should i use": "disease_treatment",
            "how to disinfect farming tools": "disease_prevention",
            "what insect is causing this damage": "pest_control",
            "what organic pest repellent works best": "organic_farming",
            "when is the best time to spray pesticide": "pest_control",
            "what npk dosage is recommended": "fertilizer",
            "how often should i irrigate my crop": "irrigation",
            "what are common diseases to watch out for": "disease_id",
            
            # Kannada
            "ಈ ಶಿಲೀಂಧ್ರ ರೋಗಕ್ಕೆ ಕಾರಣವೇನು": "disease_id",
            "ಶಿಲೀಂಧ್ರ ರೋಗ ಇತರ ಗಿಡಗಳಿಗೆ ಹರಡುವುದನ್ನು ತಡೆಯುವುದು ಹೇಗೆ": "disease_prevention",
            "ಯಾವ ರಾಸಾಯನಿಕ ಶಿಲೀಂಧ್ರನಾಶಕ ಅತ್ಯುತ್ತಮ": "disease_treatment",
            "ಯಾವ ವೈರಸ್ ಈ ರೋಗಕ್ಕೆ ಕಾರಣ": "disease_id",
            "ರೋಗ ಹರಡುವ ಕీటಗಳನ್ನು ನಿಯಂತ್ರಿಸುವುದು ಹೇಗೆ": "pest_control",
            "ರೋಗಗ್ರಸ್ತ ಗಿಡವನ್ನು ಕಿತ್ತು ಹಾಕಬೇಕೇ": "disease_prevention",
            "ಬ್ಯಾಕ್ಟೀರಿಯಾ ರೋಗ ಹೇಗೆ ಹరಡುತ್ತದೆ": "disease_id",
            "ಯಾವ ಬ್ಯಾಕ್ಟೀರಿಯಾ ನಾಶಕ ಸಿಂಪಡಿಸಬೇಕು": "disease_treatment",
            "ಕೃಷಿ ಉಪಕರಣಗಳನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸುವುದು ಹೇಗೆ": "disease_prevention",
            "ಯಾವ ಕೀಟ ಈ ಹಾನಿಯನ್ನು ಉಂಟುಮಾಡುತ್ತಿದೆ": "pest_control",
            "ಯಾವ ಸಾವಯವ ಕೀಟನಾಶಕ ಅತ್ಯುತ್ತಮ": "organic_farming",
            "ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಲು ಸೂಕ್ತ ಸಮಯ ಯಾವುದು": "pest_control",
            "ಯಾವ npk ಗೊಬ್ಬರದ ಪ್ರಮಾಣ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ": "fertilizer",
            "ಬೆಳೆಗೆ ಎಷ್ಟು ಬಾರಿ ನೀರು ಹಾಯಿಸಬೇಕು": "irrigation",
            "ಬೆಳೆಗೆ ಬರುವ ಇತರ ಪ್ರಮುಖ ರೋಗಗಳು ಯಾವುವು": "disease_id",

            # Hindi
            "इस फंगल संक्रमण का कारण क्या है": "disease_id",
            "फंगल बीजाणुओं को फैलने से कैसे रोकें": "disease_prevention",
            "कौन सा रासायनिक फफूंदनाशी सर्वोत्तम है": "disease_treatment",
            "इस बीमारी का कारण कौन सा वायरस है": "disease_id",
            "इसे फैलाने वाले कीट वाहकों को कैसे नियंत्रित करें": "pest_control",
            "क्या मुझे संक्रमित पौधे को नष्ट कर देना चाहिए": "disease_prevention",
            "बैक्टीरियल ब्लाइट कैसे फैलता है": "disease_id",
            "मुझे किस जीवाणुनाशक स्प्रे का उपयोग करना चाहिए": "disease_treatment",
            "खेती के औजारों को कीटाणुरहित कैसे करें": "disease_prevention",
            "यह नुकसान कौन सा कीट पहुंचा रहा है": "pest_control",
            "कौन सा जैविक कीट विकर्षक सबसे अच्छा काम करता है": "organic_farming",
            "कौन सा जैविक कीट विकर्षक सबसे अच्छा काम करता": "organic_farming",
            "कीटनाशक छिड़कने का सबसे अच्छा समय क्या है": "pest_control",
            "कौन सी एनपीके खुराक की सिफारिश की जाती है": "fertilizer",
            "मुझे अपनी फसल की सिंचाई कितनी बार करनी चाहिए": "irrigation",
            "ध्यान देने योग्य सामान्य बीमारियाँ कौन सी हैं": "disease_id",

            # Telugu
            "ఈ శిలీంధ్ర తెగులు రావడానికి కారణం ఏమిటి": "disease_id",
            "శిలీంధ్ర వ్యాప్తిని ఎలా అరికట్టాలి": "disease_prevention",
            "ఏ రసాయన శిలీంధ్రనాశకం ఉత్తమమైనది": "disease_treatment",
            "ఈ తెగులుకు కారణమైన వైరస్ ఏది": "disease_id",
            "వైరస్ వ్యాప్తి చేసే కీటకాలను ఎలా నియంత్రించాలి": "pest_control",
            "తెగులు సోకిన మొక్కను తీసివేసి నాశనం చేయాలా": "disease_prevention",
            "బ్యాక్టీరియా తెగులు ఎలా వ్యాపిస్తుంది": "disease_id",
            "ఏ బ్యాక్టీరియా నాశక పిచికారీ వాడాలి": "disease_treatment",
            "వ్యవసాయ పనిముట్లను ఎలా శుభ్రపరచాలి": "disease_prevention",
            "ఈ నష్టం కలిగిస్తున్న పురుగు ఏది": "pest_control",
            "ఏ సేంద్రీయ పురుగు నివారణ పద్ధతి బాగా పనిచేస్తుంది": "organic_farming",
            "పురుగుల మందు పిచికారీ చేయడానికి సరైన సమయం ఏది": "pest_control",
            "పంటకు ఎంత ఎన్పికె మోతాదు సిఫార్సు చేయబడింది": "fertilizer",
            "పంటకు ఎంత ఎన్.పి.కె మోతాదు సిఫార్సు చేయబడింది": "fertilizer",
            "పంటకు ఎంత ఎన్.పి.కె (npk) మోతాదు సిఫార్సు చేయబడింది": "fertilizer",
            "పంటకు ఎన్ని రోజులకు ఒకసారి నీటి తడులు ఇవ్వాలి": "irrigation",
            "పంటకు వచ్చే సాధారణ తెగుళ్లు ఏమిటి": "disease_id",

            # Tamil
            "இந்த பூஞ்சை தொற்றுக்கு என்ன காரணம்": "disease_id",
            "பூஞ்சை காளான்கள் பரவாமல் தடுப்பது எப்படி": "disease_prevention",
            "எந்த இரசாயன பூஞ்சைக் கொல்லி சிறந்தது": "disease_treatment",
            "இந்த நோயை உண்டாக்கும் வைரஸ் எது": "disease_id",
            "வைரஸைப் பரப்பும் பூச்சிகளைக் கட்டுப்படுத்துவது எப்படி": "pest_control",
            "பாதிக்கப்பட்ட பயிரை அழிக்க வேண்டுமா": "disease_prevention",
            "பாக்டீரியா கருகல் நோய் எவ்வாறு பரவுகிறது": "disease_id",
            "நான் என்ன பாக்டீரியா எதிர்ப்பு மருந்து தெளிக்க வேண்டும்": "disease_treatment",
            "விவசாயக் கருவிகளை எவ்வாறு கிருமி நீக்கம் செய்வது": "disease_prevention",
            "இந்த சேதத்தை ஏற்படுத்தும் பூச்சி எது": "pest_control",
            "எந்த இயற்கை பூச்சி விரட்டி நன்றாக வேலை செய்யும்": "organic_farming",
            "பூச்சிக்கொல்லி தெளிக்க சிறந்த நேரம் எது": "pest_control",
            "பரிந்துரைக்கப்படும் npk உர அளவு என்ன": "fertilizer",
            "பயிர்களுக்கு எவ்வளவு அடிக்கடி நீர் பாய்ச்ச வேண்டும்": "irrigation",
            "கவனிக்க வேண்டிய பொதுவான நோய்கள் என்ன": "disease_id",

            # Malayalam
            "ഈ കുമിൾ രോഗത്തിന് കാരണമെന്താണ്": "disease_id",
            "കുമിൾ രോഗം പടരുന്നത് എങ്ങനെ തടയാം": "disease_prevention",
            "ഏറ്റവും മികച്ച രാസ കുമിൾനാശിനി ഏതാണ്": "disease_treatment",
            "ഏത് വൈറസാണ് ഈ രോഗത്തിന് കാരണം": "disease_id",
            "രോഗം പരത്തുന്ന കീടങ്ങളെ എങ്ങനെ നിയന്ത്രിക്കാം": "pest_control",
            "രോഗം ബാധിച്ച ചെടി നശിപ്പിച്ചു കളയേണ്ടതുണ്ടോ": "disease_prevention",
            "ബാക്ടീരിയൽ വാട്ടം എങ്ങനെയാണ് പടരുന്നത്": "disease_id",
            "ഏത് ബാക്ടീരിയനാശിനിയാണ് തളിക്കേണ്ടത്": "disease_treatment",
            "കാർഷിക ഉപകരണങ്ങൾ എങ്ങനെ അണുവിമുക്തമാക്കാം": "disease_prevention",
            "ഏത് കീടമാണ് ഈ നാശനഷ്ടം ഉണ്ടാക്കുന്നത്": "pest_control",
            "ഏത് ജൈവ കീടനാശിനിയാണ് ഏറ്റവും ഫലപ്രദം": "organic_farming",
            "കീടനാശിനി തളിക്കാൻ ഏറ്റവും അനുയോജ്യമായ സമയം എപ്പോഴാണ്": "pest_control",
            "ശുപാർശ ചെയ്യുന്ന npk വളത്തിന്റെ അളവ് എത്രയാണ്": "fertilizer",
            "വിളകൾ നനയ്ക്കേണ്ടത് എത്ര ദിവസങ്ങളുടെ ഇടവേളകളിലാണ്": "irrigation",
            "ശ്രദ്ധിക്കേണ്ട പ്രധാന രോഗങ്ങൾ ഏതെല്ലാമാണ്": "disease_id"
        }

        best_intent = None
        if message_no_punct in direct_mapping:
            best_intent = direct_mapping[message_no_punct]
        elif message_clean in direct_mapping:
            best_intent = direct_mapping[message_clean]

        if best_intent:
            return self.responses[lang].get(best_intent, self.responses["en"][best_intent])

        # Calculate scores for each intent
        scores = {}
        for intent, patterns in self.keywords.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message_clean):
                    score += 1
            if score > 0:
                scores[intent] = score

        if not scores:
            # General Agronomist fallback response
            fallback_responses = {
                "en": "I understand your interest. As an expert Agronomist, I recommend:\n1. **Inspect** the crop leaf closely for color patterns or insect bites.\n2. **Check soil pH** (ideal pH is 6.0-6.8 for most vegetables, 5.5-6.5 for paddy).\n3. **Use balanced splits** of Nitrogen (Urea), Phosphorus (SSP), and Potassium (MOP) to prevent leaf burn.\n4. **Apply Neem oil (2%)** organic sprays for insects like aphids or whiteflies.\n5. Run a digital scan on the **Leaf Scanner** page for detailed computer vision diagnosis!",
                "kn": "ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಅರ್ಥವಾಯಿತು. ಕೃಷಿ ತಜ್ಞನಾಗಿ ನನ್ನ ಶಿಫಾರಸುಗಳು:\n1. ಎಲೆಗಳ ಬಣ್ಣ ಮತ್ತು ಕೀಟಗಳ ಹಾನಿಯನ್ನು ಸೂಕ್ಷ್ಮವಾಗಿ ಗಮನಿಸಿ.\n2. ಮಣ್ಣಿನ ತೇವಾံಶ ಮತ್ತು pH ಮಟ್ಟವನ್ನು ನಿಯಮಿತವಾಗಿ ಪರೀಕ್ಷಿಸಿ.\n3. ಸಾರಜನಕ, ರಂಜಕ ಮತ್ತು ಪೊಟ್ಯಾಷ್ ಗೊಬ್ಬರಗಳನ್ನು ಹಂತ ಹಂತವಾಗಿ ನೀಡಿ.\n4. ಹೆಚ್ಚಿನ ವಿವರಗಳಿಗೆ ನಮ್ಮ **ಎಲೆ ಸ್ಕ್ಯಾನರ್** ಪುಟದಲ್ಲಿ ಫೋಟೋ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ ನೋಡಿ!",
                "ml": "നിങ്ങളുടെ ചോദ്യം മനസ്സിലായി. കാർഷിക വിദഗ്ദ്ധൻ എന്ന നിലയിലുള്ള എന്റെ നിർദ്ദേശങ്ങൾ:\n1. ഇലകളിലെ കറുത്ത പാടുകളോ കീടങ്ങളുടെ ഉപദ്രവമോ ശ്രദ്ധിക്കുക.\n2. മണ്ണിലെ അമ്ലത്വം (pH) കൃത്യമായ ഇടവേളകളിൽ അളക്കുക.\n3. രാസവളങ്ങൾ ഒന്നിച്ച് പ്രയോഗിക്കാതെ ഘട്ടങ്ങളായി പ്രയോഗിക്കുക.\n4. കൂടുതൽ വിവരങ്ങൾക്ക് **ഇല സ്കാനർ** ഉപയോഗിച്ച് ഫോട്ടോ സ്കാൻ ചെയ്യുക!",
                "hi": "मैं आपकी रुचि समझता हूँ। एक कृषि विशेषज्ञ के रूप में, मैं सलाह देता हूँ:\n1. पत्तियों का रंग और कीटों के लक्षण ध्यान से देखें।\n2. अधिकांश सब्जियों के लिए मिट्टी का पीएच 6.0-6.8 और धान के लिए 5.5-6.5 रखें।\n3. नाइट्रोजन, फास्फोरस और पोटाश खादों को विभाजित मात्रा (splits) में ही डालें।\n4. कीटों से बचाव के लिए 2% नीम के तेल का जैविक छिड़काव करें।\n5. विवरण विश्लेषण के लिए हमारे **लीफ स्कैनर** पेज पर स्कैन करें!",
                "te": "మీ ఆసక్తిని నేను అర్థం చేసుకున్నాను. వ్యవసాయ నిపుణుడిగా నా సూచనలు:\n1. ఆకుల రంగు మార్పులు మరియు పురుగుల ఉనికిని నిశితంగా గమనించండి.\n2. మట్టిలో తేమ మరియు పి.హెచ్ (pH) స్థాయిలను నిరంతరం తనిఖీ చేయండి.\n3. నత్రజని, భాస్వరం మరియు పొటాష్ ఎరువులను దఫదఫాలుగా మాత్రమే వేయండి.\n4. మరిన్ని వివరాల కోసం మన **లీఫ్ స్కానర్** పేజీలో ఫోటో స్కాన్ చేసి విశ్లేషించండి!",
                "ta": "உங்கள் கேள்வியை நான் புரிந்து கொள்கிறேன். விவசாய நிபுணர் என்ற முறையில் எனது பரிந்துரைகள்:\n1. இலைகளின் நிற மாற்றங்கள் அல்லது பூச்சிகளின் தடிமன்களை கவனிக்கவும்.\n2. மண்ணின் ஈரப்பதம் மற்றும் pH அளவுகளை சீராக கண்காணிக்கவும்.\n3. நைட்ரஜன், பாஸ்பரஸ் மற்றும் பொட்டாசியம் உரங்களை தகுந்த இடைவெளியில் இடவும்.\n4. விரிவான விவரங்களுக்கு எங்களது **இலை ஸ்கேனர்** பக்கத்தில் ஸ்கேன் செய்து பார்க்கவும்!"
            }
            return fallback_responses.get(lang, fallback_responses["en"])

        # Find the highest scoring intent
        best_intent = max(scores, key=scores.get)
        
        # Fetch the response
        return self.responses[lang].get(best_intent, self.responses["en"][best_intent])
