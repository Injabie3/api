import glob
import json
import os

import pytest
import injabie3api
from injabie3api import create_app

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "UPLOAD_FOLDER": f"{DIR_PATH}/cam/"
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_hello(client):
    response = client.get("/hello")
    assert "hello" in response.json
    assert response.json["hello"] == "world"

def test_get_webcam_non_existent(client):
    response = client.get("/cam/someNonExistentCamera")
    assert response.status_code == 404
    assert "message" in response.json
    assert "Camera not found" in response.json["message"]

def test_get_webcam_existent(client):
    response = client.get("/cam/aCameraThatExists")
    assert response.status_code == 200
    listOfFiles = glob.glob(f"{DIR_PATH}/cam/aCameraThatExists/*")
    latestFile = max(listOfFiles, key=os.path.getctime)
    fileSize = os.path.getsize(latestFile)
    assert fileSize == len(response.data)

def testPostWebcamWithGoodArguments(client):
    fileToUpload=f"{DIR_PATH}/meirochou.jpg"
    response = client.post(
        "/cam/aCameraThatExists",
        data=dict(image=open(fileToUpload,"rb",))
    )
    assert response.status_code == 200
