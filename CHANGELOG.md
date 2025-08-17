# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- version list -->

## v1.1.6 (2025-08-17)

### Bug Fixes

- Remove end of file empty line
  ([`9d75c68`](https://github.com/muxu-io/mqtt-connector/commit/9d75c684072153d721345962a12fc218198da06d))


## v1.1.5 (2025-08-17)

### Bug Fixes

- Use local pypi publish workflow
  ([`8416b96`](https://github.com/muxu-io/mqtt-connector/commit/8416b96cad41759357aee33ad2708dee06eed7ab))


## v1.1.4 (2025-08-17)

### Bug Fixes

- Add version to publish job
  ([`df1408b`](https://github.com/muxu-io/mqtt-connector/commit/df1408bae5e133ff06e53f74b631101ae02cd30d))


## v1.1.3 (2025-08-17)

### Bug Fixes

- Rename CI job
  ([`e0a82c7`](https://github.com/muxu-io/mqtt-connector/commit/e0a82c78a5d92972642abec7b9d4489bb74edf73))


## v1.1.2 (2025-08-17)

### Bug Fixes

- Reusable workflows
  ([`519d989`](https://github.com/muxu-io/mqtt-connector/commit/519d9897752965aa916420d747e6d513cb990da5))


## v1.1.1 (2025-08-17)

### Bug Fixes

- More reusable workflows fixes
  ([`58facb3`](https://github.com/muxu-io/mqtt-connector/commit/58facb386afa4ebf1520b88ea6047c8460af094f))


## v1.1.0 (2025-08-17)

### Bug Fixes

- Move ci configuration to .github
  ([`f796ee5`](https://github.com/muxu-io/mqtt-connector/commit/f796ee57acfd62fce7f4aa233128a0e5ade8ba44))

### Features

- Use reusable workflows
  ([`a3aa740`](https://github.com/muxu-io/mqtt-connector/commit/a3aa740777d97a8da8ffce65bad4c54e716d50f3))


## v1.0.3 (2025-08-16)

### Bug Fixes

- Update dependencies
  ([`7f2fa4e`](https://github.com/muxu-io/mqtt-connector/commit/7f2fa4e63ecca2943df6b4708f8f93b8c41fd78a))


## v1.0.2 (2025-08-16)

### Bug Fixes

- Use version from pyproject
  ([`fc4fdc4`](https://github.com/muxu-io/mqtt-connector/commit/fc4fdc4ebea23dcd973ab68d5b04f32507910fbc))


## v1.0.1 (2025-08-16)

### Bug Fixes

- Print version information on initial connection
  ([`7d2e15d`](https://github.com/muxu-io/mqtt-connector/commit/7d2e15d7429d332df79fd9fad3abaac5581b713d))


## v1.0.0 (2025-08-16)

### Bug Fixes

- Update the CI/CD workflows
  ([`eb90695`](https://github.com/muxu-io/mqtt-connector/commit/eb906951d888f622d7d453dfd8ab85f7f7475049))


## v0.3.0 (2025-08-16)

### Features

- Implement async callbacks
  ([`093ccd1`](https://github.com/muxu-io/mqtt-connector/commit/093ccd1780e48dfdcc6a266ff8fd8430da04ba74))


## v0.2.1 (2025-08-15)

### Bug Fixes

- Change the project name to match pypi publisher
  ([`bb21f12`](https://github.com/muxu-io/mqtt-connector/commit/bb21f12c620dd11f9538469d74448697a2ba544e))


## v0.2.0 (2025-08-15)

### Features

- Use admin token for semantic release
  ([`8ee4c6e`](https://github.com/muxu-io/mqtt-connector/commit/8ee4c6e63388ef9041e88aba6f9a73effc779d30))

- Workflows: print actor_id for semantic release
  ([`e6a6cff`](https://github.com/muxu-io/mqtt-connector/commit/e6a6cff690a90fd74c478b48fbc15730de5c5094))

- Workflows: print actor_id for semantic release
  ([`d5a858b`](https://github.com/muxu-io/mqtt-connector/commit/d5a858b7c3c47442b752017ec211b4f5c4dd6b9f))

- Workflows: release: add pipy publishing
  ([`484a2c3`](https://github.com/muxu-io/mqtt-connector/commit/484a2c385521ac054ab91774550eb92af2365f0d))


## v0.1.0 (2025-08-13)

- Initial Release

## [Unreleased]

### Added
- Initial implementation of MqttConnector class
- Asynchronous MQTT communication support
- Automatic reconnection handling
- SSL/TLS support with client certificates
- Message throttling functionality
- Comprehensive test suite
- CI/CD build and release pipeline

### Changed
- Project structure with src/ layout
- Modern Python packaging with pyproject.toml

### Fixed
- N/A

## [0.1.0] - 2025-08-12

### Added
- Initial release of mqtt-connector package
- Basic MQTT functionality with paho-mqtt
- Async/await support
- Example usage documentation
