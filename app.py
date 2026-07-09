

from flask import Flask, render_template, request, jsonify, url_for, session
import os
import sys
import re
import database
from models.disease_detector import DiseaseDetector, DISEASE_DATABASE
from models.agribot import AgriBot
from models.weather import get_live_weather

# Ensure models directory is in python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)
# Initialize chatbot
bot = AgriBot()
app.config['SECRET_KEY'] = 'agricultural-ai-secret-key-12345'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Initialize database tables on startup
database.init_db()

# Initialize detector
detector = DiseaseDetector()

# Standardized Crop Fertilizer baseline requirements (12 Crops)
FERTILIZER_DATABASE = {
    "coconut": {
        "name": "Coconut (Palm)",
        "category": "Palms",
        "unit": "per tree / year",
        "nutrients": {
            "N": 500,
            "P": 320,
            "K": 1200,
            "organic": 50,
            "lime": 1000,
            "boron": 50
        },
        "soil_adjustments": {
            "sandy": {"organic": 20, "K": 15},
            "clayey": {"organic": 0, "drainage_note": "Construct deep mounds and raised bunds to prevent root rot."},
            "laterite": {"lime": 50, "P": 20},
            "loamy": {}
        },
        "splits": 2,
        "splits_schedule": [
            {"time": "Pre-Monsoon (May-June)", "percent": 50, "action": "Incorporate first NPK dose with compost in circular trenches."},
            {"time": "Post-Monsoon (Sept-Oct)", "percent": 50, "action": "Apply second NPK dose under moist soil conditions."}
        ]
    },
    "arecanut": {
        "name": "Arecanut (Palm)",
        "category": "Palms",
        "unit": "per tree / year",
        "nutrients": {
            "N": 100,
            "P": 40,
            "K": 140,
            "organic": 12,
            "lime": 500,
            "magnesium": 150
        },
        "soil_adjustments": {
            "sandy": {"organic": 25, "K": 20},
            "clayey": {"organic": 0, "drainage_note": "Aerate trenches and add sand/compost mixtures."},
            "laterite": {"lime": 40, "P": 15},
            "loamy": {}
        },
        "splits": 2,
        "splits_schedule": [
            {"time": "Pre-Monsoon (May-June)", "percent": 50, "action": "Apply half dose of NPK and complete organic compost."},
            {"time": "Post-Monsoon (Sept-Oct)", "percent": 50, "action": "Apply remaining NPK along with Magnesium Sulfate correctives."}
        ]
    },
    "banana": {
        "name": "Banana / Plantain",
        "category": "Fruits",
        "unit": "per plant / year",
        "nutrients": {
            "N": 250,
            "P": 120,
            "K": 450,
            "organic": 15,
            "lime": 300,
            "zinc": 20
        },
        "soil_adjustments": {
            "sandy": {"organic": 30, "K": 25},
            "clayey": {"organic": -10, "drainage_note": "Extremely critical: Water stagnation causes Panama Wilt outbreaks."},
            "laterite": {"lime": 30, "P": 10},
            "loamy": {}
        },
        "splits": 4,
        "splits_schedule": [
            {"time": "At Planting", "percent": 15, "action": "Mix basal organic compost and entire Phosphorus (SSP) in pit."},
            {"time": "30 Days (Vegetative Stage)", "percent": 25, "action": "Apply first Nitrogen (Urea) and Potassium (MOP) top dressing."},
            {"time": "60 Days (Tillering Stage)", "percent": 30, "action": "Apply second split of Urea and MOP close to root base."},
            {"time": "90 Days (Pre-flowering Stage)", "percent": 30, "action": "Apply final split of Nitrogen, Potassium, and Zinc Sulfate correctives."}
        ]
    },
    "mango": {
        "name": "Mango Tree",
        "category": "Fruits",
        "unit": "per tree / year",
        "nutrients": {
            "N": 1000,
            "P": 1000,
            "K": 1500,
            "organic": 50,
            "lime": 2000,
            "boron": 50
        },
        "soil_adjustments": {
            "sandy": {"organic": 20, "K": 10},
            "clayey": {"drainage_note": "Avoid stagnant water near collar. Prune lower canopy during post-harvest."},
            "laterite": {"lime": 40, "P": 20},
            "loamy": {}
        },
        "splits": 2,
        "splits_schedule": [
            {"time": "Pre-Monsoon (June-July)", "percent": 50, "action": "Apply 1/2 of NPK along with all organic compost in tree basin."},
            {"time": "Post-Monsoon (Sept-Oct)", "percent": 50, "action": "Apply remaining 1/2 of NPK and Borax trace elements."}
        ]
    },
    "papaya": {
        "name": "Papaya",
        "category": "Fruits",
        "unit": "per plant / year",
        "nutrients": {
            "N": 250,
            "P": 250,
            "K": 500,
            "organic": 10,
            "lime": 400,
            "boron": 20
        },
        "soil_adjustments": {
            "sandy": {"organic": 25, "K": 20},
            "clayey": {"organic": -15, "drainage_note": "Papaya roots decay easily. Provide raised ridge planting."},
            "laterite": {"lime": 30, "P": 15},
            "loamy": {}
        },
        "splits": 4,
        "splits_schedule": [
            {"time": "At Transplanting", "percent": 25, "action": "Apply first split of NPK mixed with compost in planting pit."},
            {"time": "2 Months after transplanting", "percent": 25, "action": "Apply second split of NPK around plant roots."},
            {"time": "4 Months after transplanting", "percent": 25, "action": "Apply third NPK split under soil surface."},
            {"time": "6 Months (Fruiting stage)", "percent": 25, "action": "Apply final NPK split along with Boron minerals."}
        ]
    },
    "tomato": {
        "name": "Tomato",
        "category": "Vegetables",
        "unit": "per plant / crop cycle",
        "nutrients": {
            "N": 5,
            "P": 5,
            "K": 10,
            "organic": 2,
            "lime": 50,
            "zinc": 2 # Zinc / Calcium equivalent
        },
        "soil_adjustments": {
            "sandy": {"organic": 30, "K": 20},
            "clayey": {"organic": -10, "drainage_note": "Raised beds are highly recommended to prevent damping-off diseases."},
            "laterite": {"lime": 20, "P": 15},
            "loamy": {}
        },
        "splits": 3,
        "splits_schedule": [
            {"time": "Basal Dressing (Transplanting)", "percent": 30, "action": "Apply 30% Urea, entire SSP, 50% MOP, and all organic compost."},
            {"time": "Active Growth (30 Days)", "percent": 40, "action": "Apply 40% Urea and Calcium/Zinc micronutrients."},
            {"time": "Fruit Development (60 Days)", "percent": 30, "action": "Apply remaining 30% Urea and remaining 50% MOP."}
        ]
    },
    "brinjal": {
        "name": "Brinjal (Eggplant)",
        "category": "Vegetables",
        "unit": "per plant / crop cycle",
        "nutrients": {
            "N": 6,
            "P": 6,
            "K": 8,
            "organic": 2.5,
            "lime": 60,
            "magnesium": 10
        },
        "soil_adjustments": {
            "sandy": {"organic": 20, "K": 15},
            "clayey": {"drainage_note": "Aerate tree basins. Prune weak shoots to improve ventilation."},
            "laterite": {"lime": 30, "P": 15},
            "loamy": {}
        },
        "splits": 3,
        "splits_schedule": [
            {"time": "Basal Dressing (Transplanting)", "percent": 30, "action": "Apply half of Potassium, all Phosphorus, and 1/3 of Nitrogen."},
            {"time": "Active Growth (30 Days)", "percent": 40, "action": "Apply second split of Nitrogen and Magnesium Sulfate correctives."},
            {"time": "Fruit Setting (60 Days)", "percent": 30, "action": "Apply remaining Nitrogen and remaining half of Potassium."}
        ]
    },
    "chilli": {
        "name": "Chilli / Capsicum",
        "category": "Vegetables",
        "unit": "per plant / crop cycle",
        "nutrients": {
            "N": 4,
            "P": 3,
            "K": 4,
            "organic": 1.5,
            "lime": 40,
            "boron": 5
        },
        "soil_adjustments": {
            "sandy": {"organic": 25, "K": 20},
            "clayey": {"organic": -10, "drainage_note": "Mulch soil to prevent thrips pupation in soil cracks."},
            "laterite": {"lime": 20, "P": 10},
            "loamy": {}
        },
        "splits": 3,
        "splits_schedule": [
            {"time": "Basal Dressing (Transplanting)", "percent": 30, "action": "Apply entire Phosphorus, 1/3 of Nitrogen, and half of Potassium."},
            {"time": "Active Growth (30 Days)", "percent": 45, "action": "Apply second split of Nitrogen and Borax minerals."},
            {"time": "Fruit Setting (60 Days)", "percent": 25, "action": "Apply remaining Nitrogen and remaining half of Potassium."}
        ]
    },
    "pepper": {
        "name": "Black Pepper",
        "category": "Spices",
        "unit": "per vine / year",
        "nutrients": {
            "N": 100,
            "P": 40,
            "K": 140,
            "organic": 5,
            "lime": 200,
            "magnesium": 50
        },
        "soil_adjustments": {
            "sandy": {"organic": 20, "K": 15},
            "clayey": {"organic": -15, "drainage_note": "Improve drainage around base support tree collar."},
            "laterite": {"lime": 50, "P": 20},
            "loamy": {}
        },
        "splits": 2,
        "splits_schedule": [
            {"time": "Pre-Monsoon (May-June)", "percent": 50, "action": "Incorporate organic manure and first split of NPK around root zone."},
            {"time": "Post-Monsoon (Sept-Oct)", "percent": 50, "action": "Apply second split of NPK and Magnesium Sulfate."}
        ]
    },
    "cocoa": {
        "name": "Cocoa",
        "category": "Beverages",
        "unit": "per tree / year",
        "nutrients": {
            "N": 100,
            "P": 40,
            "K": 150,
            "organic": 10,
            "lime": 400,
            "boron": 15
        },
        "soil_adjustments": {
            "sandy": {"organic": 15, "K": 10},
            "clayey": {"organic": 0, "drainage_note": "Aerate tree basins and prevent canopy over-shading."},
            "laterite": {"lime": 30, "P": 15},
            "loamy": {}
        },
        "splits": 2,
        "splits_schedule": [
            {"time": "Pre-Monsoon (May-June)", "percent": 50, "action": "Apply half NPK and all organic compost."},
            {"time": "Post-Monsoon (Sept-Oct)", "percent": 50, "action": "Apply remaining NPK and Borax correctives."}
        ]
    },
    "paddy": {
        "name": "Paddy (Rice)",
        "category": "Cereals",
        "unit": "per hectare / crop season",
        "nutrients": {
            "N": 120000,
            "P": 60000,
            "K": 60000,
            "organic": 5000,
            "lime": 500000,
            "zinc": 25000
        },
        "soil_adjustments": {
            "sandy": {"organic": 20, "K": 30},
            "clayey": {"drainage_note": "Paddy tolerates clay well. Keep water level at 5cm during active tillering."},
            "laterite": {"lime": 20, "P": 25},
            "loamy": {}
        },
        "splits": 3,
        "splits_schedule": [
            {"time": "Basal Dressing (At transplanting)", "percent": 30, "action": "Apply 30% Nitrogen, entire Phosphorus, and half Potassium."},
            {"time": "Active Tillering (30 Days)", "percent": 40, "action": "Apply second split of Nitrogen and Zinc Sulfate correctives."},
            {"time": "Panicle Initiation (60 Days)", "percent": 30, "action": "Apply remaining Nitrogen and remaining half Potassium."}
        ]
    },
    "rubber": {
        "name": "Rubber Tree",
        "category": "Plantation",
        "unit": "per tree / year",
        "nutrients": {
            "N": 300,
            "P": 250,
            "K": 250,
            "organic": 10,
            "lime": 500,
            "magnesium": 100
        },
        "soil_adjustments": {
            "sandy": {"organic": 25, "K": 20},
            "clayey": {"organic": -10, "drainage_note": "Construct deep terraced drains on slopes."},
            "laterite": {"lime": 40, "P": 15},
            "loamy": {}
        },
        "splits": 2,
        "splits_schedule": [
            {"time": "Pre-Monsoon (April-May)", "percent": 50, "action": "Apply first split of NPK in shallow circular channels."},
            {"time": "Post-Monsoon (Sept-Oct)", "percent": 50, "action": "Apply second split of NPK and Magnesium Sulfate."}
        ]
    }
}

