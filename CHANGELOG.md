# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- `keepachangelog.to_dict` now contains `url` key for each item if a link is available for the version.

## [0.5.0] - 2021-04-19
### Added
- `keepachangelog.release` function to guess new version number based on `Unreleased` section, update changelog and return new version number.
- `keepachangelog.to_raw_dict` function returning a raw markdown description of the release under `raw` dict.

### Fixed
- Handle any category name.
- Add more flexibility for release format.

### Changed
- `Unreleased` is now reported as lower cased `unreleased`.

## [0.4.0] - 2020-09-21
### Added
- `keepachangelog.flask_restx.add_changelog_endpoint` function to add a changelog endpoint to a [Flask-RestX](https://flask-restx.readthedocs.io/en/latest/) application.

## [0.3.1] - 2020-07-13
### Fixed
- Keep star character at the end of a line as it can be used to mark as italic.

## [0.3.0] - 2020-03-01
### Changed
- Information is now stored without star, space or caret at start or end of line.

## [0.2.0] - 2020-02-24
### Added
- It is now possible to retrieve "Unreleased" information thanks to the `show_unreleased` parameter. (Thanks [Alessandro Ogier](https://github.com/aogier))

## [0.1.0] - 2020-02-17
### Added
- `keepachangelog.starlette.add_changelog_endpoint` function to add a changelog endpoint to a [Starlette](https://www.starlette.io) application.

## [0.0.1] - 2020-02-17
### Added
- Initial release.

[Unreleased]: https://github.com/Colin-b/keepachangelog/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/Colin-b/keepachangelog/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/Colin-b/keepachangelog/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/Colin-b/keepachangelog/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/Colin-b/keepachangelog/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Colin-b/keepachangelog/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Colin-b/keepachangelog/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/Colin-b/keepachangelog/releases/tag/v0.0.1
