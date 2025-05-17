from flask import Flask, request
from .requestHandler import RequestHandler
from backend_shared.configurator import Configurator
import os

api = Flask(__name__)

request_handler = None

base_route = "/api/v1"
data_path = f"{os.getcwd()}/binarys"

@api.route("/", methods=["GET"])
def index():
    return "200 OK from video-service"

@api.route(f"{base_route}/healthz", methods=["GET"])
def healthz():
    return "200 OK from video-service"

@api.route(f"{base_route}/video", methods=["POST"])
def post_video():
    return request_handler.create_video(request)

def run(conf):
    global config, request_handler
    config = conf
    request_handler = RequestHandler(config)
    if config["video_service"]["cors_enabled"]:
        from flask_cors import CORS
        cors = CORS(api)
    api.run(debug=True, host=config["video_service"]["hostname"], port=config["video_service"]["port"])