# --- Web Page Routes ---

@app.route('/')
def dashboard():
    history = database.get_scan_history(limit=15)
    all_scans = database.get_scan_history(limit=1000)
    total_scans = len(all_scans)
    
    active_infections = 0
    healthy_scans = 0
    
    for scan in all_scans:
        if scan['disease_code'] == 'Healthy':
            healthy_scans += 1
        elif scan['status'] in ['Pending', 'Monitoring']:
            active_infections += 1
            
    healthy_rate = "100%"
    if total_scans > 0:
        healthy_rate = f"{round((healthy_scans / total_scans) * 100)}%"
        
    location = session.get('location', 'Mysuru')
    try:
        weather_data = get_live_weather(location)
    except Exception as e:
        print(f"Error fetching live weather: {e}")
        weather_data = {
            "location": location,
            "temperature": "28°C",
            "humidity": "74%",
            "weather_condition": "Partly Cloudy",
            "soil_moisture": "Moderate (38%)"
        }
        
    stats = {
        "location": weather_data.get("location", location),
        "temperature": weather_data.get("temperature", "28°C"),
        "humidity": weather_data.get("humidity", "74%"),
        "soil_moisture": weather_data.get("soil_moisture", "Moderate (38%)"),
        "weather_condition": weather_data.get("weather_condition", "Partly Cloudy"),
        "scans_today": total_scans,
        "active_alerts": active_infections,
        "crop_health_index": healthy_rate
    }
    return render_template('dashboard.html', stats=stats, history=history)

