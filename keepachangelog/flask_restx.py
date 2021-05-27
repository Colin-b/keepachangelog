from typing import Union

import flask_restx
import flask

from keepachangelog._changelog import to_dict


def add_changelog_endpoint(
    namespace: Union[flask_restx.Namespace, flask_restx.Api], changelog_path: str
):
    """
    Create /changelog: Changelog endpoint parsing https://keepachangelog.com/en/1.0.0/

    :param namespace: The Flask-RestX namespace.
    :param changelog_path: Path to CHANGELOG.md.
    """

    @namespace.route("/changelog")
    @namespace.doc(
        responses={
            200: (
                "Service changelog.",
                [
                    namespace.model(
                        "ChangelogReleaseModel",
                        {
                            "metadata": namespace.model(
                                "ChangelogReleaseMetaDataModel",
                                {
                                    "version": flask_restx.fields.String(
                                        description="Release version following semantic versioning.",
                                        required=True,
                                        example="3.12.5",
                                    ),
                                    "release_date": flask_restx.fields.Date(
                                        description="Release date.",
                                        required=True,
                                        example="2019-12-31",
                                    ),
                                },
                            ),
                            "added": flask_restx.fields.List(
                                flask_restx.fields.String(description="New features.")
                            ),
                            "changed": flask_restx.fields.List(
                                flask_restx.fields.String(
                                    description="Changes in existing functionaliy."
                                )
                            ),
                            "deprecated": flask_restx.fields.List(
                                flask_restx.fields.String(
                                    description="Soon-to-be removed features."
                                )
                            ),
                            "removed": flask_restx.fields.List(
                                flask_restx.fields.String(
                                    description="Removed features."
                                )
                            ),
                            "fixed": flask_restx.fields.List(
                                flask_restx.fields.String(description="Any bug fixes.")
                            ),
                            "security": flask_restx.fields.List(
                                flask_restx.fields.String(
                                    description="Vulnerabilities."
                                )
                            ),
                        },
                    )
                ],
            )
        }
    )
    class Changelog(flask_restx.Resource):
        def get(self):
            """
            Retrieve service changelog.
            """
            try:
                return flask.jsonify(to_dict(changelog_path))
            except FileNotFoundError:
                return flask.jsonify({})
