# CLAUDE.md

This file provides guidance to Claude Code when working with the MQTT Connector repository - a Python package for robust MQTT communication with asyncio support.

## Project Overview

**mqtt-connector** is a lightweight, robust Python package that provides asynchronous MQTT communication capabilities with automatic reconnection, message throttling, and SSL/TLS support. It's part of the larger ICSIA project ecosystem.

### Key Features
- Asynchronous API using Python's asyncio
- Automatic reconnection handling with configurable intervals and retry limits
- Message throttling to prevent broker flooding
- SSL/TLS encryption support with certificate verification options
- Authentication support (username/password)
- JSON and string message publishing
- Customizable logging via callback functions
- Context manager support for automatic connection management
- Quality of Service (QoS) levels 0, 1, and 2

## Architecture

### Core Components

**MqttConnector** (`src/mqtt_connector/connector.py:13`): Main class providing:
- Connection management with auto-reconnection (`connect()`, `disconnect()`)
- Message publishing with throttling (`publish()`)
- Topic subscription (`subscribe()`)
- SSL/TLS configuration (`_setup_client()`)
- Logging and callback systems

### Dependencies
- **paho-mqtt>=2.0.0**: Core MQTT client functionality
- **asyncio-mqtt>=0.12.0**: Async wrapper for MQTT operations

## Development Commands

### Environment Setup
```bash
# Install in development mode
pip install -e ".[dev]"

# Or install specific dependencies
pip install -e .
pip install pytest pytest-asyncio black ruff bandit[toml] pip-audit build
```

### Testing
The project uses **integration-first testing** with real MQTT brokers:

```bash
# Run all tests (requires internet for external broker)
pytest

# Run only local broker tests (faster)
pytest -m "not external"

# Run with coverage
pytest --cov=src/mqtt_connector --cov-report=html

# Run specific test categories
pytest -m ssl          # SSL/TLS tests
pytest -m integration  # Integration tests
pytest -m local        # Local broker tests
pytest -m external     # External broker tests
```

**Important**: Tests use `test.mosquitto.org` for SSL/authentication tests and can use local broker via environment variables.

### Code Quality & Security
```bash
# Format code
black .

# Lint code  
ruff check .

# Security scan for vulnerabilities
bandit -r src/

# Check dependencies for known vulnerabilities
pip-audit

# Scan for secrets and credentials
trufflehog git file://. --only-verified

# Type checking (if enabled)
mypy src/
```

### Building
```bash
# Build package
python -m build

# Install locally
pip install -e .
```

## Configuration

### Environment Variables
Tests and examples respect these environment variables:
- `MQTT_BROKER_HOST`: Broker hostname (default: "test.mosquitto.org")
- `MQTT_BROKER_PORT`: Broker port (default: "1883")
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### MQTT Broker Testing Strategy
- **Local tests**: Use environment variables or local Mosquitto broker (CI uses Docker)
- **SSL tests**: Always use `test.mosquitto.org:8885` with authentication (`rw`/`readwrite`)
- **CI**: Uses `namoshek/mosquitto-github-action` for local broker setup

## CI/CD Pipeline

### GitHub Actions Workflows

The project uses two GitHub Actions workflows for comprehensive CI/CD automation:

#### Main CI Pipeline (`.github/workflows/default.yml`)
Triggers on pull requests to `master`, `main`, or `maint` branches and manual workflow dispatch.

**Workflow Features:**
- **Concurrency Control**: Cancels previous runs when new commits are pushed to the same PR
- **Parallel Job Execution**: All jobs run concurrently where possible for speed
- **Comprehensive Testing**: Full matrix testing across Python versions with real MQTT broker

**Jobs:**
1. **commitlint** (`ubuntu-latest`):
   - Validates all commits in PR follow conventional commit format
   - Uses `@commitlint/config-conventional` and `@commitlint/cli`
   - Validates from first commit to PR head with `--verbose` output

