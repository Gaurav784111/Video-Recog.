from flask import Flask, request, jsonify
import face_recognition
import numpy as np
import pickle

app = Flask(__name__)

# Load known faces
with open("db.pkl", "rb") as f:
    db = pickle.load(f)

@app.route("/recognize", methods=["POST"])
def recognize():
    file = request.files["image"]

    image = face_recognition.load_image_file(file)
    encs = face_recognition.face_encodings(image)

    if len(encs) == 0:
        return jsonify({"name": "No Face"})

    encoding = encs[0]

    names = [x["name"] for x in db]
    encodings = [x["encoding"] for x in db]

    matches = face_recognition.compare_faces(encodings, encoding)
    distances = face_recognition.face_distance(encodings, encoding)

    if len(distances) > 0:
        best = np.argmin(distances)
        if matches[best]:
            return jsonify({"name": names[best]})

    return jsonify({"name": "Unknown"})

app.run(host="0.0.0.0", port=5000)
