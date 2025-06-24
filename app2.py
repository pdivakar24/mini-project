from flask import Flask, request, render_template_string
import re
import numpy as np
import webbrowser
import threading

app = Flask(__name__)

def extract_features(url):
    features = []
    features.append(1 if re.search(r'(\d{1,3}\.){3}\d{1,3}', url) else 0)  
    features.append(1 if len(url) > 75 else 0)                             
    features.append(1 if '@' in url else 0)                                
    features.append(1 if url.count('-') > 3 else 0)                        
    features.append(1 if url.startswith('https') == False else 0)         
    features.append(1 if re.search(r'(login|update|secure|account)', url.lower()) else 0)  
    return np.array([features])

def predict_phishing(features):
    score = 0
    weights = [30, 20, 10, 10, 20, 30]  # Weight per feature
    for i in range(len(features[0])):
        score += features[0][i] * weights[i]
    probability = min(score, 100)
    prediction = 1 if probability >= 50 else 0
    return prediction, probability


template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Phishing URL Detector</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; padding-top: 50px; }
        input[type="text"] { width: 60%%; padding: 10px; font-size: 16px; }
        input[type="submit"] { padding: 10px 20px; font-size: 16px; }
        .result { font-size: 1.2em; margin-top: 20px; color: #333; }
        .container { background-color: white; width: 60%%; margin: auto; padding: 40px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="container">
        <h1>Phishing URL Detector</h1>
        <form method="post">
            <input type="text" name="url" placeholder="Enter URL here..." required>
            <br><br>
            <input type="submit" value="Detect">
        </form>
        {% if url %}
            <div class="result"><strong>Entered URL:</strong> {{ url }}</div>
            <div class="result"><strong>Prediction:</strong> {{ result }}</div>
            <div class="result"><strong>Confidence:</strong> {{ confidence }}%%</div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    url = ''
    result = ''
    confidence = ''
    if request.method == 'POST':
        url = request.form['url']
        features = extract_features(url)
        prediction, prob = predict_phishing(features)
        result = 'Phishing' if prediction == 1 else 'Legitimate'
        confidence = prob
    return render_template_string(template, url=url, result=result, confidence=confidence)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True)
