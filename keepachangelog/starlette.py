from starlette.applications import Starlette
from starlette.responses import JSONResponse

from keepachangelog._changelog import to_dict


def add_changelog_endpoint(app: Starlette, changelog_path: str):
    """
    Create /changelog: Changelog endpoint parsing https://keepachangelog.com/en/1.0.0/

    :param app: The ASGI application.
    :param changelog_path: Path to CHANGELOG.md.
    """

    @app.route("/changelog")
    async def changelog(request):
        """
        responses:
            200:
                description: "Service changelog."
                schema:
                    type: object
        summary: "Retrieve service changelog"
        operationId: get_changelog
        tags:
            - Monitoring
        """
        try:
            return JSONResponse(to_dict(changelog_path))
        except FileNotFoundError:
            return JSONResponse({})
