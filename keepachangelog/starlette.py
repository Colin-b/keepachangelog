from typing import Callable

from starlette.responses import JSONResponse

from keepachangelog._changelog import to_dict


def changelog_endpoint(changelog_path: str) -> Callable:
    """
    Create /changelog: Changelog endpoint parsing https://keepachangelog.com/en/1.0.0/

    :param changelog_path: Path to CHANGELOG.md.
    :returns: The endpoint to add as a route.
    """

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

    return changelog
