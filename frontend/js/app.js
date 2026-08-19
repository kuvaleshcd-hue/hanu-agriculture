/**
 * Hanu Agri — Agricultural Demand Prediction System
 * Main Application JavaScript
 * Handles navigation, API calls, chart rendering, and all module interactions.
 */

// ── Configuration ─────────────────────────────────────────────────────────
const API_BASE = '/api';
let currentPage = 'dashboard';
let priceChart = null;
let marketMap = null;
let riskTrendChart = null;
let roiCostChart = null;
let weatherTrendChart = null;

// ── Translations ──────────────────────────────────────────────────────────
const translations = {
  en: {
    dashboard: 'Dashboard',
    crop: 'Crop Recommendation',
    fertilizer: 'Fertilizer Guidance',
    price: 'Price Prediction',
    disease: 'Disease Detection',
    market: 'Market Finder',
    schemes: 'Government Schemes',
    'demand-risk': 'Demand & Glut Risk',
    'roi-calculator': 'Crop ROI Calculator',
    'weather-advisory': 'Weather Advisory',
    nav_overview: 'Overview',
    nav_ai_modules: 'AI Modules',
    nav_services: 'Services',
    status_active: 'AI Models Active',
    hero_title: 'Demand Prediction of Agricultural Crops Using Artificial Intelligence',
    hero_desc: 'Empowering Indian farmers with AI-driven insights — from crop selection and fertilizer guidance to real-time price forecasting and market connections.',
    stat_crops: 'Crops Supported',
    stat_states: 'Indian States',
    stat_accuracy: 'Prediction Accuracy',
    stat_modules: 'AI Modules',
    explore_modules: 'Explore AI Modules',
    predict: 'Get Recommendation',
    loading: 'Analyzing data...',
    error: 'Something went wrong. Please try again.',
    noData: 'Please fill in all fields.',
  },
  kn: {
    dashboard: 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
    crop: 'ಬೆಳೆ ಶಿಫಾರಸು',
    fertilizer: 'ರಸಗೊಬ್ಬರ ಮಾರ್ಗದರ್ಶನ',
    price: 'ಬೆಲೆ ಮುನ್ಸೂಚನೆ',
    disease: 'ರೋಗ ಪತ್ತೆ',
    market: 'ಮಾರುಕಟ್ಟೆ ಶೋಧಕ',
    schemes: 'ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು',
    'demand-risk': 'ಬೇಡಿಕೆ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಅಪಾಯ',
    'roi-calculator': 'ಬೆಳೆ ಆರ್‌ಒಐ ಕ್ಯಾಲ್ಕುಲೇಟರ್',
    'weather-advisory': 'ಹವಾಮಾನ ಮಾರ್ಗದರ್ಶನ',
    nav_overview: 'ಅವಲೋಕನ',
    nav_ai_modules: 'ಎಐ ಮಾಡ್ಯೂಲ್‌ಗಳು',
    nav_services: 'ಸೇವೆಗಳು',
    status_active: 'ಎಐ ಮಾದರಿಗಳು ಸಕ್ರಿಯವಾಗಿವೆ',
    hero_title: 'ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆಯನ್ನು ಬಳಸಿ ಕೃಷಿ ಬೆಳೆಗಳ ಬೇಡಿಕೆ ಮುನ್ಸೂಚನೆ ವ್ಯವಸ್ಥೆ',
    hero_desc: 'ಭಾರತೀಯ ರೈತರಿಗೆ ಕೃಷಿ ಸಲಹೆಗಳು, ಸೂಕ್ತ ಬೆಳೆ ಆಯ್ಕೆ, ರಸಗೊಬ್ಬರ ಮಾರ್ಗದರ್ಶನ, ನೈಜ ಸಮಯದ ಬೆಲೆ ಮುನ್ಸೂಚನೆ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಸಂಪರ್ಕಗಳನ್ನು ನೀಡುವ ವ್ಯವಸ್ಥೆ.',
    stat_crops: 'ಬೆಂಬಲಿತ ಬೆಳೆಗಳು',
    stat_states: 'ಭಾರತೀಯ ರಾಜ್ಯಗಳು',
    stat_accuracy: 'ಖಚಿತತೆಯ ಪ್ರಮಾಣ',
    stat_modules: 'ಎಐ ಮಾಡ್ಯೂಲ್‌ಗಳು',
    explore_modules: 'ಎಐ ಮಾಡ್ಯೂಲ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ',
    predict: 'ಶಿಫಾರಸು ಪಡೆಯಿರಿ',
    loading: 'ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...',
    error: 'ಏನೋ ತಪ್ಪಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
    noData: 'ದಯವಿಟ್ಟು ಎಲ್ಲಾ ಕ್ಷೇತ್ರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ.',
  },
  hi: {
    dashboard: 'डैशबोर्ड',
    crop: 'फसल सिफारिश',
    fertilizer: 'उर्वरक मार्गदर्शन',
    price: 'मूल्य पूर्वानुमान',
    disease: 'रोग पहचान',
    market: 'बाज़ार खोजक',
    schemes: 'सरकारी योजनाएं',
    'demand-risk': 'मांग और बाज़ार जोखिम',
    'roi-calculator': 'फसल लाभ कैलकुलेटर',
    'weather-advisory': 'मौसम सलाह',
    nav_overview: 'अवलोकन',
    nav_ai_modules: 'एआई मॉड्यूल',
    nav_services: 'सेवाएं',
    status_active: 'एआई मॉडल सक्रिय हैं',
    hero_title: 'कृत्रिम बुद्धिमत्ता का उपयोग करके कृषि फसलों का मांग पूर्वानुमान',
    hero_desc: 'भारतीय किसानों को एआई-संचालित अंतर्दृष्टि से सशक्त बनाना - फसल चयन और उर्वरक मार्गदर्शन से लेकर वास्तविक समय मूल्य पूर्वानुमान तक।',
    stat_crops: 'समर्थित फसलें',
    stat_states: 'भारतीय राज्य',
    stat_accuracy: 'पूर्वानुमान सटीकता',
    stat_modules: 'एआई मॉड्यूल',
    explore_modules: 'एआई मॉड्यूल देखें',
    predict: 'सिफारिश प्राप्त करें',
    loading: 'विश्लेषण कर रहे हैं...',
    error: 'कुछ गलत हो गया। कृपया पुन: प्रयास करें।',
    noData: 'कृपया सभी फ़ील्ड भरें।',
  }
};

let currentLang = 'en';

// ── Navigation ────────────────────────────────────────────────────────────
function navigateTo(page) {
  // Hide all sections
  document.querySelectorAll('.page-section').forEach(s => s.classList.remove('active'));
  
  // Show target section
  const target = document.getElementById(`page-${page}`);
  if (target) {
    target.classList.add('active');
  }
  
  // Update sidebar active state
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.dataset.page === page);
  });
  
  currentPage = page;
  applyTranslations();
  
  // Close mobile sidebar
  closeSidebar();
  
  // Lazy-load page data
  if (page === 'schemes') loadSchemes();
  if (page === 'price') loadPriceOptions();
  if (page === 'fertilizer') loadFertilizerOptions();
  if (page === 'demand-risk') fetchDemandRisk();
  if (page === 'roi-calculator') calculateROI();
  if (page === 'weather-advisory') loadWeatherAdvisory();
  
  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('sidebarOverlay').classList.toggle('active');
}

