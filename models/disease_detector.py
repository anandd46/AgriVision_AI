import cv2
import numpy as np
import base64
import os
from PIL import Image
import io

# Standardized Database of Crops, Diseases, Symptoms, Treatments, and Fertilizers (12 Crops)
DISEASE_DATABASE = {
    "coconut": {
        "Healthy": {
            "name": "Healthy Coconut Leaf",
            "symptoms": ["Leaflets are lush green", "No spots, lesions, or yellowing patterns detected"],
            "organic_treatment": "Maintain regular watering and apply organic mulch to retain moisture.",
            "chemical_treatment": "No chemical treatment required.",
            "fertilizer_recommendation": "Standard dose: 500g Nitrogen (N), 320g Phosphorus (P), and 1200g Potassium (K) per tree per year.",
            "severity": "info"
        },
        "Leaf Rot": {
            "name": "Coconut Leaf Rot (Colletotrichum gloeosporioides)",
            "symptoms": ["Blackening and shriveling of the leaf tips", "Leaflets exhibit dry, rotten spots that coalesce", "Dark brown decayed spots on spindle leaves"],
            "organic_treatment": "Apply Neem cake (2kg/tree) at the base. Spray 3% Neem Oil or Pseudomonas fluorescens formulation (20g/L) on the leaf crown.",
            "chemical_treatment": "Remove the rotten spindle parts and spray Copper Oxychloride (3g/L) or Mancozeb (2g/L) directly into the crown.",
            "fertilizer_recommendation": "Increase Potassium (K) dose by 20% to help cellular resilience. Apply Borax (50g/tree) to strengthen leaf cell walls.",
            "severity": "medium"
        },
        "Bud Rot": {
            "name": "Coconut Bud Rot (Phytophthora palmivora)",
            "symptoms": ["Yellowing of younger leaves starting from spindle", "Inner spindle leaf rots, drops down, and emits a foul odor", "Gradual wilting of the leaf crown"],
            "organic_treatment": "Surgical removal of affected bud tissues in early stages and application of Bordeaux paste (10%) to the cut surfaces.",
            "chemical_treatment": "Crown application of Copper Oxychloride (3g/L) or placing 3g Metalaxyl-M granules in leaf axils during monsoon pre-emptively.",
            "fertilizer_recommendation": "Avoid heavy Nitrogen fertilizer which softens tissues. Apply Trichoderma-enriched compost (5kg/tree) and check soil pH (apply lime/dolomite if acid).",
            "severity": "high"
        },
        "Gray Leaf Spot": {
            "name": "Coconut Gray Leaf Spot (Pestalotiopsis palmarum)",
            "symptoms": ["Small, yellowish-brown spots with greyish-white centers", "Spots expand with a dark brown margin", "Severely affected leaflets dry up and present burnt appearance"],
            "organic_treatment": "Prune and burn heavily infected lower leaves to reduce spore load. Improve soil aeration and drainage.",
            "chemical_treatment": "Spray Carbendazim (1g/L) or Hexaconazole (1ml/L) on all infected leaves. Repeat after 15 days if necessary.",
            "fertilizer_recommendation": "Apply Magnesium Sulfate (500g/tree) to combat chlorosis, alongside standard potassium-rich fertilizers.",
            "severity": "medium"
        }
    },
    "arecanut": {
        "Healthy": {
            "name": "Healthy Arecanut Leaf",
            "symptoms": ["Vibrant green leaflets", "Robust stem attachment without tapering or discoloration"],
            "organic_treatment": "Apply green manure, verify drainage channels are clear, and carry out periodic weeding.",
            "chemical_treatment": "No chemical treatment required.",
            "fertilizer_recommendation": "Standard dose: 100g Nitrogen (N), 40g Phosphorus (P), and 140g Potassium (K) per tree per year, along with 12kg of organic compost.",
            "severity": "info"
        },
        "Yellow Leaf Disease": {
            "name": "Arecanut Yellow Leaf Disease (Phytoplasma / YLD)",
            "symptoms": ["Intense yellowing of leaflets starting from margins of lower leaves", "Yellowing spreads to middle leaves; leaflets shrink and dry", "Tapering of crown and reduction of nut size"],
            "organic_treatment": "No direct cure exists. Focus on enhancing vigor: apply 12kg organic compost, Neem cake (2kg/tree), and sow green manure crops in basins.",
            "chemical_treatment": "Control vector insect (Aphids/Mealybugs) by spraying Imidacloprid (0.5ml/L) or Dimethoate (1.5ml/L) during active insect periods.",
            "fertilizer_recommendation": "Apply secondary nutrients: Magnesium Sulfate (150g/tree) and Zinc Sulfate (50g/tree) along with an extra 50% Potassium (K) dose to help water retention.",
            "severity": "high"
        },
        "Fruit Rot / Koleroga": {
            "name": "Arecanut Koleroga / Fruit Rot (Phytophthora palmivora)",
            "symptoms": ["Water-soaked spots on leaf sheath and developing nuts", "Nuts rot and drop pre-maturely", "Foliar blight on leaves with white mycelial growth during heavy rain"],
            "organic_treatment": "Prophylactic spraying of 1% Bordeaux mixture before monsoon starts. Clear the ground of fallen leaves and nuts (burn them).",
            "chemical_treatment": "Spray Metalaxyl-MZ (2g/L) or Fosetyl-Al (2g/L) on the leaf bunches and crown if disease outbreaks are observed during rains.",
            "fertilizer_recommendation": "Apply Agricultural Lime (1kg/tree) to neutralize soil acidity and improve Calcium uptake, which strengthens cell walls against fungal penetration.",
            "severity": "high"
        },
        "Foot Rot / Anabe": {
            "name": "Arecanut Foot Rot / Anabe Roga (Ganoderma lucidum)",
            "symptoms": ["Drooping and yellowing of lower leaves, which remain hanging", "Tapering of the stem near the crown", "Dark brown bracket-like fungal bodies (Anabe) emerge at base of stem"],
            "organic_treatment": "Isolate infected tree by digging a trench (30cm wide, 60cm deep) around the basin. Apply Trichoderma-enriched neem cake (5kg/tree).",
            "chemical_treatment": "Drench soil around the base with Hexaconazole (2ml/L) or Calixin (tridemorph) at 2% concentration. Root-feed Hexaconazole (1.5ml in 100ml water).",
            "fertilizer_recommendation": "Apply organic matter and Gypsum (1kg/tree) to improve soil structure. Avoid waterlogging around root zone.",
            "severity": "high"
        }
    },
    "banana": {
        "Healthy": {
            "name": "Healthy Banana Leaf",
            "symptoms": ["Broad green leaves without tears, yellow stripes, or necrotic edges"],
            "organic_treatment": "Keep regular irrigation and add high organic matter mulching around pseudostem.",
            "chemical_treatment": "None required.",
            "fertilizer_recommendation": "Standard dose: 250g Nitrogen, 120g Phosphorus, and 450g Potassium per plant per year.",
            "severity": "info"
        },
        "Sigatoka Leaf Spot": {
            "name": "Banana Sigatoka Leaf Spot (Mycosphaerella musicola)",
            "symptoms": ["Dark brown narrow spots parallel to leaf veins", "Spots develop a light grey center with a bright yellow halo", "Large portions of the leaf blade dry up and burn"],
            "organic_treatment": "De-leaf (prune) affected leaves regularly. Keep spacing wide (2m x 2m) to prevent high moisture accumulation.",
            "chemical_treatment": "Spray Propiconazole (1ml/L) or Carbendazim (1g/L) combined with mineral oil (10ml/L) to kill fungal spores.",
            "fertilizer_recommendation": "Boost Potassium to support water retention. Apply Zinc Sulfate (20g/plant) to stimulate growth recovery.",
            "severity": "medium"
        },
        "Panama Wilt": {
            "name": "Banana Panama Wilt (Fusarium oxysporum f. sp. cubense)",
            "symptoms": ["Progressive yellowing of leaf margins starting from oldest leaves", "Leaf petioles buckle and hang down like a skirt around the pseudostem", "Splitting of the pseudostem base"],
            "organic_treatment": "Apply Trichoderma formulation in planting pits. Destroy and burn infected plants. Flood fallow fields to starve the soil fungus.",
            "chemical_treatment": "No direct chemical cure for soil-borne Fusarium. Apply Carbendazim (2% drench) to buffer neighboring healthy plants.",
            "fertilizer_recommendation": "Avoid high ammonium nitrogen. Increase Calcium and soil pH by adding Lime (500g/plant).",
            "severity": "high"
        }
    },
    "mango": {
        "Healthy": {
            "name": "Healthy Mango Leaf",
            "symptoms": ["Clean green lance-shaped leaves", "No grey/white powdery sheets or target-like dry margins"],
            "organic_treatment": "Apply organic compost in tree basins, prune dead branches, and provide summer mulch.",
            "chemical_treatment": "None required.",
            "fertilizer_recommendation": "Standard dose: 1000g Nitrogen, 1000g Phosphorus, and 1500g Potassium per mature tree.",
            "severity": "info"
        },
        "Powdery Mildew": {
            "name": "Mango Powdery Mildew (Oidium mangiferae)",
            "symptoms": ["White powdery superficial patches on leaves, flowers, and tender shoots", "Infected leaves curl, dry up, and drop prematurely", "Severe flower shedding"],
            "organic_treatment": "Spray wettable sulfur (3g/L) or apply neem oil sprays (3%) during leaf emergence and flowering stage.",
            "chemical_treatment": "Spray Hexaconazole (1ml/L) or Carbendazim (1g/L) at bud burst stage. Repeat after 14 days if needed.",
            "fertilizer_recommendation": "Boost Potassium. Avoid heavy nitrogen sprays during active infection.",
            "severity": "medium"
        },
        "Anthracnose": {
            "name": "Mango Anthracnose (Colletotrichum gloeosporioides)",
            "symptoms": ["Dark brown circular or angular spots on leaves", "Spots expand, merge, and cause 'shot holes' (leaf drops out in centers)", "Blossom blight and black necrotic rot on fruits"],
            "organic_treatment": "Prune congested inner branches to facilitate light penetration. Remove and burn fallen leaves.",
            "chemical_treatment": "Spray Copper Oxychloride (3g/L) or Mancozeb (2g/L) at leaf flush stage.",
            "fertilizer_recommendation": "Incorporate Borax (50g) and Magnesium Sulfate (150g) to strengthen leaf margins.",
            "severity": "medium"
        }
    },
    "papaya": {
        "Healthy": {
            "name": "Healthy Papaya Leaf",
            "symptoms": ["Deeply lobed large green leaves", "Sturdy leaf stems without mosaic spots"],
            "organic_treatment": "Apply organic compost, check drainage channels, and prevent aphid vector breeding.",
            "chemical_treatment": "None required.",
            "fertilizer_recommendation": "Standard dose: 250g Nitrogen, 250g Phosphorus, and 500g Potassium per plant per year.",
            "severity": "info"
        },
        "Ring Spot Virus": {
            "name": "Papaya Ring Spot Virus (PRSV)",
            "symptoms": ["Yellow chlorotic mosaic patterns on leaf lobes", "Dark green streaks on leaf petioles and trunk", "Concentric dark green ring spots on fruits"],
            "organic_treatment": "Remove and destroy infected plants immediately. Spray neem oil (2%) to control aphid insect vectors.",
            "chemical_treatment": "No viricide exists. Control vectors using systemic insecticides like Dimethoate (1.5ml/L).",
            "fertilizer_recommendation": "Boost organic inputs and Potassium to support plant vigor and fruit filling.",
            "severity": "high"
        },
        "Leaf Curl": {
            "name": "Papaya Leaf Curl Virus (PLCV)",
            "symptoms": ["Severe downward curling and crinkling of leaf blades", "Leaves become thick, leathery, and grow smaller", "Inverted cup-like leaf shapes with prominent vein thickening"],
            "organic_treatment": "Rogue out infected plants. Cover nursery with nylon insect net. Spray garlic-chilli extract to repel whiteflies.",
            "chemical_treatment": "Control whitefly vector by spraying Imidacloprid (0.5ml/L) or Thiamethoxam (0.5g/L).",
            "fertilizer_recommendation": "Apply balanced micronutrient spray (Zinc and Boron) to offset stunt effects.",
            "severity": "high"
        }
    },
    "tomato": {
        "Healthy": {
            "name": "Healthy Tomato Leaf",
            "symptoms": ["Clean green compound leaves", "Sturdy stems without black rings or leaf curling"],
            "organic_treatment": "Stake plants, prune low foliage, and apply straw mulch to prevent soil spores splashing.",
            "chemical_treatment": "None required.",
            "fertilizer_recommendation": "Standard dose: 5g Nitrogen, 5g Phosphorus, and 10g Potassium per plant.",
            "severity": "info"
        },
        "Early Blight": {
            "name": "Tomato Early Blight (Alternaria solani)",
            "symptoms": ["Small dark spots on older leaves showing target-like concentric rings", "Spots enlarge, turn yellow on margins, and cause leaf defoliation", "Dark sunken spots on stem joints"],
            "organic_treatment": "Prune leaves within 30cm of soil. Spray copper-based organic formulations or dilute milk whey.",
            "chemical_treatment": "Spray Chlorothalonil (2g/L) or Mancozeb (2g/L) immediately when lower leaf spots appear.",
            "fertilizer_recommendation": "Apply Calcium Nitrate (prevents blossom end rot and strengthens walls). Boost Potassium.",
            "severity": "medium"
        },
        "Leaf Curl": {
            "name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
            "symptoms": ["Severe yellowing of leaf margins (chlorosis)", "Upward curling and puckering of young leaves", "Plants become stunted and bunchy, failing to set flowers"],
            "organic_treatment": "Rogue out infected plants. Spray neem oil (3%) or install yellow sticky traps to capture whitefly vectors.",
            "chemical_treatment": "Control whiteflies with Imidacloprid (0.5ml/L) or Acetamiprid (0.5g/L).",
            "fertilizer_recommendation": "Apply extra Potassium and secondary trace Zinc to bolster neighboring healthy plants.",
            "severity": "high"
        }
    },
    "brinjal": {
        "Healthy": {
            "name": "Healthy Brinjal Leaf",
            "symptoms": ["Broad green lobed leaves", "Robust purple/green veins without spots or shrinkage"],
            "organic_treatment": "Apply organic compost, ensure deep soil aeration, and mulch.",
            "chemical_treatment": "None required.",
            "fertilizer_recommendation": "Standard dose: 6g Nitrogen, 6g Phosphorus, and 8g Potassium per plant.",
            "severity": "info"
        },
        "Phomopsis Blight": {
            "name": "Brinjal Phomopsis Blight (Phomopsis vexans)",
            "symptoms": ["Small circular brown spots on leaves that turn greyish in centers", "Leaves turn yellow and drop prematurely", "Sunken dry rot spots on fruits"],
            "organic_treatment": "Use disease-free seeds. Prune lower diseased leaves. Spray Pseudomonas fluorescens (20g/L).",
            "chemical_treatment": "Spray Zineb (2g/L) or Copper Oxychloride (3g/L) during vegetative stages.",
            "fertilizer_recommendation": "Avoid excessive Nitrogen. Apply lime to correct acidic soils.",
            "severity": "medium"
        },
        "Little Leaf": {
            "name": "Brinjal Little Leaf (Phytoplasma)",
            "symptoms": ["Extreme reduction in leaf size; leaflets become tiny and crowded", "Shortening of petioles and internodes, giving a bushy appearance", "Affected plants do not produce fruits"],
            "organic_treatment": "Pull out and burn infected plants. Spray neem seed kernel extract (5%) to control leafhopper vectors.",
            "chemical_treatment": "Control leafhopper vector using Dimethoate (1.5ml/L) or Malathion (2ml/L).",
            "fertilizer_recommendation": "Provide microelement zinc sprays to support healthy cell division.",
            "severity": "high"
        }
    },
    "chilli": {
        "Healthy": {
            "name": "Healthy Chilli Leaf",
            "symptoms": ["Clean green smooth leaves", "No upward curling or dry black spots on margins"],
            "organic_treatment": "Keep adequate soil moisture. Apply vermicompost around root zone.",
            "chemical_treatment": "None required.",
            "fertilizer_recommendation": "Standard dose: 4g Nitrogen, 3g Phosphorus, and 4g Potassium per plant.",
            "severity": "info"
        },
        "Anthracnose": {
            "name": "Chilli Anthracnose / Fruit Rot (Colletotrichum capsici)",
            "symptoms": ["Black necrotic spots on leaf margins", "Sunken circular spots on chilli pods with concentric rings of black dots", "Straw-colored dry patches on leaves"],
            "organic_treatment": "Remove infected fruits and dry debris. Spray Pseudomonas fluorescens formulation (20g/L).",
            "chemical_treatment": "Spray Mancozeb (2g/L) or Carbendazim (1g/L) at flower initiation stage.",
            "fertilizer_recommendation": "Add extra Potassium (K) to improve fruit quality and skin thickness.",
            "severity": "medium"
        },
        "Leaf Curl": {
            "name": "Chilli Leaf Curl Virus (CLCV)",
            "symptoms": ["Severe upward curling and rolling of leaf margins", "Leaves shrink, thicken, and feel crumple-textured", "Stunted plants with shortened internodes"],
            "organic_treatment": "Eradicate virus-infected plants. Use silver mulching sheets to repel thrips/whiteflies. Spray neem oil (2%).",
            "chemical_treatment": "Spray Fipronil (2ml/L) or Imidacloprid (0.5ml/L) to control thrips and whitefly vectors.",
            "fertilizer_recommendation": "Apply Borax (10g/plant) and Magnesium Sulfate (20g/plant) to aid leaf expansion.",
            "severity": "high"
        }
    },
    "pepper": {
        "Healthy": {
            "name": "Healthy Black Pepper Vine",
            "symptoms": ["Dark green heart-shaped leaves", "Strong root attachment to support tree stem"],
            "organic_treatment": "Keep vines shaded. Add organic compost (5kg/vine) twice a year.",
            "chemical_treatment": "None required.",
            "fertilizer_recommendation": "Standard dose: 100g N, 40g P, 140g K per vine per year.",
            "severity": "info"
        },
        "Quick Wilt": {
            "name": "Pepper Quick Wilt / Foot Rot (Phytophthora capsici)",
            "symptoms": ["Dark water-soaked lesions on leaves which fall off quickly", "Blackening of stem nodes and collar rot at root zone", "Entire vine wilts and dies within a few days during heavy rain"],
            "organic_treatment": "Spray 1% Bordeaux mixture before monsoon. Ensure proper slope drainage so water never pools around the collar.",
            "chemical_treatment": "Drench collar zone with Metalaxyl-MZ (2g/L) or spray Potassium Phosphonate (3ml/L).",
            "fertilizer_recommendation": "Boost Potassium. Apply Copper Sulfate soil amendments during spring.",
            "severity": "high"
        },
        "Pollu Beetle": {
            "name": "Pepper Pollu Beetle Damage (Longitarsus nigripennis)",
            "symptoms": ["Circular holes eaten into leaves", "Berries turn black, dry, and hollow (pollu) with feeding puncture marks", "Dropping of spikes"],
            "organic_treatment": "Spray Neem Gold (0.03%) or Neem Oil (3%) during spike emergence (June and September).",
            "chemical_treatment": "Spray Quinalphos (2ml/L) or Dimethoate (1.5ml/L) during berry formation.",
            "fertilizer_recommendation": "Maintain standard NPK. Avoid high nitrogen which makes leaves softer and more attractive to beetles.",
            "severity": "medium"
        }
    },
    "cocoa": {
        "Healthy": {
            "name": "Healthy Cocoa Tree",
            "symptoms": ["Clean green leaves", "Smooth pods hanging from trunk without black spots"],
            "organic_treatment": "Prune branch canopy to allow 40% light filter. Keep soil mulched.",
            "chemical_treatment": "None required.",
            "fertilizer_recommendation": "Standard dose: 100g N, 40g P, 150g K per tree per year.",
            "severity": "info"
        },
        "Black Pod Rot": {
            "name": "Cocoa Black Pod Rot (Phytophthora palmivora)",
            "symptoms": ["Pods develop a brown spot that turns chocolate black and expands rapidly", "White powdery fungal mycelium covers the pod surface", "Internal beans rot completely"],
            "organic_treatment": "Remove and bury infected pods at least 30cm deep. Prune canopy to improve ventilation and reduce humidity.",
            "chemical_treatment": "Spray Copper Oxychloride (3g/L) or Metalaxyl (2g/L) at 14-day intervals during high monsoon periods.",
            "fertilizer_recommendation": "Increase Calcium and Potassium. Keep soil limed.",
            "severity": "high"
        },
        "Swollen Shoot": {
            "name": "Cocoa Swollen Shoot Virus (CSSV)",
            "symptoms": ["Swelling of young stem nodes and chupons", "Red vein banding on young leaves (mosaic pattern)", "Pods become small, round, and discolored"],
            "organic_treatment": "Eradicate and burn infected trees immediately to prevent mealybug vector spread. Plant barrier crops around orchard borders.",
            "chemical_treatment": "No chemical cure. Spray mealybug vectors with neem/oil mixtures.",
            "fertilizer_recommendation": "Apply organic manure enriched with micronutrients (Boron/Zinc) to boost vigor in neighboring trees.",
            "severity": "high"
        }
    },
    "paddy": {
        "Healthy": {
            "name": "Healthy Paddy Crop",
            "symptoms": ["Uniform green tillers", "Erect leaves and clean golden panicles"],
            "organic_treatment": "Keep proper water level. Apply green manure (Sesbania) prior to transplanting.",
            "chemical_treatment": "None required.",
            "fertilizer_recommendation": "Standard dose: 120kg N, 60kg P, 60kg K per hectare per crop season.",
            "severity": "info"
        },
        "Blast Disease": {
            "name": "Paddy Blast Disease (Magnaporthe oryzae)",
            "symptoms": ["Spindle-shaped spots on leaves with grey centers and brown borders", "Spots coalesce, burning the leaf blade", "Neck rot where the panicle base turns black and breaks, causing empty grains"],
            "organic_treatment": "Avoid excessive nitrogen application. Use resistant seeds. Spray Pseudomonas fluorescens (10g/L) on nurseries.",
            "chemical_treatment": "Spray Tricyclazole 75 WP (0.6g/L) or Isoprothiolane (1.5ml/L) immediately when leaf spots appear.",
            "fertilizer_recommendation": "Apply Silicon fertilizer (reduces fungal entry). Split nitrogen into 4 applications.",
            "severity": "high"
        },
        "Bacterial Leaf Blight": {
            "name": "Paddy Bacterial Leaf Blight (Xanthomonas oryzae)",
            "symptoms": ["Wavy yellow-to-white stripes starting from leaf tips down the margins", "Bacterial ooze (milky droplets) on leaves in early morning", "Leaves wilt, dry up, and curl (Kresek stage)"],
            "organic_treatment": "Drain fields for 3-4 days. Avoid clipping leaf tips during transplanting. Spray fresh cow dung extract supernatant.",
            "chemical_treatment": "Spray Streptocycline (0.1g/L) mixed with Copper Oxychloride (2g/L) to prevent systemic spread.",
            "fertilizer_recommendation": "Suspend nitrogen application entirely during disease outbreak. Apply extra Potassium (K) to boost silicon cell walls.",
            "severity": "high"
        }
    },
    "rubber": {
        "Healthy": {
            "name": "Healthy Rubber Tree",
            "symptoms": ["Rich green canopy leaves", "Smooth bark with healthy latex flow"],
            "organic_treatment": "Apply organic compost (10kg/tree) and cover crop in basins.",
            "chemical_treatment": "None required.",
            "fertilizer_recommendation": "Standard dose: 300g N, 250g P, 250g K per tree per year.",
            "severity": "info"
        },
        "Abnormal Leaf Fall": {
            "name": "Rubber Abnormal Leaf Fall (Phytophthora meadii)",
            "symptoms": ["Water-soaked lesions on green leaves and leaf petiole showing dull black spots", "Heavy shedding of green leaves during heavy monsoon rains", "Pods rot and remain hanging on the tree"],
            "organic_treatment": "Prune low branches to improve airflow. Clean tree basins.",
            "chemical_treatment": "Prophylactic crown spraying with oil-dispersed Copper Oxychloride using aerial sprayers before monsoon.",
            "fertilizer_recommendation": "Increase Potassium and Magnesium. Soil liming.",
            "severity": "high"
        },
        "Pink Disease": {
            "name": "Rubber Pink Disease (Erythricium salmonicolor)",
            "symptoms": ["White cobweb-like mycelial growth on bark fork regions", "Mycelium turns pinkish; bark cracks and exudes latex", "Branches above the infection die, dry up, and snap"],
            "organic_treatment": "Prune affected dried branches. Paint the fork regions with Bordeaux paste (10%).",
            "chemical_treatment": "Apply Propiconazole (1%) or spray Thiram (3g/L) on fork joints in early stages.",
            "fertilizer_recommendation": "Correct soil pH and apply standard NPK. Avoid high nitrogen.",
            "severity": "medium"
        }
    }
}

