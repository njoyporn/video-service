from backend_shared.database import db_connection, db_utils
from backend_shared.security import verifier, token
from backend_shared.logger import logger
from backend_shared.utils import random
from backend_shared.types import BusinessResponse, BusinessError
from video import videoEditor

class RequestHandler:
    def __init__(self, config):
        self.config = config
        self.db_connection = db_connection.Connection(self.config["database"]["hostname"], self.config["database"]["user"]["username"], self.config["database"]["user"]["password"], self.config["database"]["name"], self.config["database"]["port"])
        self.verifier = verifier.Verifier(self.db_connection, self.config)
        self.db_utils = db_utils.DBUtils()
        self.logger = logger.Logger()
        self.random = random.Random()
        self.video_editor = videoEditor.VideoEditor(self.db_connection, self.config)
        self.tokenizer = token.Tokenizer(self.config)

    def create_video(self, request):
        try:self.logger.log("INFO", f"Addr: {request.headers['X-Forwarded-For']} want to create video")
        except: pass
        try:
            authHeader = request.headers["Authorization"]
            self.logger.log("INFO", f"Want to create video with token: {authHeader}")
        except: return BusinessResponse(self.random.CreateRandomId(), "ERROR", [], BusinessError(self.random.CreateRandomId(), "CAN_NOT_CREATE_VIDEO")).toJson()
        userData = self.tokenizer.decode(request.headers["Authorization"])
        try:
            if userData["role"] == self.config["roles"]["administrator"]:
                self.logger.log("INFO", f"DEBUG VIDEO_CREATION")
                # return BusinessResponse(self.random.CreateRandomId(), "VIDEO_CREATED", []).toJson()
                file = request.files["videoFile"]
                try: original_filename = self.verifier.escape_characters(file.filename)
                except: return BusinessResponse(self.random.CreateRandomId(), "ERRROR", [], BusinessError(self.random.CreateRandomId(), "MISSING_FILE")).toJson()
                self.logger.log("INFO", f"Pulling file {original_filename} from request")
                try: 
                    title = request.form["title"]
                    description = self.verifier.escape_characters(request.form["description"])
                    tags = self.verifier.escape_characters(request.form["tags"])
                    categories = self.verifier.escape_characters(request.form["categories"])
                    sub_categories = self.verifier.escape_characters(request.form["sub_categories"])
                    visibility = self.verifier.escape_characters(request.form["visibility"])
                    happy_ends = self.verifier.escape_characters(request.form["happy_ends"])
                    timestamps = self.verifier.escape_characters(request.form["timestamps"])
                    try: free = int(bool(self.verifier.escape_characters(request.form["free"])))
                    except: free = 1
                    try: public = int(bool(self.verifier.escape_characters(request.form["public"])))
                    except: public = 1
                    try: trailer = int(bool(self.verifier.escape_characters(request.form["trailer"])))
                    except: trailer = 0
                    id = self.random.CreateRandomId()
                    self.logger.log("INFO", f"Pulling data from request for new file with id: {id}")
                except Exception as e: return BusinessResponse(self.random.CreateRandomId(), "ERRROR", [], BusinessError(self.random.CreateRandomId(), "CAN_NOT_READ_VIDEO_INFO")).toJson()
                try:
                    self.video_editor.save_video_file(file, id, original_filename, f"{id}.mp4", title, description, categories, sub_categories, tags, visibility, happy_ends, timestamps, userData['id'], free, public, trailer)#session.account_id
                    self.logger.log("INFO", f"Video file and thumnails saved for id: {id}")
                except Exception as e:
                    self.logger.log("ERROR", str(e))
                    return BusinessResponse(self.random.CreateRandomId(), "ERRROR", [], BusinessError(self.random.CreateRandomId(), "CAN_NOT_SAVE_VIDEO")).toJson() 
                return BusinessResponse(self.random.CreateRandomId(), "VIDEO_CREATED", []).toJson()
            self.logger.log("WARNING", f"Accound: {userData['id']} could not create video")
            return BusinessResponse(self.random.CreateRandomId(), "ERRROR", [], BusinessError(self.random.CreateRandomId(), "CAN_NOT_CREATE_VIDEO")).toJson()
        except Exception as e:
            self.logger.log("ERROR", str(e))
            return BusinessResponse(self.random.CreateRandomId(), "ERRROR", [], BusinessError(self.random.CreateRandomId(), "CAN_NOT_CREATE_VIDEO")).toJson()