@app.route('/scan', methods=['GET'])
def scan_page():
    return render_template('scan.html')

@app.route('/fertilizer', methods=['GET'])
def fertilizer_page():
    return render_template('fertilizer.html')

@app.route('/calendar', methods=['GET'])
def calendar_page():
    return render_template('calendar.html')

@app.route('/library')
def library_page():
    from models.agri_data import BEGINNER_GUIDE, FAQ_DATABASE
    return render_template('library.html', database=DISEASE_DATABASE, beginner_guide=BEGINNER_GUIDE, faq_database=FAQ_DATABASE)

@app.route('/api-docs')
def api_docs_page():
    return render_template('api_docs.html')

# --- API Endpoints ---

@app.route('/api/scan', methods=['POST'])
def api_scan():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided."}), 400
        
    file = request.files['image']
    crop = request.form.get('crop', 'coconut').lower()
    lang = request.form.get('lang', 'en').lower().strip()
    
    if crop not in FFERTILIZER_DATABASE:
        # FERTILIZER_DATABASE is the local name, let's check
        pass
    # Wait, let's keep the exact check from original code: FERTILIZER_DATABASE
    if crop not in FERTILIZER_DATABASE:
        return jsonify({"error": f"Unsupported crop variety: '{crop}'"}), 400
        
    if file.filename == '':
        return jsonify({"error": "Empty filename."}), 400
        
    try:
        image_bytes = file.read()
        result = detector.analyze_image(image_bytes, crop_hint=crop)
        
        database.save_scan(
            crop=result['crop'],
            disease_code=result['disease_code'],
            disease_name=result['disease_name'],
            confidence=result['confidence'],
            severity=result['severity'],
            symptoms=result['symptoms'],
            organic=result['organic_treatment'],
            chemical=result['chemical_treatment'],
            green_pct=result['metrics']['green_percentage'],
            yellow_pct=result['metrics']['yellow_percentage'],
            brown_pct=result['metrics']['brown_percentage']
        )
        
        # Categorize disease for follow-up questions
        disease_code = result['disease_code']
        fungal_diseases = [
            "Leaf Rot", "Bud Rot", "Gray Leaf Spot", "Fruit Rot / Koleroga", "Foot Rot / Anabe",
            "Sigatoka Leaf Spot", "Powdery Mildew", "Anthracnose", "Phomopsis Blight", 
            "Quick Wilt", "Black Pod Rot", "Blast Disease", "Abnormal Leaf Fall", "Pink Disease"
        ]
        viral_diseases = ["Ring Spot Virus", "Leaf Curl", "Swollen Shoot", "Little Leaf"]
        bacterial_diseases = ["Bacterial Leaf Blight"]
        pest_diseases = ["Pollu Beetle"]
        
        if disease_code == "Healthy":
            category = "healthy"
        elif disease_code in fungal_diseases:
            category = "fungal"
        elif disease_code in viral_diseases:
            category = "viral"
        elif disease_code in bacterial_diseases:
            category = "bacterial"
        elif disease_code in pest_diseases:
            category = "pest"
        else:
            category = "healthy"
            
        category_question_keys = {
            "fungal": ["q_fungal_cause", "q_fungal_prevent", "q_fungal_chemical"],
            "viral": ["q_viral_cause", "q_viral_vector", "q_viral_destroy"],
            "bacterial": ["q_bacterial_cause", "q_bacterial_spray", "q_bacterial_prevent"],
            "pest": ["q_pest_cause", "q_pest_organic", "q_pest_spray"],
            "healthy": ["q_healthy_npk", "q_healthy_water", "q_healthy_disease"]
        }
        result['follow_up_questions'] = category_question_keys.get(category, category_question_keys["healthy"])
        
        # Map severity to priority translation keys
        severity_map = {
            "high": "priority_high",
            "medium": "priority_medium",
            "info": "priority_info"
        }
        result['priority_key'] = severity_map.get(result['severity'], "priority_info")
        
        # Weather-aware recommendations & regional tips
        location = session.get('location', 'Mysuru')
        try:
            weather_data = get_live_weather(location)
            from models.weather import get_weather_tips
            result['weather_tips'] = get_weather_tips(weather_data, lang)
            result['weather_data'] = weather_data
        except Exception as we:
            print(f"Weather fetch error in scan API: {we}")
            result['weather_tips'] = ""
            result['weather_data'] = None
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500

