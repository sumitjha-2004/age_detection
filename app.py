from flask import Flask
from flask import render_template
from flask import request

from PIL import Image

from predict import predict

app = Flask(__name__)

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def prediction():

    file = request.files["image"]

    image = Image.open(file).convert("RGB")

    age, confidence = predict(image)

    return render_template(
        "index.html",
        prediction=age,
        confidence=round(confidence,2)
    )

app.run(debug=True)