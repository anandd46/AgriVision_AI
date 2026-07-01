document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------------------------------
    // Theme Toggle Functionality
    // ----------------------------------------------------
    const themeToggleBtn = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const activeTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }

    function updateThemeIcon(theme) {
        if (!themeToggleBtn) return;
        if (theme === 'dark') {
            themeToggleBtn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="5"></circle>
                    <line x1="12" y1="1" x2="12" y2="3"></line>
                    <line x1="12" y1="21" x2="12" y2="23"></line>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                    <line x1="1" y1="12" x2="3" y2="12"></line>
                    <line x1="21" y1="12" x2="23" y2="12"></line>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                </svg>
            `;
        } else {
            themeToggleBtn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
            `;
        }
    }

    // ----------------------------------------------------
    // Crop Card Selection Toggle (Reusable) & Scroll Fades
    // ----------------------------------------------------
    const cropCards = document.querySelectorAll('.crop-card-option');
    const hiddenCropInput = document.getElementById('selected-crop');

    cropCards.forEach(card => {
        card.addEventListener('click', () => {
            cropCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            if (hiddenCropInput) {
                hiddenCropInput.value = card.dataset.crop;
            }
        });
    });

    const cropSelectRow = document.querySelector('.crop-select-row');
    const fadeLeft = document.querySelector('.scroll-fade-left');
    const fadeRight = document.querySelector('.scroll-fade-right');
    
    if (cropSelectRow && fadeLeft && fadeRight) {
        const updateFades = () => {
            const scrollLeft = cropSelectRow.scrollLeft;
            const maxScroll = cropSelectRow.scrollWidth - cropSelectRow.clientWidth;
            
            fadeLeft.style.opacity = scrollLeft > 10 ? '1' : '0';
            fadeRight.style.opacity = scrollLeft < maxScroll - 10 ? '1' : '0';
        };
        
        cropSelectRow.addEventListener('scroll', updateFades);
        window.addEventListener('resize', updateFades);
        // Run after DOM settles
        setTimeout(updateFades, 200);
    }

    // ----------------------------------------------------
    // Leaf Scanner Module
    // ----------------------------------------------------
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('leaf-image-input');
    const previewWrapper = document.getElementById('preview-wrapper');
    const previewImage = document.getElementById('preview-image');
    const scanLaser = document.getElementById('scan-laser');
    const loadingIndicator = document.getElementById('loading-indicator');
    const resultCard = document.getElementById('result-card');

    if (uploadZone && fileInput) {
        // Trigger file browser on click
        uploadZone.addEventListener('click', (e) => {
            if (e.target !== fileInput && !previewWrapper.contains(e.target)) {
                fileInput.click();
            }
        });

        // Drag and Drop
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                uploadZone.style.borderColor = 'var(--primary-light)';
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                uploadZone.style.borderColor = 'var(--border-color)';
            }, false);
        });

        uploadZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length) {
                fileInput.files = files;
                handleFileSelect(files[0]);
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                handleFileSelect(fileInput.files[0]);
            }
        });
    }

    function handleFileSelect(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewWrapper.style.display = 'block';
            document.querySelector('.upload-prompt').style.display = 'none';
            if (uploadZone) uploadZone.classList.add('has-preview');
            
            // Clear prior results
            if (resultCard) resultCard.style.display = 'none';
            
            // Auto run scan
            runScanProcess(file);
        };
        reader.readAsDataURL(file);
    }

    function runScanProcess(file) {
        if (!scanLaser || !loadingIndicator) return;
        
        scanLaser.style.display = 'block';
        loadingIndicator.style.display = 'flex';
        
        const tips = document.getElementById('instruction-tips');
        if (tips) tips.style.display = 'none';
        
        const cropType = hiddenCropInput ? hiddenCropInput.value : 'coconut';
        const activeLang = localStorage.getItem('agri_lang') || 'en';
        const formData = new FormData();
        formData.append('image', file);
        formData.append('crop', cropType);
        formData.append('lang', activeLang);

        fetch('/api/scan', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Detection failed.');
            }
            return response.json();
        })
        .then(data => {
            // Stop scanning effects after brief delay for visual effect
            setTimeout(() => {
                scanLaser.style.display = 'none';
                loadingIndicator.style.display = 'none';
                if (tips) tips.style.display = 'flex';
                displayScanResults(data);
            }, 1200);
        })
        .catch(err => {
            scanLaser.style.display = 'none';
            loadingIndicator.style.display = 'none';
            if (tips) tips.style.display = 'flex';
            alert('Error scanning leaf. Please try a different image format.');
            console.error(err);
        });
    }

    function displayScanResults(data) {
        if (!resultCard) return;
        
        const activeLang = localStorage.getItem('agri_lang') || 'en';

        // Show annotated image containing bounding boxes
        if (data.annotated_image) {
            previewImage.src = data.annotated_image;
        }

        // Set Diagnosis details
        document.getElementById('res-disease-name').textContent = data.disease_name;
        document.getElementById('res-confidence-text').textContent = `${data.confidence}%`;
        
        // Confidence bar animation
        const fillBar = document.getElementById('res-confidence-fill');
        if (fillBar) {
            fillBar.style.width = '0%';
            setTimeout(() => {
                fillBar.style.width = `${data.confidence}%`;
            }, 100);
        }

        // Severity Badge
        const badge = document.getElementById('res-severity-badge');
        if (badge) {
            badge.className = `severity-badge badge-${data.severity}`;
            badge.textContent = data.severity;
        }

        // Action Priority Indicator Warning Banner
        const priorityBanner = document.getElementById('res-priority-banner');
        if (priorityBanner) {
            const priorityText = (TRANSLATIONS[activeLang] && TRANSLATIONS[activeLang][data.priority_key]) 
                ? TRANSLATIONS[activeLang][data.priority_key] 
                : "Priority Advisory";
            priorityBanner.textContent = priorityText;
            
            // Style by priority
            if (data.severity === 'high') {
                priorityBanner.style.backgroundColor = 'rgba(234, 67, 53, 0.15)';
                priorityBanner.style.color = '#ea4335';
                priorityBanner.style.border = '1px solid rgba(234, 67, 53, 0.25)';
            } else if (data.severity === 'medium') {
                priorityBanner.style.backgroundColor = 'rgba(255, 176, 0, 0.15)';
                priorityBanner.style.color = '#b37b00';
                priorityBanner.style.border = '1px solid rgba(255, 176, 0, 0.25)';
            } else {
                priorityBanner.style.backgroundColor = 'rgba(25, 135, 84, 0.15)';
                priorityBanner.style.color = '#198754';
                priorityBanner.style.border = '1px solid rgba(25, 135, 84, 0.25)';
            }
            priorityBanner.style.display = 'flex';
        }

        // Populate Follow-up Questions
        const followupsContainer = document.getElementById('res-followups-container');
        const followupsList = document.getElementById('res-followup-questions');
        if (followupsContainer && followupsList) {
            followupsList.innerHTML = '';
            if (data.follow_up_questions && data.follow_up_questions.length > 0) {
                data.follow_up_questions.forEach(qKey => {
                    const qText = (TRANSLATIONS[activeLang] && TRANSLATIONS[activeLang][qKey]) 
                        ? TRANSLATIONS[activeLang][qKey] 
                        : null;
                    if (qText) {
                        const btn = document.createElement('button');
                        btn.className = 'btn';
                        btn.style.padding = '0.4rem 1rem';
                        btn.style.fontSize = '0.8rem';
                        btn.style.borderRadius = '50px';
                        btn.style.background = 'rgba(25, 135, 84, 0.1)';
                        btn.style.color = 'var(--primary-light)';
                        btn.style.border = '1px solid rgba(25, 135, 84, 0.2)';
                        btn.style.cursor = 'pointer';
                        btn.style.fontWeight = '600';
                        btn.style.transition = 'all 0.2s';
                        btn.textContent = qText;
                        
                        btn.addEventListener('click', () => {
                            askAgriBot(qText);
                        });
                        
                        followupsList.appendChild(btn);
                    }
                });
                followupsContainer.style.display = 'block';
            } else {
                followupsContainer.style.display = 'none';
            }
        }

        // Populate Symptoms
        const symptomContainer = document.getElementById('res-symptoms');
        if (symptomContainer) {
            symptomContainer.innerHTML = '';
            data.symptoms.forEach(sym => {
                const tag = document.createElement('span');
                tag.className = 'symptom-tag';
                tag.textContent = sym;
                symptomContainer.appendChild(tag);
            });
        }

        // Populate Treatments
        document.getElementById('res-organic-treatment').textContent = data.organic_treatment;
        document.getElementById('res-chemical-treatment').textContent = data.chemical_treatment;
        document.getElementById('res-fertilizer-tip').textContent = data.fertilizer_recommendation;

        // Populate Weather-Aware Regional Advisory
        const weatherAdvisory = document.getElementById('res-weather-advisory');
        const weatherTipsEl = document.getElementById('res-weather-tips');
        if (weatherAdvisory && weatherTipsEl) {
            if (data.weather_tips) {
                weatherTipsEl.textContent = data.weather_tips;
                weatherAdvisory.style.display = 'block';
            } else {
                weatherAdvisory.style.display = 'none';
            }
        }

        // Populate Color breakdown metrics
        document.getElementById('pct-green').textContent = `${data.metrics.green_percentage}%`;
        document.getElementById('pct-yellow').textContent = `${data.metrics.yellow_percentage}%`;
        document.getElementById('pct-brown').textContent = `${data.metrics.brown_percentage}%`;

        // Display results block
        resultCard.style.display = 'block';
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // ----------------------------------------------------
    // Fertilizer Recommendation Module
    // ----------------------------------------------------
    const fertForm = document.getElementById('fertilizer-calculator-form');
    const fertResults = document.getElementById('fertilizer-results');

    if (fertForm) {
        fertForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const crop = document.getElementById('selected-crop').value;
            const age = document.getElementById('tree-age').value;
            const soil = document.getElementById('soil-type').value;
            const healthStatus = document.getElementById('health-status').value;

            fetch('/api/fertilizer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    crop: crop,
                    age: age,
                    soil: soil,
                    health_status: healthStatus
                })
            })
            .then(res => res.json())
            .then(data => {
                displayFertilizerRecommendations(data);
            })
            .catch(err => {
                alert('Error computing recommendation.');
                console.error(err);
            });
        });
    }

    function displayFertilizerRecommendations(data) {
        if (!fertResults) return;

        // Set unit label
        const unitLabel = document.getElementById('recipe-unit-label');
        if (unitLabel) unitLabel.textContent = data.unit;

        // Pure nutrients elemental values
        document.getElementById('val-n').textContent = `${data.pure_nutrients.nitrogen_N_g}g`;
        document.getElementById('val-p').textContent = `${data.pure_nutrients.phosphorus_P_g}g`;
        document.getElementById('val-k').textContent = `${data.pure_nutrients.potassium_K_g}g`;

        // Commercial bags weights
        document.getElementById('bag-urea').textContent = data.recommendations.urea_g >= 1000 
            ? `${(data.recommendations.urea_g/1000).toFixed(2)}kg` 
            : `${data.recommendations.urea_g}g`;
        document.getElementById('bag-ssp').textContent = data.recommendations.ssp_g >= 1000 
            ? `${(data.recommendations.ssp_g/1000).toFixed(2)}kg` 
            : `${data.recommendations.ssp_g}g`;
        document.getElementById('bag-mop').textContent = data.recommendations.mop_g >= 1000 
            ? `${(data.recommendations.mop_g/1000).toFixed(2)}kg` 
            : `${data.recommendations.mop_g}g`;

        // Organic and Lime
        document.getElementById('val-organic').textContent = `${data.recommendations.organic_manure_kg}kg`;
        document.getElementById('val-lime').textContent = data.recommendations.lime_dolomite_g >= 1000
            ? `${(data.recommendations.lime_dolomite_g/1000).toFixed(2)}kg`
            : `${data.recommendations.lime_dolomite_g}g`;

        // Trace correctives
        let traceTexts = [];
        if (data.special_nutrients.borax_g > 0) {
            traceTexts.push(`Borax: ${data.special_nutrients.borax_g}g`);
        }
        if (data.special_nutrients.zinc_sulfate_g > 0) {
            traceTexts.push(`Zinc Sulfate: ${data.special_nutrients.zinc_sulfate_g}g`);
        }
        if (data.special_nutrients.magnesium_sulfate_g > 0) {
            traceTexts.push(`Magnesium Sulfate: ${data.special_nutrients.magnesium_sulfate_g}g`);
        }
        document.getElementById('val-special').textContent = traceTexts.length > 0 ? traceTexts.join(', ') : 'None required.';

        // Soil and Health notes
        document.getElementById('note-soil').textContent = data.notes.soil_note || 'Standard soil conditions apply.';
        document.getElementById('note-health').textContent = data.notes.health_note;
        document.getElementById('note-application').textContent = data.notes.application_method;

        // Render Split Schedule Timeline
        const timeline = document.getElementById('split-schedule-timeline');
        if (timeline) {
            timeline.innerHTML = '';
            data.splits_schedule.forEach((split, index) => {
                const card = document.createElement('div');
                card.className = 'treatment-panel';
                card.style.borderLeft = '4px solid var(--secondary)';
                
                const uVal = split.urea_split_g >= 1000 ? `${(split.urea_split_g/1000).toFixed(2)}kg` : `${split.urea_split_g}g`;
                const sVal = split.ssp_split_g >= 1000 ? `${(split.ssp_split_g/1000).toFixed(2)}kg` : `${split.ssp_split_g}g`;
                const mVal = split.mop_split_g >= 1000 ? `${(split.mop_split_g/1000).toFixed(2)}kg` : `${split.mop_split_g}g`;
                
                card.innerHTML = `
                    <div style="display:flex; justify-content:space-between; font-weight:700; font-size:0.9rem; margin-bottom:0.25rem;">
                        <span>Split ${index+1}: ${split.time}</span>
                        <span style="color:var(--primary-light);">${split.percent}%</span>
                    </div>
                    <p style="font-size:0.8rem; opacity:0.85; margin-bottom:0.5rem;">${split.action}</p>
                    <div style="display:flex; gap:1.25rem; font-size:0.8rem; font-weight:700; opacity:0.8;">
                        <span>Urea: <span style="color:#ff5722;">${uVal}</span></span>
                        <span>SSP: <span style="color:#8d6e63;">${sVal}</span></span>
                        <span>MOP: <span style="color:#4caf50;">${mVal}</span></span>
                    </div>
                `;
                timeline.appendChild(card);
            });
        }

        // Gauges scale limits
        const cropLower = data.crop.toLowerCase();
        let maxN = 600;
        let maxP = 400;
        let maxK = 1200;
        
        if (cropLower === "paddy") {
            maxN = 120000;
            maxP = 60000;
            maxK = 60000;
        } else if (cropLower === "mango") {
            maxN = 1000;
            maxP = 1000;
            maxK = 1500;
        } else if (["tomato", "brinjal", "chilli"].includes(cropLower)) {
            maxN = 10;
            maxP = 10;
            maxK = 15;
        } else if (cropLower === "rubber") {
            maxN = 300;
            maxP = 250;
            maxK = 250;
        } else if (cropLower === "papaya") {
            maxN = 250;
            maxP = 250;
            maxK = 500;
        }
        
        animateGauge('gauge-n', (data.pure_nutrients.nitrogen_N_g / maxN) * 100);
        animateGauge('gauge-p', (data.pure_nutrients.phosphorus_P_g / maxP) * 100);
        animateGauge('gauge-k', (data.pure_nutrients.potassium_K_g / maxK) * 100);

        // Show Results panel
        fertResults.style.display = 'block';
        fertResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function animateGauge(gaugeId, percent) {
        const container = document.getElementById(gaugeId);
        if (!container) return;
        const circle = container.querySelector('.circular-bar');
        if (!circle) return;

        const radius = circle.r.baseVal.value;
        const circumference = 2 * Math.PI * radius; // 2 * pi * 50 = 314
        
        const offset = circumference - (Math.min(100, Math.max(0, percent)) / 100) * circumference;
        circle.style.strokeDashoffset = offset;
    }

    // ----------------------------------------------------
    // Disease Library Filter Chips
    // ----------------------------------------------------
    const filterChips = document.querySelectorAll('.filter-chip');
    const diseaseCards = document.querySelectorAll('.disease-card');

    filterChips.forEach(chip => {
        chip.addEventListener('click', () => {
            filterChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');

            const filterValue = chip.dataset.filter;

            diseaseCards.forEach(card => {
                if (filterValue === 'all') {
                    card.style.display = 'flex';
                } else {
                    if (card.dataset.crop === filterValue) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        });
    });

    // ----------------------------------------------------
    // Chatbot (AgriBot) Interaction Logic
    // ----------------------------------------------------
    const chatTrigger = document.getElementById('chat-trigger');
    const chatClose = document.getElementById('chat-close');
    const chatWindow = document.getElementById('chat-window');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');

    if (chatTrigger && chatWindow) {
        chatTrigger.addEventListener('click', () => {
            const isVisible = chatWindow.style.display === 'flex';
            chatWindow.style.display = isVisible ? 'none' : 'flex';
            if (!isVisible) {
                chatInput.focus();
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        });
    }

    if (chatClose) {
        chatClose.addEventListener('click', () => {
            chatWindow.style.display = 'none';
        });
    }

    function appendChatMessage(sender, text) {
        if (!chatMessages) return;
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender === 'user' ? 'user-msg' : 'bot-msg'}`;
        msgDiv.innerHTML = text.replace(/\n/g, '<br>');
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function handleChatSend() {
        if (!chatInput) return;
        const text = chatInput.value.trim();
        if (!text) return;

        appendChatMessage('user', text);
        chatInput.value = '';

        // Add typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-msg typing';
        typingDiv.textContent = '...';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        const activeLang = localStorage.getItem('agri_lang') || 'en';
        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, lang: activeLang })
        })
        .then(res => res.json())
        .then(data => {
            typingDiv.remove();
            appendChatMessage('bot', data.reply);
        })
        .catch(err => {
            typingDiv.remove();
            appendChatMessage('bot', 'Sorry, I am having trouble connecting right now.');
            console.error(err);
        });
    }

    if (chatSend) {
        chatSend.addEventListener('click', handleChatSend);
    }
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleChatSend();
        });
    }

    // ----------------------------------------------------
    // SQLite Scan History Status Update
    // ----------------------------------------------------
    const statusSelects = document.querySelectorAll('.status-select');
    statusSelects.forEach(select => {
        select.addEventListener('change', () => {
            const id = select.dataset.id;
            const newStatus = select.value;

            fetch('/api/history/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: parseInt(id), status: newStatus })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Flash success effect
                    const cell = select.parentElement;
                    cell.style.backgroundColor = 'rgba(25, 135, 84, 0.15)';
                    setTimeout(() => {
                        cell.style.backgroundColor = '';
                    }, 800);
                } else {
                    alert('Failed to update status.');
                }
            })
            .catch(err => {
                alert('Connection error.');
                console.error(err);
            });
        });
    });

    // ----------------------------------------------------
    // Multi-Language Localization Engine
    // ----------------------------------------------------
    const TRANSLATIONS = {
        en: {
            nav_dashboard: "Dashboard",
            nav_scanner: "Leaf Scanner",
            nav_fertilizer: "Fertilizer Guide",
            nav_library: "Disease Library",
            nav_mobile: "Mobile API Docs",
            welcome_note: "Welcome to AgriVision AI",
            dashboard_title: "Agriculture AI Dashboard",
            nav_home_mobile: "Home",
            nav_scan_mobile: "Scan",
            nav_fert_mobile: "Fertilizer",
            nav_lib_mobile: "Library",
            bot_status: "Online Agronomist",
            bot_welcome: "Hello! I am AgriBot. Ask me about palm crop NPK values, palm tree spacing, or leaf disease treatments.",
            stat_weather_title: "Live Weather & Condition",
            weather_passing: "Passing Showers",
            weather_placeholder: "Search city (e.g. Mysuru)...",
            weather_go: "Go",
            stat_location: "Location",
            stat_moisture_title: "Soil Moisture Status",
            stat_moisture_val: "Moderate (42%)",
            moisture_desc: "Optimal range for root nutrient uptake in light laterite soils.",
            stat_humidity: "Humidity level",
            stat_alerts_title: "Active Leaf Infections",
            active_threats: "Threats",
            threat_warning: "Infected trees logged in database requiring active chemical spray treatment.",
            stat_alert_footer: "Attention required in scan history logs.",
            fungal_title: "Fungal Spore Outbreak Risk: HIGH (78%)",
            fungal_desc: "High ambient humidity (82%) coupled with warm temperatures creates optimal germination conditions for Phytophthora palmivora spores (Bud Rot / Koleroga).",
            badge_warning: "Warning",
            toolset_title: "Farmer Toolset",
            tool_scanner: "Scan Crop Leaf",
            tool_scanner_desc: "Upload leaf photo to diagnose diseases instantly.",
            tool_fert: "Fertilizer Guide",
            tool_fert_desc: "Calculate exact NPK ratios and organic compost.",
            tool_lib: "Disease Database",
            tool_lib_desc: "Browse list of treatments, causes, and symptoms.",
            history_title: "Leaf Diagnosis Registry",
            th_date: "Date",
            th_crop: "Crop",
            th_diagnosis: "Diagnosis",
            th_conf: "Confidence",
            th_status: "Treatment Status",
            empty_history: "No Diagnostic Log Registered",
            empty_history_desc: "Navigate to the Leaf Scanner page to run your first computer vision analysis.",
            
            // Expanded crops & categories
            filter_all: "All Crops",
            crop_coconut: "Coconut",
            crop_arecanut: "Arecanut",
            crop_banana: "Banana",
            crop_mango: "Mango",
            crop_papaya: "Papaya",
            crop_tomato: "Tomato",
            crop_brinjal: "Brinjal",
            crop_chilli: "Chilli",
            crop_pepper: "Black Pepper",
            crop_cocoa: "Cocoa",
            crop_paddy: "Paddy (Rice)",
            crop_rubber: "Rubber",
            grp_palms: "Palm Crops",
            grp_fruits: "Fruit Crops",
            grp_vegetables: "Vegetable Crops",
            grp_spices: "Spices & Climbers",
            grp_beverages: "Beverages",
            grp_cereals: "Cereal Crops",
            grp_plantation: "Plantation Trees",
            
            // Fertilizer labels & inputs
            calc_dosage_title: "Calculate Tree Nutrient Dosages",
            form_crop: "Crop Variety",
            form_age: "Crop Age (Years)",
            form_age_help: "NPK scales automatically from sapling to adult tree.",
            form_soil: "Soil Type",
            form_health: "Crop Health Status",
            btn_generate: "Generate Nutrient Recipe",
            recipe_title: "Calculated Nutrient Recipe",
            th_pure_nutrients: "Target Elemental N-P-K (Pure)",
            th_comm_fert: "Commercial Fertilizer Weights (Bag Equivalents)",
            th_split_schedule: "Split Application Schedule",
            
            // Bags & elements
            lbl_urea: "Urea (46% N)",
            lbl_ssp: "SSP (16% P₂O₅)",
            lbl_mop: "MOP (60% K₂O)",
            bag_urea_desc: "Nitrogen fertilizer",
            bag_ssp_desc: "Single Super Phosphate",
            bag_mop_desc: "Muriate of Potash",
            lbl_n: "Nitrogen (N)",
            lbl_p: "Phosphorus (P)",
            lbl_k: "Potassium (K)",
            
            // Organic, soils & health dropdowns
            org_additive_title: "Organic & Base Additives",
            lbl_compost: "Compost/Farmyard Manure",
            lbl_lime: "Lime / Dolomite application",
            lbl_deficiency_corrective: "Trace Deficiency Correctives",
            agri_actions_title: "Agronomic Field Actions",
            lbl_soil_note: "Soil Note",
            lbl_health_corr: "Health Correction",
            lbl_best_practice: "Best Application Practice",
            
            health_healthy: "Healthy (Standard Maintenance)",
            health_fungal: "Fungal/Bacterial Infection (Immunity Boost)",
            health_pest: "Insect/Pest Damage (Defensive Recovery)",
            health_deficiency: "Nutrient Deficiency (Corrective Dose)",
            health_stress: "Climate Stress (Waterlogged/Drought)",
            
            soil_loamy: "Loamy / Alluvial (Optimal)",
            soil_sandy: "Sandy Soil (Leaches nutrients)",
            soil_laterite: "Laterite Soil (Acidic, P-fixing)",
            soil_clayey: "Clayey Soil (Heavy, waterlogs)",
            
            // Scanner steps
            scan_step_1: "1. Select Crop Variety",
            scan_step_2: "2. Upload Leaf Photograph",
            prompt_tap: "Tap to take photo or browse",
            prompt_format: "Supports JPG, PNG formats up to 10MB",
            load_parsing: "Analyzing leaf pixel structure...",
            load_running: "Running OpenCV contour calculations",
            scan_instructions_title: "Instructions & Tips",
            tips_title: "Tips for Best Accuracy:",
            tips_light: "Capture the leaf leaflet in bright, natural daylight. Avoid heavy shadows.",
            tips_focus: "Focus closely on the area showing discoloration, spots, or rot.",
            tips_flat: "Keep the leaf relatively flat against a contrasting background if possible.",
            tips_blur: "Avoid blurry shots; hold the smartphone camera steady.",
            res_header: "Diagnosis Result",
            green_chlorophyll: "Healthy Chlorophyll",
            yellow_chlorosis: "Yellow Chlorosis",
            necrotic_brown: "Necrotic Brown",
            observed_sym: "Observed Symptoms:",
            org_recovery: "Organic Recovery",
            chem_control: "Chemical Control",
            fert_adjust: "Fertilizer Adjustments"
        },
        kn: {
            nav_dashboard: "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
            nav_scanner: "ಎಲೆ ಸ್ಕ್ಯಾನರ್",
            nav_fertilizer: "ಗೊಬ್ಬರ ಮಾರ್ಗದರ್ಶಿ",
            nav_library: "ರೋಗ ಗ್ರಂಥಾಲಯ",
            nav_mobile: "ಮೊಬೈಲ್ API ಮಾಹಿತಿ",
            welcome_note: "ಅಗ್ರಿವಿಷನ್ AI ಗೆ ಸ್ವಾಗತ",
            dashboard_title: "ಕೃಷಿ AI ನಿಯಂತ್ರಣ ಫಲಕ",
            nav_home_mobile: "ಮುಖಪುಟ",
            nav_scan_mobile: "ಸ್ಕ್ಯಾನ್",
            nav_fert_mobile: "ಗೊಬ್ಬರ",
            nav_lib_mobile: "ಗ್ರಂಥಾಲಯ",
            bot_status: "ಸಕ್ರಿಯ ಕೃಷಿ ತಜ್ಞ",
            bot_welcome: "ನಮಸ್ಕಾರ! ನಾನು ಅಗ್ರಿಬಾಟ್. ಕೃಷಿ ರಸಗೊಬ್ಬರ, ಅಡಿಕೆ ಅಥವಾ ತೆಂಗಿನ ಎಲೆ ರೋಗಗಳ ಚಿಕಿತ್ಸೆ ಬಗ್ಗೆ ಕೇಳಿ.",
            stat_weather_title: "ಹವಾಮಾನ ಮಾಹಿತಿ",
            weather_passing: "ಹಗುರ ಮಳೆ",
            weather_placeholder: "ನಗರವನ್ನು ಹುಡುಕಿ (ಉದಾ. ಮೈಸೂರು)...",
            weather_go: "ಹೋಗಿ",
            stat_location: "ಸ್ಥಳ",
            stat_moisture_title: "ಮಣ್ಣಿನ ತೇವಾಂಶ ಮಟ್ಟ",
            stat_moisture_val: "ಮಧ್ಯಮ (42%)",
            moisture_desc: "ಹಗುರ ಜೇಡಿ ಮಣ್ಣಿನಲ್ಲಿ ಬೇರುಗಳ ಪೋಷಕಾಂಶಗಳ ಹೀರಿಕೊಳ್ಳುವಿಕೆಗೆ ಸೂಕ್ತ ಪರಿಸ್ಥಿತಿ.",
            stat_humidity: "ಗಾಳಿಯ ತೇವಾಂಶ",
            stat_alerts_title: "ಸಕ್ರಿಯ ರೋಗ ಬಾಧೆಗಳು",
            active_threats: "ರೋಗಗಳು",
            threat_warning: "ತಕ್ಷಣ ಕೀಟನಾಶಕ ಸಿಂಪಡನೆ ಅಥವಾ ಚಿಕಿತ್ಸೆಯ ಅಗತ್ಯವಿರುವ ದಾಖಲಿತ ರೋಗಗಳು.",
            stat_alert_footer: "ರೋಗ ಚಿಕಿತ್ಸಾ ಲಾಗ್‌ಗಳ ಕಡೆ ಗಮನ ಹರಿಸಿ.",
            fungal_title: "ಶಿಲೀಂಧ್ರ ರೋಗ ಹರಡುವ ಅಪಾಯ: ಹೆಚ್ಚು (78%)",
            fungal_desc: "ಹೆಚ್ಚಿನ ಗಾಳಿಯ ತೇವಾಂಶ (82%) ಮತ್ತು ಬೆಚ್ಚನೆಯ ವಾತಾವರಣವು ಕೊಳೆರೋಗ ಮತ್ತು ಮೊಗ್ಗು ಕೊಳೆ ರೋಗದ ಬೀಜಕಗಳನ್ನು ಹರಡಲು ಪ್ರೇರೇಪಿಸುತ್ತದೆ.",
            badge_warning: "ಎಚ್ಚರಿಕೆ",
            toolset_title: "ರೈತ ಪರಿಕರಗಳು",
            tool_scanner: "ಎಲೆ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ",
            tool_scanner_desc: "ರೋಗ ತಕ್ಷಣ ಪತ್ತೆ ಮಾಡಲು ಎಲೆಯ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ.",
            tool_fert: "ಗೊಬ್ಬರ ಮಾರ್ಗದರ್ಶಿ",
            tool_fert_desc: "ಖಚಿತವಾದ NPK ಅನುಪಾತ ಮತ್ತು ಸಾವಯವ ಗೊಬ್ಬರ ಲೆಕ್ಕ ಹಾಕಿ.",
            tool_lib: "ರೋಗ ಮಾಹಿತಿ ಕೋಶ",
            tool_lib_desc: "ರೋಗಗಳ ಲಕ್ಷಣಗಳು, ಕಾರಣಗಳು ಮತ್ತು ಸಾವಯವ/ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆಗಳ ಪಟ್ಟಿ.",
            history_title: "ಎಲೆ ರೋಗ ಪತ್ತೆ ನೋಂದಣಿ ಪುಸ್ತಕ",
            th_date: "ದಿನಾಂಕ",
            th_crop: "ಬೆಳೆ",
            th_diagnosis: "ಪತ್ತೆಯಾದ ರೋಗ",
            th_conf: "ನಿಖರತೆ",
            th_status: "ಚಿಕಿತ್ಸಾ ಸ್ಥಿತಿ",
            empty_history: "ಯಾವುದೇ ಇತಿಹಾಸ ಲಾಗ್ ಇಲ್ಲ",
            empty_history_desc: "ಕೃಷಿ ಎಲೆ ಸ್ಕ್ಯಾನರ್ ಪುಟಕ್ಕೆ ಭೇಟಿ ನೀಡಿ ಮೊದಲ ಬಾರಿಗೆ ಎಲೆ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ.",
            
            filter_all: "ಎಲ್ಲಾ ಬೆಳೆಗಳು",
            crop_coconut: "ತೆಂಗು",
            crop_arecanut: "ಅಡಿಕೆ",
            crop_banana: "ಬಾಳೆ",
            crop_mango: "ಮಾವು",
            crop_papaya: "ಪಪ್ಪಾಯಿ",
            crop_tomato: "ಟೊಮೇಟೊ",
            crop_brinjal: "ಬದನೆಕಾಯಿ",
            crop_chilli: "ಮೆಣಸಿನಕಾಯಿ",
            crop_pepper: "ಕರಿಮೆಣಸು",
            crop_cocoa: "ಕೋಕೋ",
            crop_paddy: "ಭತ್ತ",
            crop_rubber: "ರಬ್ಬರ್",
            grp_palms: "ತಾಳೆ ಬೆಳೆಗಳು",
            grp_fruits: "ಹಣ್ಣಿನ ಬೆಳೆಗಳು",
            grp_vegetables: "ತರಕಾರಿ ಬೆಳೆಗಳು",
            grp_spices: "ಮಸಾಲೆ ಬೆಳೆಗಳು",
            grp_beverages: "ಪಾನೀಯಗಳು",
            grp_cereals: "ಧಾನ್ಯ ಬೆಳೆಗಳು",
            grp_plantation: "ತೋಟದ ಬೆಳೆಗಳು",
            
            calc_dosage_title: "ಬೆಳೆಗಳ ಪೋಷಕಾಂಶಗಳ ಲೆಕ್ಕಾಚಾರ",
            form_crop: "ಬೆಳೆ ಪ್ರಕಾರ",
            form_age: "ಬೆಳೆ ವಯಸ್ಸು (ವರ್ಷಗಳು)",
            form_age_help: "ಸಸಿ ಹಂತದಿಂದ ಮರವಾಗುವವರೆಗೆ NPK ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಬದಲಾಗುತ್ತದೆ.",
            form_soil: "ಮಣ್ಣಿನ ವಿಧ",
            form_health: "ಬೆಳೆ ಆರೋಗ್ಯ ಸ್ಥಿತಿ",
            btn_generate: "ಪೋಷಕಾಂಶದ ಚಾರ್ಟ್ ತಯಾರಿಸಿ",
            recipe_title: "ಲೆಕ್ಕಾಚಾರದ ರಸಗೊಬ್ಬರ ಚಾರ್ಟ್",
            th_pure_nutrients: "ಶುದ್ಧ ಪೋಷಕಾಂಶಗಳ ಗುರಿ (N-P-K)",
            th_comm_fert: "ಮಾರುಕಟ್ಟೆಯ ರಸಗೊಬ್ಬರ ತೂಕ (ಚೀಲಗಳ ಪ್ರಮಾಣ)",
            th_split_schedule: "ಗೊಬ್ಬರ ನೀಡುವ ಹಂತಗಳ ವೇಳಾಪಟ್ಟಿ",
            
            lbl_urea: "ಯೂರಿಯಾ (Urea - 46% N)",
            lbl_ssp: "ಎಸ್.ಎಸ್.ಪಿ (SSP - 16% P₂O₅)",
            lbl_mop: "ಎಂ.ಓ.ಪಿ (MOP - 60% K₂O)",
            bag_urea_desc: "ಸಾರಜನಕ ಗೊಬ್ಬರ",
            bag_ssp_desc: "ರಂಜಕ ಗೊಬ್ಬರ",
            bag_mop_desc: "ಪೊಟ್ಯಾಶ್ ಗೊಬ್ಬರ",
            lbl_n: "ಸಾರಜನಕ (N)",
            lbl_p: "ರಂಜಕ (P)",
            lbl_k: "ಪೊಟ್ಯಾಷಿಯಂ (K)",
            
            org_additive_title: "ಸಾವಯವ ಮತ್ತು ಬೇಸ್ ಮಿಶ್ರಣಗಳು",
            lbl_compost: "ಕೊಳೆತ ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ",
            lbl_lime: "ಸುಣ್ಣ / ಡಾಲಮೈಟ್ ಅಪ್ಲಿಕೇಶನ್",
            lbl_deficiency_corrective: "ಲಘು ಪೋಷಕಾಂಶಗಳ ಕೊರತೆ ನೀಗಿಸುವಿಕೆ",
            agri_actions_title: "ಕೃಷಿ ಕ್ಷೇತ್ರ ಶಿಫಾರಸುಗಳು",
            lbl_soil_note: "ಮಣ್ಣಿನ ಸೂಚನೆ",
            lbl_health_corr: "ಆರೋಗ್ಯ ತಿದ್ದುಪಡಿ",
            lbl_best_practice: "ಗೊಬ್ಬರ ಹಾಕುವ ಉತ್ತಮ ವಿಧಾನ",
            
            health_healthy: "ಆರೋಗ್ಯಕರ (ನಿರ್ವಹಣೆ ಡೋಸ್)",
            health_fungal: "ಶಿಲೀಂಧ್ರ / ಬ್ಯಾಕ್ಟೀರಿಯಾ ಸೋಂಕು (ರೋಗ ನಿರೋಧಕ ಶಕ್ತಿ)",
            health_pest: "ಕೀಟ ಬಾಧೆ (ರಕ್ಷಣಾತ್ಮಕ ಚಿಕಿತ್ಸೆ)",
            health_deficiency: "ಪೋಷಕಾಂಶಗಳ ಕೊರತೆ (ಪರಿಹಾರ ಡೋಸ್)",
            health_stress: "ಹವಾಮಾನ ಒತ್ತಡ (ನೀರು ನಿಲ್ಲುವಿಕೆ/ಬರ)",
            
            soil_loamy: "ರೇವಣ್ಣು / ಜೇಡಿ ಮಿಶ್ರಿತ ಮಣ್ಣು (ಅತ್ಯುತ್ತಮ)",
            soil_sandy: "ಮರಳು ಮಣ್ಣು (ಪೋಷಕಾಂಶ ಸೋರಿಕೆ)",
            soil_laterite: "ಕೆಂಪು ಮಣ್ಣು (ಆಮ್ಲೀಯ, ರಂಜಕ ಬಂಧಿಸುವಿಕೆ)",
            soil_clayey: "ನೀರ್ನಿಲ ನಿಲ್ಲುವ ಜೇಡಿ ಮಣ್ಣು",
            
            scan_step_1: "೧. ಬೆಳೆ ಪ್ರಕಾರವನ್ನು ಆರಿಸಿ",
            scan_step_2: "೨. ಎಲೆಯ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ",
            prompt_tap: "ಫೋಟೋ ತೆಗೆಯಲು ಅಥವಾ ಗ್ಯಾಲರಿ ವೀಕ್ಷಿಸಲು ಟ್ಯಾಪ್ ಮಾಡಿ",
            prompt_format: "ಗರಿಷ್ಠ ೧೦ಎಂಬಿ ವರೆಗಿನ ಜೆಪಿಜಿ, ಪಿಎನ್‌ಜಿ ಫೈಲ್ ಬೆಂಬಲಿಸುತ್ತದೆ",
            load_parsing: "ಎಲೆಯ ಪಿಕ್ಸೆಲ್ ರಚನೆ ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...",
            load_running: "OpenCV ಕಾಂಟೂರ್ ಲೆಕ್ಕಾಚಾರಗಳು ಚಾಲನೆಯಲ್ಲಿವೆ",
            scan_instructions_title: "ಸೂಚನೆಗಳು ಮತ್ತು ಸಲಹೆಗಳು",
            tips_title: "ಹೆಚ್ಚಿನ ನಿಖರತೆಗಾಗಿ ಸಲಹೆಗಳು:",
            tips_light: "ಸ್ಪಷ್ಟ ನೈಸರ್ಗಿಕ ಬೆಳಕಿನಲ್ಲಿ ಎಲೆಯ ಫೋಟೋ ಸೆರೆಹಿಡಿಯಿರಿ. ನೆರಳುಗಳನ್ನು ತಪ್ಪಿಸಿ.",
            tips_focus: "ರೋಗದ ಕಲೆಗಳು ಅಥವಾ ಕೊಳೆತ ಜಾಗವನ್ನು ಹತ್ತಿರದಿಂದ ಫೋಕಸ್ ಮಾಡಿ.",
            tips_flat: "ಸಾಧ್ಯವಾದರೆ ಎಲೆಯನ್ನು ಸರಳ ಹಿನ್ನೆಲೆಯಲ್ಲಿ ಇರಿಸಿ ಫೋಟೋ ತೆಗೆಯಿರಿ.",
            tips_blur: "ಅಲುಗಾಡದಂತೆ ಕ್ಯಾಮೆರಾವನ್ನು ಸ್ಥಿರವಾಗಿ ಹಿಡಿದುಕೊಳ್ಳಿ.",
            res_header: "ರೋಗ ತಪಾಸಣೆ ಫಲಿತಾಂಶ",
            green_chlorophyll: "ಹಸಿರು ಕ್ಲೋರೊಫಿಲ್",
            yellow_chlorosis: "ಹಳದಿ ಬಣ್ಣ (ಕ್ಲೋರೊಸಿಸ್)",
            necrotic_brown: "ರೋಗಪೀಡಿತ ಕಂದು ಬಣ್ಣ",
            observed_sym: "ಕಂಡುಬಂದ ಲಕ್ಷಣಗಳು:",
            org_recovery: "ಜೈವಿಕ ಚಿಕಿತ್ಸೆ",
            chem_control: "ರಾಸಾಯನಿಕ ನಿಯಂತ್ರಣ",
            fert_adjust: "ರಸಗೊಬ್ಬರ ತಿದ್ದುಪಡಿಗಳು"
        },
        hi: {
            nav_dashboard: "डैशबोर्ड",
            nav_scanner: "लीफ स्कैनर",
            nav_fertilizer: "खाद गाइड",
            nav_library: "रोग लाइब्रेरी",
            nav_mobile: "मोबाइल एपीआई",
            welcome_note: "एग्रीविज़न एआई में आपका स्वागत है",
            dashboard_title: "कृषि एआई डैशबोर्ड",
            nav_home_mobile: "होम",
            nav_scan_mobile: "स्कैन",
            nav_fert_mobile: "उर्वरक",
            nav_lib_mobile: "लाइब्रेरी",
            bot_status: "ऑनलाइन कृषि विशेषज्ञ",
            bot_welcome: "नमस्ते! मैं एग्रीबॉट हूँ। मुझसे फसलों की खाद, दूरी या रोगों के उपचार के बारे में पूछें।",
            stat_weather_title: "मौसम और स्थिति",
            weather_passing: "हल्की बारिश",
            weather_placeholder: "शहर का नाम खोजें (उदा. मैसूर)...",
            weather_go: "खोजें",
            stat_location: "स्थान",
            stat_moisture_title: "मिट्टी की नमी",
            stat_moisture_val: "मध्यम (42%)",
            moisture_desc: "जड़ों के पोषण सेवन के लिए अनुकूल स्थिति।",
            stat_humidity: "आर्द्रता",
            stat_alerts_title: "सक्रिय पत्ती रोग",
            active_threats: "खतरे",
            threat_warning: "तत्काल छिड़काव की आवश्यकता वाले पंजीकृत रोग।",
            stat_alert_footer: "स्कैन इतिहास लॉग पर ध्यान दें।",
            fungal_title: "फंगल संक्रमण का खतरा: उच्च (78%)",
            fungal_desc: "हवा में उच्च नमी (82%) फंगल रोगों को बढ़ावा देती है।",
            badge_warning: "चेतावनी",
            toolset_title: "किसान उपकरण",
            tool_scanner: "पत्ती स्कैन करें",
            tool_scanner_desc: "रोग का तुरंत पता लगाने के लिए फोटो अपलोड करें।",
            tool_fert: "उर्वरक गाइड",
            tool_fert_desc: "सटीक एनपीके और जैविक खाद की गणना करें।",
            tool_lib: "रोग डेटाबेस",
            tool_lib_desc: "उपचारों, लक्षणों और कारणों की सूची देखें।",
            history_title: "पत्ती निदान रजिस्ट्री",
            th_date: "दिनांक",
            th_crop: "फसल",
            th_diagnosis: "निदान",
            th_conf: "सटीकता",
            th_status: "उपचार स्थिति",
            empty_history: "कोई लॉग पंजीकृत नहीं है",
            empty_history_desc: "पहला विश्लेषण शुरू करने के लिए लीफ स्कैनर पेज पर जाएं।",
            filter_all: "सभी फसलें",
            crop_coconut: "नारियल",
            crop_arecanut: "सुपारी",
            crop_banana: "केला",
            crop_mango: "आम",
            crop_papaya: "पपीता",
            crop_tomato: "टमाटर",
            crop_brinjal: "बैंगन",
            crop_chilli: "मिर्च",
            crop_pepper: "काली मिर्च",
            crop_cocoa: "कोको",
            crop_paddy: "धान (चावल)",
            crop_rubber: "रबर",
            grp_palms: "ताड़ की फसलें",
            grp_fruits: "फलों की फसलें",
            grp_vegetables: "सब्जियों की फसलें",
            grp_spices: "मसाले और बेलें",
            grp_beverages: "पेय पदार्थ",
            grp_cereals: "अनाज की फसलें",
            grp_plantation: "बागवानी पेड़",
            calc_dosage_title: "फसलों के लिए पोषक तत्वों की गणना",
            form_crop: "फसल की किस्म",
            form_age: "फसल की आयु (वर्ष)",
            form_age_help: "पौधे से पेड़ बनने तक एनपीके स्वतः बदलता है।",
            form_soil: "मिट्टी का प्रकार",
            form_health: "फसल का स्वास्थ्य",
            btn_generate: "पोषक तत्व नुस्खा बनाएं",
            recipe_title: "गणना किया गया पोषक तत्व नुस्खा",
            th_pure_nutrients: "लक्ष्य तत्व एन-पी-के (शुद्ध)",
            th_comm_fert: "व्यावसायिक उर्वरक वजन",
            th_split_schedule: "विभाजित अनुप्रयोग अनुसूची",
            lbl_urea: "यूरिया (Urea - 46% N)",
            lbl_ssp: "एसएसपी (SSP - 16% P2O5)",
            lbl_mop: "एमओपी (MOP - 60% K2O)",
            bag_urea_desc: "नाइट्रोजन उर्वरक",
            bag_ssp_desc: "सिंगल सुपर फॉस्फेट",
            bag_mop_desc: "मुरिएट ऑफ पोटाश",
            lbl_n: "नाइट्रोजन (N)",
            lbl_p: "फास्फोरस (P)",
            lbl_k: "पोटेशियम (K)",
            org_additive_title: "जैविक और बुनियादी मिश्रण",
            lbl_compost: "कम्पोस्ट/गोबर की खाद",
            lbl_lime: "चूना / डोलोमाइट अनुप्रयोग",
            lbl_deficiency_corrective: "सूक्ष्म पोषक तत्वों की कमी का सुधार",
            agri_actions_title: "कृषि क्षेत्र की सिफारिशें",
            lbl_soil_note: "मिट्टी की टिप्पणी",
            lbl_health_corr: "स्वास्थ्य सुधार",
            lbl_best_practice: "खाद डालने का सबसे अच्छा तरीका",
            health_healthy: "स्वस्थ (सामान्य खुराक)",
            health_fungal: "फंगल/बैक्टीरियल संक्रमण (प्रतिरोधक शक्ति)",
            health_pest: "कीट का प्रकोप (रक्षात्मक रिकवरी)",
            health_deficiency: "पोषक तत्वों की कमी (सुधारात्मक खुराक)",
            health_stress: "मौसम का तनाव (जलभराव/सूखा)",
            soil_loamy: "दोमट / जलोढ़ (सर्वोत्तम)",
            soil_sandy: "बलुई मिट्टी (पोषक तत्व बह जाते हैं)",
            soil_laterite: "लेटराइट मिट्टी (अम्लीय, फॉस्फोरस लॉक)",
            soil_clayey: "चिकनी मिट्टी (भारी, जलभराव)",
            scan_step_1: "1. फसल की किस्म चुनें",
            scan_step_2: "2. पत्ती का फोटो अपलोड करें",
            prompt_tap: "फोटो लेने या ब्राउज़ करने के लिए टैप करें",
            prompt_format: "10MB तक की JPG, PNG फाइलों का समर्थन",
            load_parsing: "पत्ती के पिक्सेल का विश्लेषण...",
            load_running: "OpenCV कंटूर गणना चल रही है",
            scan_instructions_title: "निर्देश और सुझाव",
            tips_title: "सर्वोत्तम सटीकता के लिए सुझाव:",
            tips_light: "प्राकृतिक रोशनी में फोटो लें। घनी परछाई से बचें।",
            tips_focus: "रोगग्रस्त या सड़े हुए हिस्से पर फोकस करें।",
            tips_flat: "पत्ती को एक सपाट पृष्ठभूमि पर रखकर फोटो लें।",
            tips_blur: "धुंधले फोटो से बचें, कैमरे को स्थिर रखें।",
            res_header: "निदान परिणाम",
            green_chlorophyll: "स्वस्थ क्लोरोफिल",
            yellow_chlorosis: "पीला क्लोरोसिस",
            necrotic_brown: "कड़ा भूरा सड़न",
            observed_sym: "देखे गए लक्षण:",
            org_recovery: "जैविक उपचार",
            chem_control: "रासायनिक नियंत्रण",
            fert_adjust: "उर्वरक समायोजन"
        },
        te: {
            nav_dashboard: "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
            nav_scanner: "ఆకు స్కానర్",
            nav_fertilizer: "ఎరువుల గైడ్",
            nav_library: "தெగుళ్ల లైబ్రరీ",
            nav_mobile: "మొబైల్ ఏపీఐ",
            welcome_note: "అగ్రివిజన్ ఏఐ కి స్వాగతం",
            dashboard_title: "వ్యవసాయ ఏఐ కంట్రోల్ ప్యానెల్",
            nav_home_mobile: "హోమ్",
            nav_scan_mobile: "స్కాన్",
            nav_fert_mobile: "ఎరువులు",
            nav_lib_mobile: "లైబ్రరీ",
            bot_status: "ఆన్‌లైన్ వ్యవసాయ నిపుణుడు",
            bot_welcome: "నమస్కారం! నేను అగ్రిబాట్. పంటల ఎరువులు, సాగు దూరాలు లేదా తెగుళ్ల నివారణ గురించి అడగండి.",
            stat_weather_title: "వాతావరణం & పరిస్థితి",
            weather_passing: "తేలికపాటి వర్షం",
            weather_placeholder: "నగరాన్ని శోధించండి (ఉదా. మైసూర్)...",
            weather_go: "వెళ్ళు",
            stat_location: "ప్రాంతం",
            stat_moisture_title: "మట్టి తేమ శాతం",
            stat_moisture_val: "మధ్యస్థం (42%)",
            moisture_desc: "వేర్ల పోషకాల గ్రహణ శక్తికి అనుకూల వాతావరణం.",
            stat_humidity: "గాలిలో తేమ",
            stat_alerts_title: "సక్రియ తెగుళ్లు",
            active_threats: "ప్రమాదాలు",
            threat_warning: "వెంటనే మందు పిచికారీ చేయాల్సిన అవసరం ఉన్న నమోదిత తెగుళ్లు.",
            stat_alert_footer: "స్కాన్ చరిత్ర లాగ్‌ను గమనించండి.",
            fungal_title: "శిలీంధ్ర వ్యాప్తి ముప్పు: ఎక్కువ (78%)",
            fungal_desc: "గాలిలో తేమ (82%) పెరిగినಾಗ తెగుళ్లు వేగంగా వ్యాపిస్తాయి.",
            badge_warning: "హెచ్చరిక",
            toolset_title: "రైతు పరికరాలు",
            tool_scanner: "ఆకు స్కాన్ చేయండి",
            tool_scanner_desc: "తెగులు వెంటనే గుర్తించడానికి ఫోటో అప్లోడ్ చేయండి.",
            tool_fert: "ఎరువుల గైడ్",
            tool_fert_desc: "ఖచ్చితమైన ఎన్.పి.కె మరియు సేంద్రీయ ఎరువులను లెక్కించండి.",
            tool_lib: "తెగుళ్ల డేటాబేస్",
            tool_lib_desc: "చికిత్సలు, లక్షణాలు మరియు కారణాల జాబితాను చూడండి.",
            history_title: "ఆకు తెగుళ్ల రిజిస్ట్రీ",
            th_date: "తేదీ",
            th_crop: "పంట",
            th_diagnosis: "నిర్ధారణ",
            th_conf: "ఖచ్చితత్వం",
            th_status: "చికిత్స పరిస్థితి",
            empty_history: "ఎటువంటి చరిత్ర నమోదు కాలేదు",
            empty_history_desc: "మొదటి విశ్లేషణను ప్రారంభించడానికి లీఫ్ స్కానర్ పేజీకి వెళ్ళండి.",
            filter_all: "అన్ని పంటలు",
            crop_coconut: "కొబ్బరి",
            crop_arecanut: "పోక / అడక",
            crop_banana: "అరటి",
            crop_mango: "మామిడి",
            crop_papaya: "బొప్పాయి",
            crop_tomato: "టమోటా",
            crop_brinjal: "వంకాయ",
            crop_chilli: "మిర్చి",
            crop_pepper: "మిరియాలు",
            crop_cocoa: "కోకో",
            crop_paddy: "వరి",
            crop_rubber: "ರಬ್ಬರು",
            grp_palms: "తాటి పంటలు",
            grp_fruits: "పండ్ల పంటలు",
            grp_vegetables: "కూరగాయల పంటలు",
            grp_spices: "మసాలాలు & తీగలు",
            grp_beverages: "పానీయాలు",
            grp_cereals: "ధాನ್ಯಪು పంటలు",
            grp_plantation: "తోట తోటలు",
            calc_dosage_title: "పంటల పోషకాల పరిమాణం",
            form_crop: "పంట రకం",
            form_age: "పంట వయస్సు (సంవత్సరాలు)",
            form_age_help: "మొక్క నుండి పెద్ద చెట్టు అయ్యేవరకు ఎన్.పి.కె పరిమాణం మారుతుంది.",
            form_soil: "నేల రకం",
            form_health: "పంట ఆరోగ్యం",
            btn_generate: "పోషకాల చార్ట్ పొందండి",
            recipe_title: "Calculated Nutrient Recipe",
            th_pure_nutrients: "లక్ష్య శుద్ధ పోషకాలు (N-P-K)",
            th_comm_fert: "మార్కెట్ రసాయన ఎరువుల బరువు",
            th_split_schedule: "దఫాల వారీగా వేసే పద్ధతి",
            lbl_urea: "ಯೂರಿಯಾ (Urea - 46% N)",
            lbl_ssp: "ఎస్.ಎಸ್.పి (SSP - 16% P2O5)",
            lbl_mop: "ఎమ్.ఓ.പി (MOP - 60% K2O)",
            bag_urea_desc: "నత్రజని ఎరువు",
            bag_ssp_desc: "సింగిల్ సూపర్ ఫాస్ఫేట్",
            bag_mop_desc: "మ్యూరియేట్ ఆఫ్ పొటాష్",
            lbl_n: "నత్రజని (N)",
            lbl_p: "భాస్వరం (P)",
            lbl_k: "పొటాషియం (K)",
            org_additive_title: "సేంద్రీయ మరియు బేస్ ఎరువులు",
            lbl_compost: "పశువుల ఎరువు / కంపోస్ట్",
            lbl_lime: "ಸುಣ್ಣ / ಡೋಲಮೈಟ್ ವಾಡಕಂ",
            lbl_deficiency_corrective: "సూక్ష్మ పోషకాల లోపాల సవరణ",
            agri_actions_title: "వ్యవసాయ క్షేత్ర సలహాలు",
            lbl_soil_note: "మట్టి నోట్",
            lbl_health_corr: "ఆరోగ్య సవరణ",
            lbl_best_practice: "ఎరువులు వేయవలసిన సరైన పద్ధతి",
            health_healthy: "ఆరోగ్యకరమైనది (సాధാരണ మోతాదు)",
            health_fungal: "శిలీంధ్ర/బ్యాక్టీరియా తెగులు (నిరోధక శక్తి)",
            health_pest: "పురుగుల దాడి (రక్షణ చికిత్స)",
            health_deficiency: "పోషకాల లోపాలు (పరిహార మోతాదు)",
            health_stress: "వాతావरण ఒత్తిడి (వెள்ளಕ್ಕೆಟ್ಟು/కరువు)",
            soil_loamy: "లోమీ / వండ్రు మట్టి (అత్యుత్తమ)",
            soil_sandy: "ఇసుక నేలలు",
            soil_laterite: "ఎర్ర నేలలు",
            soil_clayey: "బంకమట్టి నేలలు",
            scan_step_1: "1. పంట రకాన్ని ఎంచుకోండి",
            scan_step_2: "2. ఆకు ఫోటో అప్లోడ్ చేయండి",
            prompt_tap: "ఫోటో తీయడానికి లేదా అప్లోడ్ చేయడానికి ట్యాప్ చేయండి",
            prompt_format: "గరిష్టంగా 10MB వరకు ఉన్న JPG, PNG ఫైళ్లకు మద్దతు ఇస్తుంది",
            load_parsing: "ఆకు పిక్సెల్ విశ్లేషణ...",
            load_running: "OpenCV లెక్కలు జరుగుతున్నాయి",
            scan_instructions_title: "సూచనలు & సలహాలు",
            tips_title: "ఖచ్చితత్వం కోసం కొన్ని సలహాలు:",
            tips_light: "సహజమైన వెలుతురులో ఫోటో తీయండి. నీడలు లేకుండా చూసుకోండి.",
            tips_focus: "తెగులు సోకిన భాగాలపై దగ్గరగా ఫోకస్ చేయండి.",
            tips_flat: "సాధ్యమైతే ఆకును ఒక ఫ్లాట్ నేలపై ఉంచి ఫోటో తీయండి.",
            tips_blur: "కెమెరా కదలకుండా స్థిరంగా పట్టుకోండి.",
            res_header: "ఫలితం",
            green_chlorophyll: "పచ్చని హరితరేణువు",
            yellow_chlorosis: "పసుపు క్లోరోసిస్",
            necrotic_brown: "కాలిపోయిన గోధుమ రంగు",
            observed_sym: "గమనించిన లక్షణాలు:",
            org_recovery: "సేంద్రీయ చికిత్స",
            chem_control: "రసాయన నివారణ",
            fert_adjust: "ఎరువుల సర్దుబాటు"
        },
        ta: {
            nav_dashboard: "டாஷ்போர்டு",
            nav_scanner: "இலை ஸ்கேனர்",
            nav_fertilizer: "உர வழிகாட்டி",
            nav_library: "நோய் களஞ்சியம்",
            nav_mobile: "மொபைல் ஏபிஐ",
            welcome_note: "அக்ரிவிஷன் ஏஐ-க்கு வரவேற்கிறோம்",
            dashboard_title: "விவசாய ஏஐ கட்டுப்பாட்டு வாரியம்",
            nav_home_mobile: "முகப்பு",
            nav_scan_mobile: "ஸ்கேன்",
            nav_fert_mobile: "உரங்கள்",
            nav_lib_mobile: "களஞ்சியம்",
            bot_status: "ஆன்லைன் விவசாய நிபுணர்",
            bot_welcome: "வணக்கம்! நான் அக்ரிபாட். உரங்கள், நடவு முறைகள் அல்லது நோய்கள் குறித்து கேளுங்கள்.",
            stat_weather_title: "வானிலை & தட்பவெப்ப நிலை",
            weather_passing: "மிதமான மழை",
            weather_placeholder: "நகரத்தைத் தேடு (உதாரணம். மைசூர்)...",
            weather_go: "செல்",
            stat_location: "இடம்",
            stat_moisture_title: "மண் ஈரப்பத நிலை",
            stat_moisture_val: "மிதமான (42%)",
            moisture_desc: "வேர்கள் ஊட்டச்சத்துக்களை உறிஞ்சுவதற்கு ஏதுவான நிலை.",
            stat_humidity: "ஈரப்பதம்",
            stat_alerts_title: "பாதிக்கப்பட்ட பயிர்கள்",
            active_threats: "அச்சுறுத்தல்கள்",
            threat_warning: "உடனடியாக மருந்து தெளிக்க வேண்டிய நோய்கள்.",
            stat_alert_footer: "ஸ்கேன் வரலாற்றுப் பதிவேட்டை கவனிக்கவும்.",
            fungal_title: "பூஞ்சை பரவும் அபாயம்: அதிகம் (78%)",
            fungal_desc: "ஈரப்பதம் (82%) மற்றும் வெப்பம் பூஞ்சை நோய்களை வேகமாக பரக்கும்.",
            badge_warning: "எச்சரிக்கை",
            toolset_title: "விவசாய கருவிகள்",
            tool_scanner: "இலை ஸ்கேன் செய்க",
            tool_scanner_desc: "நோய்களை உடனுக்குடன் கண்டறிய புகைப்படத்தை பதிவேற்றவும்.",
            tool_fert: "உர வழிகாட்டி",
            tool_fert_desc: "துல்லியமான NPK மற்றும் இயற்கை உர தேவைகளை கணக்கிடுங்கள்.",
            tool_lib: "நோய் தரவுத்தளம்",
            tool_lib_desc: "நோய்கள், அறிகுறிகள் மற்றும் சிகிச்சை முறைகளின் பட்டியல்.",
            history_title: "நோய் கண்டறியும் பதிவேடு",
            th_date: "தேதி",
            th_crop: "பயிர்",
            th_diagnosis: "நோய்",
            th_conf: "துல்லியம்",
            th_status: "சிகிச்சை நிலை",
            empty_history: "விவரங்கள் எதுவும் பதிவாகவில்லை",
            empty_history_desc: "இலை ஸ்கேனரை பயன்படுத்தி முதன்முறையாக பரிசோதிக்கவும்.",
            filter_all: "அனைத்து பயிர்கள்",
            crop_coconut: "தென்னை",
            crop_arecanut: "பாக்கு",
            crop_banana: "வாழை",
            crop_mango: "மாம்பழம்",
            crop_papaya: "பப்பாளி",
            crop_tomato: "தக்காளி",
            crop_brinjal: "கத்தரிக்காய்",
            crop_chilli: "மிளகாய்",
            crop_pepper: "மிளகு",
            crop_cocoa: "கோகோ",
            crop_paddy: "நெல்",
            crop_rubber: "ரப்பர்",
            grp_palms: "பனை பயிர்கள்",
            grp_fruits: "பழ பயிர்கள்",
            grp_vegetables: "காய்கறி பயிர்கள்",
            grp_spices: "நறுமணப் பொருட்கள் & கொடிகள்",
            grp_beverages: "பானங்கள்",
            grp_cereals: "தானியப் பயிர்கள்",
            grp_plantation: "தோட்ட மரங்கள்",
            calc_dosage_title: "பயிர்களுக்கான உர கணக்கீடு",
            form_crop: "பயிர் வகை",
            form_age: "பயிர் வயது (ஆண்டுகள்)",
            form_age_help: "கன்று முதல் மரம் வரை NPK தேவை மாறுபடும்.",
            form_soil: "மண் வகை",
            form_health: "பயிரின் ஆரோக்கியம்",
            btn_generate: "உர அட்டவணை பெறுக",
            recipe_title: "கணக்கிடப்பட்ட உர அட்டவணை",
            th_pure_nutrients: "இலக்கு ஊட்டச்சத்துக்கள் (N-P-K)",
            th_comm_fert: "சந்தையில் கிடைக்கும் உரங்களின் அளவு",
            th_split_schedule: "தவணை முறை உர அட்டவணை",
            lbl_urea: "யூரியா (Urea - 46% N)",
            lbl_ssp: "எஸ்.எஸ்.பி (SSP - 16% P2O5)",
            lbl_mop: "எம்.ஓ.பி (MOP - 60% K2O)",
            bag_urea_desc: "நைட்ரஜன் உரம்",
            bag_ssp_desc: "சிங்கிள் சூப்பர் பாஸ்பேட்",
            bag_mop_desc: "மியூரியேட் ஆஃப் பொட்டாஷ்",
            lbl_n: "நைட்ரஜன் (N)",
            lbl_p: "பாஸ்பரஸ் (P)",
            lbl_k: "பொட்டாசியம் (K)",
            org_additive_title: "இயற்கை மற்றும் பிற உரங்கள்",
            lbl_compost: "தொழு உரம் / கമ്പോஸ்ட்",
            lbl_lime: "சுண்ணாம்பு / டோலமைட் பயன்பாடு",
            lbl_deficiency_corrective: "நுண்ணூட்ட சத்து குறைபாடுகளை சரிசெய்தல்",
            agri_actions_title: "விவசாய நில பரிந்துரைகள்",
            lbl_soil_note: "மண் குறிப்பு",
            lbl_health_corr: "ஆரோக்கிய திருத்தம்",
            lbl_best_practice: "உரம் இடுவதற்கான சரியான வழி",
            health_healthy: "ஆரோக்கியமானது (சாதாரண அளவு)",
            health_fungal: "பூஞ்சை/பாக்டீरिया நோய் (நோய் எதிர்ப்பு உரம்)",
            health_pest: "பூச்சி தாக்குதல் (பாதுகாப்பு உரம்)",
            health_deficiency: "சத்து குறைபாடு (நிவாரண உரம்)",
            health_stress: "வானிலை அழுத்தம் (வெள்ளம்/வறட்சி)",
            soil_loamy: "வண்டல் மண் (மிகவும் சிறந்தது)",
            soil_sandy: "மணல் மண் (உரம் எளிதில் அடித்து செல்லப்படும்)",
            soil_laterite: "செம்மண் (அமிலத்தன்மை கொண்டது, P-பிணைப்பு)",
            soil_clayey: "களிமண் (அதிக நீர் தேங்கும்)",
            scan_step_1: "1. பயிர் வகையைத் தேர்ந்தெடுக்கவும்",
            scan_step_2: "2. இலையின் புகைப்படத்தைப் பதிவேற்றவும்",
            prompt_tap: "புகைப்படம் எடுக்க அல்லது பதிவேற்ற இங்கே தட்டவும்",
            prompt_format: "10MB வரையிலான JPG, PNG வடிவங்களை ஆதரிக்கிறது",
            load_parsing: "இலையின் பிகசல் ഘടന വിശകലനം ചെയ്യുന്നു...",
            load_running: "OpenCV கணக்கீடுகள் நிகழ்கின்றன",
            scan_instructions_title: "வழிமுறைகள் & குறிப்புகள்",
            tips_title: "துல்லியமான முடிவுகளுக்கு குறிப்புகள்:",
            tips_light: "இயற்கையான பகல் வெளிச்சத்தில் படம் எடுக்கவும். நிழல்களை தவிர்க்கவும்.",
            tips_focus: "பாதிக்கப்பட்ட பகுதிகளை நெருக்கமாக படம் பிடிக்கவும்.",
            tips_flat: "இலையை சமமான பரப்பில் வைத்து படம் பிடிக்கவும்.",
            tips_blur: "கேமரா அசையாமல் நிலையாக பிடிக்கவும்.",
            res_header: "நோய் கண்டறிதல் முடிவு",
            green_chlorophyll: "ஆரோக்கியமான பச்சையம்",
            yellow_chlorosis: "மஞ்சள் பச்சைய சோகை",
            necrotic_brown: "கருகிய பழுப்பு நிறம்",
            observed_sym: "கண்டறியப்பட்ட அறிகுறிகள்:",
            org_recovery: "இயற்கை மருத்துவம்",
            chem_control: "இரசாயன கட்டுப்பாடு",
            fert_adjust: "உர சரிசெய்தல்"
        },
        ml: {
            nav_dashboard: "ഡാഷ്‌ബോർഡ്",
            nav_scanner: "ഇല സ്കാനർ",
            nav_fertilizer: "വളപ്രയോഗ സഹായി",
            nav_library: "രോഗ വിവരപ്പട്ടിക",
            nav_mobile: "മൊബൈൽ API വിവരങ്ങൾ",
            welcome_note: "അഗ്രിവിഷൻ AI-ലേക്ക് സ്വാഗതം",
            dashboard_title: "കൃഷി AI കൺട്രോൾ പാനൽ",
            nav_home_mobile: "ഹോം",
            nav_scan_mobile: "സ്കാൻ",
            nav_fert_mobile: "വളം",
            nav_lib_mobile: "വിവരങ്ങൾ",
            bot_status: "സജീവ കൃഷി സഹായി",
            bot_welcome: "നമസ്കാരം! ഞാൻ അഗ്രിബോട്ട് ആണ്. വളപ്രയോഗം, രോഗങ്ങൾ, അല്ലെങ്കിൽ കായ്പൊഴിച്ചിൽ എന്നിവയെക്കുറിച്ച് ചോദിക്കാം.",
            stat_weather_title: "കാലാവസ്ഥാ വിവരങ്ങൾ",
            weather_passing: "ചെറിയ മഴ",
            weather_placeholder: "നഗരം തിരയുക (ഉദാ: മൈസൂർ)...",
            weather_go: "പോകൂ",
            stat_location: "സ്ഥലം",
            stat_moisture_title: "മണ്ണിലെ ഈർപ്പം",
            stat_moisture_val: "മിതമായത് (42%)",
            moisture_desc: "ചെമ്മണ്ണിൽ വേരുകൾ പോഷകങ്ങൾ വലിച്ചെടുക്കുന്നതിന് ഏറ്റവും അനുയോജ്യമായ അവസ്ഥ.",
            stat_humidity: "അന്തരീക്ഷ ഈർപ്പം",
            stat_alerts_title: "സജീവ രോഗബാധകൾ",
            active_threats: "രോഗങ്ങൾ",
            threat_warning: "ഡാറ്റാബേസിൽ രേഖപ്പെടുത്തിയ രോഗബാധയുള്ള മരങ്ങൾക്ക് ഉടൻ മരുന്ന് തളിക്കേണ്ടതുണ്ട്.",
            stat_alert_footer: "രോഗ ചികിത്സാ ഹിസ്റ്ററി പരിശോധിക്കുക.",
            fungal_title: "കുമിൾ രോഗ സാധ്യത: വളരെ കൂടുതൽ (78%)",
            fungal_desc: "അന്തരീക്ഷ ഈർപ്പവും (82%) ചൂടും കൂടുമ്പോൾ കൊളരോഗം, ചീയൽ രോഗം എന്നിവ പടരാൻ കാരണമാകുന്നു.",
            badge_warning: "മുന്നറിയിപ്പ്",
            toolset_title: "കർഷക സഹായികൾ",
            tool_scanner: "ഇല സ്കാൻ ചെയ്യുക",
            tool_scanner_desc: "രോഗം തിരിച്ചറിയാൻ ഇലയുടെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക.",
            tool_fert: "വളപ്രയോഗ സഹായി",
            tool_fert_desc: "കൃത്യമായ NPK അളവും ജൈവവളങ്ങളും കണക്കാക്കുക.",
            tool_lib: "രോഗവിവര കോശം",
            tool_lib_desc: "ലക്ഷണങ്ങൾ, കാരണങ്ങൾ, ജൈവ/രാസ ചികിത്സാ രീതികളുടെ പട്ടിക.",
            history_title: "രോഗനിർണ്ണയ വിവരപ്പട്ടിക",
            th_date: "തീയതി",
            th_crop: "വിള",
            th_diagnosis: "രോഗം",
            th_conf: "കൃത്യത",
            th_status: "ചികിത്സാ പുരോഗതി",
            empty_history: "രോഗ വിവരങ്ങൾ ലഭ്യമല്ല",
            empty_history_desc: "ഇല സ്കാനർ ഉപയോഗിച്ച് നിങ്ങളുടെ ആദ്യ പരിശോധന ആരംഭിക്കുക.",

            filter_all: "എല്ലാ വിളകളും",
            crop_coconut: "തെങ്ങ്",
            crop_arecanut: "കവുങ്ങ്",
            crop_banana: "വാഴ",
            crop_mango: "മാവ്",
            crop_papaya: "പപ്പായ",
            crop_tomato: "തക്കാളി",
            crop_brinjal: "വഴുതനങ്ങ",
            crop_chilli: "മുളക്",
            crop_pepper: "കുരുമുളക്",
            crop_cocoa: "കോകോ",
            crop_paddy: "നെല്ല്",
            crop_rubber: "റബ്ബർ",
            grp_palms: "പനവർഗ്ഗ വിളകൾ",
            grp_fruits: "പഴവർഗ്ഗങ്ങൾ",
            grp_vegetables: "പച്ചക്കറികൾ",
            grp_spices: "വ്യഞ്ജനങ്ങൾ",
            grp_beverages: "പാനീയ വിളകൾ",
            grp_cereals: "ധാന്യങ്ങൾ",
            grp_plantation: "തോട്ടവിളകൾ",
            
            calc_dosage_title: "വളപ്രയോഗം കണക്കാക്കുക",
            form_crop: "വിളയുടെ ഇനം",
            form_age: "വിളയുടെ പ്രായം (വർഷത്തിൽ)",
            form_age_help: "തൈകൾ മുതൽ മുതിർന്ന വിളകൾ വരെ NPK അളവ് സ്വയം ക്രമീകരിക്കപ്പെടുന്നു.",
            form_soil: "മണ്ണിന്റെ ഇനം",
            form_health: "വിളയുടെ ആരോഗ്യസ്ഥിതി",
            btn_generate: "വളപ്രയോഗ വിവരങ്ങൾ ലഭിക്കുക",
            recipe_title: "കണക്കാക്കിയ വളപ്രയോഗ വിവരങ്ങൾ",
            th_pure_nutrients: "ലക്ഷ്യമിടുന്ന മൂലകങ്ങൾ (N-P-K)",
            th_comm_fert: "വിപണിയിലെ രാസവളങ്ങളുടെ അളവ് (ചാക്കുകളുടെ അനുപാതം)",
            th_split_schedule: "വിവിധ ഘട്ടങ്ങളിലെ വളപ്രയോഗ ഷെഡ്യൂൾ",
            
            lbl_urea: "യൂറിയ (Urea - 46% N)",
            lbl_ssp: "എസ്.എസ്.പി (SSP - 16% P₂O₅)",
            lbl_mop: "എം.ഒ.പി (MOP - 60% K₂O)",
            bag_urea_desc: "നൈട്രജൻ വളം",
            bag_ssp_desc: "ഫോസ്ഫറസ് വളം",
            bag_mop_desc: "പൊട്ടാസ്യം വളം",
            lbl_n: "നൈട്രജൻ (N)",
            lbl_p: "ഫോസ്ഫറസ് (P)",
            lbl_k: "പൊട്ടാസ്യം (K)",
            
            org_additive_title: "ജൈവവളങ്ങളും മറ്റ് പൂരകങ്ങളും",
            lbl_compost: "കാലിവളം/കമ്പോസ്റ്റ്",
            lbl_lime: "കുമ്മായം/ഡോളമൈറ്റ് പ്രയോഗം",
            lbl_deficiency_corrective: "ലഘുപോലക മൂലകങ്ങളുടെ കുറവ് നികത്തൽ",
            agri_actions_title: "കാർഷിക നിർദ്ദേശങ്ങൾ",
            lbl_soil_note: "മണ്ണിനെക്കുറിച്ചുള്ള കുറിപ്പ്",
            lbl_health_corr: "ആരോഗ്യസ്ഥിതി പരിഹാരം",
            lbl_best_practice: "വളപ്രയോഗത്തിന്റെ ശരിയായ രീതി",
            
            health_healthy: "ആരോഗ്യമുള്ളത് (സാധാരണ അളവ്)",
            health_fungal: "കുമിൾ/ബാക്ടീരിയ ബാധ (പ്രതിരോധ അളവ്)",
            health_pest: "കീടബാധ (പ്രതിരോധവും വീണ്ടെടുപ്പും)",
            health_deficiency: "പോഷകക്കുറവ് (പരിഹാര അളവ്)",
            health_stress: "കാലാവസ്ഥാ വ്യതിയാനം (വെള്ളക്കെട്ട്/വരൾച്ച)",
            
            soil_loamy: "എക്കൽ മണ്ണ് / ലോമി മണ്ണ് (ഏറ്റവും അനുയോജ്യം)",
            soil_sandy: "മണൽ മണ്ണ് (വളം ഒലിച്ചുപോകുന്നു)",
            soil_laterite: "ചെമ്മണ്ണ് (അമ്ലഗുണമുള്ളത്, ഫോസ്ഫറസ് തടയുന്നു)",
            soil_clayey: "കളിമണ്ണ് (വെള്ളക്കെട്ടുള്ളത്)",
            
            scan_step_1: "1. വിള തിരഞ്ഞെടുക്കുക",
            scan_step_2: "2. ഇലയുടെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
            prompt_tap: "ഫോട്ടോ എടുക്കാനോ തിരഞ്ഞെടുക്കാനോ ഇവിടെ ടാപ്പ് ചെയ്യുക",
            prompt_format: "പരമാവധി 10MB വരെയുള്ള JPG, PNG ചിത്രങ്ങൾ",
            load_parsing: "ഇലയുടെ പികസൽ ഘടന വിശകലനം ചെയ്യുന്നു...",
            load_running: "OpenCV കോണ്ടൂർ കണക്കുകൂട്ടലുകൾ പുരോഗമിക്കുന്നു",
            scan_instructions_title: "നിർദ്ദേശങ്ങളും നുറുങ്ങുകളും",
            tips_title: "കൃത്യത ഉറപ്പാക്കാൻ ചില നിർദ്ദേശങ്ങൾ:",
            tips_light: "നല്ല സ്വാഭാവിക വെളിച്ചത്തിൽ ഇലയുടെ ചിത്രം എടുക്കുക. നിഴലുകൾ ഒഴിവാക്കുക.",
            tips_focus: "രോഗബാധയുള്ള ഭാഗം കൃത്യമായി ഫോക്കസ് ചെയ്യുക.",
            tips_flat: "സാധ്യമെങ്കിൽ ഇല പരന്ന പ്രതലത്തിൽ വെച്ച് ഫോട്ടോ എടുക്കുക.",
            tips_blur: "ക്യാമറ ചലിക്കാതെ സ്ഥിരമായി പിടിക്കുക.",
            res_header: "പരിശോധനാ ഫലം",
            green_chlorophyll: "പച്ചപ്പ്‌ (ക്ലോറോഫിൽ)",
            yellow_chlorosis: "മഞ്ഞനിറം (ക്ലോറോസിസ്)",
            necrotic_brown: "കരിഞ്ഞ കവിൾച്ച (നെക്രോട്ടിക്)",
            observed_sym: "കണ്ടെത്തിയ ലക്ഷണങ്ങൾ:",
            org_recovery: "ജൈവ ചികിത്സ",
            chem_control: "രാസ ചികിത്സ",
            fert_adjust: "വളപ്രയോഗ ക്രമീകരണങ്ങൾ"
        }
    };

    const langSelector = document.getElementById('lang-selector');

    function translatePage(lang) {
        document.querySelectorAll('.trn').forEach(element => {
            const key = element.dataset.key;
            if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
                const tagName = element.tagName.toUpperCase();
                if (tagName === 'INPUT') {
                    element.placeholder = TRANSLATIONS[lang][key];
                } else if (tagName === 'OPTGROUP') {
                    element.label = TRANSLATIONS[lang][key];
                } else {
                    element.textContent = TRANSLATIONS[lang][key];
                }
            }
        });
        
        const placeholders = {
            en: 'Ask AgriBot...',
            kn: 'ಅಗ್ರಿಬಾಟ್ ಜೊತೆ ಮಾತನಾಡಿ...',
            ml: 'ചോദിക്കൂ...',
            hi: 'एग्रीबॉट से पूछें...',
            te: 'అగ్రిబాట్ ని అడగండి...',
            ta: 'அக்ரிபாட்டிடம் கேளுங்கள்...'
        };
        const cInput = document.getElementById('chat-input');
        if (cInput) {
            cInput.placeholder = placeholders[lang] || 'Ask AgriBot...';
        }
    }

    // ----------------------------------------------------
    // Weather Search Functionality
    // ----------------------------------------------------
    const weatherForm = document.getElementById('weather-search-form');
    const weatherInput = document.getElementById('weather-search-input');
    
    if (weatherForm && weatherInput) {
        weatherForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const locationVal = weatherInput.value.trim();
            if (!locationVal) return;
            
            const goBtn = weatherForm.querySelector('button');
            const originalBtnText = goBtn.textContent;
            goBtn.textContent = '...';
            goBtn.disabled = true;
            
            fetch('/api/weather', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ location: locationVal })
            })
            .then(res => {
                if (!res.ok) {
                    throw new Error('Weather fetch failed');
                }
                return res.json();
            })
            .then(data => {
                const tempEl = document.getElementById('val-temperature');
                const condEl = document.getElementById('val-condition');
                const locEl = document.getElementById('val-location');
                const humEl = document.getElementById('val-humidity');
                const moistEl = document.getElementById('val-soil-moisture');
                
                if (tempEl) tempEl.textContent = data.temperature;
                if (condEl) {
                    condEl.textContent = data.weather_condition;
                    condEl.removeAttribute('data-key'); 
                }
                if (locEl) locEl.textContent = data.location;
                if (humEl) humEl.textContent = data.humidity;
                if (moistEl) {
                    moistEl.textContent = data.soil_moisture;
                    moistEl.removeAttribute('data-key');
                }
                
                weatherInput.value = '';
            })
            .catch(err => {
                console.error(err);
                alert('Could not fetch weather data for that location. Please try again.');
            })
            .finally(() => {
                goBtn.textContent = originalBtnText;
                goBtn.disabled = false;
            });
        });
    }

    // ----------------------------------------------------
    // Dynamic Translation overrides & New keys
    // ----------------------------------------------------
    const newTranslations = {
        en: {
            nav_calendar: "Farming Calendar",
            nav_cal_mobile: "Calendar",
            calendar_title: "Interactive Farming Calendar",
            form_sowing_date: "Sowing / Planting Date",
            btn_generate_calendar: "Generate Farming Schedule",
            calendar_start_date: "Planted on",
            btn_clear_calendar: "Clear Schedule",
            followup_q_label: "📷 Follow-up Questions (Click to Ask Bot):",
            weather_advisory_title: "Regional & Weather-Aware Advisory",
            guide_select_crop: "Select Crop to View Guide",
            guide_soil: "Soil Requirements",
            guide_sowing: "Sowing & Planting",
            guide_irrigation: "Irrigation Schedule",
            guide_npk: "NPK & Compost",
            guide_harvest: "Harvest Indicators",
            guide_storage: "Post-Harvest Storage",
            faq_hub_title: "Frequently Asked Farming Questions",
            tab_encyclopedia: "Disease Encyclopedia",
            tab_beginner: "Beginner's Guide",
            tab_faq: "Farming FAQ Hub",
            priority_high: "🚨 Immediate Action Required",
            priority_medium: "⚠️ Moderate Severity - Monitor & Treat",
            priority_info: "🟢 Routine Care - Crop Healthy",
            q_fungal_cause: "What causes this fungal infection?",
            q_fungal_prevent: "How to prevent fungal spores from spreading?",
            q_fungal_chemical: "Which chemical fungicide is best?",
            q_viral_cause: "What virus causes this disease?",
            q_viral_vector: "How to control the insect vectors spreading it?",
            q_viral_destroy: "Should I destroy the infected crop?",
            q_bacterial_cause: "How does bacterial blight spread?",
            q_bacterial_spray: "What bactericide spray should I use?",
            q_bacterial_prevent: "How to disinfect farming tools?",
            q_pest_cause: "What insect is causing this damage?",
            q_pest_organic: "What organic pest repellent works best?",
            q_pest_spray: "When is the best time to spray pesticide?",
            q_healthy_npk: "What NPK dosage is recommended?",
            q_healthy_water: "How often should I irrigate my crop?",
            q_healthy_disease: "What are common diseases to watch out for?",
            cal_stage_planting: "Planting / Sowing",
            cal_stage_fert1: "First Fertilizer Application",
            cal_stage_fert2: "Second Fertilizer Application",
            cal_stage_fert3: "Third Fertilizer Application",
            cal_stage_harvest: "Maturity & Harvesting",
            cal_desc_basal_palm: "Dig pit, mix with organic compost and basal Phosphorus/Potassium.",
            cal_desc_fert_palm1: "Apply first split of Urea and MOP close to root base in wet soil.",
            cal_desc_fert_palm2: "Apply remaining split of Urea, MOP and Magnesium Sulfate.",
            cal_desc_harvest_palm: "Harvest mature crop yielding fruits.",
            cal_desc_basal_veg: "Prepare bed, mix basal NPK and organic compost.",
            cal_desc_fert_veg1: "Vegetative stage: Top dress with Nitrogen (Urea) and trace elements.",
            cal_desc_fert_veg2: "Fruiting stage: Apply remaining splits of Nitrogen and Potassium.",
            cal_desc_harvest_veg: "Harvest mature green/ripe fruits regularly.",
            cal_desc_basal_field: "Puddle field, mix basal compost and initial NPK split.",
            cal_desc_fert_field1: "Tillering stage: Apply Urea split and Zinc Sulfate corrective.",
            cal_desc_fert_field2: "Panicle stage: Apply final Urea split and remaining MOP.",
            cal_desc_harvest_field: "Harvest golden stalks when grains reach maturity."
        },
        kn: {
            nav_calendar: "ಕೃಷಿ ಕ್ಯಾಲೆಂಡರ್",
            nav_cal_mobile: "ಕ್ಯಾಲೆಂಡರ್",
            calendar_title: "ಸಂವಾದಾತ್ಮಕ ಕೃಷಿ ಕ್ಯಾಲೆಂಡರ್",
            form_sowing_date: "ಬಿತ್ತನೆ / ನಾಟಿ ದಿನಾಂಕ",
            btn_generate_calendar: "ಕೃಷಿ ವೇಳಾಪಟ್ಟಿ ತಯಾರಿಸಿ",
            calendar_start_date: "ನಾಟಿ ಮಾಡಿದ ದಿನಾಂಕ",
            btn_clear_calendar: "ವೇಳಾಪಟ್ಟಿ ಅಳಿಸಿ",
            followup_q_label: "📷 ಅನುಸರಣಾ ಪ್ರಶ್ನೆಗಳು (ಬಾಟ್‌ಗೆ ಕೇಳಲು ಕ್ಲಿಕ್ ಮಾಡಿ):",
            weather_advisory_title: "ಪ್ರಾದೇಶಿಕ ಮತ್ತು ಹವಾಮಾನ ಸಲಹೆ",
            guide_select_crop: "ಮಾರ್ಗದರ್ಶಿ ವೀಕ್ಷಿಸಲು ಬೆಳೆಯನ್ನು ಆರಿಸಿ",
            guide_soil: "ಮಣ್ಣಿನ ಅವಶ್ಯಕತೆಗಳು",
            guide_sowing: "ಬಿತ್ತನೆ ಮತ್ತು ನಾಟಿ",
            guide_irrigation: "ನೀರಾವರಿ ವೇಳಾಪಟ್ಟಿ",
            guide_npk: "NPK ಮತ್ತು ಕಾಂಪೋಸ್ಟ್",
            guide_harvest: "ಕೊಯ್ಲು ಸೂಚಕಗಳು",
            guide_storage: "ಕೊಯ್ಲಿನ ನಂತರದ ಶೇಖರಣೆ",
            faq_hub_title: "ಸಾಮಾನ್ಯ ಕೃಷಿ ಪ್ರಶ್ನೋತ್ತರಗಳು",
            tab_encyclopedia: "ರೋಗ ಮಾಹಿತಿ ಕೋಶ",
            tab_beginner: "ಆರಂಭಿಕರ ಮಾರ್ಗದರ್ಶಿ",
            tab_faq: "ಕೃಷಿ FAQ ಹಬ್",
            priority_high: "🚨 ತಕ್ಷಣದ ಕ್ರಮ ಅಗತ್ಯ",
            priority_medium: "⚠️ ಮಧ್ಯಮ ತೀವ್ರತೆ - ಗಮನಿಸಿ ಮತ್ತು ಚಿಕಿತ್ಸೆ ನೀಡಿ",
            priority_info: "🟢 ನಿಯಮಿತ ರಕ್ಷಣೆ - ಬೆಳೆ ಆರೋಗ್ಯಕರವಾಗಿದೆ",
            q_fungal_cause: "ಈ ಶಿಲೀಂಧ್ರ ರೋಗಕ್ಕೆ ಕಾರಣವೇನು?",
            q_fungal_prevent: "ಶಿಲೀಂಧ್ರ ರೋಗ ಇತರ ಗಿಡಗಳಿಗೆ ಹರಡುವುದನ್ನು ತಡೆಯುವುದು ಹೇಗೆ?",
            q_fungal_chemical: "ಯಾವ ರಾಸಾಯನಿಕ ಶಿಲೀಂಧ್ರನಾಶಕ ಅತ್ಯುತ್ತಮ?",
            q_viral_cause: "ಯಾವ ವೈರಸ್ ಈ ರೋಗಕ್ಕೆ ಕಾರಣ?",
            q_viral_vector: "ರೋಗ ಹರಡುವ ಕೀಟಗಳನ್ನು ನಿಯಂತ್ರಿಸುವುದು ಹೇಗೆ?",
            q_viral_destroy: "ರೋಗಗ್ರಸ್ತ ಗಿಡವನ್ನು ಕಿತ್ತು ಹಾಕಬೇಕೇ?",
            q_bacterial_cause: "ಬ್ಯಾಕ್ಟೀರಿಯಾ ರೋಗ ಹೇಗೆ ಹರಡುತ್ತದೆ?",
            q_bacterial_spray: "ಯಾವ ಬ್ಯಾಕ್ಟೀರಿಯಾ ನಾಶಕ ಸಿಂಪಡಿಸಬೇಕು?",
            q_bacterial_prevent: "ಕೃಷಿ ಉಪಕರಣಗಳನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸುವುದು ಹೇಗೆ?",
            q_pest_cause: "ಯಾವ ಕೀಟ ಈ ಹಾನಿಯನ್ನು ಉಂಟುಮಾಡುತ್ತಿದೆ?",
            q_pest_organic: "ಯಾವ ಸಾವಯವ ಕೀಟನಾಶಕ ಅತ್ಯುತ್ತಮ?",
            q_pest_spray: "ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಲು ಸೂಕ್ತ ಸಮಯ ಯಾವುದು?",
            q_healthy_npk: "ಯಾವ NPK ಗೊಬ್ಬರದ ಪ್ರಮಾಣ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ?",
            q_healthy_water: "ಬೆಳೆಗೆ ಎಷ್ಟು ಬಾರಿ ನೀರು ಹಾಯಿಸಬೇಕು?",
            q_healthy_disease: "ಬೆಳೆಗೆ ಬರುವ ಇತರ ಪ್ರಮುಖ ರೋಗಗಳು ಯಾವುವು?",
            cal_stage_planting: "ನಾಟಿ / ಬಿತ್ತನೆ",
            cal_stage_fert1: "ಮೊದಲ ರಸಗೊಬ್ಬರ ಅನ್ವಯ",
            cal_stage_fert2: "ಎರಡನೇ ರಸಗೊಬ್ಬರ ಅನ್ವಯ",
            cal_stage_fert3: "ಮೂರನೇ ರಸಗೊಬ್ಬರ ಅನ್ವಯ",
            cal_stage_harvest: "ಪಕ್ವತೆ ಮತ್ತು ಕೊಯ್ಲು",
            cal_desc_basal_palm: "ಗುಂಡಿ ತೆಗೆಯಿರಿ, ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ ಮತ್ತು ಮೂಲ ಗೊಬ್ಬರ ಮಿಶ್ರಣ ಮಾಡಿ.",
            cal_desc_fert_palm1: "ತೇವವಾದ ಮಣ್ಣಿನಲ್ಲಿ ಯೂರಿಯಾ ಮತ್ತು ಎಂ.ಓ.ಪಿ ಮೊದಲ ಕಂತನ್ನು ಬುಡಕ್ಕೆ ನೀಡಿ.",
            cal_desc_fert_palm2: "ಯೂರಿಯಾ, ಎಂ.ಓ.ಪಿ ಮತ್ತು ಮೆಗ್ನೀಸಿಯಮ್ ಗೊಬ್ಬರದ ಕೊನೆಯ ಕಂತನ್ನು ಬುಡಕ್ಕೆ ನೀಡಿ.",
            cal_desc_harvest_palm: "ಬಲಿತ ಬೆಳೆ ಮತ್ತು ಕಾಯಿಗಳನ್ನು ಕೊಯ್ಲು ಮಾಡಿ.",
            cal_desc_basal_veg: "ಮಡಿಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಿ, ಮೂಲ ರಸಗೊಬ್ಬರ ಮತ್ತು ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ ಮಿಶ್ರಣ ಮಾಡಿ.",
            cal_desc_fert_veg1: "ಸಸ್ಯ ಬೆಳವಣಿಗೆ ಹಂತ: ಸಾರಜನಕ ಮತ್ತು ಲಘು ಪೋಷಕಾಂಶಗಳನ್ನು ಮೇಲುಗೊಬ್ಬರವಾಗಿ ನೀಡಿ.",
            cal_desc_fert_veg2: "ಕಾಯಿ ಹಂತ: ಸಾರಜನಕ ಮತ್ತು ಪೊಟ್ಯಾಷಿಯಂ ಗೊಬ್ಬರದ ಕೊನೆಯ ಕಂತನ್ನು ನೀಡಿ.",
            cal_desc_harvest_veg: "ಬಲಿತ ಹಣ್ಣುಗಳನ್ನು ನಿಯಮಿತವಾಗಿ ಕೊಯ್ಲು ಮಾಡಿ.",
            cal_desc_basal_field: "ಹೊಲವನ್ನು ಕೆಸರು ಮಾಡಿ, ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ ಮತ್ತು ಆರಂಭಿಕ ರಸಗೊಬ್ಬರ ಮಿಶ್ರಣ ಮಾಡಿ.",
            cal_desc_fert_field1: "ಪಿಲಿಕೊಡೆಯುವ ಹಂತ: ಯೂರಿಯಾ ಮತ್ತು ಜಿಂಕ್ ಸಲ್ಫೇಟ್ ಗೊಬ್ಬರವನ್ನು ನೀಡಿ.",
            cal_desc_fert_field2: "ತೆನೆ ಬರುವ ಹಂತ: ಕೊನೆಯ ಯೂರಿಯಾ ಕಂತು ಮತ್ತು ಪೊಟ್ಯಾಷಿಯಂ ಗೊಬ್ಬರವನ್ನು ನೀಡಿ.",
            cal_desc_harvest_field: "ತೆನೆಗಳು ಬಂಗಾರದ ಬಣ್ಣಕ್ಕೆ ತಿರುಗಿದಾಗ ಕಟಾವು ಮಾಡಿ."
        },
        hi: {
            nav_calendar: "कृषि कैलेंडर",
            nav_cal_mobile: "कैलेंडर",
            calendar_title: "इंटरैक्टिव कृषि कैलेंडर",
            form_sowing_date: "बुवाई / रोपाई की तिथि",
            btn_generate_calendar: "कृषि अनुसूची बनाएं",
            calendar_start_date: "रोपाई की तिथि",
            btn_clear_calendar: "अनुसूची हटाएं",
            followup_q_label: "📷 अनुवर्ती प्रश्न (बॉट से पूछने के लिए क्लिक करें):",
            weather_advisory_title: "क्षेत्रीय और मौसम संबंधी सलाह",
            guide_select_crop: "मार्गदर्शिका देखने के लिए फसल चुनें",
            guide_soil: "मिट्टी की आवश्यकताएं",
            guide_sowing: "बुवाई और रोपाई",
            guide_irrigation: "सिंचाई अनुसूची",
            guide_npk: "एनपीके और कम्पोस्ट",
            guide_harvest: "कटाई के संकेतक",
            guide_storage: "कटाई के बाद भंडारण",
            faq_hub_title: "अक्सर पूछे जाने वाले कृषि प्रश्न",
            tab_encyclopedia: "रोग विश्वकोश",
            tab_beginner: "शुरुआती गाइड",
            tab_faq: "कृषि एफएक्यू हब",
            priority_high: "🚨 तत्काल कार्रवाई की आवश्यकता",
            priority_medium: "⚠️ मध्यम गंभीरता - निगरानी और उपचार",
            priority_info: "🟢 सामान्य देखभाल - फसल स्वस्थ है",
            q_fungal_cause: "इस फंगल संक्रमण का कारण क्या है?",
            q_fungal_prevent: "फंगल बीजाणुओं को फैलने से कैसे रोकें?",
            q_fungal_chemical: "कौन सा रासायनिक फफूंदनाशी सर्वोत्तम है?",
            q_viral_cause: "इस बीमारी का कारण कौन सा वायरस है?",
            q_viral_vector: "इसे फैलाने वाले कीट वाहकों को कैसे नियंत्रित करें?",
            q_viral_destroy: "क्या मुझे संक्रमित पौधे को नष्ट कर देना चाहिए?",
            q_bacterial_cause: "बैक्टीरियल ब्लाइट कैसे फैलता है?",
            q_bacterial_spray: "मुझे किस जीवाणुनाशक स्प्रे का उपयोग करना चाहिए?",
            q_bacterial_prevent: "खेती के औजारों को कीटाणुरहित कैसे करें?",
            q_pest_cause: "यह नुकसान कौन सा कीट पहुंचा रहा है?",
            q_pest_organic: "कौन सा जैविक कीट विकर्षक सबसे अच्छा काम करता है?",
            q_pest_spray: "कीटनाशक छिड़कने का सबसे अच्छा समय क्या है?",
            q_healthy_npk: "कौन सी एनपीके खुराक की सिफारिश की जाती है?",
            q_healthy_water: "मुझे अपनी फसल की सिंचाई कितनी बार करनी चाहिए?",
            q_healthy_disease: "ध्यान देने योग्य सामान्य बीमारियाँ कौन सी हैं?",
            cal_stage_planting: "बुवाई / रोपाई",
            cal_stage_fert1: "पहला उर्वरक अनुप्रयोग",
            cal_stage_fert2: "दूसरा उर्वरक अनुप्रयोग",
            cal_stage_fert3: "तीसरा उर्वरक अनुप्रयोग",
            cal_stage_harvest: "परिपक्वता और कटाई",
            cal_desc_basal_palm: "गड्ढा खोदें, जैविक खाद और बुनियादी फास्फोरस/पोटाश मिलाएं।",
            cal_desc_fert_palm1: "गीली मिट्टी में जड़ों के पास यूरिया और एमओपी की पहली किस्त डालें।",
            cal_desc_fert_palm2: "यूरिया, एमओपी और मैग्नीशियम सल्फेट की शेष किस्त डालें।",
            cal_desc_harvest_palm: "फलों की कटाई या तुड़ाई करें।",
            cal_desc_basal_veg: "क्यारी तैयार करें, आधार एनपीके और जैविक खाद मिलाएं।",
            cal_desc_fert_veg1: "वानस्पतिक अवस्था: नाइट्रोजन (यूरिया) और सूक्ष्म तत्वों से टॉप ड्रेसिंग करें।",
            cal_desc_fert_veg2: "फल लगने की अवस्था: नाइट्रोजन और पोटेशियम की शेष किस्तें डालें।",
            cal_desc_harvest_veg: "नियमित रूप से परिपक्व फलों की तुड़ाई करें।",
            cal_desc_basal_field: "खेत तैयार करें, आधार कम्पोस्ट और प्रारंभिक एनपीके खुराक मिलाएं।",
            cal_desc_fert_field1: "कल्ले फूटने की अवस्था: यूरिया और जिंक सल्फेट डालें।",
            cal_desc_fert_field2: "बाली निकलने की अवस्था: अंतिम यूरिया और शेष एमओपी डालें।",
            cal_desc_harvest_field: "दानों के पकने पर सुनहरी बालियों की कटाई करें।"
        },
        te: {
            nav_calendar: "వ్యవసాయ క్యాలెండర్",
            nav_cal_mobile: "క్యాలెండర్",
            calendar_title: "ఇంటరాక్టివ్ వ్యవసాయ క్యాలెండర్",
            form_sowing_date: "విత్తే / నాటే తేదీ",
            btn_generate_calendar: "వ్యవసాయ షెడ్యూల్ పొందండి",
            calendar_start_date: "నాటిన తేదీ",
            btn_clear_calendar: "షెడ్యూల్ తొలగించు",
            followup_q_label: "📷 అనుసరణ ప్రశ్నలు (బాల్ట్‌ని అడగడానికి క్లిక్ చేయండి):",
            weather_advisory_title: "ప్రాంతీయ & వాతావరణ సలహా",
            guide_select_crop: "సాగు గైడ్ చూడటానికి పంటను ఎంచుకోండి",
            guide_soil: "మట్టి అవసరాలు",
            guide_sowing: "విత్తడం & నాటడం",
            guide_irrigation: "నీటి యాజమాన్యం",
            guide_npk: "NPK మరియు కంపోస్ట్",
            guide_harvest: "కోత గుర్తులు",
            guide_storage: "కోత అనంతర నిల్వ",
            faq_hub_title: "తరచుగా అడిగే వ్యవసాయ ప్రశ్నలు",
            tab_encyclopedia: "తెగుళ్ల డేటాబేస్",
            tab_beginner: "ఆరంభకుల గైడ్",
            tab_faq: "వ్యవసాయ ప్రశ్నల హబ్",
            priority_high: "🚨 తక్షణ చర్య అవసరం",
            priority_medium: "⚠️ సాధారణ తీవ్రత - పర్యవేక్షణ & నివారణ",
            priority_info: "🟢 సాధారణ సంరక్షణ - పంట ఆరోగ్యంగా ఉంది",
            q_fungal_cause: "ఈ శిలీంధ్ర తెగులు రావడానికి కారణం ఏమిటి?",
            q_fungal_prevent: "శిలీంధ్ర వ్యాప్తిని ఎలా అరికట్టాలి?",
            q_fungal_chemical: "ఏ రసాయన శిలీంధ్రనాశకం ఉత్తమమైనది?",
            q_viral_cause: "ఈ తెగులుకు కారణమైన వైరస్ ఏది?",
            q_viral_vector: "వైరస్ వ్యాప్తి చేసే కీటకాలను ఎలా నియంత్రించాలి?",
            q_viral_destroy: "తెగులు సోకిన మొక్కను తీసివేసి నాశనం చేయాలా?",
            q_bacterial_cause: "బ్యాక్టీరియా తెగులు ఎలా వ్యాపిస్తుంది?",
            q_bacterial_spray: "ఏ బ్యాక్టీరియా నాశక పిచికారీ వాడాలి?",
            q_bacterial_prevent: "వ్యవసాయ పనిముట్లను ఎలా శుభ్రపరచాలి?",
            q_pest_cause: "ఈ నష్టం కలిగిస్తున్న పురుగు ఏది?",
            q_pest_organic: "ఏ సేంద్రీయ పురుగు నివారణ పద్ధతి బాగా పనిచేస్తుంది?",
            q_pest_spray: "పురుగుల మందు పిచికారీ చేయడానికి సరైన సమయం ఏది?",
            q_healthy_npk: "పంటకు ఎంత ఎన్.పి.కె (NPK) మోతాదు సిఫార్సు చేయబడింది?",
            q_healthy_water: "పంటకు ఎన్ని రోజులకు ఒకసారి నీటి తడులు ఇవ్వాలి?",
            q_healthy_disease: "పంటకు వచ్చే సాధారణ తెగుళ్లు ఏమిటి?",
            cal_stage_planting: "నాటడం / విత్తడం",
            cal_stage_fert1: "మొదటి ఎరువుల విడత",
            cal_stage_fert2: "రెండవ ఎరువుల విడత",
            cal_stage_fert3: "మూడవ ఎరువుల విడత",
            cal_stage_harvest: "పంట కోత దశ",
            cal_desc_basal_palm: "గుంత తవ్వి, సేంద్రీయ ఎరువు మరియు మొదటి విడత భాస్వరం/పొటాష్ కలపండి.",
            cal_desc_fert_palm1: "తడి నేలలో వేర్ల దగ్గర యూరియా మరియు ఎమ్.ఓ.పి మొదటి విడత వేయండి.",
            cal_desc_fert_palm2: "యూరియా, ఎమ్.ఓ.పి మరియు మెగ్నీషియం సల్ఫేట్ చివరి విడత వేయండి.",
            cal_desc_harvest_palm: "పక్వానికి వచ్చిన కాయలు కోయండి.",
            cal_desc_basal_veg: "నేల సిద్ధం చేసి, ఎరువులు మరియు సేంద్రీయ కంపోస్ట్ కలపండి.",
            cal_desc_fert_veg1: "ఎదుగుదల దశ: నత్రజని (యూరియా) మరియు సూక్ష్మ పోషకాలను వేయండి.",
            cal_desc_fert_veg2: "కాయ దశ: మిగిలిన నత్రజని మరియు పొటాషియం ఎరువులు వేయండి.",
            cal_desc_harvest_veg: "పక్వానికి వచ్చిన కాయలను క్రమం తప్పకుండా కోయండి.",
            cal_desc_basal_field: "దుక్కి దున్ని, బేసల్ కంపోస్ట్ మరియు ప్రారంభ ఎరువులు వేయండి.",
            cal_desc_fert_field1: "పిలక దశ: యూరియా మరియు జింక్ సల్ఫేట్ వేయండి.",
            cal_desc_fert_field2: "పొట్ట దశ: చివరి యూరియా మరియు పొటాషియం ఎరువులు వేయండి.",
            cal_desc_harvest_field: "వెన్నులు బంగారు రంగుకు మారినప్పుడు పంట కోయండి."
        },
        ta: {
            nav_calendar: "விவசாய நாட்காட்டி",
            nav_cal_mobile: "நாட்காட்டி",
            calendar_title: "விவசாய நாட்காட்டி வழிகாட்டி",
            form_sowing_date: "விதைப்பு / நடவு தேதி",
            btn_generate_calendar: "விவசாய அட்டவணை பெறுக",
            calendar_start_date: "நடவு செய்யப்பட்ட தேதி",
            btn_clear_calendar: "அட்டவணையை அழி",
            followup_q_label: "📷 தொடர் கேள்விகள் (பதில் பெற கிளிக் செய்யவும்):",
            weather_advisory_title: "மண்டல & வானிலை ஆலோசனை",
            guide_select_crop: "சாகுபடி வழிகாட்டி பெற பயிரை தேர்வு செய்க",
            guide_soil: "மண் தேவைகள்",
            guide_sowing: "விதைப்பு மற்றும் நடவு",
            guide_irrigation: "நீர் மேலாண்மை அட்டவணை",
            guide_npk: "NPK மற்றும் உரம்",
            guide_harvest: "அறுவடை அறிகுறிகள்",
            guide_storage: "அறுவடைக்கு பின் சேமிப்பு",
            faq_hub_title: "விவசாயம் சார்ந்த பொதுவான கேள்விகள்",
            tab_encyclopedia: "நோய் களஞ்சியம்",
            tab_beginner: "தொடக்க வழிகாட்டி",
            tab_faq: "விவசாய FAQ மையம்",
            priority_high: "🚨 உடனடி நடவடிக்கை தேவை",
            priority_medium: "⚠️ நடுத்தர பாதிப்பு - கண்காணித்து உரமிடவும்",
            priority_info: "🟢 வழக்கமான பராமரிப்பு - பயிர் ஆரோக்கியமாக உள்ளது",
            q_fungal_cause: "இந்த பூஞ்சை தொற்றுக்கு என்ன காரணம்?",
            q_fungal_prevent: "பூஞ்சை காளான்கள் பரவாமல் தடுப்பது எப்படி?",
            q_fungal_chemical: "எந்த இரசாயன பூஞ்சைக் கொல்லி சிறந்தது?",
            q_viral_cause: "இந்த நோயை உண்டாக்கும் வைரஸ் எது?",
            q_viral_vector: "வைரஸைப் பரப்பும் பூச்சிகளைக் கட்டுப்படுத்துவது எப்படி?",
            q_viral_destroy: "பாதிக்கப்பட்ட பயிரை அழிக்க வேண்டுமா?",
            q_bacterial_cause: "பாக்டீரியா கருகல் நோய் எவ்வாறு பரவுகிறது?",
            q_bacterial_spray: "நான் என்ன பாக்டீரியா எதிர்ப்பு மருந்து தெளிக்க வேண்டும்?",
            q_bacterial_prevent: "விவசாயக் கருவிகளை எவ்வாறு கிருமி நீக்கம் செய்வது?",
            q_pest_cause: "இந்த சேதத்தை ஏற்படுத்தும் பூச்சி எது?",
            q_pest_organic: "எந்த இயற்கை பூச்சி விரட்டி நன்றாக வேலை செய்யும்?",
            q_pest_spray: "பூச்சிக்கொல்லி தெளிக்க சிறந்த நேரம் எது?",
            q_healthy_npk: "பரிந்துரைக்கப்படும் NPK உர அளவு என்ன?",
            q_healthy_water: "பயிர்களுக்கு எவ்வளவு அடிக்கடி நீர் பாய்ச்ச வேண்டும்?",
            q_healthy_disease: "கவனிக்க வேண்டிய பொதுவான நோய்கள் என்ன?",
            cal_stage_planting: "நடவு / விதைப்பு",
            cal_stage_fert1: "முதல் தவணை உரமிடுதல்",
            cal_stage_fert2: "இரண்டாம் தவணை உரமிடுதல்",
            cal_stage_fert3: "மூன்றாம் தவணை உரமிடுதல்",
            cal_stage_harvest: "அறுவடை பருவம்",
            cal_desc_basal_palm: "குழி தோண்டி, இயற்கை உரம் மற்றும் அடி உரங்களை இடவும்.",
            cal_desc_fert_palm1: "ஈரமான மண்ணில் யூரியா மற்றும் எம்.ഓ.பி முதல் தவணை இடவும்.",
            cal_desc_fert_palm2: "யூரியா, எம்.ഓ.பி மற்றும் மெக்னீசியம் சல்பேட் இறுதி தவணை இடவும்.",
            cal_desc_harvest_palm: "முதிர்ந்த காய்களை அறுவடை செய்யவும்.",
            cal_desc_basal_veg: "நிலம் தயாரித்து, அடி உரம் மற்றும் இயற்கை உரம் இடவும்.",
            cal_desc_fert_veg1: "வளர்ச்சி பருவம்: நைட்ரஜன் மற்றும் நுண்ணூட்ட சத்துக்களை இடவும்.",
            cal_desc_fert_veg2: "காய் பருவம்: மீதமுள்ள நைட்ரஜன் மற்றும் பொட்டாசியம் உரங்களை இடவும்.",
            cal_desc_harvest_veg: "முதிர்ந்த காய்களை வழக்கமாக அறுவடை செய்யவும்.",
            cal_desc_basal_field: "சேற்றுழவு செய்து, தொழு உரம் மற்றும் அடி உரம் இடவும்.",
            cal_desc_fert_field1: "தூர்க்கட்டும் பருவம்: யூரியா மற்றும் துத்தநாக சல்பேட் இடவும்.",
            cal_desc_fert_field2: "கருதிப் பருவம்: இறுதி யூரியா மற்றும் மீதமுள்ள பொட்டாசியம் இடவும்.",
            cal_desc_harvest_field: "கதிர்கள் பொன்னிறமாக மாறியதும் அறுவடை செய்யவும்."
        },
        ml: {
            nav_calendar: "കൃഷി കലണ്ടർ",
            nav_cal_mobile: "കലണ്ടർ",
            calendar_title: "ഇന്ററാക്ടീവ് കൃഷി കലണ്ടർ",
            form_sowing_date: "വിതച്ച / നട്ട തീയതി",
            btn_generate_calendar: "കൃഷി ഷെഡ്യൂൾ നിർമ്മിക്കുക",
            calendar_start_date: "നട്ട തീയതി",
            btn_clear_calendar: "ഷെഡ്യൂൾ ഒഴിവാക്കുക",
            followup_q_label: "📷 തുടർ ചോദ്യങ്ങൾ (ചോദിക്കാൻ ക്ലിക്ക് ചെയ്യുക):",
            weather_advisory_title: "പ്രാദേശിക & കാലാവസ്ഥാ നിർദ്ദേശം",
            guide_select_crop: "കൃഷി രീതി കാണാൻ വിള തിരഞ്ഞെടുക്കുക",
            guide_soil: "മണ്ണിന്റെ ആവശ്യകതകൾ",
            guide_sowing: "വിത്തു വിതയ്ക്കലും നടീലും",
            guide_irrigation: "നനയ്ക്കൽ ക്രമം",
            guide_npk: "NPK വളങ്ങളും കമ്പോസ്റ്റും",
            guide_harvest: "വിളവെടുപ്പ് ലക്ഷണങ്ങൾ",
            guide_storage: "വിളവെടുപ്പിന് ശേഷമുള്ള സംഭരണം",
            faq_hub_title: "പതിവായുള്ള കാർഷിക ചോദ്യങ്ങൾ",
            tab_encyclopedia: "രോഗ വിവരപ്പട്ടിക",
            tab_beginner: "തുടക്കക്കാർക്കുള്ള സഹായി",
            tab_faq: "കൃഷി FAQ ഹബ്",
            priority_high: "🚨 അടിയന്തര നടപടി ആവശ്യമാണ്",
            priority_medium: "⚠️ ഇടത്തരം രോഗബാധ - നിരീക്ഷിച്ച് വളമിടുക",
            priority_info: "🟢 സാധാരണ പരിചരണം - വിള ആരോഗ്യമുള്ളതാണ്",
            q_fungal_cause: "ഈ കുമിൾ രോഗത്തിന് കാരണമെന്താണ്?",
            q_fungal_prevent: "കുമിൾ രോഗം പടരുന്നത് എങ്ങനെ തടയാം?",
            q_fungal_chemical: "ഏറ്റവും മികച്ച രാസ കുമിൾനാശിനി ഏതാണ്?",
            q_viral_cause: "ഏത് വൈറസാണ് ഈ രോഗത്തിന് കാരണം?",
            q_viral_vector: "രോഗം പരത്തുന്ന കീടങ്ങളെ എങ്ങനെ നിയന്ത്രിക്കാം?",
            q_viral_destroy: "രോഗം ബാധിച്ച ചെടി നശിപ്പിച്ചു കളയേണ്ടതുണ്ടോ?",
            q_bacterial_cause: "ബാക്ടീരിയൽ വാട്ടം എങ്ങനെയാണ് പടരുന്നത്?",
            q_bacterial_spray: "ഏത് ബാക്ടീരിയനാശിനിയാണ് തളിക്കേണ്ടത്?",
            q_bacterial_prevent: "കാർഷിക ഉപകരണങ്ങൾ എങ്ങനെ അണുവിമുക്തമാക്കാം?",
            q_pest_cause: "ഏത് കീടമാണ് ഈ നാശനഷ്ടം ഉണ്ടാക്കുന്നത്?",
            q_pest_organic: "ഏത് ജൈവ കീടനാശിനിയാണ് ഏറ്റവും ഫലപ്രദം?",
            q_pest_spray: "കീടനാശിനി തളിക്കാൻ ഏറ്റവും അനുയോജ്യമായ സമയം എപ്പോഴാണ്?",
            q_healthy_npk: "ശുപാർശ ചെയ്യുന്ന NPK വളത്തിന്റെ അളവ് എത്രയാണ്?",
            q_healthy_water: "വിളകൾ നനയ്ക്കേണ്ടത് എത്ര ദിവസങ്ങളുടെ ഇടവേളകളിലാണ്?",
            q_healthy_disease: "ശ്രദ്ധിക്കേണ്ട പ്രധാന രോഗങ്ങൾ ഏതെല്ലാമാണ്?",
            cal_stage_planting: "നടീൽ / വിതയ്ക്കൽ",
            cal_stage_fert1: "ഒന്നാം ഘട്ട വളപ്രയോഗം",
            cal_stage_fert2: "രണ്ടാം ഘട്ട വളപ്രയോഗം",
            cal_stage_fert3: "മൂന്നാം ഘട്ട വളപ്രയോഗം",
            cal_stage_harvest: "വിളവെടുപ്പ് ഘട്ടം",
            cal_desc_basal_palm: "തടമെടുത്ത് കാലിവളവും ആദ്യത്തെ വളപ്രയോഗവും നടത്തുക.",
            cal_desc_fert_palm1: "നനവുള്ള മണ്ണിൽ വേരിന് ചുറ്റും യൂറിയയും പൊട്ടാഷും ചേർക്കുക.",
            cal_desc_fert_palm2: "ബാക്കി യൂറിയ, പൊട്ടാഷ്, മഗ്നീഷ്യം എന്നിവ ചേർക്കുക.",
            cal_desc_harvest_palm: "വിളവെടുപ്പ് നടത്തി ആദായം എടുക്കുക.",
            cal_desc_basal_veg: "തടമൊരുക്കി അടിസ്ഥാന വളങ്ങളും ജൈവവളങ്ങളും ചേർക്കുക.",
            cal_desc_fert_veg1: "വളർച്ചാ ഘട്ടം: നൈട്രജനും ലഘു പോഷക മൂലകങ്ങളും ചേർക്കുക.",
            cal_desc_fert_veg2: "കായ്ക്കുന്ന ഘട്ടം: ബാക്കി നൈട്രജൻ, പൊട്ടാസ്യം വളങ്ങൾ ചേർക്കുക.",
            cal_desc_harvest_veg: "പഴുത്ത കായ്കൾ പതിവായി വിളവെടുക്കുക.",
            cal_desc_basal_field: "നിലമൊരുക്കി അടിസ്ഥാന വളങ്ങളും കമ്പോസ്റ്റും ചേർക്കുക.",
            cal_desc_fert_field1: "പൊട്ടിമുളയ്ക്കുന്ന ഘട്ടം: യൂറിയയും സിങ്ക് സൾഫേറ്റും ചേർക്കുക.",
            cal_desc_fert_field2: "കതിര് വരുന്ന ഘട്ടം: അവസാന ഘട്ട വളപ്രയോഗം നടത്തുക.",
            cal_desc_harvest_field: "നെൽക്കതിരുകൾ സ്വർണ്ണനിറമാകുമ്പോൾ വിളവെടുക്കുക."
        }
    };

    // Merge new translations
    Object.keys(newTranslations).forEach(lang => {
        if (TRANSLATIONS[lang]) {
            Object.assign(TRANSLATIONS[lang], newTranslations[lang]);
        }
    });

    // ----------------------------------------------------
    // Ask AgriBot Launcher helper
    // ----------------------------------------------------
    window.askAgriBot = function(questionText) {
        const chatWindow = document.getElementById('chat-window');
        const chatInput = document.getElementById('chat-input');
        const chatSend = document.getElementById('chat-send');
        const chatMessages = document.getElementById('chat-messages');
        
        if (chatWindow && chatInput && chatSend) {
            chatWindow.style.display = 'flex';
            chatInput.value = questionText;
            if (chatMessages) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            setTimeout(() => {
                chatSend.click();
            }, 300);
        }
    };

    // Library page FAQ bot-link click events
    document.querySelectorAll('.ask-bot-faq-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const activeLang = localStorage.getItem('agri_lang') || 'en';
            const parent = btn.closest('.faq-accordion');
            const qTextEl = parent.querySelector(`.faq-q-text[data-lang="${activeLang}"]`);
            if (qTextEl) {
                const qText = qTextEl.textContent.replace('❓ ', '').trim();
                window.askAgriBot(qText);
            }
        });
    });

    // ----------------------------------------------------
    // Interactive Farming Calendar Logic
    // ----------------------------------------------------
    const CALENDAR_OFFSETS = {
        coconut: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_palm", badge: "🌱 Planting" },
            { offset: 30, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_palm1", badge: "🧪 Fertilizer" },
            { offset: 180, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_palm2", badge: "🧪 Fertilizer" },
            { offset: 365, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_palm", badge: "🧺 Harvest" }
        ],
        arecanut: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_palm", badge: "🌱 Planting" },
            { offset: 30, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_palm1", badge: "🧪 Fertilizer" },
            { offset: 180, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_palm2", badge: "🧪 Fertilizer" },
            { offset: 365, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_palm", badge: "🧺 Harvest" }
        ],
        banana: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_veg", badge: "🌱 Planting" },
            { offset: 30, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_veg1", badge: "🧪 Fertilizer" },
            { offset: 90, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_veg2", badge: "🧪 Fertilizer" },
            { offset: 300, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_veg", badge: "🧺 Harvest" }
        ],
        mango: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_palm", badge: "🌱 Planting" },
            { offset: 45, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_palm1", badge: "🧪 Fertilizer" },
            { offset: 120, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_palm2", badge: "🧪 Fertilizer" },
            { offset: 365, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_palm", badge: "🧺 Harvest" }
        ],
        papaya: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_veg", badge: "🌱 Planting" },
            { offset: 60, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_veg1", badge: "🧪 Fertilizer" },
            { offset: 180, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_veg2", badge: "🧪 Fertilizer" },
            { offset: 270, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_veg", badge: "🧺 Harvest" }
        ],
        tomato: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_veg", badge: "🌱 Planting" },
            { offset: 30, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_veg1", badge: "🧪 Fertilizer" },
            { offset: 60, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_veg2", badge: "🧪 Fertilizer" },
            { offset: 95, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_veg", badge: "🧺 Harvest" }
        ],
        brinjal: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_veg", badge: "🌱 Planting" },
            { offset: 30, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_veg1", badge: "🧪 Fertilizer" },
            { offset: 60, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_veg2", badge: "🧪 Fertilizer" },
            { offset: 110, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_veg", badge: "🧺 Harvest" }
        ],
        chilli: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_veg", badge: "🌱 Planting" },
            { offset: 30, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_veg1", badge: "🧪 Fertilizer" },
            { offset: 60, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_veg2", badge: "🧪 Fertilizer" },
            { offset: 110, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_veg", badge: "🧺 Harvest" }
        ],
        pepper: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_palm", badge: "🌱 Planting" },
            { offset: 30, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_palm1", badge: "🧪 Fertilizer" },
            { offset: 120, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_palm2", badge: "🧪 Fertilizer" },
            { offset: 240, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_palm", badge: "🧺 Harvest" }
        ],
        cocoa: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_palm", badge: "🌱 Planting" },
            { offset: 45, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_palm1", badge: "🧪 Fertilizer" },
            { offset: 120, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_palm2", badge: "🧪 Fertilizer" },
            { offset: 365, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_palm", badge: "🧺 Harvest" }
        ],
        paddy: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_field", badge: "🌱 Planting" },
            { offset: 30, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_field1", badge: "🧪 Fertilizer" },
            { offset: 60, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_field2", badge: "🧪 Fertilizer" },
            { offset: 135, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_field", badge: "🧺 Harvest" }
        ],
        rubber: [
            { offset: 0, key: "cal_stage_planting", tr_desc: "cal_desc_basal_palm", badge: "🌱 Planting" },
            { offset: 30, key: "cal_stage_fert1", tr_desc: "cal_desc_fert_palm1", badge: "🧪 Fertilizer" },
            { offset: 120, key: "cal_stage_fert2", tr_desc: "cal_desc_fert_palm2", badge: "🧪 Fertilizer" },
            { offset: 365, key: "cal_stage_harvest", tr_desc: "cal_desc_harvest_palm", badge: "🧺 Harvest" }
        ]
    };

    const calendarForm = document.getElementById('calendar-generator-form');
    const calendarResults = document.getElementById('calendar-results-section');
    
    function addDays(dateStr, days) {
        const d = new Date(dateStr);
        d.setDate(d.getDate() + days);
        return d.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
    }

    function renderCalendar() {
        if (!calendarResults) return;
        
        const crop = localStorage.getItem('agri_calendar_crop');
        const sowDate = localStorage.getItem('agri_calendar_sow_date');
        const activeLang = localStorage.getItem('agri_lang') || 'en';
        
        if (!crop || !sowDate) {
            calendarResults.style.display = 'none';
            return;
        }

        // Set title and starting date
        const cropNameKey = `crop_${crop}`;
        const cropName = (TRANSLATIONS[activeLang] && TRANSLATIONS[activeLang][cropNameKey]) 
            ? TRANSLATIONS[activeLang][cropNameKey] 
            : crop;
        
        document.getElementById('cal-crop-title').textContent = `${cropName} Schedule`;
        document.getElementById('cal-start-date-text').textContent = new Date(sowDate).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });

        // Retrieve completed tasks array
        let completedTasks = [];
        try {
            completedTasks = JSON.parse(localStorage.getItem('agri_calendar_tasks')) || [];
        } catch (e) {
            completedTasks = [];
        }

        const container = document.getElementById('calendar-timeline-container');
        if (!container) return;
        
        container.innerHTML = '';
        const events = CALENDAR_OFFSETS[crop] || [];
        
        events.forEach((ev, idx) => {
            const eventDate = addDays(sowDate, ev.offset);
            const isCompleted = completedTasks[idx] || false;
            
            // Translate label and description
            const evLabel = (TRANSLATIONS[activeLang] && TRANSLATIONS[activeLang][ev.key]) 
                ? TRANSLATIONS[activeLang][ev.key] 
                : ev.key;
            const evDesc = (TRANSLATIONS[activeLang] && TRANSLATIONS[activeLang][ev.tr_desc]) 
                ? TRANSLATIONS[activeLang][ev.tr_desc] 
                : ev.tr_desc;

            const timelineNode = document.createElement('div');
            timelineNode.className = 'timeline-node';
            timelineNode.style.display = 'flex';
            timelineNode.style.gap = '1.5rem';
            timelineNode.style.position = 'relative';
            timelineNode.style.alignItems = 'flex-start';
            timelineNode.style.padding = '0.5rem 0';
            
            timelineNode.innerHTML = `
                <!-- Checkbox -->
                <div style="display: flex; align-items: center; justify-content: center; height: 24px; width: 24px;">
                    <input type="checkbox" class="cal-task-check" data-idx="${idx}" ${isCompleted ? 'checked' : ''} style="width: 20px; height: 20px; cursor: pointer; accent-color: var(--primary-light);">
                </div>
                
                <!-- Dot overlay marker on line -->
                <div style="position: absolute; left: -2.35rem; top: 0.6rem; width: 10px; height: 10px; border-radius: 50%; background: ${isCompleted ? 'var(--primary-light)' : 'var(--border-color)'}; border: 2px solid var(--body-bg); z-index: 2;"></div>

                <!-- Event Details Card -->
                <div class="glass-panel" style="flex: 1; padding: 1.25rem; margin: 0; border-radius: 12px; transition: all 0.25s; opacity: ${isCompleted ? '0.6' : '1'}; border-left: 4px solid ${isCompleted ? 'var(--border-color)' : 'var(--primary-light)'};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem;">
                        <span class="severity-badge" style="background: rgba(25, 135, 84, 0.1); color: var(--primary-light); font-size: 0.75rem; padding: 0.25rem 0.75rem;">
                            ${ev.badge}
                        </span>
                        <strong style="font-size: 0.85rem; opacity: 0.8;">${eventDate}</strong>
                    </div>
                    <h3 style="font-size: 1.1rem; margin-bottom: 0.25rem; text-decoration: ${isCompleted ? 'line-through' : 'none'};">${evLabel}</h3>
                    <p style="font-size: 0.85rem; opacity: 0.8; line-height: 1.5;">${evDesc}</p>
                </div>
            `;
            
            // Add Checkbox change event listener
            const checkbox = timelineNode.querySelector('.cal-task-check');
            checkbox.addEventListener('change', (e) => {
                completedTasks[idx] = e.target.checked;
                localStorage.setItem('agri_calendar_tasks', JSON.stringify(completedTasks));
                renderCalendar(); // re-render to apply dimming effects and status colors
            });
            
            container.appendChild(timelineNode);
        });

        calendarResults.style.display = 'block';
    }

    if (calendarForm) {
        calendarForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const cropVal = document.getElementById('cal-crop').value;
            const dateVal = document.getElementById('cal-sowing-date').value;
            
            localStorage.setItem('agri_calendar_crop', cropVal);
            localStorage.setItem('agri_calendar_sow_date', dateVal);
            localStorage.setItem('agri_calendar_tasks', JSON.stringify([false, false, false, false]));
            
            renderCalendar();
            calendarResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });
        
        // Populate inputs from localStorage if existing
        const storedCrop = localStorage.getItem('agri_calendar_crop');
        const storedDate = localStorage.getItem('agri_calendar_sow_date');
        if (storedCrop) document.getElementById('cal-crop').value = storedCrop;
        if (storedDate) document.getElementById('cal-sowing-date').value = storedDate;
    }

    const clearCalendarBtn = document.getElementById('clear-calendar-btn');
    if (clearCalendarBtn) {
        clearCalendarBtn.addEventListener('click', () => {
            localStorage.removeItem('agri_calendar_crop');
            localStorage.removeItem('agri_calendar_sow_date');
            localStorage.removeItem('agri_calendar_tasks');
            if (calendarForm) {
                calendarForm.reset();
            }
            renderCalendar();
        });
    }

    // Render calendar initially on calendar page load
    renderCalendar();

    if (langSelector) {
        langSelector.addEventListener('change', () => {
            const selectedLang = langSelector.value;
            localStorage.setItem('agri_lang', selectedLang);
            translatePage(selectedLang);
            renderCalendar(); // Refresh calendar labels on language change
        });

        // Initialize from localStorage
        const storedLang = localStorage.getItem('agri_lang') || 'en';
        langSelector.value = storedLang;
        translatePage(storedLang);
        renderCalendar();
    }
});