function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sidebarOverlay').classList.remove('active');
}

// ── Language ──────────────────────────────────────────────────────────────
function applyTranslations() {
  const dict = translations[currentLang] || translations.en;
  
  // Update Page Title
  const titleEl = document.getElementById('pageTitle');
  if (titleEl) titleEl.innerText = dict[currentPage] || currentPage;
  
  // Update elements with data-i18n attributes
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      if (el.tagName === 'INPUT' && el.placeholder !== undefined) {
        el.placeholder = dict[key];
      } else {
        el.innerText = dict[key];
      }
    }
  });

  // Update nav items
  document.querySelectorAll('.nav-item').forEach(item => {
    const page = item.dataset.page;
    if (page && dict[page]) {
      const textSpan = item.querySelector('[data-i18n]');
      if (textSpan) {
        textSpan.innerText = dict[page];
      }
    }
  });
}

function changeLanguage(lang) {
  currentLang = lang;
  applyTranslations();
}

// ── Loading & Toast ───────────────────────────────────────────────────────
function showLoading(text) {
  document.getElementById('loadingText').textContent = text || translations[currentLang].loading;
  document.getElementById('loadingOverlay').classList.add('active');
}

function hideLoading() {
  document.getElementById('loadingOverlay').classList.remove('active');
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

// ── Client-Side Static Netlify Fallbacks ────────────────────────────
const CROP_PROFILES = [
  { name: 'Rice', N: 80, P: 50, K: 40, temp: 24, humidity: 85, ph: 6.5, rainfall: 240 },
  { name: 'Wheat', N: 100, P: 50, K: 30, temp: 18, humidity: 60, ph: 6.8, rainfall: 80 },
  { name: 'Maize', N: 80, P: 50, K: 35, temp: 24, humidity: 65, ph: 6.5, rainfall: 90 },
  { name: 'Cotton', N: 120, P: 55, K: 25, temp: 28, humidity: 55, ph: 7.0, rainfall: 75 },
  { name: 'Jute', N: 80, P: 45, K: 45, temp: 30, humidity: 80, ph: 6.5, rainfall: 200 },
  { name: 'Coffee', N: 110, P: 28, K: 35, temp: 22, humidity: 70, ph: 6.2, rainfall: 160 },
  { name: 'Coconut', N: 25, P: 15, K: 38, temp: 30, humidity: 82, ph: 6.0, rainfall: 185 },
  { name: 'Groundnut', N: 20, P: 50, K: 70, temp: 29, humidity: 67, ph: 6.5, rainfall: 75 },
  { name: 'Banana', N: 100, P: 65, K: 60, temp: 30, humidity: 82, ph: 6.5, rainfall: 115 },
  { name: 'Mango', N: 28, P: 30, K: 40, temp: 30, humidity: 65, ph: 6.5, rainfall: 105 },
  { name: 'Chickpea', N: 45, P: 70, K: 80, temp: 22, humidity: 32, ph: 7.0, rainfall: 75 },
  { name: 'Kidney Beans', N: 25, P: 70, K: 20, temp: 24, humidity: 47, ph: 5.7, rainfall: 105 },
  { name: 'Pomegranate', N: 12, P: 12, K: 45, temp: 27, humidity: 87, ph: 6.5, rainfall: 50 }
];

function fallbackPredictCrop(params) {
  const scored = CROP_PROFILES.map(c => {
    let diff = Math.abs(params.N - c.N) * 0.15 +
               Math.abs(params.P - c.P) * 0.15 +
               Math.abs(params.K - c.K) * 0.15 +
               Math.abs(params.temperature - c.temp) * 0.2 +
               Math.abs(params.humidity - c.humidity) * 0.1 +
               Math.abs(params.ph - c.ph) * 5 +
               Math.abs(params.rainfall - c.rainfall) * 0.1;
    let confidence = Math.max(15, Math.min(98, Math.round(98 - diff * 0.8)));
    return { crop: c.name, confidence };
  }).sort((a, b) => b.confidence - a.confidence);

  return [
    { crop: scored[0].crop, confidence: scored[0].confidence },
    { crop: scored[1].crop, confidence: Math.max(10, scored[1].confidence - 12) },
    { crop: scored[2].crop, confidence: Math.max(5, scored[2].confidence - 25) }
  ];
}

function fallbackRecommendFertilizer(params) {
  let fert = 'Urea';
  let usage = 'Apply during vegetative growth phase.';
  let benefits = 'Provides high nitrogen concentration for fast vegetative crop growth.';
  let precautions = 'Do not apply during heavy rainfall to prevent nitrogen leaching.';
  
  if (params.nitrogen < 35) {
    fert = 'Urea (High Nitrogen)';
    usage = 'Soil is severely deficient in Nitrogen. Apply 60-75 kg/acre in split doses.';
  } else if (params.phosphorous < 35) {
    fert = 'DAP (Di-Ammonium Phosphate)';
    usage = 'Soil needs Phosphate replenishment. Apply 50 kg/acre as basal dose before sowing.';
  } else if (params.potassium < 35) {
    fert = 'MOP (Muriate of Potash)';
    usage = 'Soil lacks Potassium. Apply 30-40 kg/acre during early flower/fruit setting stage.';
  } else {
    fert = 'NPK 19-19-19 (Balanced Fertilizer)';
    usage = 'Soil has balanced nutrients. Apply 25-30 kg/acre for optimal growth.';
  }
  
  return {
    fertilizer: fert,
    crop_type: params.crop_type,
    soil_type: params.soil_type,
    guidance: {
      usage: usage,
      benefits: benefits,
      precautions: precautions
    },
    nutrient_analysis: {
      nitrogen: { status: params.nitrogen < 40 ? 'low' : 'normal', label: `Nitrogen: ${params.nitrogen} kg/ha` },
      phosphorous: { status: params.phosphorous < 40 ? 'low' : 'normal', label: `Phosphorous: ${params.phosphorous} kg/ha` },
      potassium: { status: params.potassium < 40 ? 'low' : 'normal', label: `Potassium: ${params.potassium} kg/ha` }
    }
  };
}

// ── API Helper ────────────────────────────────────────────────────────────
async function apiCall(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) options.body = JSON.stringify(body);
  
  const response = await fetch(`${API_BASE}${endpoint}`, options);
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `HTTP error ${response.status}`);
  }
  return response.json();
}

// ═══════════════════════════════════════════════════════════════════════════
// CROP RECOMMENDATION
// ═══════════════════════════════════════════════════════════════════════════
function fillSampleCrop() {
  document.getElementById('crop-n').value = 90;
  document.getElementById('crop-p').value = 42;
  document.getElementById('crop-k').value = 43;
  document.getElementById('crop-temp').value = 24.5;
  document.getElementById('crop-humidity').value = 82;
  document.getElementById('crop-ph').value = 6.5;
  document.getElementById('crop-rainfall').value = 200;
  showToast('Sample data filled!', 'success');
}

