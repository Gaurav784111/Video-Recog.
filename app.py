from flask import Flask, request, jsonify, render_template
from deepface import DeepFace
import cv2
import numpy as np
import base64

app = Flask(__name__)

# Build face database once
database_path = "dataset"

@app.route("/")
def home():
    return render_template("index.html")


def decode_image(data):
    img_data = base64.b64decode(data.split(",")[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img


@app.route("/recognize", methods=["POST"])
def recognize():
    data = request.json["image"]
    frame = decode_image(data)

    try:
        result = DeepFace.find(
            img_path=frame,
            db_path=database_path,
            enforce_detection=False
        )

        if len(result[0]) > 0:
            name = result[0]["identity"].iloc[0].split("/")[-2]
            return jsonify({"name": name})

        return jsonify({"name": "Unknown"})

    except Exception as e:
        return jsonify({"name": "Error", "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