2. **code-quality** (`ubuntu-latest`):
   - **Black**: Checks code formatting with `--check --diff` (no auto-fixing)
   - **Ruff**: Lints code for style and error detection
   - **Bandit**: Scans for common security vulnerabilities in Python code
   - **pip-audit**: Checks dependencies for known security vulnerabilities
   - **TruffleHog**: Scans for exposed secrets and credentials in code and git history
   - Uses Python 3.11 for consistency

3. **test** (`ubuntu-latest`, Python 3.8-3.12 matrix):
   - **MQTT Broker Setup**: Spins up Mosquitto 2.0 container on port 1883 using `namoshek/mosquitto-github-action`
   - **Broker Verification**: Waits up to 30s for broker accessibility, shows container status and logs
   - **Test Execution**: Runs `pytest -v --tb=short --maxfail=5 -x` with 600s timeout protection
   - **Environment**: Sets `MQTT_BROKER_HOST=localhost`, `MQTT_BROKER_PORT=1883`, `PYTEST_TIMEOUT=30`
   - **Fail-Fast Strategy**: Stops matrix on first Python version failure

4. **build** (`ubuntu-latest`):
   - Builds Python wheel/sdist packages using `python -m build`
   - Validates packages with `twine check dist/*`
   - Uploads artifacts as `python-package-distributions`

#### Release Pipeline (`.github/workflows/release.yml`)
Triggers on pushes to `master`/`main`/`maint` branches and manual dispatch.

**Workflow Features:**
- **Semantic Release Integration**: Fully automated versioning and releases
- **Conditional Execution**: Only builds/publishes if semantic-release creates new version
- **GitHub Release Creation**: Automatic release notes and asset uploads

**Jobs:**
1. **semantic-release** (`ubuntu-latest`):
   - **Commit Analysis**: Uses `python-semantic-release` to analyze conventional commits
   - **Version Bump**: Automatically updates version in `src/mqtt_connector/__init__.py:__version__`
   - **Changelog Generation**: Updates `CHANGELOG.md` with new entries
   - **GitHub Release**: Creates release with auto-generated notes using `upload_to_vcs_release = true`
   - **Tag Creation**: Creates git tags in format `v{version}` (e.g., `v0.1.1`)
   - **Output Variables**: Sets `released`, `version`, and `tag` for downstream jobs

2. **build-and-publish** (`ubuntu-latest`, conditional on release):
   - **Conditional Execution**: Only runs if `semantic-release.outputs.released == 'true'`
   - **Source Checkout**: Checks out specific release tag for consistency
   - **Package Building**: Creates wheel and sdist distributions
   - **Package Verification**: Validates packages with `twine check`
   - **Artifact Upload**: Uploads with version-specific naming
   - **PyPI Publishing**: Automatic deployment using GitHub Trusted Publishers (no API tokens required)

### Branch Protection Strategy

Required status checks for protected branches (`master`, `maint`):
- `commitlint`: Ensures commit message quality
- `code-quality`: Guarantees code formatting, linting standards, and security
- `test (3.8, ubuntu-latest)` through `test (3.12, ubuntu-latest)`: Full Python compatibility
- `build`: Verifies package can be built successfully

**Merge Requirements:**
- All required checks must pass
- At least one approval (if configured)
- Up-to-date branch with base branch

### How to Use the CI/CD Pipeline

#### For Contributors:
1. **Feature Development**:
   ```bash
   # Create feature branch
   git checkout -b feat/new-feature
   
   # Make changes following code style and security standards
   black .
   ruff check .
   bandit -r src/
   pip-audit
   trufflehog git file://. --only-verified
   pytest
   
   # Commit with conventional format
   git commit -m "feat: add SSL certificate validation"
   ```

2. **Pull Request Process**:
   - Open PR to `master` branch
   - CI runs automatically on PR creation/updates  
   - Fix any failing checks (formatting, linting, tests)
   - All matrix jobs must pass before merge