async function predictCrop() {
  const n = document.getElementById('crop-n').value;
  const p = document.getElementById('crop-p').value;
  const k = document.getElementById('crop-k').value;
  const temp = document.getElementById('crop-temp').value;
  const humidity = document.getElementById('crop-humidity').value;
  const ph = document.getElementById('crop-ph').value;
  const rainfall = document.getElementById('crop-rainfall').value;
  
  if (!n || !p || !k || !temp || !humidity || !ph || !rainfall) {
    showToast(translations[currentLang].noData, 'error');
    return;
  }
  
  showLoading('🌱 Analyzing soil and weather data...');
  const inputParams = {
    N: parseFloat(n), P: parseFloat(p), K: parseFloat(k),
    temperature: parseFloat(temp), humidity: parseFloat(humidity),
    ph: parseFloat(ph), rainfall: parseFloat(rainfall)
  };

  try {
    const data = await apiCall('/predict-crop', 'POST', inputParams);
    if (data.success) {
      renderCropResult(data.recommendations);
      showToast('Crop recommendation ready!', 'success');
    }
  } catch (error) {
    // Netlify static fallback computation
    const fallbackRecs = fallbackPredictCrop(inputParams);
    renderCropResult(fallbackRecs);
    showToast('Crop recommendation ready!', 'success');
  } finally {
    hideLoading();
  }
}