@app.route('/api/fertilizer', methods=['POST'])
def api_fertilizer():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No parameters provided."}), 400
        
    crop = data.get('crop', '').lower()
    age = data.get('age')
    soil = data.get('soil', 'loamy').lower()
    health_status = data.get('health_status', 'Healthy')
    
    if crop not in FERTILIZER_DATABASE:
        return jsonify({"error": f"Crop '{crop}' not supported."}), 400
        
    try:
        age = float(age)
    except (TypeError, ValueError):
        return jsonify({"error": "Age must be a numeric value."}), 400
        
    base = FERTILIZER_DATABASE[crop]["nutrients"]
    adjustments = FERTILIZER_DATABASE[crop]["soil_adjustments"].get(soil, {})
    
    # Scale based on crop parameters
    if crop == "paddy":
        scale_factor = 1.0  # Paddy does not scale by age
    elif crop in ["tomato", "brinjal", "chilli"]:
        scale_factor = min(1.0, age / 1.0) # Veggies mature in 1 season
    elif crop == "rubber":
        scale_factor = min(1.0, age / 7.0)
    elif crop == "banana":
        scale_factor = min(1.0, age / 1.0)
    else: # Palms, cocoa, mango, pepper
        maturity_age = 10 if crop == "mango" else 5
        if crop == "arecanut": maturity_age = 4
        scale_factor = min(1.0, age / maturity_age)
        
    n_final = base["N"] * scale_factor
    p_final = base["P"] * scale_factor
    k_final = base["K"] * scale_factor
    org_final = base["organic"] * scale_factor
    lime_final = base.get("lime", 0) * scale_factor
    
    # Soil Adjustments
    soil_note = adjustments.get("drainage_note", "")
    if "organic" in adjustments:
        org_final *= (1 + adjustments["organic"] / 100)
    if "K" in adjustments:
        k_final *= (1 + adjustments["K"] / 100)
    if "P" in adjustments:
        p_final *= (1 + adjustments["P"] / 100)
    if "lime" in adjustments:
        lime_final *= (1 + adjustments["lime"] / 100)

    # Health Condition Multipliers
    health_note = "Regular maintenance dose."
    zinc_corrective = base.get("zinc", 0)
    boron_corrective = base.get("boron", 0)
    magnesium_corrective = base.get("magnesium", 0)

    if health_status == 'Fungal':
        k_final *= 1.20      # boost cellular walls
        org_final *= 1.15
        health_note = "Fungal Infection Alert: Potassium boosted by 20% to fortify crop cells. Increase organic manure to stimulate beneficial soil bacteria."
    elif health_status == 'Pest':
        n_final *= 0.85      # reduce soft leaves
        k_final *= 1.10
        health_note = "Pest Infestation Alert: Nitrogen reduced by 15% to slow down tender leaf shoots which attract pests. Potassium raised to support recovery."
    elif health_status == 'Deficiency':
        n_final *= 1.10
        p_final *= 1.10
        k_final *= 1.10
        zinc_corrective *= 1.5
        boron_corrective *= 1.5
        magnesium_corrective *= 1.5
        health_note = "Nutrient Deficiency Alert: Primary NPK targets raised by 10%. Application of micronutrients (Boron, Zinc, Magnesium) is mandatory."
    elif health_status == 'Stress':
        n_final *= 0.90      # avoid root burn
        org_final *= 1.20
        health_note = "Climate Stress (Drought/Waterlogged): Nitrogen reduced by 10% to prevent root burn. Organic manure raised to improve soil carbon and drainage."

    # Convert pure N, P, K targets to commercial fertilizer weights
    urea_final = n_final / 0.46
    ssp_final = p_final * 14.3
    mop_final = k_final * 2.0

    # Build crop splits schedule
    splits_count = FERTILIZER_DATABASE[crop]["splits"]
    base_schedule = FERTILIZER_DATABASE[crop]["splits_schedule"]
    calculated_splits = []
    
    for split in base_schedule:
        pct = split["percent"] / 100.0
        calculated_splits.append({
            "time": split["time"],
            "percent": split["percent"],
            "action": split["action"],
            "urea_split_g": round(urea_final * pct),
            "ssp_split_g": round(ssp_final * pct),
            "mop_split_g": round(mop_final * pct)
        })

    result = {
        "crop": crop,
        "crop_fullname": FERTILIZER_DATABASE[crop]["name"],
        "unit": FERTILIZER_DATABASE[crop]["unit"],
        "age": age,
        "soil_type": soil.capitalize(),
        "health_status": health_status,
        "pure_nutrients": {
            "nitrogen_N_g": round(n_final),
            "phosphorus_P_g": round(p_final),
            "potassium_K_g": round(k_final)
        },
        "recommendations": {
            "urea_g": round(urea_final),
            "ssp_g": round(ssp_final),
            "mop_g": round(mop_final),
            "organic_manure_kg": round(org_final, 1),
            "lime_dolomite_g": round(lime_final)
        },
        "special_nutrients": {
            "borax_g": round(boron_corrective * scale_factor),
            "zinc_sulfate_g": round(zinc_corrective * scale_factor),
            "magnesium_sulfate_g": round(magnesium_corrective * scale_factor)
        },
        "splits_count": splits_count,
        "splits_schedule": calculated_splits,
        "notes": {
            "soil_note": soil_note,
            "health_note": health_note,
            "application_method": "Apply in circular basins dug around the crop base. Incorporate with soil, mulch, and irrigate immediately."
        }
    }
    
    return jsonify(result)

