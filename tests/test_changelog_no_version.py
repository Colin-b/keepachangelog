import os
import os.path

import pytest
from flask import Flask
from flask_restplus import Api

import layab


@pytest.fixture
def changelog():
    changelog_file_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "CHANGELOG.md"
    )

    with open(changelog_file_path, "wt") as file:
        file.write("This is the changelog content.\n")
        file.write("This is the second line.\n")

    yield changelog_file_path
    os.remove(changelog_file_path)


@pytest.fixture
def app(changelog):
    application = Flask(__name__)
    application.testing = True
    api = Api(application, version="3.2.1")

    def pass_details():
        return "pass", {"toto2": {"status": "pass"}}

    layab.add_monitoring_namespace(api, pass_details)
    return application


def test_changelog_without_versions(client):
    response = client.get("/changelog")
    assert response.status_code == 200
    assert response.json == []