3. **Code Quality & Security Fixes**:
   ```bash
   # Fix Black formatting issues
   black .
   
   # Fix Ruff linting issues
   ruff check . --fix
   
   # Check for security vulnerabilities
   bandit -r src/
   
   # Check dependencies for vulnerabilities
   pip-audit
   
   # Scan for exposed secrets
   trufflehog git file://. --only-verified
   
   # Run local tests before pushing
   pytest -m "not external"  # Skip external broker tests
   ```

#### For Maintainers:
1. **Merge Process**:
   - Ensure all required checks pass
   - Use "Squash and merge" for clean history
   - Maintain conventional commit format in merge commit

2. **Release Process** (Automatic):
   - Merge to `master` triggers release workflow
   - Semantic-release analyzes commits since last release
   - If releasable commits found:
     - Version is bumped automatically
     - `CHANGELOG.md` is updated
     - Git tag is created
     - GitHub release is published
     - Build artifacts are uploaded

3. **Manual Release Trigger**:
   - Use "Run workflow" button in GitHub Actions tab
   - Select `release.yml` workflow
   - Useful for re-running failed releases

#### Understanding Release Types:
```bash
# Patch release (0.1.0 → 0.1.1) - Bug fixes
fix: resolve connection timeout issue
fix: handle SSL certificate errors properly

# Minor release (0.1.0 → 0.2.0) - New features
feat: add message throttling capability
feat: support QoS level configuration

# Major release (0.x.x → 1.0.0) - Breaking changes
feat!: redesign connection API

BREAKING CHANGE: Connection method signature has changed.
```

#### Troubleshooting CI Failures:

**Commitlint Failures**:
- Fix commit message format: `type: description`
- Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Use `git commit --amend -m "feat: new message"` to fix

**Code Quality Failures**:
- Run `black .` to auto-format
- Run `ruff check . --fix` to auto-fix linting issues
- Check output for manual fixes needed

**Security Scan Failures**:
- Run `bandit -r src/ -v` for detailed vulnerability information
- Review and fix security issues manually (never ignore without justification)
- Run `pip-audit --format=json` to see detailed vulnerability reports
- Update vulnerable dependencies: `pip install --upgrade package-name`

**Secret Detection Failures**:
- Run `trufflehog git file://. --debug` for detailed secret detection information
- **CRITICAL**: Never ignore secret detection failures - always investigate
- Remove secrets from code immediately and consider them compromised
- Use environment variables or secure vaults for credentials
- If secrets are in git history, consider cleaning git history or rotating credentials

**Test Failures**:
- Check if MQTT broker is accessible locally
- Use `LOG_LEVEL=DEBUG pytest` for detailed logging
- Run specific failing tests: `pytest tests/test_connector.py::test_name -v`

**Build Failures**:
- Ensure `pyproject.toml` is valid
- Check for import errors in package structure
- Verify version format in `__init__.py`

**Release Failures**:
- Ensure conventional commit format for all commits
- Check semantic-release configuration in `pyproject.toml`
- Verify GitHub token has sufficient permissions

## Semantic Versioning

Uses **python-semantic-release** with conventional commits:

### Commit Message Format
```bash
# Patch release (0.1.0 → 0.1.1)
fix: handle connection timeout properly

# Minor release (0.1.0 → 0.2.0)  
feat: add SSL certificate validation

# Major release (0.x.x → 1.0.0)
feat!: stable v1.0.0 API release

BREAKING CHANGE: Official stable release with finalized public API.
```

### Configuration
- Version variable: `src/mqtt_connector/__init__.py:__version__`
- Changelog: Auto-generated `CHANGELOG.md`
- Releases: Automatic GitHub releases with notes
- Tags: Format `v{version}` (e.g., `v0.1.1`)

## Common Development Tasks

### Running Examples
```bash
cd examples
python basic_usage.py

# With debug logging
LOG_LEVEL=DEBUG python basic_usage.py
```

