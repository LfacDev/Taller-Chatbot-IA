from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

comentarios = []
analyzer = SentimentIntensityAnalyzer()

EMOCIONES_IMAGENES = {
    "Positiva": "https://png.pngtree.com/png-clipart/20240523/original/pngtree-happy-face-emoji-clipart-image-png-image_15164130.png",
    "Negativa": "https://cdn3d.iconscout.com/3d/free/thumb/free-cara-triste-3750922-3144984.png?f=webp",
    "Neutral": "https://png.pngtree.com/png-clipart/20240913/original/pngtree-neutral-face-emoji-png-image_16001969.png"
}

# 🔹 Palabras clave que pueden ayudar a mejorar la detección de emociones
PALABRAS_POSITIVAS = {"feliz", "contento", "genial", "increíble", "maravilloso", "alegría", "bueno", "excelente", "bonito", "lindo"}
PALABRAS_NEGATIVAS = {"triste", "horrible", "terrible", "desastroso", "malo", "deprimido", "morir", "feo", "pésimo", "aburrido"}

@app.route("/emocion", methods=["POST"])
def detectar_emocion():
    data = request.json
    comentario = data.get("comentario", "").lower()  # 🔹 Convertir a minúsculas para evitar errores

    if not comentario:
        return jsonify({"error": "Comentario vacío"}), 400

    # 🔹 Analizar con VADER
    scores = analyzer.polarity_scores(comentario)
    compound = scores["compound"]

    # 🔹 Revisión de palabras clave
    palabras = set(comentario.split())

    if compound >= 0.05 or palabras & PALABRAS_POSITIVAS:
        emocion = "Positiva"
    elif compound <= -0.05 or palabras & PALABRAS_NEGATIVAS:
        emocion = "Negativa"
    else:
        emocion = "Neutral"

    print(f"📌 Comentario: {comentario} → Compound Score: {compound} → Emoción: {emocion}")

    resultado = {
        "texto": comentario,
        "emocion": emocion,
        "imagen": EMOCIONES_IMAGENES[emocion]
    }

    comentarios.append(resultado)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
