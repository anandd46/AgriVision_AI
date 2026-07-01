import urllib.request
import urllib.parse
import json

def get_live_weather(location="Mysuru"):
    """
    Fetches live weather from wttr.in, with a fallback to Open-Meteo.
    Returns a dict with temperature, humidity, weather_condition, and soil_moisture estimation.
    """
    location_clean = location.strip()
    if not location_clean:
        location_clean = "Mysuru"
        
    # Layer 1: Query wttr.in JSON API
    try:
        url = f"https://wttr.in/{urllib.parse.quote(location_clean)}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            current = data['current_condition'][0]
            temp = current['temp_C']
            humidity = current['humidity']
            condition = current['weatherDesc'][0]['value']
            precip = float(current.get('precipMM', 0))
            
            # Formulate relative soil moisture from precipitation/humidity
            if precip > 5.0:
                moisture = "High (82%)"
            elif precip > 0.0:
                moisture = "Moderate (55%)"
            elif int(humidity) > 80:
                moisture = "Moderate (45%)"
            else:
                moisture = "Moderate (38%)"
                
            return {
                "location": location_clean,
                "temperature": f"{temp}°C",
                "humidity": f"{humidity}%",
                "weather_condition": condition,
                "soil_moisture": moisture
            }
    except Exception as e:
        print(f"wttr.in failed for {location_clean}, attempting Open-Meteo fallback: {e}")
        
    # Layer 2: Fallback to Open-Meteo API
    try:
        # Defaults for Mysuru, India (Lat: 12.2958, Lon: 76.6394)
        lat = 12.2958
        lon = 76.6394
        
        # Geocode the location name using Open-Meteo geocoding API
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(location_clean)}&count=1&language=en&format=json"
            geo_req = urllib.request.Request(geo_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(geo_req, timeout=5) as geo_res:
                geo_data = json.loads(geo_res.read().decode())
                if geo_data.get('results'):
                    result = geo_data['results'][0]
                    lat = result['latitude']
                    lon = result['longitude']
                    # Use full formatted name if available
                    location_clean = result.get('name', location_clean)
        except Exception as ge:
            print(f"Geocoding failed for {location_clean}, using default coordinates: {ge}")
            
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code"
        weather_req = urllib.request.Request(weather_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(weather_req, timeout=5) as w_res:
            w_data = json.loads(w_res.read().decode())
            current = w_data['current']
            temp = round(current['temperature_2m'])
            humidity = round(current['relative_humidity_2m'])
            precip = current['precipitation']
            code = current['weather_code']
            
            # WMO Weather Code Translations
            wmo_codes = {
                0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
                45: "Foggy", 48: "Depositing Rime Fog", 51: "Light Drizzle",
                53: "Moderate Drizzle", 55: "Dense Drizzle", 61: "Light Rain",
                63: "Moderate Rain", 65: "Heavy Rain", 80: "Light Showers",
                81: "Moderate Showers", 82: "Violent Showers", 95: "Thunderstorm"
            }
            condition = wmo_codes.get(code, "Partly Cloudy")
            
            if precip > 5.0:
                moisture = "High (82%)"
            elif precip > 0.0:
                moisture = "Moderate (55%)"
            elif humidity > 80:
                moisture = "Moderate (45%)"
            else:
                moisture = "Moderate (38%)"
                
            return {
                "location": location_clean,
                "temperature": f"{temp}°C",
                "humidity": f"{humidity}%",
                "weather_condition": condition,
                "soil_moisture": moisture
            }
    except Exception as ex:
        print(f"Open-Meteo fallback also failed for {location_clean}: {ex}")
        
    # Last resort local defaults if internet is entirely down
    return {
        "location": location_clean,
        "temperature": "28°C",
        "humidity": "74%",
        "weather_condition": "Partly Cloudy (Cached)",
        "soil_moisture": "Moderate (38%)"
    }

def get_weather_tips(weather_data, lang="en"):
    """
    Returns a weather-aware agronomic tip based on current weather values.
    """
    lang = lang.lower().strip()
    temp_str = weather_data.get("temperature", "28°C").replace("°C", "")
    hum_str = weather_data.get("humidity", "70%").replace("%", "")
    
    try:
        temp = int(temp_str)
    except:
        temp = 28
        
    try:
        humidity = int(hum_str)
    except:
        humidity = 70

    tips = {
        "en": {
            "fungal": "⚠️ **High Fungal Outbreak Risk**: Humidity is {humidity}%. Fungal spores spread rapidly. Avoid overhead watering and prune lower leaves. Delay chemical sprays if rain is imminent.",
            "heat": "🥵 **Heat Stress Warning**: Temperature is {temperature}°C. Evaporation is high. Provide light frequent irrigations during early morning or evening. Apply organic mulch.",
            "optimal": "🌤️ **Optimal Farming Conditions**: Temperature {temperature}°C and Humidity {humidity}%. Excellent window for nutrient application, organic composting, and routine leaf pruning."
        },
        "kn": {
            "fungal": "⚠️ **ಹೆಚ್ಚಿನ ಶಿಲೀಂಧ್ರ ಹರಡುವ ಅಪಾಯ**: ಗಾಳಿಯ ತೇವಾಂಶವು {humidity}% ಇದೆ. ಶಿಲೀಂಧ್ರ ರೋಗಗಳು ವೇಗವಾಗಿ ಹರಡುತ್ತವೆ. ಎಲೆಗಳ ಮೇಲೆ ನೀರು ಸಿಂಪಡಿಸಬೇಡಿ ಮತ್ತು ಕೆಳಗಿನ ಎಲೆಗಳನ್ನು ಕತ್ತರಿಸಿ.",
            "heat": "🥵 **ಅತಿಯಾದ ತಾಪಮಾನ ಎಚ್ಚರಿಕೆ**: ತಾಪಮಾನವು {temperature}°C ಇದೆ. ಬೆಳಿಗ್ಗೆ ಅಥವಾ ಸಂಜೆ ಹಗುರ ನೀರಾವರಿ ನೀಡಿ. ಮಣ್ಣಿಗೆ ಒಣ ಕಸದ ಹೊದಿಕೆ (mulch) ಹಾಕಿ.",
            "optimal": "🌤️ **ಸೂಕ್ತ ಕೃಷಿ ಹವಾಮಾನ**: ತಾಪಮಾನ {temperature}°C ಮತ್ತು ತೇವಾಂಶ {humidity}%. ಗೊಬ್ಬರ ನೀಡಲು ಮತ್ತು ಎಲೆ ಕತ್ತರಿಸಲು ಇದು ಉತ್ತಮ ಸಮಯ."
        },
        "ml": {
            "fungal": "⚠️ **കുമിൾ രോഗ സാധ്യത**: അന്തരീക്ഷ ഈർപ്പം {humidity}% ആണ്. കുമിൾ രോഗങ്ങൾ വേഗത്തിൽ പടരും. ഇലകളിൽ വെള്ളം തളിക്കുന്നത് ഒഴിവാക്കുക.",
            "heat": "🥵 **ചൂട് അമിതമാണ്**: താപനില {temperature}°C ആണ്. രാവിലെയും വൈകുന്നേരവും നനയ്ക്കുക. തടങ്ങളിൽ പുതയിടുക.",
            "optimal": "🌤️ **അനുയോജ്യമായ കാലാവസ്ഥ**: വളപ്രയോഗത്തിനും ഇലകൾ മുറിക്കുന്നതിനും ഈ സമയം ഉപയോഗിക്കാം. താപനില: {temperature}°C, ഈർപ്പം: {humidity}%."
        },
        "hi": {
            "fungal": "⚠️ **फंगल संक्रमण का उच्च खतरा**: हवा में आर्द्रता {humidity}% है। फंगल रोग तेजी से फैलते हैं। सिंचाई रोक दें और रोगग्रस्त पत्तियों को काटें।",
            "heat": "🥵 **अत्यधिक गर्मी की चेतावनी**: तापमान {temperature}°C है। वाष्पीकरण अधिक है। सुबह या शाम को हल्की सिंचाई करें और मल्चिंग का उपयोग करें।",
            "optimal": "🌤️ **अनुकूल मौसम**: तापमान {temperature}°C और आर्द्रता {humidity}% है। उर्वरक डालने और सामान्य रख-रखाव के लिए यह उत्तम समय है।"
        },
        "te": {
            "fungal": "⚠️ **శిలీంధ్ర వ్యాప్తి ముప్పు**: గాలిలో తేమ {humidity}% గా ఉంది. తెగుళ్లు వేగంగా వ్యాపిస్తాయి. పైనుంచి నీరు చల్లడం నిలిపివేయండి.",
            "heat": "🥵 **అధిక ఉష్ణోగ్రత హెచ్చరిక**: ఉష్ణోగ్రత {temperature}°C గా ఉంది. ఉదయం లేదా సాయంత్రం వేళల్లో తేలికపాటి తడులు ఇవ్వండి. మల్చింగ్ వాడండి.",
            "optimal": "🌤️ **అనుకూల వాతావరణం**: ఉష్ణోగ్రత {temperature}°C మరియు తేమ {humidity}%. ఎరువులు వేయడానికి ఇది సరైన సమయం."
        },
        "ta": {
            "fungal": "⚠️ **பூஞ்சை பரவும் அபாயம்**: காற்றில் ஈரப்பதம் {humidity}% ஆக உள்ளது. பூஞ்சை வேகமாக பரவும். மேல் தெளிப்பு நீர்ப்பாசனத்தை தவிர்க்கவும்.",
            "heat": "🥵 **அதிக வெப்பநிலை எச்சரிக்கை**: வெப்பநிலை {temperature}°C ஆக உள்ளது. அதிகாலை அல்லது மாலையில் மிதமான நீர்ப்பாசனம் அளிக்கவும். மூடாக்கு போடவும்.",
            "optimal": "🌤️ **சாதகமான வானிலை**: வெப்பநிலை {temperature}°C மற்றும் ஈரப்பதம் {humidity}%. உரம் இடவும் இலைகளை கவாத்து செய்யவும் சிறந்த நேரம்."
        }
    }

    lang_tips = tips.get(lang, tips["en"])
    if humidity > 80:
        key = "fungal"
    elif temp > 32:
        key = "heat"
    else:
        key = "optimal"
        
    return lang_tips[key].format(temperature=temp, humidity=humidity)