### Creating Tests
- Use `pytest.mark.asyncio` for async tests
- Use `mqtt_connector` fixture for basic tests
- Use `ssl_auth_mqtt_connector` fixture for SSL tests
- Generate unique client IDs and topics to avoid conflicts
- Mark tests appropriately: `@pytest.mark.ssl`, `@pytest.mark.external`

### Testing Locally vs CI
```python
# Tests adapt to environment:
mqtt_host = os.getenv("MQTT_BROKER_HOST", "test.mosquitto.org")
mqtt_port = int(os.getenv("MQTT_BROKER_PORT", "1883"))

# CI sets: MQTT_BROKER_HOST=localhost MQTT_BROKER_PORT=1883
# Local dev can override or use defaults
```

### Adding Features
1. Implement in `src/mqtt_connector/connector.py`
2. Add comprehensive tests in `tests/test_connector.py`
3. Update documentation in `README.md`
4. Use conventional commit format
5. Run code quality and security checks: `black . && ruff check . && bandit -r src/ && pip-audit`
6. Ensure all tests pass: `pytest`

## Repository Structure
```
mqtt-connector/
├── src/mqtt_connector/          # Main package
│   ├── __init__.py              # Version and exports
│   └── connector.py             # Core MqttConnector class
├── tests/                       # Comprehensive test suite
│   ├── __init__.py
│   └── test_connector.py        # Integration tests with real brokers
├── examples/                    # Usage examples
│   └── basic_usage.py
├── .github/workflows/           # CI/CD pipelines
│   ├── default.yml              # Main CI workflow
│   └── release.yml              # Automated releases
├── .ci/                         # CI configuration
│   └── mosquitto.conf           # MQTT broker config for testing
├── pyproject.toml               # Build config, tool settings, semantic-release
├── renovate.json                # Dependency management
├── README.md                    # Usage documentation
├── CHANGELOG.md                 # Auto-generated changelog
├── TODO.md                      # CI/CD enhancement roadmap
└── REPO-TODO.md                 # Repository configuration guide
```

## Troubleshooting

### Test Failures
- **MQTT connection issues**: Check broker availability, use `LOG_LEVEL=DEBUG`
- **SSL test failures**: Verify `test.mosquitto.org:8885` accessibility
- **Throttling test failures**: May need timing adjustments for slow systems
- **CI broker issues**: Check if Mosquitto action is configured correctly

### Development Issues
- **Import errors**: Ensure `pip install -e .` was run
- **Missing dependencies**: Run `pip install -e ".[dev]"`
- **Linting failures**: Run `black .` to auto-format, then `ruff check .`

### Release Issues
- **Semantic-release failures**: Ensure conventional commit format
- **Tag conflicts**: May need to clean remote tags manually
- **Changelog not updating**: Check semantic-release configuration in `pyproject.toml`

## Integration with ICSIA Ecosystem

This package is designed as a low-level component for higher-level ICSIA packages:
- **mqtt-application**: Uses mqtt-connector for application framework
- **mqtt-logger**: May depend on mqtt-connector for log transport
- **dummy-icsia**: Example applications using the connector

When making changes, consider impact on dependent packages and maintain backward compatibility.

## Best Practices

### Code Style
- Follow Black formatting (88 character line length)
- Use async/await consistently
- Add type hints where beneficial
- Include comprehensive docstrings
- Handle exceptions gracefully with logging

### Testing
- Test both success and failure scenarios
- Use real MQTT brokers for integration testing
- Include SSL/TLS and authentication testing
- Test all QoS levels and message formats
- Verify automatic reconnection behavior

### Commits
- Use conventional commit format strictly
- Write clear, descriptive commit messages
- Include breaking change notes when applicable
- Reference issues/PRs when relevant

### Security
- Never commit credentials or certificates
- Use environment variables for configuration
- Test SSL certificate verification paths
- Handle authentication failures gracefully