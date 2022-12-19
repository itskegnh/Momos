import requests
# import BytesIO
from PIL import Image
import base64

ENDPOINT = "https://momos-backend.onrender.com/%s"

class Attachment:
    def __init__(self, filepath):
        # convert the file to: data image or video web
        self.filepath = filepath
        self.filetype = self.filepath.split(".")[-1]
        self.filetype = self.filetype.lower()
        self.filetype = "image" if self.filetype in ["jpg", "jpeg", "png"] else "video"
        self.filetype = "web" if self.filetype not in ["image", "video"] else self.filetype

        self.file = open(self.filepath, "rb").read()
        self.file = base64.b64encode(self.file).decode("utf-8")
    
    def get_data(self):
        return 'data:' + self.filetype + '/mp4;base64,' + self.file
        


class Client:
    def __init__(self, username, password):
        self.credentials = {
            "username": username,
            "password": password,
        }
        self.credentials["token"] = self.login(self.credentials)
    
    def login(self, credentials, verbose=False):
        r = requests.post(ENDPOINT % "auth/login", json=credentials)

        if verbose: return r.json()
        
        if "token" not in r.json():
            raise Exception("Client failed to login!", r.json())
        
        return r.json()["token"]
    
    def create_post(self, content : str, attachment):
        payload = {
            "text": content,
        }

        if attachment is not None:
            payload["filetype"] = attachment.filetype
            payload["imageblob"] = attachment.get_data()

        r = requests.post(ENDPOINT % "newpost", json=payload)
        return r.json()

