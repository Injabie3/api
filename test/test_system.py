import glob
import json
import os
from unittest.mock import PropertyMock

import pytest
import injabie3api
from injabie3api import create_app

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class TestShutdownSchedule:
    @pytest.fixture()
    def app(self, mocker):
        app = create_app()
        app.config.update({"TESTING": True, "UPLOAD_FOLDER": f"{DIR_PATH}/cam/"})

        # other setup can go here

        yield app

        # clean up / reset resources here

    @pytest.fixture()
    def client(self, app):
        return app.test_client()

    @pytest.fixture()
    def runner(self, app):
        return app.test_cli_runner()

    def testSystemShutdownScheduleWithNonIntTime(self, client):
        response = client.get("/system/shutdown/schedule/asdf")
        assert response.status_code == 400
        assert "message" in response.json
        assert response.json["message"] == "Please enter a valid time"

    def testSystemShutdownScheduleWithInvalidTime(self, client):
        response = client.get("/system/shutdown/schedule/-1")
        assert response.status_code == 400
        assert "message" in response.json
        assert (
            response.json["message"] == "Please enter a time between 0 and 60 inclusive"
        )

        response = client.get("/system/shutdown/schedule/61")
        assert response.status_code == 400
        assert "message" in response.json
        assert (
            response.json["message"] == "Please enter a time between 0 and 60 inclusive"
        )

    def testSystemShutdownScheduleWithValidTimeInvalidOs(self, mocker, client):
        osName = PropertyMock(return_value="invalidOs")
        mocker.patch("injabie3api.system.shutdown.os", return_value=osName)
        type(injabie3api.system.shutdown.os).name = osName

        response = client.get("/system/shutdown/schedule/10")
        assert response.status_code == 501

    def testSystemShutdownScheduleWithValidTimeLinux(self, mocker, client):
        osName = PropertyMock(return_value="posix")
        mocker.patch("injabie3api.system.shutdown.os", return_value=osName)
        type(injabie3api.system.shutdown.os).name = osName

        mocker.patch("injabie3api.system.shutdown.shutdownLinux", return_value=0)

        response = client.get("/system/shutdown/schedule/10")
        assert response.status_code == 200
        injabie3api.system.shutdown.shutdownLinux.assert_called_with(10)

    def testSystemShutdownScheduleWithValidTimeWindows(self, mocker, client):
        osName = PropertyMock(return_value="nt")
        mocker.patch("injabie3api.system.shutdown.os", return_value=osName)
        type(injabie3api.system.shutdown.os).name = osName

        mocker.patch("injabie3api.system.shutdown.shutdownWindows", return_value=0)
        response = client.get("/system/shutdown/schedule/10")
        assert response.status_code == 200
        injabie3api.system.shutdown.shutdownWindows.assert_called_with(10)

    def testSystemShutdownCancelWithInvalidOs(self, mocker, client):
        osName = PropertyMock(return_value="invalidOs")
        mocker.patch("injabie3api.system.shutdown.os", return_value=osName)
        type(injabie3api.system.shutdown.os).name = osName

        response = client.get("/system/shutdown/cancel")
        assert response.status_code == 501

    def testSystemShutdownCancelWithLinux(self, mocker, client):
        osName = PropertyMock(return_value="posix")
        mocker.patch("injabie3api.system.shutdown.os", return_value=osName)
        type(injabie3api.system.shutdown.os).name = osName

        mocker.patch("injabie3api.system.shutdown.shutdownLinux", return_value=0)
        response = client.get("/system/shutdown/cancel")
        assert response.status_code == 200
        injabie3api.system.shutdown.shutdownLinux.assert_called_with(cancel=True)

    def testSystemShutdownCancelWithWindows(self, mocker, client):
        osName = PropertyMock(return_value="nt")
        mocker.patch("injabie3api.system.shutdown.os", return_value=osName)
        type(injabie3api.system.shutdown.os).name = osName

        mocker.patch("injabie3api.system.shutdown.shutdownWindows", return_value=0)
        response = client.get("/system/shutdown/cancel")
        assert response.status_code == 200
        injabie3api.system.shutdown.shutdownWindows.assert_called_with(cancel=True)
