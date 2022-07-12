#!/usr/bin/env python3
from flask import Flask, send_file as sendFile
from flask_restx import Api

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.utils import secure_filename as secureFilename

from .constants import UPLOAD_FOLDER
from .webcam import api as webcamNamespace
from .helloworld import api as helloWorldNamespace
from .system import addSystemNamespacesToApi


def createApp(testConfig=None):
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    api = Api(app)

    api.add_namespace(webcamNamespace, path="/cam")
    api.add_namespace(helloWorldNamespace, path="/hello")
    addSystemNamespacesToApi(api)

    return app


def create_app(test_config=None):
    return createApp(testConfig=test_config)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
