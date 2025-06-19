from flask import Flask, jsonify, request

from backend.damage_detection import decode_image, detect_damage

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "Cycle Tourism Platform API"})


@app.route("/health")
def health_check():
    return jsonify({"status": "ok"})


@app.route("/detect_road_damage", methods=["POST"])
def detect_road_damage():
    data = request.get_json(force=True)
    if not data or "image" not in data:
        return jsonify({"error": "image field required"}), 400
    try:
        image = decode_image(data["image"])
        boxes = detect_damage(image)
        return jsonify({"boxes": boxes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5005)
