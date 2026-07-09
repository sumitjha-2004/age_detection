from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from PIL import Image

from predict import predict

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def prediction():

    file = request.files.get("image")
    if not file:
        return jsonify(error="Please upload an image."), 400

    try:
        image = Image.open(file).convert("RGB")
    except Exception:
        return jsonify(error="Could not read that file as an image."), 400

    age, confidence, distribution = predict(image)   # <-- 3 values, not 2

    return jsonify(
        prediction=age,
        confidence=round(confidence, 2),
        distribution=distribution
    )

if __name__ == "__main__":
    app.run(debug=True)