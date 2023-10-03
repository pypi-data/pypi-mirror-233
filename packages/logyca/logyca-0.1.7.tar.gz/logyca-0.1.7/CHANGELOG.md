# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

## [0.1.7] - 2023-10-02
### Fixed
- The url address for the logyca logo is corrected
- Adjust return code for LogycaStatusEnum class: LogycaStatusEnum.Created==HTTPStatus.CREATED
- Adjust return code for LogycaStatusEnum class: LogycaStatusEnum.InProcess==HTTPStatus.ACCEPTED
- Adjust return code for LogycaStatusEnum class: LogycaStatusEnum.Partial==HTTPStatus.ACCEPTED
- Empty files __init__.py removed

## [0.1.6] - 2023-09-11
### Fixed
- Pydantic restriction for versions lower than 2.0 is removed

## [0.1.5] - 2023-03-27
### Fixed
- Release ready for production

