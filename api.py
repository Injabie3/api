#!/usr/bin/env python3
from pathlib import Path
import os

from flask import Flask
from flask_restx import Resource, Api

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename as secureFilename

ALLOWED_EXTENSIONS = [ "png", "jpg", "jpeg" ]
UPLOAD_FOLDER = "/home/pi/git/webcam/webcam/images/"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

uploadParser = api.parser()
uploadParser.add_argument('image', location='files',
                                   type=FileStorage, required=True,
                                   help="The image to upload.")

def isAllowedFilename(filename):
    dotInName = "." in filename
    allowedExtension = filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    return dotInName and allowedExtension


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route("/cam/<camName>")
class Webcam(Resource):
    @api.expect(uploadParser)
    @api.doc(responses={200: "Image successfully uploaded", 400: "Bad request"})
    def post(self, camName: str):
        """Upload a webcam image
        
        Parameters
        ----------
        camName: The webcam name.
        """
        camName = secureFilename(camName)
        args = uploadParser.parse_args()
        image = args["image"]
        if not isAllowedFilename(image.filename):
            raise BadRequest("Bad filename")
        # TODO f-string after moving from Python3.5
        filename = secureFilename(image.filename)
        pathName = app.config["UPLOAD_FOLDER"] + camName
        Path(pathName).mkdir(parents=True, exist_ok=True)
        image.save(os.path.join(pathName, filename))
        return {"message": "Successfully uploaded as {}".format(filename)}, 200

    def get(self, camName: str):
        """Get the latest webcam image

        Parameters
        ----------
        camName: The webcam name.
        """
        pass

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