@app.route('/api/history/update', methods=['POST'])
def api_update_history():
    data = request.get_json()
    if not data or 'id' not in data or 'status' not in data:
        return jsonify({"error": "Missing parameters."}), 400
        
    success = database.update_scan_status(data['id'], data['status'])
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Failed to update record."}), 404

@app.route('/api/weather', methods=['POST'])
def api_weather():
    data = request.get_json()
    if not data or 'location' not in data:
        return jsonify({"error": "Location parameter is required."}), 400
        
    location = data.get('location', '').strip()
    if not location:
        return jsonify({"error": "Location cannot be empty."}), 400
        
    try:
        weather_data = get_live_weather(location)
        session['location'] = weather_data.get('location', location)
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch weather: {str(e)}"}), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Message is empty."}), 400
        
    user_msg = data.get('message', '').strip()
    lang = data.get('lang', 'en').strip()
    
    is_weather_query = False
    user_msg_lower = user_msg.lower()
    
    for pattern in bot.keywords.get("weather", []):
        if re.search(pattern, user_msg_lower):
            is_weather_query = True
            break
            
    regional_weather_keywords = [
        "weather", "forecast", "rain", "temperature", "climate", "condition", "humidity",
        "ಹವಾಮಾನ", "ಮಳೆ", "ತಾಪಮಾನ", "ಮಳೆಯ",
        "मौसम", "बारिश", "तापमान", "वर्षा",
        "వాతావరణం", "వర్షం", "ఉష్ణోగ్రత",
        "வானிலை", "மழை", "வெப்பநிலை",
        "കാലാവസ്ഥ", "മഴ", "ചൂട്"
    ]
    if not is_weather_query:
        if any(kw in user_msg_lower for kw in regional_weather_keywords):
            is_weather_query = True
            
    if is_weather_query:
        def extract_location(message):
            text = re.sub(r'[?.,!:]', ' ', message).strip()
            match = re.search(r'(?:weather|forecast|temperature|humidity|climate|condition|conditions|in|at|for|of|near)\s+([a-zA-Z]{3,}(?:\s+[a-zA-Z]{3,})*)', text, re.IGNORECASE)
            if match:
                loc = match.group(1).strip()
                stopwords = {"today", "tomorrow", "now", "here", "karnataka", "kerala", "tamilnadu", "india"}
                if loc.lower() not in stopwords:
                    return loc
            match_rev = re.search(r'\b([a-zA-Z]{3,}(?:\s+[a-zA-Z]{3,})*)\s+(?:weather|forecast|temperature|climate|conditions)\b', text, re.IGNORECASE)
            if match_rev:
                loc = match_rev.group(1).strip()
                stopwords = {"today", "tomorrow", "now", "here", "local", "current", "live"}
                if loc.lower() not in stopwords:
                    return loc
            return None
            
        loc = extract_location(user_msg)
        if not loc:
            loc = session.get('location', 'Mysuru')
            
        try:
            weather_data = get_live_weather(loc)
            weather_responses = {
                "en": "🌤️ **Live Weather in {location}**:\n- **Temperature**: {temperature}\n- **Humidity**: {humidity}\n- **Condition**: {weather_condition}\n- **Soil Moisture**: {soil_moisture}\n\n*Agronomy Tip*: If rain is expected or soil moisture is high, avoid spraying chemical fungicides/pesticides or over-irrigating.",
                "kn": "🌤️ **{location} ನಲ್ಲಿ ನೇರ ಹವಾಮಾನ ವರದಿ**:\n- **ತಾಪಮಾನ**: {temperature}\n- **ಗಾಳಿಯ ತೇವಾಂಶ**: {humidity}\n- **ಹವಾಮಾನ ಸ್ಥಿತಿ**: {weather_condition}\n- **ಮಣ್ಣಿನ ತೇವಾಂಶ**: {soil_moisture}\n\n*ಸಲಹೆ*: ಮಳೆ ಬರುವ ಮುನ್ಸೂಚನೆ ಇದ್ದರೆ ಅಥವಾ ಮಣ್ಣಿನಲ್ಲಿ ಹೆಚ್ಚಿನ ತೇವಾंಶವಿದ್ದರೆ, ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಬೇಡಿ ಮತ್ತು ನೀರಾವರಿ ನಿಲ್ಲಿಸಿ.",
                "ml": "🌤️ **{location}-ലെ തത്സമയ കാലാവസ്ഥ**:\n- **താപനില**: {temperature}\n- **അന്തരീക്ഷ ഈർപ്പം**: {humidity}\n- **കാലാവസ്ഥാ അവസ്ഥ**: {weather_condition}\n- **മണ്ണിലെ ഈർപ്പം**: {soil_moisture}\n\n*നിർദ്ദേശം*: മഴ പെയ്യാൻ സാധ്യതയുള്ളപ്പോഴോ മണ്ണിൽ അമിത ഈർപ്പമുള്ളപ്പോഴോ രാസവളങ്ങളും കീടനാശിനികളും തളിക്കരുത്.",
                "hi": "🌤️ **{location} में लाइव मौसम की स्थिति**:\n- **तापमान**: {temperature}\n- **आर्द्रता**: {humidity}\n- **मौसम**: {weather_condition}\n- **मिट्टी की नमी**: {soil_moisture}\n\n*सुझाव*: यदि बारिश की संभावना हो या मिट्टी में नमी अधिक हो, तो सिंचाई रोक दें और कीटनाशकों का छिड़काव न करें।",
                "te": "🌤️ **{location} లో ప్రస్తుత వాతావరణం**:\n- **ఉష్ణోగ్రత**: {temperature}\n- **తేమ శాతం**: {humidity}\n- **వాతావరణ పరిస్థితి**: {weather_condition}\n- **మట్టి తేమ**: {soil_moisture}\n\n*సలహా*: వర్ష సూచన ఉన్నప్పుడు లేదా నేలలో తేమ ఎక్కువగా ఉన్నప్పుడు ఎరువుల పిచికారీ మరియు నీటి తడులు నిలిపివేయండి.",
                "ta": "🌤️ **{location}-ல் நேரடி வானிலை நிலவரம்**:\n- **வெப்பநிலை**: {temperature}\n- **ஈரப்பதம்**: {humidity}\n- **வானிலை நிலை**: {weather_condition}\n- **மண் ஈரப்பதம்**: {soil_moisture}\n\n*விவசாய ஆலோசனை*: மழை பெய்யும் வாய்ப்பு இருந்தாலோ அல்லது மண்ணில் அதிக ஈரப்பதம் இருந்தாலோ, மருந்து தெளிப்பதையோ அல்லது நீர் பாய்ச்சுவதையோ தவிர்க்கவும்."
            }
            lang_code = lang.lower().strip()
            if lang_code not in weather_responses:
                lang_code = "en"
            reply = weather_responses[lang_code].format(
                location=weather_data["location"],
                temperature=weather_data["temperature"],
                humidity=weather_data["humidity"],
                weather_condition=weather_data["weather_condition"],
                soil_moisture=weather_data["soil_moisture"]
            )
        except Exception as ex:
            print(f"Chatbot weather retrieval error: {ex}")
            reply = bot.respond(user_msg, lang=lang)
    else:
        reply = bot.respond(user_msg, lang=lang)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