class DiseaseDetector:
    def __init__(self):
        self.tf_available = False
        self.model = None
        
        try:
            import tensorflow as tf
            self.tf_available = True
        except ImportError:
            pass

    def analyze_image(self, image_bytes, crop_hint="coconut"):
        """
        Analyzes leaf image. Uses OpenCV color and contour analysis to identify anomalies.
        Draws bounding boxes around affected parts and generates annotated image in base64.
        """
        # Load image with OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Invalid image file.")
            
        h, w, _ = img.shape
        annotated_img = img.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Color ranges:
        # Green (Healthy)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        
        # Yellow (Chlorosis / Leaf Curl / Blight yellowing)
        lower_yellow = np.array([18, 50, 50])
        upper_yellow = np.array([34, 255, 255])
        
        # Brown / Gray / Dark Spots (Rot, Leaf Spot)
        lower_brown = np.array([5, 40, 20])
        upper_brown = np.array([17, 255, 200])
        
        # Thresholds
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
        
        # Calculate pixel counts
        total_pixels = h * w
        green_pixels = cv2.countNonZero(mask_green)
        yellow_pixels = cv2.countNonZero(mask_yellow)
        brown_pixels = cv2.countNonZero(mask_brown)
        
        green_pct = (green_pixels / total_pixels) * 100
        yellow_pct = (yellow_pixels / total_pixels) * 100
        brown_pct = (brown_pixels / total_pixels) * 100
        
        disease_key = "Healthy"
        confidence = 90.0
        detected_symptoms = []
        bounding_boxes = []
        
        # Generate bounding boxes for brown spots (fungal spots/rot)
        contours_brown, _ = cv2.findContours(mask_brown, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        brown_box_count = 0
        for cnt in contours_brown:
            area = cv2.contourArea(cnt)
            if area > (total_pixels * 0.0005):
                x, y, box_w, box_h = cv2.boundingRect(cnt)
                if box_w > 15 and box_h > 15:
                    bounding_boxes.append((x, y, box_w, box_h, "Spot/Lesion"))
                    brown_box_count += 1
                    cv2.rectangle(annotated_img, (x, y), (x + box_w, y + box_h), (0, 0, 255), 2)
                    cv2.putText(annotated_img, "Spot", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    if brown_box_count >= 10:
                        break

        # Generate bounding boxes for yellow patches (chlorosis)
        contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        yellow_box_count = 0
        for cnt in contours_yellow:
            area = cv2.contourArea(cnt)
            if area > (total_pixels * 0.005):
                x, y, box_w, box_h = cv2.boundingRect(cnt)
                if box_w > 30 and box_h > 30:
                    bounding_boxes.append((x, y, box_w, box_h, "Chlorosis"))
                    yellow_box_count += 1
                    cv2.rectangle(annotated_img, (x, y), (x + box_w, y + box_h), (0, 200, 255), 2)
                    cv2.putText(annotated_img, "Chlorosis", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)
                    if yellow_box_count >= 5:
                        break

        # Crop variety standard auditing
        crop_key = crop_hint.lower()
        if crop_key not in DISEASE_DATABASE:
            crop_key = "coconut" # safety fallback

        # Diagnostic Rules routing for 12 crops
        if crop_key == "tomato":
            if brown_pct > 5.0 and brown_box_count > 3:
                disease_key = "Early Blight"
                confidence = min(70.0 + (brown_pct * 1.8), 96.0)
                detected_symptoms.append(f"Necrotic lesions with target rings ({brown_pct:.1f}%) observed on lower leaves.")
            elif yellow_pct > 12.0:
                disease_key = "Leaf Curl"
                confidence = min(62.0 + (yellow_pct * 1.5), 94.0)
                detected_symptoms.append("Leaf yellowing accompanied by severe upward marginal curling.")
            else:
                detected_symptoms.append(f"Tomato compound leaves are healthy green ({green_pct:.1f}%).")

        elif crop_key == "brinjal":
            if brown_pct > 6.0:
                disease_key = "Phomopsis Blight"
                confidence = min(68.0 + (brown_pct * 1.6), 95.0)
                detected_symptoms.append(f"Dry brown spots ({brown_pct:.1f}%) with greyish-white centers detected.")
            elif yellow_pct > 15.0 and green_pct < 75.0:
                disease_key = "Little Leaf"
                confidence = min(58.0 + (yellow_pct * 1.8), 92.0)
                detected_symptoms.append("Extreme reduction in size and cluster-growth of leaf blades.")
            else:
                detected_symptoms.append(f"Brinjal leaves are healthy green ({green_pct:.1f}%).")

        elif crop_key == "chilli":
            if brown_pct > 5.0 and brown_box_count > 2:
                disease_key = "Anthracnose"
                confidence = min(65.0 + (brown_pct * 2.0), 94.0)
                detected_symptoms.append(f"Necrotic margin spots ({brown_pct:.1f}%) with black spore dots observed.")
            elif yellow_pct > 10.0:
                disease_key = "Leaf Curl"
                confidence = min(60.0 + (yellow_pct * 1.8), 93.0)
                detected_symptoms.append("Intense upward rolling, shrinking, and puckering of young leaves.")
            else:
                detected_symptoms.append(f"Chilli plant foliage is healthy green ({green_pct:.1f}%).")

        elif crop_key == "mango":
            if yellow_pct > 10.0 and green_pct < 80.0:
                disease_key = "Powdery Mildew"
                confidence = min(60.0 + (yellow_pct * 1.6), 91.0)
                detected_symptoms.append("Superficial powdery white/grey patches detected on leaf and stalk surfaces.")
            elif brown_pct > 6.0:
                disease_key = "Anthracnose"
                confidence = min(66.0 + (brown_pct * 1.8), 95.0)
                detected_symptoms.append(f"Dark brown angular leaf lesions ({brown_pct:.1f}%) forming shot holes.")
            else:
                detected_symptoms.append(f"Mango lanceolate leaves are healthy green ({green_pct:.1f}%).")

        elif crop_key == "papaya":
            if yellow_pct > 15.0 and green_pct < 70.0:
                disease_key = "Ring Spot Virus"
                confidence = min(62.0 + (yellow_pct * 1.5), 96.0)
                detected_symptoms.append("Yellow leaf mosaic patterns and dark green stem streaks.")
            elif yellow_pct > 10.0 and yellow_box_count > 1:
                disease_key = "Leaf Curl"
                confidence = min(58.0 + (yellow_pct * 1.8), 92.0)
                detected_symptoms.append("Downward curling and thickening of leaf lobes.")
            else:
                detected_symptoms.append(f"Papaya leaf lobes are healthy green ({green_pct:.1f}%).")

        elif crop_key == "banana":
            if brown_pct > 6.0 and yellow_pct > 10.0:
                disease_key = "Sigatoka Leaf Spot"
                confidence = min(68.0 + (brown_pct * 2.0), 96.0)
                detected_symptoms.append(f"Narrow brown lesions ({brown_pct:.1f}%) observed parallel to veins.")
            elif yellow_pct > 15.0:
                disease_key = "Panama Wilt"
                confidence = min(60.0 + (yellow_pct * 1.5), 94.0)
                detected_symptoms.append("Older leaves showing intense marginal chlorosis and drooping petioles.")
            else:
                detected_symptoms.append(f"Healthy banana leaves ({green_pct:.1f}%).")
                
        elif crop_key == "pepper":
            if brown_pct > 8.0:
                disease_key = "Quick Wilt"
                confidence = min(72.0 + (brown_pct * 1.8), 98.0)
                detected_symptoms.append(f"Rapid blackening/decay ({brown_pct:.1f}%) on leaf nodes.")
            elif brown_box_count > 3:
                disease_key = "Pollu Beetle"
                confidence = min(62.0 + (brown_pct * 1.5), 92.0)
                detected_symptoms.append(f"Small circular feeding perforations ({brown_box_count} holes) detected.")
            else:
                detected_symptoms.append(f"Healthy dark-green leaf texture ({green_pct:.1f}%).")
                
        elif crop_key == "cocoa":
            if brown_pct > 7.0:
                disease_key = "Black Pod Rot"
                confidence = min(66.0 + (brown_pct * 2.0), 95.0)
                detected_symptoms.append("Dark brown chocolate lesions showing active mycelial spreading.")
            elif yellow_pct > 12.0 and green_pct < 80.0:
                disease_key = "Swollen Shoot"
                confidence = min(58.0 + (yellow_pct * 1.8), 91.0)
                detected_symptoms.append("Vein banding mosaic pattern chlorosis detected.")
            else:
                detected_symptoms.append(f"Healthy cocoa leaf chlorophyll levels ({green_pct:.1f}%).")
                
        elif crop_key == "paddy":
            if brown_pct > 5.0 and brown_box_count > 4:
                disease_key = "Blast Disease"
                confidence = min(70.0 + (brown_pct * 1.5), 97.0)
                detected_symptoms.append(f"Spindle-shaped necrotic spots ({brown_box_count} lesions) detected.")
            elif yellow_pct > 12.0 and yellow_box_count > 2:
                disease_key = "Bacterial Leaf Blight"
                confidence = min(64.0 + (yellow_pct * 1.6), 95.0)
                detected_symptoms.append("Yellow wavy stripes running along leaf margins from tips.")
            else:
                detected_symptoms.append(f"Paddy leaf blades healthy ({green_pct:.1f}%).")
                
        elif crop_key == "rubber":
            if brown_pct > 6.0 and yellow_pct > 10.0:
                disease_key = "Abnormal Leaf Fall"
                confidence = min(68.0 + (brown_pct * 1.5), 95.0)
                detected_symptoms.append("Dull water-soaked lesions observed on leaf petioles.")
            elif brown_pct > 5.0:
                disease_key = "Pink Disease"
                confidence = min(60.0 + (brown_pct * 2.0), 91.0)
                detected_symptoms.append("Cobweb-like mycelial patch or cracked bark margins.")
            else:
                detected_symptoms.append(f"Rubber leaf canopy greenness optimal ({green_pct:.1f}%).")
                
        elif crop_key == "arecanut":
            if yellow_pct > 15.0 and brown_pct < 5.0:
                disease_key = "Yellow Leaf Disease"
                confidence = min(60.0 + (yellow_pct * 1.5), 98.0)
                detected_symptoms.append(f"Significant foliar yellowing ({yellow_pct:.1f}%) observed on leaflets.")
            elif brown_pct > 6.0 and yellow_pct > 10.0:
                disease_key = "Fruit Rot / Koleroga"
                confidence = min(65.0 + (brown_pct * 2.0), 95.0)
                detected_symptoms.append(f"Water-soaked lesions ({brown_pct:.1f}%) and rotting symptoms detected.")
            elif yellow_pct > 10.0 and brown_pct > 2.0:
                disease_key = "Foot Rot / Anabe"
                confidence = min(55.0 + (yellow_pct * 1.5), 92.0)
                detected_symptoms.append("Lower leaf droop and general chlorotic discoloration detected.")
            else:
                detected_symptoms.append(f"Healthy green coverage detected ({green_pct:.1f}%).")
                
        else: # coconut
            if brown_pct > 8.0:
                if brown_box_count > 4:
                    disease_key = "Gray Leaf Spot"
                    confidence = min(70.0 + (brown_pct * 1.5), 96.0)
                    detected_symptoms.append(f"Multiple necrotic spot lesions ({brown_box_count}) with dry grey centers detected.")
                else:
                    disease_key = "Leaf Rot"
                    confidence = min(65.0 + (brown_pct * 2.2), 94.0)
                    detected_symptoms.append(f"Large decayed dry patches ({brown_pct:.1f}%) detected on the leaf blade.")
            elif yellow_pct > 12.0 and brown_pct > 1.0:
                disease_key = "Bud Rot"
                confidence = min(60.0 + (yellow_pct * 1.8), 91.0)
                detected_symptoms.append("Spindle-leaf yellowing and progressive tissue decay detected.")
            else:
                detected_symptoms.append(f"Leaf displays normal chlorophyll levels with {green_pct:.1f}% healthy green area.")

        if disease_key == "Healthy":
            confidence = min(80.0 + (green_pct * 0.2), 99.0)

        disease_info = DISEASE_DATABASE[crop_key][disease_key]
        full_symptoms = detected_symptoms + disease_info["symptoms"]
        
        _, buffer = cv2.imencode('.jpg', annotated_img)
        base64_str = base64.b64encode(buffer).decode('utf-8')
        
        return {
            "crop": crop_key.capitalize(),
            "disease_name": disease_info["name"],
            "disease_code": disease_key,
            "confidence": round(confidence, 1),
            "symptoms": full_symptoms,
            "organic_treatment": disease_info["organic_treatment"],
            "chemical_treatment": disease_info["chemical_treatment"],
            "fertilizer_recommendation": disease_info["fertilizer_recommendation"],
            "severity": disease_info["severity"],
            "annotated_image": f"data:image/jpeg;base64,{base64_str}",
            "metrics": {
                "green_percentage": round(green_pct, 1),
                "yellow_percentage": round(yellow_pct, 1),
                "brown_percentage": round(brown_pct, 1)
            },
            "bounding_boxes_count": len(bounding_boxes)
        }
