import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem

def generate_pdf():
    pdf_filename = "Hanu_Agri_Project_Details_and_QA.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = 1 # Center
    heading_style = styles['Heading2']
    subheading_style = styles['Heading3']
    normal_style = styles['Normal']
    normal_style.fontSize = 11
    normal_style.leading = 14
    
    question_style = ParagraphStyle(
        name='Question',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        spaceBefore=6,
        spaceAfter=2
    )
    answer_style = ParagraphStyle(
        name='Answer',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica',
        leftIndent=15,
        spaceAfter=10
    )

    story = []

    # Title
    story.append(Paragraph("Hanu Agri: Demand Prediction System", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Project Architecture, Tools & Top 50 Viva Questions", styles['Heading3']))
    story.append(Spacer(1, 20))

    # Part 1: Properties & Architecture
    story.append(Paragraph("1. Project Properties & Architecture", heading_style))
    story.append(Spacer(1, 6))
    props = [
        "<b>Frontend:</b> Pure HTML5, CSS3, and Vanilla JavaScript. Ensures lightweight, fast rendering without heavy frameworks.",
        "<b>Backend:</b> Python with Flask framework. Serves RESTful APIs for the frontend to consume.",
        "<b>Machine Learning Models:</b> Built using Scikit-Learn (Random Forest classifiers/regressors) for crop and fertilizer recommendations.",
        "<b>Computer Vision:</b> OpenCV and basic Deep Learning/Image Processing for Crop Disease Detection.",
        "<b>External APIs:</b> Uses open-source APIs (like wttr.in for weather) and OpenStreetMap (Leaflet.js) for finding nearby APMC markets.",
        "<b>Multi-language Support:</b> Built-in i18n system in JavaScript to toggle between English, Hindi, and Kannada.",
        "<b>Architecture Pattern:</b> Client-Server architecture with stateless REST APIs.",
    ]
    for p in props:
        story.append(Paragraph(f"• {p}", normal_style))
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 12))

    # Part 2: Tools Used
    story.append(Paragraph("2. Tools & Technologies Used", heading_style))
    story.append(Spacer(1, 6))
    tools = [
        "<b>Programming Languages:</b> Python 3.12, JavaScript (ES6+)",
        "<b>Libraries (Python):</b> Flask, Flask-CORS, Pandas, NumPy, Scikit-Learn, OpenCV (opencv-python-headless), urllib",
        "<b>Libraries (JS):</b> Leaflet.js (for interactive maps), Chart.js (for data visualization)",
        "<b>Version Control & Deployment:</b> Git, GitHub, Render (PaaS), Railway",
        "<b>Data Processing:</b> Pandas for data cleaning and mock dataset generation",
        "<b>Development Environment:</b> VS Code, Chrome Developer Tools"
    ]
    for t in tools:
        story.append(Paragraph(f"• {t}", normal_style))
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 20))

    # Part 3: Top 50 Questions
    story.append(Paragraph("3. Top 50 Viva / Interview Questions", heading_style))
    story.append(Spacer(1, 10))

    qa_list = [
        # General & Motivation
        ("What is the main objective of the Hanu Agri project?", "To empower farmers with AI-driven insights for crop selection, fertilizer use, and market prices to maximize profitability."),
        ("Why did you choose Flask over Django for the backend?", "Flask is a lightweight micro-framework, which is perfect for serving simple REST APIs for our Machine Learning models without unnecessary overhead."),
        ("What real-world problem does this project solve?", "It solves the lack of data-driven decision making in traditional farming, helping farmers avoid crop failure and market gluts."),
        ("How does the system ensure it is accessible to rural farmers?", "By providing multi-language support (English, Hindi, Kannada) and an easy-to-use intuitive UI."),
        
        # Architecture & Frontend
        ("What architectural pattern is used in this project?", "Client-Server architecture. The frontend is fully decoupled from the backend and communicates via REST APIs."),
        ("Why did you use Vanilla JavaScript instead of React or Angular?", "To keep the project lightweight, minimize dependencies, and ensure fast load times even on slow networks."),
        ("How is multi-language support implemented?", "A JavaScript dictionary stores translations. A function traverses the DOM elements with a 'data-i18n' attribute and updates their inner text based on the selected language."),
        ("How does the frontend communicate with the backend?", "Using the JavaScript Fetch API to send GET and POST requests to the Flask server endpoints."),
        ("What is Leaflet.js used for in your project?", "It is used in the 'Market Finder' module to render an interactive map and display the user's location alongside nearby APMC markets."),
        ("How is the user's location retrieved?", "Using the HTML5 Geolocation API (navigator.geolocation.getCurrentPosition)."),
        
        # Machine Learning (Crop & Fertilizer)
        ("Which machine learning algorithm is used for Crop Recommendation?", "Random Forest Classifier. It handles non-linear data well and is robust to overfitting."),
        ("What features are used to predict the best crop?", "Nitrogen (N), Phosphorus (P), Potassium (K), Temperature, Humidity, pH, and Rainfall."),
        ("How did you handle the lack of real-world agricultural data?", "We wrote a Python script to synthesize highly realistic datasets based on known agricultural parameters for Indian crops."),
        ("Why is Random Forest preferred over Decision Trees here?", "Random Forest builds multiple decision trees and averages them, preventing the overfitting that a single decision tree is prone to."),
        ("How does the Fertilizer Guidance module work?", "It takes the current soil nutrients and crop type, compares them to ideal thresholds, and recommends specific fertilizers (like Urea or DAP) to bridge the gap."),
        ("What preprocessing is applied to the data before training?", "Data is scaled using StandardScaler to normalize feature ranges, and labels are encoded."),
        ("How is the trained model integrated into the Flask app?", "The model and scaler are serialized using 'pickle' and loaded into memory when the Flask server starts."),
        ("What happens if a user enters extremely out-of-bound soil values?", "The Random Forest model will predict the closest matching crop, but the system also has threshold checks to warn users if the land is uncultivable."),
        
        # Price Prediction & Demand
        ("How does the Price Prediction module work?", "It uses historical mock data and a regression model to forecast the price of a commodity for upcoming months."),
        ("What is the Demand & Glut Risk module?", "It analyzes current market trends and advises farmers if planting a specific crop might lead to an oversupply (glut) and low prices."),
        ("How do you calculate ROI (Return on Investment)?", "By subtracting estimated cultivation costs from the predicted market revenue (Price × Expected Yield)."),
        
        # Disease Detection
        ("How does the Crop Disease Detection module work?", "The user uploads an image. OpenCV is used to process the image, extract color/texture features, and classify the disease."),
        ("Why use OpenCV instead of a CNN (like ResNet)?", "OpenCV allows for lightweight, rule-based color masking (e.g., detecting yellowing or brown spots) which runs very fast without needing a GPU."),
        ("What image preprocessing steps are performed?", "Resizing, Gaussian blurring to reduce noise, and converting from BGR to HSV color space for better color segmentation."),
        
        # Chatbot & External APIs
        ("How does the AI Chatbot understand user queries?", "It uses Regex and keyword matching to identify intents like 'weather' or 'fertilizer prices'."),
        ("Which API is used for weather fetching?", "The wttr.in API, which provides free weather data without requiring an API key."),
        ("Why did you switch from Open-Meteo/Nominatim to wttr.in?", "Cloud hosting providers (like Render) often get IP-blocked by Nominatim. wttr.in is more cloud-friendly for fetching weather."),
        ("How does the chatbot handle unsupported questions?", "It has a fallback default response guiding the user to ask about supported topics like weather or crop prices."),
        
        # Backend & Deployment
        ("What is the role of Gunicorn in this project?", "Gunicorn is a Python Web Server Gateway Interface (WSGI) HTTP server. It is used to serve the Flask app in production, handling multiple concurrent requests."),
        ("Why can't we just use 'app.run()' in production?", "Flask's built-in server is not designed for production; it is single-threaded and cannot handle concurrent traffic efficiently."),
        ("How is the project deployed?", "It is deployed as a Web Service on Render, which automatically builds the environment from 'requirements.txt' and runs Gunicorn."),
        ("What is the purpose of the 'render.yaml' file?", "It is an Infrastructure-as-Code Blueprint that tells Render exactly how to build and start the application."),
        ("Why are the ML models trained during the 'build' phase on Render?", "Because Gunicorn doesn't run the 'if __name__ == __main__' block. Training during the build ensures models exist before workers start, preventing file-not-found errors."),
        ("What is CORS and why is it used?", "Cross-Origin Resource Sharing. It's enabled in Flask to allow the frontend (if hosted on a different domain) to make API requests to the backend."),
        
        # Code specific & Debugging
        ("What happens if the weather API goes down?", "The backend wraps the request in a try-except block and returns a graceful error message instead of crashing the server."),
        ("How do you handle missing environment variables?", "We provide default fallback values in the code, though Render injects necessary variables like PORT automatically."),
        ("What is 'pickle' in Python?", "A module used for serializing and de-serializing Python object structures, used here to save trained ML models."),
        ("Why use 'np.argsort()[::-1]' in predictions?", "It sorts the prediction probabilities in descending order so we can recommend the top 3 or top 5 best crops."),
        ("How does the 'Harvest Readiness' module analyze videos?", "It extracts frames using OpenCV (`cv2.VideoCapture`), analyzes the color distribution of the crop in those frames, and averages the results to determine maturity."),
        ("How is state managed in the frontend?", "State (like current language and current page) is managed using global variables in 'app.js'."),
        
        # Evaluation & Future scope
        ("What is the accuracy of your Crop Recommendation model?", "Typically around 95-98% on our synthesized dataset."),
        ("How do you evaluate a classification model?", "Using metrics like Accuracy, Precision, Recall, and F1-Score, derived from a Confusion Matrix."),
        ("How would you improve the Disease Detection module?", "By replacing OpenCV color masking with a deep learning CNN model like MobileNet trained on the PlantVillage dataset."),
        ("What is the biggest limitation of your current system?", "It relies heavily on synthesized data. Real-world implementation requires integration with live IoT soil sensors and real APMC market data APIs."),
        ("How could you make the chatbot smarter?", "By integrating a Large Language Model (LLM) API like Google Gemini or OpenAI to handle conversational context naturally."),
        ("How is user data security handled?", "Currently, the app doesn't require user logins or save personal data, ensuring complete privacy."),
        ("What is the role of CSS Variables in your project?", "CSS variables (e.g., --color-primary) define the theme. They make it extremely easy to maintain consistency and implement Dark Mode in the future."),
        ("How is the app made responsive for mobile devices?", "Using CSS media queries, flexbox, and a toggleable mobile sidebar."),
        ("Why do you use 'object-fit: cover' for images?", "It ensures images (like the background or profile photo) fill their container without distorting their aspect ratio."),
        ("What was the most challenging bug you faced during deployment?", "The models failing to load on Render because Gunicorn bypasses the main execution block, which was solved by adding a dedicated setup script during the build phase.")
    ]

    for i, (q, a) in enumerate(qa_list, 1):
        story.append(Paragraph(f"Q{i}: {q}", question_style))
        story.append(Paragraph(f"<b>Ans:</b> {a}", answer_style))

    doc.build(story)
    print(f"PDF successfully generated at {pdf_filename}")

if __name__ == '__main__':
    generate_pdf()
