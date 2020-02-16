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
        file.write(
            """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Enhancement 1
- sub enhancement 1
- sub enhancement 2
- Enhancement 2

### Fixed
- Bug fix 1
- sub bug 1
- sub bug 2
- Bug fix 2

### Security
- Known issue 1
- Known issue 2

### Deprecated
- Deprecated feature 1
- Future removal 2

### Removed
- Deprecated feature 2
- Future removal 1

## [1.1.0] - 2018-05-31

## [1.0.1] - 2018-05-31
### Fixed
- Bug fix 1 (1.0.1)
- sub bug 1
- sub bug 2
- Bug fix 2 (1.0.1)

## [1.0.0] - 2017-04-10
### Deprecated
- Known issue 1 (1.0.0)
- Known issue 2 (1.0.0)
"""
        )
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


def test_changelog_with_versions_and_no_changed(client):
    response = client.get("/changelog")
    assert response.status_code == 200
    assert response.json == [
        {"release_date": "2018-05-31", "version": "1.1.0"},
        {
            "fixed": [
                "- Bug fix 1 (1.0.1)",
                "- sub bug 1",
                "- sub bug 2",
                "- Bug fix 2 (1.0.1)",
            ],
            "release_date": "2018-05-31",
            "version": "1.0.1",
        },
        {
            "deprecated": ["- Known issue 1 (1.0.0)", "- Known issue 2 (1.0.0)"],
            "release_date": "2017-04-10",
            "version": "1.0.0",
        },
    ]
