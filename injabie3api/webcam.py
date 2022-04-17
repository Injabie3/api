
import glob
from pathlib import Path
import os

from flask import Flask, send_file as sendFile
from flask_restx import Api, Resource, Namespace

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.utils import secure_filename as secureFilename

ALLOWED_EXTENSIONS = [ "png", "jpg", "jpeg" ]
UPLOAD_FOLDER = "/home/pi/git/webcam/webcam/images/"

api = Namespace("webcam", description="Webcam related operations") 

uploadParser = api.parser()
uploadParser.add_argument('image', location='files',
                                   type=FileStorage, required=True,
                                   help="The image to upload.")

@api.route("/<camName>")
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

    @api.doc(responses={200: "Camera found", 404: "Camera not found"})
    def get(self, camName: str):
        """Get the latest webcam image

        Parameters
        ----------
        camName: The webcam name.
        """

        camName = secureFilename(camName)
        listOfFiles = glob.glob(
                app.config["UPLOAD_FOLDER"] + "{}/*".format(camName))
        if listOfFiles:
            latestFile = max(listOfFiles, key=os.path.getctime)
            return sendFile(latestFile)
        raise NotFound("Camera not found")