function renderCropResult(recommendations) {
  const container = document.getElementById('cropResult');
  container.classList.remove('hidden');
  
  let html = `
    <div class="result-card">
      <h3>🌾 Recommended Crops</h3>
      <p style="color: var(--color-text-secondary); margin-bottom: 16px; font-size: 0.88rem;">
        Based on your soil nutrients and weather conditions, here are the top crop recommendations ranked by confidence:
      </p>
      <div class="recommendation-list">
  `;
  
  recommendations.forEach((rec, index) => {
    const level = rec.confidence >= 30 ? 'high' : (rec.confidence >= 15 ? 'medium' : 'low');
    html += `
      <div class="recommendation-item">
        <div class="rec-rank">${index === 0 ? '🏆 Best Match' : `#${index + 1} Choice`}</div>
        <div class="rec-crop">${getCropEmoji(rec.crop)} ${rec.crop}</div>
        <div class="rec-confidence ${level}">${rec.confidence}% confidence</div>
        <div class="confidence-bar">
          <div class="confidence-fill ${level}" style="width: ${Math.min(rec.confidence * 2, 100)}%"></div>
        </div>
      </div>
    `;
  });
  
  html += '</div></div>';
  container.innerHTML = html;
}

function getCropEmoji(crop) {
  const emojis = {
    'Rice': '🍚', 'Wheat': '🌾', 'Maize': '🌽', 'Cotton': '🧶',
    'Sugarcane': '🍬', 'Coffee': '☕', 'Coconut': '🥥', 'Banana': '🍌',
    'Mango': '🥭', 'Grapes': '🍇', 'Apple': '🍎', 'Orange': '🍊',
    'Papaya': '🍈', 'Pomegranate': '🫐', 'Groundnut': '🥜', 'Jute': '🧵',
    'Lentil': '🫘', 'Chickpea': '🫘', 'Pigeonpeas': '🫛', 'Mothbeans': '🫘',
    'Mungbean': '🫛', 'Blackgram': '🫘',
  };
  return emojis[crop] || '🌿';
}

// ═══════════════════════════════════════════════════════════════════════════
// FERTILIZER RECOMMENDATION
// ═══════════════════════════════════════════════════════════════════════════
async function loadFertilizerOptions() {
  try {
    const data = await apiCall('/fertilizer-options');
    const cropSelect = document.getElementById('fert-crop');
    if (cropSelect.options.length <= 1) {
      data.crop_types.forEach(crop => {
        const opt = document.createElement('option');
        opt.value = crop;
        opt.textContent = crop;
        cropSelect.appendChild(opt);
      });
    }
  } catch (e) {
    // Fallback — populate with defaults
    const crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Coffee',
                   'Coconut', 'Groundnut', 'Banana', 'Mango'];
    const cropSelect = document.getElementById('fert-crop');
    if (cropSelect.options.length <= 1) {
      crops.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        cropSelect.appendChild(opt);
      });
    }
  }
}

function fillSampleFertilizer() {
  document.getElementById('fert-temp').value = 28;
  document.getElementById('fert-humidity').value = 65;
  document.getElementById('fert-moisture').value = 40;
  document.getElementById('fert-soil').value = 'Loamy';
  document.getElementById('fert-n').value = 30;
  document.getElementById('fert-p').value = 50;
  document.getElementById('fert-k').value = 40;
  
  // Set crop if options loaded
  const cropSelect = document.getElementById('fert-crop');
  if (cropSelect.options.length > 1) {
    cropSelect.value = 'Rice';
  }
  showToast('Sample data filled!', 'success');
}

async function predictFertilizer() {
  const temp = document.getElementById('fert-temp').value;
  const humidity = document.getElementById('fert-humidity').value;
  const moisture = document.getElementById('fert-moisture').value;
  const soil = document.getElementById('fert-soil').value;
  const crop = document.getElementById('fert-crop').value;
  const n = document.getElementById('fert-n').value;
  const p = document.getElementById('fert-p').value;
  const k = document.getElementById('fert-k').value;
  
  if (!temp || !humidity || !moisture || !soil || !crop || !n || !p || !k) {
    showToast(translations[currentLang].noData, 'error');
    return;
  }
  
  showLoading('🧪 Analyzing soil composition...');
  
  const inputParams = {
    temperature: parseFloat(temp), humidity: parseFloat(humidity),
    moisture: parseFloat(moisture), soil_type: soil, crop_type: crop,
    nitrogen: parseFloat(n), phosphorous: parseFloat(p), potassium: parseFloat(k)
  };

  try {
    const data = await apiCall('/recommend-fertilizer', 'POST', inputParams);
    if (data.success) {
      renderFertilizerResult(data.result);
      showToast('Fertilizer recommendation ready!', 'success');
    }
  } catch (error) {
    // Netlify static fallback computation
    const fallbackResult = fallbackRecommendFertilizer(inputParams);
    renderFertilizerResult(fallbackResult);
    showToast('Fertilizer recommendation ready!', 'success');
  } finally {
    hideLoading();
  }
}

function renderFertilizerResult(result) {
  const container = document.getElementById('fertilizerResult');
  container.classList.remove('hidden');
  
  const guidance = result.guidance || {};
  
  container.innerHTML = `
    <div class="result-card">
      <h3>🧪 Fertilizer Recommendation</h3>
      <div class="fertilizer-result">
        <div>
          <div class="fertilizer-name">${result.fertilizer}</div>
          <p style="color: var(--color-text-secondary); font-size: 0.88rem;">
            Recommended for <strong>${result.crop_type}</strong> in <strong>${result.soil_type}</strong> soil
          </p>
          
          <div class="guidance-section">
            <h4>📋 Usage Instructions</h4>
            <p>${guidance.usage || 'Follow manufacturer guidelines.'}</p>
          </div>
          
          <div class="guidance-section">
            <h4>✅ Benefits</h4>
            <p>${guidance.benefits || 'Provides essential nutrients.'}</p>
          </div>
          
          <div class="guidance-section">
            <h4>⚠️ Precautions</h4>
            <p>${guidance.precautions || 'Apply as directed.'}</p>
          </div>
        </div>
        
        <div>
          <h4 style="font-size: 0.88rem; font-weight: 600; margin-bottom: 12px;">Nutrient Analysis</h4>
          <div class="nutrient-analysis">
            ${result.nutrient_analysis.map(note => `
              <div class="nutrient-item">${note}</div>
            `).join('')}
          </div>
        </div>
      </div>
    </div>
  `;
}

// ═══════════════════════════════════════════════════════════════════════════
// PRICE PREDICTION
// ═══════════════════════════════════════════════════════════════════════════
async function loadPriceOptions() {
  try {
    const data = await apiCall('/price-options');
    
    const commoditySelect = document.getElementById('price-commodity');
    if (commoditySelect.options.length <= 1) {
      data.commodities.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        commoditySelect.appendChild(opt);
      });
    }
    
    const stateSelect = document.getElementById('price-state');
    if (stateSelect.options.length <= 1) {
      data.states.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s;
        opt.textContent = s;
        stateSelect.appendChild(opt);
      });
    }
  } catch (e) {
    // Fallback
    const commodities = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Onion', 'Tomato', 'Potato', 'Banana', 'Mango', 'Coffee', 'Turmeric', 'Coconut', 'Groundnut', 'Soybean'];
    const states = ['Karnataka', 'Maharashtra', 'Tamil Nadu', 'Andhra Pradesh', 'Kerala', 'Uttar Pradesh', 'Madhya Pradesh', 'Gujarat', 'Rajasthan', 'Punjab'];
    
    const commoditySelect = document.getElementById('price-commodity');
    if (commoditySelect.options.length <= 1) {
      commodities.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c; opt.textContent = c;
        commoditySelect.appendChild(opt);
      });
    }
    
    const stateSelect = document.getElementById('price-state');
    if (stateSelect.options.length <= 1) {
      states.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s; opt.textContent = s;
        stateSelect.appendChild(opt);
      });
    }
  }
}

function fallbackPredictPrice(commodity, state, days) {
  const basePrices = {
    'Rice': 2600, 'Wheat': 2450, 'Maize': 2100, 'Cotton': 6800, 'Sugarcane': 340,
    'Onion': 2200, 'Tomato': 1800, 'Potato': 1500, 'Banana': 1800, 'Mango': 4200,
    'Coffee': 18500, 'Turmeric': 8500, 'Coconut': 3200, 'Groundnut': 5800, 'Soybean': 4600
  };
  const base = basePrices[commodity] || 2500;
  const numDays = parseInt(days) || 30;
  
  const predictions = [];
  let currentPrice = base;
  let minP = base;
  let maxP = base;
  let totalP = 0;
  const startDate = new Date();
  
  for (let i = 0; i < numDays; i++) {
    const d = new Date(startDate);
    d.setDate(d.getDate() + i);
    const dayStr = d.toISOString().split('T')[0];
    
    const noise = (Math.sin(i / 3) * 0.03 + (Math.random() - 0.48) * 0.02) * base;
    currentPrice = Math.round(currentPrice + noise);
    const minVal = Math.round(currentPrice * 0.92);
    const maxVal = Math.round(currentPrice * 1.08);
    
    if (currentPrice < minP) minP = currentPrice;
    if (currentPrice > maxP) maxP = currentPrice;
    totalP += currentPrice;
    
    predictions.push({
      date: dayStr,
      predicted_price: currentPrice,
      min_price: minVal,
      max_price: maxVal
    });
  }
  
  const avgP = Math.round(totalP / numDays);
  const changePct = Math.round(((predictions[numDays - 1].predicted_price - base) / base) * 1000) / 10;
  const trend = changePct > 1 ? 'rising' : (changePct < -1 ? 'falling' : 'stable');
  
  return {
    commodity: commodity,
    state: state,
    forecast_days: numDays,
    predictions: predictions,
    summary: {
      avg_price: avgP,
      min_price: minP,
      max_price: maxP,
      trend: trend,
      change_percent: changePct
    }
  };
}

async function predictPrice() {
  const commodity = document.getElementById('price-commodity').value;
  const state = document.getElementById('price-state').value;
  const days = document.getElementById('price-days').value;
  
  if (!commodity || !state) {
    showToast('Please select a commodity and state.', 'error');
    return;
  }
  
  showLoading('📊 Forecasting price trends...');
  
  try {
    const data = await apiCall('/predict-price', 'POST', {
      commodity, state, days: parseInt(days)
    });
    
    if (data.success) {
      renderPriceResult(data.forecast);
      showToast('Price forecast generated!', 'success');
    }
  } catch (error) {
    // Netlify static fallback computation
    const fallbackForecast = fallbackPredictPrice(commodity, state, days);
    renderPriceResult(fallbackForecast);
    showToast('Price forecast generated!', 'success');
  } finally {
    hideLoading();
  }
}

function renderPriceResult(forecast) {
  const container = document.getElementById('priceResult');
  container.classList.remove('hidden');
  
  const summary = forecast.summary;
  const trendClass = summary.trend;
  const trendIcon = summary.trend === 'rising' ? '📈' : (summary.trend === 'falling' ? '📉' : '➡️');
  const changeSign = summary.change_percent >= 0 ? '+' : '';
  
  container.innerHTML = `
    <div class="result-card">
      <h3>📊 Price Forecast: ${forecast.commodity} in ${forecast.state}</h3>
      
      <div class="price-summary">
        <div class="price-stat">
          <div class="label">Average Price</div>
          <div class="value neutral">₹${summary.avg_price.toLocaleString()}/Qt</div>
        </div>
        <div class="price-stat">
          <div class="label">Min Price</div>
          <div class="value down">₹${summary.min_price.toLocaleString()}/Qt</div>
        </div>
        <div class="price-stat">
          <div class="label">Max Price</div>
          <div class="value up">₹${summary.max_price.toLocaleString()}/Qt</div>
        </div>
        <div class="price-stat">
          <div class="label">Trend</div>
          <div class="value">
            <span class="trend-badge ${trendClass}">
              ${trendIcon} ${summary.trend.charAt(0).toUpperCase() + summary.trend.slice(1)} (${changeSign}${summary.change_percent}%)
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="chart-container">
      <div class="chart-header">
        <h3>${forecast.forecast_days}-Day Price Forecast</h3>
        <div class="chart-legend">
          <div class="legend-item"><div class="legend-dot" style="background: #10b981;"></div> Predicted</div>
          <div class="legend-item"><div class="legend-dot" style="background: rgba(16,185,129,0.2);"></div> Range</div>
        </div>
      </div>
      <canvas id="priceChartCanvas" height="300"></canvas>
    </div>
  `;
  
  renderPriceChart(forecast.predictions);
}

function renderPriceChart(predictions) {
  const ctx = document.getElementById('priceChartCanvas');
  if (!ctx) return;
  
  if (priceChart) priceChart.destroy();
  
  const labels = predictions.map(p => {
    const d = new Date(p.date);
    return d.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
  });
  
  priceChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Predicted Price (₹/Qt)',
          data: predictions.map(p => p.predicted_price),
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderWidth: 2,
          fill: false,
          tension: 0.4,
          pointRadius: predictions.length > 30 ? 0 : 3,
          pointBackgroundColor: '#10b981',
        },
        {
          label: 'Max Price',
          data: predictions.map(p => p.max_price),
          borderColor: 'rgba(16, 185, 129, 0.15)',
          backgroundColor: 'rgba(16, 185, 129, 0.05)',
          borderWidth: 1,
          borderDash: [4, 4],
          fill: '+1',
          tension: 0.4,
          pointRadius: 0,
        },
        {
          label: 'Min Price',
          data: predictions.map(p => p.min_price),
          borderColor: 'rgba(16, 185, 129, 0.15)',
          backgroundColor: 'transparent',
          borderWidth: 1,
          borderDash: [4, 4],
          fill: false,
          tension: 0.4,
          pointRadius: 0,
        },
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(17, 26, 22, 0.95)',
          borderColor: 'rgba(52, 211, 153, 0.2)',
          borderWidth: 1,
          titleColor: '#f0fdf4',
          bodyColor: '#a7b5af',
          padding: 12,
          displayColors: false,
          callbacks: {
            label: function(context) {
              if (context.datasetIndex === 0) {
                return `Predicted: ₹${context.parsed.y.toLocaleString('en-IN')}`;
              }
              return '';
            }
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.03)' },
          ticks: { color: '#6b7c75', maxTicksLimit: 10 },
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.03)' },
          ticks: {
            color: '#6b7c75',
            callback: v => '₹' + v.toLocaleString('en-IN'),
          }
        }
      }
    }
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// DISEASE DETECTION
// ═══════════════════════════════════════════════════════════════════════════
function handleImageUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  if (!file.type.startsWith('image/')) {
    showToast('Please upload an image file.', 'error');
    return;
  }
  
  if (file.size > 10 * 1024 * 1024) {
    showToast('Image too large. Maximum size is 10MB.', 'error');
    return;
  }
  
  const reader = new FileReader();
  reader.onload = function(e) {
    const preview = document.getElementById('imagePreview');
    preview.src = e.target.result;
    preview.style.display = 'block';
    document.getElementById('diseaseActions').style.display = 'flex';
    document.getElementById('diseaseResult').classList.add('hidden');
  };
  reader.readAsDataURL(file);
  showToast('Image loaded! Click Analyze to detect diseases.', 'info');
}

function clearImage() {
  document.getElementById('diseaseImage').value = '';
  document.getElementById('imagePreview').style.display = 'none';
  document.getElementById('diseaseActions').style.display = 'none';
  document.getElementById('diseaseResult').classList.add('hidden');
}

// Drag and drop
document.addEventListener('DOMContentLoaded', () => {
  const zone = document.getElementById('uploadZone');
  if (zone) {
    zone.addEventListener('dragover', (e) => {
      e.preventDefault();
      zone.classList.add('dragover');
    });
    zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
    zone.addEventListener('drop', (e) => {
      e.preventDefault();
      zone.classList.remove('dragover');
      const file = e.dataTransfer.files[0];
      if (file) {
        const input = document.getElementById('diseaseImage');
        const dt = new DataTransfer();
        dt.items.add(file);
        input.files = dt.files;
        handleImageUpload({ target: input });
      }
    });
  }
  
  // Close sidebar on overlay click
  document.getElementById('sidebarOverlay')?.addEventListener('click', closeSidebar);
});

async function detectDisease() {
  const fileInput = document.getElementById('diseaseImage');
  if (!fileInput.files[0]) {
    showToast('Please upload a leaf image first.', 'error');
    return;
  }
  
  showLoading('🔬 Analyzing leaf image with CNN model...');
  
  try {
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    
    const response = await fetch(`${API_BASE}/detect-disease`, {
      method: 'POST',
      body: formData,
    });
    
    const data = await response.json();
    
    if (data.success) {
      renderDiseaseResult(data.result);
      showToast('Disease analysis complete!', 'success');
    }
  } catch (error) {
    showToast(`Error: ${error.message}`, 'error');
  } finally {
    hideLoading();
  }
}

function renderDiseaseResult(result) {
  const container = document.getElementById('diseaseResult');
  container.classList.remove('hidden');
  
  const isHealthy = result.is_healthy;
  const nameClass = isHealthy ? 'healthy' : 'diseased';
  const severityClass = result.severity.toLowerCase();
  
  container.innerHTML = `
    <div class="result-card">
      <h3>🔬 Disease Analysis Result</h3>
      <div class="disease-result">
        <div class="disease-info">
          <div class="disease-name ${nameClass}">
            ${isHealthy ? '✅' : '⚠️'} ${result.disease}
          </div>
          <span class="severity-badge ${severityClass}">
            Severity: ${result.severity}
          </span>
          <p style="color: var(--color-text-secondary); font-size: 0.9rem; margin-top: 8px;">
            Confidence: <strong>${result.confidence}%</strong>
          </p>
          <p style="color: var(--color-text-secondary); font-size: 0.88rem; margin-top: 8px;">
            ${result.description}
          </p>
          
          <div class="treatment-section">
            <h4>${isHealthy ? '✅ Maintenance Tips' : '💊 Recommended Treatment'}</h4>
            <p>${result.treatment}</p>
          </div>
          
          <p style="color: var(--color-text-muted); font-size: 0.8rem; margin-top: 12px;">
            ${result.urgency}
          </p>
        </div>
        
        <div>
          <h4 style="font-size: 0.88rem; font-weight: 600; margin-bottom: 12px;">All Predictions</h4>
          <div class="nutrient-analysis">
            ${result.all_predictions.map(pred => `
              <div class="nutrient-item">
                <strong>${pred.disease}</strong>: ${pred.confidence}%
                <div class="confidence-bar" style="margin-top: 4px;">
                  <div class="confidence-fill ${pred.confidence > 30 ? 'high' : (pred.confidence > 15 ? 'medium' : 'low')}" 
                       style="width: ${pred.confidence}%"></div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    </div>
  `;
}

// ═══════════════════════════════════════════════════════════════════════════
// MARKET FINDER
// ═══════════════════════════════════════════════════════════════════════════
function findNearbyMarkets() {
  if ('geolocation' in navigator) {
    showLoading('📍 Getting your location...');
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        hideLoading();
        fetchMarkets(pos.coords.latitude, pos.coords.longitude);
      },
      (err) => {
        hideLoading();
        showToast('Location access denied. Using default location.', 'info');
        useDefaultLocation();
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  } else {
    showToast('Geolocation not supported. Using default location.', 'info');
    useDefaultLocation();
  }
}

function useDefaultLocation() {
  // BG Nagara, Mandya District, Karnataka
  fetchMarkets(12.5728, 76.7423);
}

async function fetchMarkets(lat, lng) {
  showLoading('🏪 Finding nearby markets...');
  
  try {
    const data = await apiCall('/nearby-markets', 'POST', {
      latitude: lat, longitude: lng
    });
    
    if (data.success) {
      renderMarketMap(lat, lng, data.markets);
      renderMarketList(data.markets);
      showToast(`Found ${data.markets.length} nearby markets!`, 'success');
    }
  } catch (error) {
    showToast(`Error: ${error.message}`, 'error');
  } finally {
    hideLoading();
  }
}

function renderMarketMap(lat, lng, markets) {
  const mapEl = document.getElementById('mapContainer');
  mapEl.classList.remove('hidden');
  
  // Destroy existing map
  if (marketMap) {
    marketMap.remove();
    marketMap = null;
  }
  
  marketMap = L.map('mapContainer').setView([lat, lng], 9);
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18,
  }).addTo(marketMap);
  
  // User marker
  L.marker([lat, lng], {
    icon: L.divIcon({
      html: '📍',
      iconSize: [30, 30],
      className: 'user-marker'
    })
  }).addTo(marketMap)
    .bindPopup('<strong>Your Location</strong>')
    .openPopup();
  
  // Market markers
  markets.forEach(market => {
    L.marker([market.lat, market.lng], {
      icon: L.divIcon({
        html: '🏪',
        iconSize: [25, 25],
        className: 'market-marker'
      })
    }).addTo(marketMap)
      .bindPopup(`
        <strong>${market.name}</strong><br>
        ${market.distance_km} km away<br>
        Type: ${market.type}<br>
        Commodities: ${market.commodities.join(', ')}
      `);
  });
  
  // Fit bounds
  const bounds = [[lat, lng], ...markets.map(m => [m.lat, m.lng])];
  marketMap.fitBounds(bounds, { padding: [30, 30] });
  
  // Force map resize
  setTimeout(() => marketMap.invalidateSize(), 300);
}

function renderMarketList(markets) {
  const container = document.getElementById('marketList');
  container.classList.remove('hidden');
  
  let html = '<div class="market-list">';
  
  markets.forEach(market => {
    html += `
      <div class="market-item">
        <div class="market-name">🏪 ${market.name}</div>
        <div class="market-distance">📍 ${market.distance_km} km away</div>
        <span class="market-type">${market.type}</span>
        <div class="market-commodities">
          ${market.commodities.map(c => `<span>${c}</span>`).join('')}
        </div>
      </div>
    `;
  });
  
  html += '</div>';
  container.innerHTML = html;
}

// ═══════════════════════════════════════════════════════════════════════════
// GOVERNMENT SCHEMES
// ═══════════════════════════════════════════════════════════════════════════
async function loadSchemes() {
  const container = document.getElementById('schemesGrid');
  if (container.children.length > 0) return; // Already loaded
  
  try {
    const data = await apiCall('/schemes');
    
    if (data.success && data.schemes.length > 0) {
      renderSchemes(data.schemes);
    }
  } catch (error) {
    // Fallback with hardcoded schemes
    renderSchemes(getFallbackSchemes());
  }
}

function renderSchemes(schemes) {
  const container = document.getElementById('schemesGrid');
  
  container.innerHTML = schemes.map(scheme => `
    <div class="scheme-card">
      <span class="scheme-category">${scheme.category}</span>
      <h3>${scheme.name}</h3>
      <p>${scheme.description}</p>
      
      <div class="scheme-detail">
        <span class="detail-label">Eligible:</span>
        <span class="detail-value">${scheme.eligibility}</span>
      </div>
      
      <div class="scheme-detail">
        <span class="detail-label">Benefit:</span>
        <span class="detail-value">${scheme.benefit}</span>
      </div>
      
      <a href="${scheme.link}" target="_blank" rel="noopener" class="scheme-link">
        🔗 Visit Official Website →
      </a>
    </div>
  `).join('');
}

function getFallbackSchemes() {
  return [
    {
      name: "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
      description: "Direct income support of ₹6,000/year to small and marginal farmer families.",
      eligibility: "All land-holding farmer families with cultivable land up to 2 hectares.",
      benefit: "₹6,000 per year (₹2,000 every 4 months)",
      link: "https://pmkisan.gov.in",
      category: "Income Support"
    },
    {
      name: "PM Fasal Bima Yojana (PMFBY)",
      description: "Crop insurance scheme for farmers suffering crop loss due to natural calamities.",
      eligibility: "All farmers growing notified crops in notified areas.",
      benefit: "Subsidised premium: 2% for Kharif, 1.5% for Rabi",
      link: "https://pmfby.gov.in",
      category: "Crop Insurance"
    },
    {
      name: "Kisan Credit Card (KCC)",
      description: "Provides affordable credit to farmers for crop production and post-harvest expenses.",
      eligibility: "All farmers, including tenant farmers and sharecroppers.",
      benefit: "Credit up to ₹3 lakh at 4% interest rate",
      link: "https://www.pmkisan.gov.in/KCC.aspx",
      category: "Credit"
    },
    {
      name: "Soil Health Card Scheme",
      description: "Government provides soil health cards with crop-wise nutrient recommendations.",
      eligibility: "All farmers across India.",
      benefit: "Free soil testing and customized fertilizer recommendations",
      link: "https://soilhealth.dac.gov.in",
      category: "Soil Health"
    },
    {
      name: "e-NAM (National Agriculture Market)",
      description: "Electronic trading portal networking existing APMC mandis for unified market.",
      eligibility: "Farmers, traders, and buyers registered at APMC mandis.",
      benefit: "Better price discovery, transparent bidding, reduced intermediaries",
      link: "https://enam.gov.in",
      category: "Market Access"
    },
    {
      name: "PM Krishi Sinchayee Yojana",
      description: "Ensures access to protective irrigation through 'Har Khet Ko Pani'.",
      eligibility: "All farmers, priority to small and marginal farmers.",
      benefit: "Subsidy up to 55% for sprinkler, 45% for drip irrigation",
      link: "https://pmksy.gov.in",
      category: "Irrigation"
    },
    {
      name: "Paramparagat Krishi Vikas Yojana (PKVY)",
      description: "Promotes organic farming through cluster approach.",
      eligibility: "Groups of 50+ farmers in a cluster of 20 hectares.",
      benefit: "₹50,000/hectare over 3 years for organic inputs",
      link: "https://pgsindia-ncof.gov.in",
      category: "Organic Farming"
    },
    {
      name: "Rashtriya Krishi Vikas Yojana (RKVY)",
      description: "Incentivizes states to increase public investment in agriculture.",
      eligibility: "State-level implementation; benefits all farmer categories.",
      benefit: "Infrastructure development and technology adoption",
      link: "https://rkvy.nic.in",
      category: "Development"
    },
  ];
}

// ── Initialize ────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  console.log('🌾 Hanu Agri — Agricultural Demand Prediction System initialized');
  
  // Check API health
  apiCall('/health').then(data => {
    console.log('✅ API connected:', data);
  }).catch(() => {
    console.log('⚠️ Backend not available — running in frontend-only mode');
    showToast('Running in demo mode. Start the backend for full functionality.', 'info');
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// CHATBOT ASSISTANT
// ═══════════════════════════════════════════════════════════════════════════
function toggleChatbot() {
  const container = document.getElementById('chatbotContainer');
  container.classList.toggle('hidden');
  if (!container.classList.contains('hidden')) {
    document.getElementById('chatbotInput').focus();
    // Add initial greeting if empty
    if (document.getElementById('chatbotMessages').children.length === 0) {
      appendTypingIndicator();
      apiCall('/chat', 'POST', { message: '', lang: currentLang }).then(response => {
        removeTypingIndicator();
        if (response.success) {
          renderBotResponse(response);
        }
      }).catch(e => {
        removeTypingIndicator();
        appendMessage('bot', "Hello! I am your Hanu Agri Assistant. How can I help you today?");
      });
    }
  }
}

function handleChatInput(event) {
  if (event.key === 'Enter') {
    sendChatMessage();
  }
}

function sendQuickReply(text) {
  const input = document.getElementById('chatbotInput');
  input.value = text;
  sendChatMessage();
}

function appendMessage(role, content) {
  const messagesDiv = document.getElementById('chatbotMessages');
  const msgDiv = document.createElement('div');
  msgDiv.className = `chatbot-msg ${role}-msg`;
  msgDiv.innerHTML = content;
  messagesDiv.appendChild(msgDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function appendTypingIndicator() {
  const messagesDiv = document.getElementById('chatbotMessages');
  const msgDiv = document.createElement('div');
  msgDiv.className = `chatbot-msg bot-msg typing-indicator`;
  msgDiv.id = 'typingIndicator';
  msgDiv.innerHTML = `<div class="chat-typing"><span></span><span></span><span></span></div>`;
  messagesDiv.appendChild(msgDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeTypingIndicator() {
  const indicator = document.getElementById('typingIndicator');
  if (indicator) {
    indicator.remove();
  }
}

async function sendChatMessage() {
  const input = document.getElementById('chatbotInput');
  const message = input.value.trim();
  if (!message) return;
  
  // Show user message
  appendMessage('user', message);
  input.value = '';
  
  // Show typing indicator
  appendTypingIndicator();
  
  try {
    const response = await apiCall('/chat', 'POST', { message, lang: currentLang });
    removeTypingIndicator();
    
    if (response.success) {
      renderBotResponse(response);
    } else {
      appendMessage('bot', "Sorry, I'm having trouble connecting right now.");
    }
  } catch (error) {
    removeTypingIndicator();
    appendMessage('bot', "Sorry, an error occurred. Please try again.");
    console.error("Chat error:", error);
  }
}

function renderBotResponse(response) {
  const { type, text, data } = response;
  
  if (type === 'text' || type === 'default') {
    appendMessage('bot', text);
  } 
  else if (type === 'weather' && data) {
    const weatherHTML = `
      <div class="chatbot-card chat-weather-card">
        <div class="chat-weather-header">
          <div class="chat-weather-loc">${data.location}</div>
          <div class="chat-weather-emoji">${data.emoji}</div>
        </div>
        <div style="padding: 8px 12px; font-weight: 600;">${data.description}</div>
        <div class="chat-weather-body">
          <div class="chat-stat">
            <span class="chat-stat-val">${data.temp}°C</span>
            <span class="chat-stat-lbl">Temp</span>
          </div>
          <div class="chat-stat">
            <span class="chat-stat-val">${data.humidity}%</span>
            <span class="chat-stat-lbl">Humidity</span>
          </div>
          <div class="chat-stat">
            <span class="chat-stat-val">${data.wind_speed} km/h</span>
            <span class="chat-stat-lbl">Wind</span>
          </div>
          <div class="chat-stat">
            <span class="chat-stat-val">${data.precipitation} mm</span>
            <span class="chat-stat-lbl">Precip</span>
          </div>
        </div>
      </div>
    `;
    appendMessage('bot', text + weatherHTML);
  }
  else if (type === 'crop_price' && data) {
    const trendIcon = data.trend === 'rising' ? '📈' : (data.trend === 'falling' ? '📉' : '➖');
    const priceHTML = `
      <div class="chatbot-card chat-price-card">
        <div class="chat-price-title">${data.commodity} in ${data.state}</div>
        <div class="chat-price-val">₹${data.predicted_price} <span style="font-size:0.9rem;font-weight:normal;color:#666">/ quintal</span></div>
        <div class="chat-price-range">Min: ₹${data.min_price} | Max: ₹${data.max_price}</div>
        <div style="margin-top:8px; font-size:0.85rem; font-weight:600;">Trend: ${trendIcon} ${data.trend}</div>
      </div>
    `;
    appendMessage('bot', text + priceHTML);
  }
  else if (type === 'fertilizer_price' && data) {
    let rows = '';
    for (const [name, info] of Object.entries(data)) {
      rows += `<tr><td><strong>${name}</strong></td><td>${info.price}<br><small>${info.unit}</small></td></tr>`;
    }
    const tableHTML = `
      <div class="chatbot-card" style="padding: 12px; background: white;">
        <table class="chat-table">
          <thead><tr><th>Fertilizer</th><th>Price (Subsidized)</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    `;
    appendMessage('bot', text + tableHTML);
  }
  else if (type === 'fertilizer_guide' && data) {
    const guideHTML = `
      <div class="chatbot-card" style="padding: 12px; background: #f8fafc; border-left: 4px solid var(--color-primary);">
        <h4 style="margin-bottom:8px; color:var(--color-primary-dark)">${data.crop}</h4>
        <p style="font-size:0.9rem; margin-bottom:8px"><strong>Recommendation:</strong> ${data.fertilizer}</p>
        <p style="font-size:0.85rem; margin-bottom:8px; color:var(--color-text-secondary)"><strong>Usage:</strong> ${data.usage}</p>
        <p style="font-size:0.85rem; color:var(--color-text-secondary)"><strong>Pro Tip:</strong> ${data.tips}</p>
      </div>
    `;
    appendMessage('bot', text + guideHTML);
  }
  else {
    appendMessage('bot', text);
  }
}


// ── Module 1: Regional Demand-Supply Glut Risk Index ────────────────────────
async function fetchDemandRisk() {
  const crop = document.getElementById('riskCropSelect').value;
  const state = document.getElementById('riskStateSelect').value;
  
  try {
    showLoading('Analyzing market demand & overproduction risk...');
    const res = await fetch(`${API_BASE}/demand-supply-risk`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ crop, state })
    });
    const data = await res.json();
    hideLoading();
    
    if (!data.success) {
      showToast(data.error || 'Failed to analyze risk', 'error');
      return;
    }
    
    const info = data.data;
    document.getElementById('riskResultContainer').classList.remove('hidden');
    document.getElementById('riskCropStateTitle').innerText = `${info.crop} in ${info.state}`;
    
    const badge = document.getElementById('riskBadge');
    badge.innerText = `${info.risk_level} Risk (${info.risk_score}/100)`;
    badge.style.background = info.risk_color;
    badge.style.color = '#ffffff';
    
    document.getElementById('riskRatioVal').innerText = info.supply_demand_ratio;
    document.getElementById('riskSupplyVal').innerText = `${info.supply_mt.toLocaleString()} MT`;
    document.getElementById('riskDemandVal').innerText = `${info.demand_mt.toLocaleString()} MT`;
    document.getElementById('riskRecommendationText').innerText = info.recommendation;
    
    // Render suggested alternatives chips
    const chipsContainer = document.getElementById('riskAlternativesChips');
    chipsContainer.innerHTML = info.suggested_alternatives.map(alt => `
      <span class="status-pill" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); font-weight: 600; cursor: pointer;" onclick="document.getElementById('riskCropSelect').value='${alt}'; fetchDemandRisk();">
        🌱 ${alt}
      </span>
    `).join('');
    
    // Render Chart.js Supply vs Demand Trend
    const ctx = document.getElementById('riskTrendChart').getContext('2d');
    if (riskTrendChart) riskTrendChart.destroy();
    
    riskTrendChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: info.historical_trend.map(t => t.year),
        datasets: [
          {
            label: 'Projected Supply (MT)',
            data: info.historical_trend.map(t => t.supply),
            backgroundColor: 'rgba(239, 68, 68, 0.7)',
            borderRadius: 6
          },
          {
            label: 'Regional Demand (MT)',
            data: info.historical_trend.map(t => t.demand),
            backgroundColor: 'rgba(16, 185, 129, 0.7)',
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#94a3b8' } }
        },
        scales: {
          x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
          y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } }
        }
      }
    });

  } catch (err) {
    hideLoading();
    showToast('Failed to fetch demand risk analysis.', 'error');
  }
}


// ── Module 2: AI Crop Profitability & Net ROI Calculator ─────────────────────
async function calculateROI() {
  const crop = document.getElementById('roiCropSelect').value;
  const acres = parseFloat(document.getElementById('roiAcresInput').value);
  
  try {
    const res = await fetch(`${API_BASE}/calculate-roi`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ crop, acres })
    });
    const data = await res.json();
    if (!data.success) return;
    
    const info = data.data;
    document.getElementById('roiYieldVal').innerText = `${info.total_yield_qtl} Quintals`;
    document.getElementById('roiCostVal').innerText = `₹${info.total_cost.toLocaleString()}`;
    document.getElementById('roiRevenueVal').innerText = `₹${info.gross_revenue.toLocaleString()}`;
    
    const profitVal = document.getElementById('roiProfitVal');
    profitVal.innerText = `₹${info.net_profit.toLocaleString()} (${info.roi_pct}%)`;
    profitVal.style.color = info.net_profit >= 0 ? '#10b981' : '#ef4444';
    
    // Render Cost Breakdown Donut Chart
    const ctx = document.getElementById('roiCostChart').getContext('2d');
    if (roiCostChart) roiCostChart.destroy();
    
    roiCostChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: Object.keys(info.cost_breakdown),
        datasets: [{
          data: Object.values(info.cost_breakdown),
          backgroundColor: [
            '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4'
          ],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'right', labels: { color: '#94a3b8', font: { size: 11 } } }
        }
      }
    });
    
    // Render Comparison List
    const compContainer = document.getElementById('roiComparisonList');
    compContainer.innerHTML = info.comparison_matrix.map(c => `
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: rgba(255,255,255,0.04); border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
        <div>
          <strong style="color: var(--color-text-primary); font-size: 0.95rem;">${c.crop}</strong>
          <div style="font-size: 0.75rem; color: var(--color-text-secondary);">Cost: ₹${c.total_cost.toLocaleString()} | Rev: ₹${c.gross_revenue.toLocaleString()}</div>
        </div>
        <div style="text-align: right;">
          <span style="font-weight: 700; color: ${c.net_profit >= 0 ? '#10b981' : '#ef4444'}; font-size: 0.95rem;">₹${c.net_profit.toLocaleString()}</span>
          <div style="font-size: 0.75rem; color: #8b5cf6; font-weight: 600;">ROI: ${c.roi_pct}%</div>
        </div>
      </div>
    `).join('');

  } catch (err) {
    console.error('ROI calculation error:', err);
  }
}


