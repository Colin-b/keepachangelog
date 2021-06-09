class InvalidSemanticVersion(Exception):
    def __init__(self, version: str):
        super().__init__(
            f"{version} is not following semantic versioning. Check https://semver.org for more information."
        )


class UnmatchingSemanticVersion(Exception):
    def __init__(self, version: str, semantic_version: dict):
        super().__init__(
            f"Semantic version {semantic_version} does not match version {version}."
        )
