# Hanu Agri — Agricultural Demand Prediction System

![Hanu Agri Banner](frontend/assets/hanu_logo.jpg) <!-- Optional, just pointing to local asset -->

Hanu Agri is an AI-powered Agricultural Demand Prediction System designed to empower Indian farmers with data-driven insights. The platform provides a suite of tools including crop recommendation, price forecasting, fertilizer guidance, disease detection, and market connections, helping farmers maximize their yield and profitability.

## 🚀 Live Demo

**Experience the application here:** [Live Demo on Render](https://hanu-agriculture-2.onrender.com)

## ✨ Features

- **Crop Recommendation:** Suggests the most suitable crops based on soil conditions (N, P, K), temperature, humidity, pH, and rainfall.
- **Fertilizer Guidance:** Recommends optimal fertilizer usage tailored to specific soil types and crops.
- **Price Forecasting:** Predicts future crop prices to help farmers decide the best time to sell their produce.
- **Disease Detection:** Identifies crop diseases and provides actionable treatment suggestions.
- **Demand & Supply Analysis:** Analyzes market trends to give farmers an edge in planning their harvest.
- **Profitability Calculator:** Estimates potential profits based on input costs and projected market prices.
- **Weather Advisory:** Provides localized weather forecasts and farming advisories.
- **Crop Maturity Analyzer:** Tracks crop growth stages and predicts harvest times.

## 🛠️ Technology Stack

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- [Chart.js](https://www.chartjs.org/) for data visualization
- [Leaflet.js](https://leafletjs.com/) for interactive maps

**Backend:**
- Python 3.x
- [Flask](https://flask.palletsprojects.com/) (Web Framework)
- Scikit-learn, Pandas, NumPy (Machine Learning & Data Processing)
- OpenCV, Pillow (Image Processing)

## 💻 Getting Started (Local Development)

Follow these instructions to set up the project on your local machine.

### Prerequisites

- Python 3.8 or higher installed
- Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kuvaleshcd-hue/hanu-agriculture.git
   cd hanu-agriculture
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run the Flask backend server:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your web browser and navigate to `http://127.0.0.1:5000/`. The backend is configured to serve the frontend files automatically.

## 📄 Documentation

The repository includes detailed project reports in the root directory:
- `Agricultural_AI_Project_Report.pdf`
- `Agricultural_AI_System_Architecture_and_Algorithms.pdf`
- `Hanu_Agri_Official_40_Page_Project_Report.pdf`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License.
