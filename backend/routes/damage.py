from flask import Blueprint, jsonify, request

from backend.services import decode_image, detect_damage


damage_bp = Blueprint("damage", __name__)


@damage_bp.route("/detect_road_damage", methods=["POST"])
def detect_road_damage_endpoint():
    data = request.get_json(force=True)
    if not data or "image" not in data:
        return jsonify({"error": "image field required"}), 400
    try:
        image = decode_image(data["image"])
        boxes = detect_damage(image)
        return jsonify({"boxes": boxes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
