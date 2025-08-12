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
pip install pytest pytest-asyncio black ruff build
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

### Code Quality
```bash
# Format code
black .

# Lint code  
ruff check .

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
- **`.github/workflows/default.yml`**: Main CI pipeline (commitlint, code quality, tests, build)
- **`.github/workflows/release.yml`**: Automated releases with semantic-release

### Workflow Jobs
1. **commitlint**: Validates conventional commit messages
2. **code-quality**: Runs Black and Ruff
3. **test**: Matrix testing across Python 3.8-3.12 with MQTT broker
4. **build**: Creates Python packages

### Branch Protection
Required status checks for `master` and `maint` branches:
- `commitlint`
- `code-quality` 
- `test (3.8, ubuntu-latest)` through `test (3.12, ubuntu-latest)`
- `build`

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
5. Run code quality checks: `black . && ruff check .`
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