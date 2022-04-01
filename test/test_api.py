import json

import pytest
from injabie3api import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
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


