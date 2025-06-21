"""
server.py
Servidor Flask para análise de emoções usando Watson NLP.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    """Renderiza a página inicial."""
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET', 'POST'])
def emotion_detector_route():
    """
    Rota para análise de emoções.

    Aceita texto via GET ou POST e retorna as emoções detectadas.
    """
    if request.method == "POST":
        text_to_analyze = request.form.get('textToAnalyze')
        if not text_to_analyze and request.is_json:
            text_to_analyze = request.get_json().get('textToAnalyze')
    else:
        text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze:
        # Entrada em branco explícita
        return jsonify({"error": "Texto inválido! Por favor, tente novamente!"}), 400

    result = emotion_detector(text_to_analyze)
    if result.get('dominant_emotion') is None:
        return jsonify({"error": "Texto inválido! Por favor, tente novamente!"}), 400
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
    