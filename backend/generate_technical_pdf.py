import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Hanu Agri — Technical Architecture & Algorithms Specification")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 612 - 54, 742)
        
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — AGRICULTURAL DEMAND PREDICTION SYSTEM")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 612 - 54, 48)
        self.restoreState()

def generate_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1e3a8a")  # Deep blue
    secondary_color = colors.HexColor("#15803d") # Deep green
    text_dark = colors.HexColor("#0f172a")
    text_muted = colors.HexColor("#475569")
    bg_light = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#cbd5e1")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark,
        leftIndent=12,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=text_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=text_dark
    )

    story = []

    # Title Block
    story.append(Paragraph("Agricultural Demand Prediction & Decision Support System", title_style))
    story.append(Paragraph("Comprehensive Technical Architecture, Languages, Databases & Machine Learning Algorithms", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=2, spaceAfter=14))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary & Project Overview", h1_style))
    story.append(Paragraph(
        "The <b>Hanu Agri Demand Prediction System</b> is an end-to-end intelligent agricultural advisory platform "
        "designed to empower Indian farmers, agronomists, and supply-chain stakeholders. The system combines multi-variable "
        "supervised machine learning models, statistical time-series forecasting, agro-climatic formulas, and geospatial analytics "
        "to deliver real-time actionable insights for crop recommendation, commodity price trends, fertilizer schedules, "
        "market glut risk, precision irrigation, and crop disease diagnosis.",
        body_style
    ))

    # Section 2: Frontend
    story.append(Paragraph("2. Frontend Technologies & Languages", h1_style))
    frontend_data = [
        [Paragraph("Layer / Component", table_header_style), Paragraph("Technology & Version", table_header_style), Paragraph("Implementation Details & Capabilities", table_header_style)],
        [Paragraph("Markup", table_cell_bold), Paragraph("HTML5", table_cell_style), Paragraph("Semantic structure for 10+ modules, responsive dashboards, modal overlays, input forms, and data cards.", table_cell_style)],
        [Paragraph("Styling", table_cell_bold), Paragraph("CSS3 (Modern Vanilla)", table_cell_style), Paragraph("Custom design system, CSS Grid/Flexbox, glassmorphism, responsive breakpoints, smooth micro-interactions, dark accents.", table_cell_style)],
        [Paragraph("Client Logic", table_cell_bold), Paragraph("JavaScript (ES6+)", table_cell_style), Paragraph("Asynchronous REST client (Fetch API), dynamic DOM updates, state management, client-side routing, voice TTS/STT handling.", table_cell_style)],
        [Paragraph("Charts & Visuals", table_cell_bold), Paragraph("Chart.js (v4.4.0)", table_cell_style), Paragraph("Interactive 30-day price trend lines, uncertainty intervals, ROI donut charts, and weather precipitation graphs.", table_cell_style)],
        [Paragraph("Geospatial Maps", table_cell_bold), Paragraph("Leaflet.js (v1.9.4) & OpenStreetMap", table_cell_style), Paragraph("Interactive APMC Mandi geolocation mapping, custom markers, user coordinate radius, and route discovery.", table_cell_style)],
        [Paragraph("Voice & Speech", table_cell_bold), Paragraph("Web Speech API", table_cell_style), Paragraph("Integrated voice-driven chatbot queries and multilingual text-to-speech audio playback in English, Kannada, and Hindi.", table_cell_style)]
    ]
    t_front = Table(frontend_data, colWidths=[90, 110, 304])
    t_front.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_front)
    story.append(Spacer(1, 10))

    # Section 3: Backend
    story.append(Paragraph("3. Backend Technologies & Frameworks", h1_style))
    backend_data = [
        [Paragraph("Component", table_header_style), Paragraph("Technology", table_header_style), Paragraph("Architectural Role", table_header_style)],
        [Paragraph("Programming Language", table_cell_bold), Paragraph("Python 3.11+", table_cell_style), Paragraph("Core runtime for data processing pipelines, ML inference, mathematical computations, and REST services.", table_cell_style)],
        [Paragraph("Web Microframework", table_cell_bold), Paragraph("Flask (v3.0+)", table_cell_style), Paragraph("Lightweight, high-throughput REST API server handling request validation, routing, JSON serialization, and static asset delivery.", table_cell_style)],
        [Paragraph("Cross-Origin Handler", table_cell_bold), Paragraph("Flask-CORS (v4.0+)", table_cell_style), Paragraph("Manages secure cross-origin resource access across web clients, endpoints, and external callers.", table_cell_style)],
        [Paragraph("Scientific ML Stack", table_cell_bold), Paragraph("Scikit-Learn, NumPy, Pandas", table_cell_style), Paragraph("High-performance matrix computing, feature scaling, model fitting, and time-series feature engineering.", table_cell_style)],
        [Paragraph("Image Engine", table_cell_bold), Paragraph("Pillow (PIL v10.0+)", table_cell_style), Paragraph("Decodes, resizes, and pre-processes leaf image buffers for plant pathology detection.", table_cell_style)]
    ]
    t_back = Table(backend_data, colWidths=[110, 110, 284])
    t_back.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_back)
    story.append(Spacer(1, 10))

    # Section 4: Database & Storage
    story.append(Paragraph("4. Database & Storage Architecture", h1_style))
    story.append(Paragraph(
        "The system uses a resilient, high-speed <b>serialized & file-based storage architecture</b> designed for low latency and zero-dependency cloud deployment:",
        body_style
    ))
    db_data = [
        [Paragraph("Storage Medium", table_header_style), Paragraph("File Path / Asset", table_header_style), Paragraph("Contents & Functionality", table_header_style)],
        [Paragraph("Tabular CSV Datasets", table_cell_bold), Paragraph("backend/data/*.csv", table_cell_style), Paragraph("Contains ground-truth crop parameter datasets (crop_data.csv), fertilizer records (fertilizer_data.csv), and historical mandi modal prices across 10+ states (price_data.csv).", table_cell_style)],
        [Paragraph("JSON Knowledge Bases", table_cell_bold), Paragraph("backend/data/*.json", table_cell_style), Paragraph("Relational structured knowledge stores for Indian government agricultural subsidies (PM-KISAN, PMFBY, PKVY) and plant pathology treatment guides (disease_labels.json).", table_cell_style)],
        [Paragraph("Pre-Trained Pickles", table_cell_bold), Paragraph("backend/models/*.pkl", table_cell_style), Paragraph("Pre-compiled binary Scikit-Learn pipelines containing trained decision trees, ensemble estimators, scalers, and label encoders for instant <10ms inference.", table_cell_style)]
    ]
    t_db = Table(db_data, colWidths=[110, 110, 284])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_db)
    story.append(Spacer(1, 14))

    # Page Break for Algorithms section
    story.append(PageBreak())

    # Section 5: Algorithms
    story.append(Paragraph("5. Comprehensive Mathematical & Machine Learning Algorithms", h1_style))
    story.append(Paragraph(
        "The platform integrates eight core machine learning models, statistical algorithms, and domain-specific agro-climatic formulas:",
        body_style
    ))

    # Alg 1
    story.append(Paragraph("A. Crop Recommendation — Random Forest Classifier", h2_style))
    story.append(Paragraph(
        "<b>Model:</b> <font name='Courier'>RandomForestClassifier(n_estimators=200, max_depth=20, min_samples_split=5)</font><br/>"
        "<b>Inputs:</b> Nitrogen (N), Phosphorus (P), Potassium (K), Temperature (°C), Humidity (%), Soil pH, Rainfall (mm).<br/>"
        "<b>Pre-processing:</b> Z-score standard normalization:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>z = (x - &mu;) / &sigma;</b><br/>"
        "<b>Mechanism:</b> Constructs an ensemble of 200 de-correlated decision trees trained via bootstrap aggregating (bagging). "
        "Outputs calibrated class probabilities for 22+ agricultural crops, returning the top 5 ranking crops with percentage confidence scores.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Alg 2
    story.append(Paragraph("B. Price & Demand Forecasting — Gradient Boosting Regressor", h2_style))
    story.append(Paragraph(
        "<b>Model:</b> <font name='Courier'>GradientBoostingRegressor(n_estimators=200, max_depth=6, learning_rate=0.1)</font><br/>"
        "<b>Time-Series Feature Engineering:</b> To capture seasonal cycles and harvest periodicity, dates are converted to harmonic circular features:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>month_sin = sin(2&pi; &times; month / 12),&nbsp;&nbsp;month_cos = cos(2&pi; &times; month / 12)</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>doy_sin = sin(2&pi; &times; doy / 365),&nbsp;&nbsp;doy_cos = cos(2&pi; &times; doy / 365)</b><br/>"
        "<b>Mechanism:</b> Sequentially trains weak regression trees minimizing Mean Squared Error (MSE). Generates 30-day projected commodity prices "
        "along with asymmetric confidence bands (92% min floor, 108% max ceiling) and directional momentum analysis.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Alg 3
    story.append(Paragraph("C. Fertilizer Recommendation — Multi-Class Decision Tree", h2_style))
    story.append(Paragraph(
        "<b>Model:</b> <font name='Courier'>DecisionTreeClassifier(max_depth=15, min_samples_split=5)</font><br/>"
        "<b>Inputs:</b> Soil Type, Crop Type, Nitrogen, Phosphorus, Potassium, Moisture, Temperature, Humidity.<br/>"
        "<b>Mechanism:</b> Employs Gini Impurity recursive partitioning to recommend the exact fertilizer formula (Urea, DAP, MOP, NPK 20-20-20, SSP, etc.) "
        "supplemented with automated agronomic nutrient threshold warnings (Low/High/Optimal).",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Alg 4
    story.append(Paragraph("D. Market Glut & Overproduction Risk Engine", h2_style))
    story.append(Paragraph(
        "<b>Algorithm:</b> Demand-Supply Elasticity & Risk Heuristic Algorithm.<br/>"
        "<b>Mathematical Formulation:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Supply-Demand Ratio (R) = Projected Production (MT) / Estimated Demand (MT)</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Risk Score = clamp(10, 95, (R - 0.85) &times; 200)</b><br/>"
        "<b>Output:</b> Classifies overproduction risk into Low (<40), Moderate (40-65), or High (>65), warning farmers against catastrophic price crashes "
        "and suggesting lower-risk alternative diversification crops.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Alg 5
    story.append(Paragraph("E. Geospatial Mandi Proximity — Haversine Distance Formula", h2_style))
    story.append(Paragraph(
        "<b>Algorithm:</b> Great-Circle Geodesic Distance Computation.<br/>"
        "<b>Mathematical Formulation:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>a = sin&sup2;(&Delta;&phi; / 2) + cos(&phi;1) &times; cos(&phi;2) &times; sin&sup2;(&Delta;&lambda; / 2)</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>d = 2 &times; R &times; arcsin(&radic;a),&nbsp;&nbsp;where R = 6,371 km</b><br/>"
        "<b>Output:</b> Computes exact geodesic distance between farmer device coordinates and regional wholesale APMC mandis.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Alg 6
    story.append(Paragraph("F. Evapotranspiration & Precision Irrigation Advisory", h2_style))
    story.append(Paragraph(
        "<b>Algorithm:</b> Hargreaves-Samani Evapotranspiration Formula (ET<sub>0</sub>).<br/>"
        "<b>Mathematical Formulation:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>ET<sub>0</sub> = 0.0023 &times; (T<sub>mean</sub> + 17.8) &times; (T<sub>max</sub> - T<sub>min</sub>)<sup>0.5</sup> &times; R<sub>a</sub></b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Crop Water Requirement (Liters/Acre) = ET<sub>0</sub> &times; 4,046.86</b><br/>"
        "<b>Output:</b> Precise daily irrigation volume recommendation, rainfall wash-off spraying alerts, and fungal pest humidity risk indexing.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Alg 7
    story.append(Paragraph("G. Crop ROI & Farm Budgeting Matrix", h2_style))
    story.append(Paragraph(
        "<b>Mathematical Model:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Total Cost = &sum;(Seeds + Land Prep + Fertilizers + Labor + Irrigation + Harvest) &times; Acres</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Gross Revenue = (Yield per Acre &times; Acres) &times; Market Price per Quintal</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Net Profit = Gross Revenue - Total Cost,&nbsp;&nbsp;ROI % = (Net Profit / Total Cost) &times; 100</b><br/>"
        "<b>Output:</b> Full financial feasibility breakdown and automated ROI comparison ranking against substitute crops.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Alg 8
    story.append(Paragraph("H. Plant Leaf Disease Pathology Detection", h2_style))
    story.append(Paragraph(
        "<b>Architecture:</b> Convolutional Neural Network (CNN) Deep Learning Classifier pipeline trained on agricultural pathology datasets (PlantVillage). "
        "Evaluates leaf lesion patterns to output disease diagnoses, severity levels (Low/Medium/High), and biological/chemical remedy protocols.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Section 6: APIs
    story.append(Paragraph("6. External Cloud Services & APIs", h1_style))
    story.append(Paragraph("&bull; <b>Open-Meteo Weather & Geocoding API:</b> Provides free, high-resolution live meteorological data and coordinate lookup.", bullet_style))
    story.append(Paragraph("&bull; <b>WeatherAPI.com:</b> Enterprise fallback live weather forecasting provider.", bullet_style))
    story.append(Paragraph("&bull; <b>OpenStreetMap Nominatim:</b> Open-access reverse geocoding and tile server mapping for APMC mandi navigation.", bullet_style))
    story.append(Paragraph("&bull; <b>HTML5 Web Speech API:</b> Multilingual speech recognition and acoustic synthesis for vernacular accessibility.", bullet_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF at: {output_path}")

if __name__ == '__main__':
    target = '/Users/kuvalesh/Downloads/agri-demand-prediction/Agricultural_AI_System_Architecture_and_Algorithms.pdf'
    generate_pdf(target)
