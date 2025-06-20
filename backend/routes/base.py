from flask import Blueprint, jsonify

base_bp = Blueprint("base", __name__)


@base_bp.route("/")
def index():
    return jsonify({"message": "Cycle Tourism Platform API"})


@base_bp.route("/health")
def health_check():
    return jsonify({"status": "ok"})