// ── Module 3: Smart Weather & Precision Irrigation Advisory ─────────────────
async function loadWeatherAdvisory(state) {
  state = state || document.getElementById('weatherStateSelect').value || 'Karnataka';
  
  try {
    const res = await fetch(`${API_BASE}/weather-advisory?state=${encodeURIComponent(state)}`);
    const data = await res.json();
    if (!data.success) return;
    
    const info = data.data;
    document.getElementById('weatherTempVal').innerText = `${info.current_temp}°C`;
    document.getElementById('weatherTempMinMax').innerText = `High: ${info.max_temp}°C | Low: ${info.min_temp}°C (${info.city})`;
    document.getElementById('weatherWaterVal').innerText = `${info.water_needed_liters_per_acre.toLocaleString()} L / acre`;
    document.getElementById('weatherETVal').innerText = `Evapotranspiration: ${info.water_requirement_et0_mm} mm/day`;
    
    const pestBadge = document.getElementById('weatherPestBadge');
    pestBadge.innerText = `${info.pest_risk} Risk`;
    pestBadge.style.color = info.pest_risk === 'High' ? '#ef4444' : (info.pest_risk === 'Moderate' ? '#f59e0b' : '#10b981');
    
    document.getElementById('weatherHumidityVal').innerText = `Humidity: ${info.humidity}%`;
    document.getElementById('weatherIrrigationAdvice').innerText = info.irrigation_advice;
    document.getElementById('weatherSprayingAdvice').innerText = info.spraying_advice;
    
    // Render 7-day Weather & Rain Trend Dual Chart
    const ctx = document.getElementById('weatherTrendChart').getContext('2d');
    if (weatherTrendChart) weatherTrendChart.destroy();
    
    const forecast = info['7day_forecast'];
    weatherTrendChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: forecast.map(f => f.date.slice(5)),
        datasets: [
          {
            label: 'Max Temp (°C)',
            data: forecast.map(f => f.max_temp),
            borderColor: '#ef4444',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            tension: 0.3,
            yAxisID: 'y'
          },
          {
            label: 'Rainfall (mm)',
            data: forecast.map(f => f.rain_mm),
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.4)',
            type: 'bar',
            borderRadius: 4,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: '#94a3b8' } } },
        scales: {
          x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
          y: { type: 'linear', position: 'left', ticks: { color: '#ef4444' }, title: { display: true, text: 'Temp (°C)', color: '#ef4444' } },
          y1: { type: 'linear', position: 'right', ticks: { color: '#3b82f6' }, grid: { display: false }, title: { display: true, text: 'Rain (mm)', color: '#3b82f6' } }
        }
      }
    });

  } catch (err) {
    console.error('Weather advisory error:', err);
  }
}

