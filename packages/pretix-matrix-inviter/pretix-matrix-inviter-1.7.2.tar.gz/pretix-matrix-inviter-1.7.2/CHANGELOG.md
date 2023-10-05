# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.7.2] - 2023-10-04
### Changed
- Move to pyproject.toml

## [1.7.1] - 2023-10-04
### Fixed
- Schedule tasks only after DB transactions are committed

## [1.7.0] - 2023-02-09
### Added
- Matrix ID Parameter for the PDF editor #12

## [1.6.0] - 2023-02-09
### Changed
- Apply updated pretix plugin cookiecutter
- Django 4 compatibility #14
- Minor translation updates
- Don't activate plugin by default

## [1.5.0] - 2022-10-09
### Added
- Allow inviting participants to multiple Matrix rooms

## [1.4.1] - 2022-05-26
### Fixed
- Syntax fix

## [1.4.0] - 2022-05-26
### Added
- Kick Matrix ID from cancelled orders #9

### Fixed
- Allow lowercase server names only #11

## [1.3.0] - 2022-04-19
### Added
- Invite Matrix ID on Order update #7

## [1.2.3] - 2022-04-15
### Fixed
- Adapt to django_scopes

## [1.2.2] - 2022-02-11
### Fixed
- Pypi won't take a new classifier

## [1.2.1] - 2022-02-11
### Fixed
- Don't crash when the configuration is empty
- Make some wording more consistent
- Better adhere to Pretix settings view styles

## [1.2.0] - 2022-02-11
### Added
- Help in the configuration panel
- French translation
- German and German informal translations

## [1.1.0] - 2022-02-08
### Added
- Make Matrix ID field help text configurable
- Add configurable reason to Matrix invitation
- Allow using a room alias anstead of a room ID

### Fixed
- Respect backoff time given by API on retry
- Properly quote user-supplied URL parts

## [1.0.0] - 2022-02-04
### Added
- Configuration panel
- Ask for Matrix ID in selected products
- Invite Pretix participants to configured Matrix room

<!-- markdownlint-disable-file MD022-->
<!-- markdownlint-disable-file MD024-->
<!-- markdownlint-disable-file MD032-->

[1.7.2]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.7.1...v1.7.2
[1.7.1]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.7.0...v1.7.1
[1.7.0]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.6.0...v1.7.0
[1.6.0]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.5.0...v1.6.0
[1.5.0]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.4.1...v1.5.0
[1.4.1]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.4.0...v1.4.1
[1.4.0]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.3.0...v1.4.0
[1.3.0]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.2.3...v1.3.0
[1.2.3]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.2.2...v1.2.3
[1.2.2]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.2.1...v1.2.2
[1.2.1]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.2.0...v1.2.1
[1.2.0]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.1.0...v1.2.0
[1.1.0]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/compare/v1.0.0...v1.1.0
[1.0.0]: https://gitlab.fachschaften.org/kif/pretix-matrix-inviter/-/tags/v1.0.0
