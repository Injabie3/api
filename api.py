#!/usr/bin/env python3
import os

from flask import Flask
from flask_restx import Resource, Api
from werkzeug.datastructures import FileStorage
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
    def post(self, camName: str):
        """Upload a webcam image
        
        Parameters
        ----------
        camName: The webcam name.
        """
        args = uploadParser.parse_args()
        image = args["image"]
        if not isAllowedFilename(image.filename):
            return "Bad filename", 500
        # TODO f-string after moving from Python3.5
        filename = secureFilename("{}-{}".format(camName, image.filename))
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
