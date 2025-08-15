# CI/CD Pipeline Documentation

This directory contains the GitHub Actions workflows that automate testing, code quality checks, security scanning, and releases for the MQTT Connector package.

## Workflows Overview

### 1. Main CI Pipeline (`default.yml`)

**Triggers:** Pull requests to `master`, `main`, or `maint` branches, manual dispatch

**Features:**
- Concurrency control (cancels previous runs on new commits)
- Parallel job execution for optimal performance
- Comprehensive testing across Python versions with real MQTT broker

**Jobs:**

#### `commitlint` (ubuntu-latest)
- Validates conventional commit format using `@commitlint/config-conventional`
- Checks all commits from PR base to head with verbose output
- **Required for merge:** Ensures commit message quality

#### `code-quality` (ubuntu-latest)
- **Black:** Code formatting validation (`--check --diff`)
- **Ruff:** Linting for style and error detection
- **Bandit:** Security vulnerability scanning (`bandit -r src/`)
- **pip-audit:** Dependency vulnerability checking
- **TruffleHog:** Secret detection in code and git history
- **Required for merge:** Guarantees code quality and security standards

#### `test` (ubuntu-latest, Python 3.8-3.12 matrix)
- **MQTT Broker:** Mosquitto 2.0 container via `nameshek/mosquitto-github-action`
- **Test Execution:** `pytest -v --tb=short --maxfail=5 -x` with 600s timeout
- **Environment:** `MQTT_BROKER_HOST=localhost`, `MQTT_BROKER_PORT=1883`
- **Strategy:** Fail-fast on first Python version failure
- **Required for merge:** Full compatibility validation

#### `build` (ubuntu-latest)
- **Package Building:** `python -m build` (wheel + sdist)
- **Package Validation:** `twine check dist/*`
- **Artifact Upload:** `python-package-distributions`
- **Required for merge:** Ensures buildable packages

### 2. Release Pipeline (`release.yml`)

**Triggers:** Pushes to `master`/`main`/`maint` branches, manual dispatch

**Features:**
- Semantic release integration with conventional commits
- Automated versioning and changelog generation
- GitHub release creation with artifacts
- **PyPI publishing via Trusted Publishers**

**Jobs:**

#### `semantic-release` (ubuntu-latest)
- **Commit Analysis:** Uses `python-semantic-release` to analyze conventional commits
- **Version Management:** Updates `src/mqtt_connector/__init__.py:__version__`
- **Changelog:** Auto-generates `CHANGELOG.md` entries
- **GitHub Release:** Creates releases with auto-generated notes
- **Tag Creation:** Git tags in format `v{version}` (e.g., `v0.1.1`)
- **Outputs:** `released`, `version`, `tag` for downstream jobs

#### `build-and-publish` (ubuntu-latest, conditional)
- **Conditional:** Only runs if `semantic-release.outputs.released == 'true'`
- **Source:** Checks out specific release tag for consistency
- **Building:** Creates wheel and sdist distributions
- **Verification:** Validates with `twine check dist/*`
- **Artifacts:** Uploads build artifacts with version naming
- **PyPI Publishing:** Automatic deployment using GitHub Trusted Publishers

## PyPI Publishing Setup

### Trusted Publishers Configuration

The release pipeline uses GitHub's Trusted Publishers feature for secure PyPI publishing:

**Required Setup on PyPI:**
1. Register package at https://pypi.org
2. Navigate to https://pypi.org/manage/account/publishing/
3. Add trusted publisher:
   - **Owner:** `muxu-io` (GitHub organization)
   - **Repository:** `icsia` 
   - **Workflow:** `release.yml`
   - **Environment:** (optional, leave blank)

**Benefits:**
- No API tokens to manage or rotate
- Automatic short-lived token generation by GitHub
- Enhanced security through OIDC authentication
- Simplified workflow configuration

### Package Publishing Process

1. **Trigger:** Push to `master` branch with conventional commits
2. **Analysis:** Semantic-release analyzes commits for version bumps
3. **Release:** If releasable commits found:
   - Version bumped in `__init__.py`
   - `CHANGELOG.md` updated
   - Git tag created (`v{version}`)
   - GitHub release published
4. **Publishing:** Package built, verified, and published to PyPI
5. **Verification:** Package hash printed for integrity checking

## Branch Protection Strategy

### Protected Branches
- `master` (primary)
- `maint` (maintenance)

### Required Status Checks
All checks must pass before merge:
- `commitlint` - Commit message validation
- `code-quality` - Formatting, linting, security
- `test (3.8, ubuntu-latest)` through `test (3.12, ubuntu-latest)` - Full Python compatibility
- `build` - Package build verification

### Merge Requirements
- All required status checks pass
- At least one approval (if configured)
- Branch up-to-date with base branch
- Linear history preferred (squash and merge)

## Workflow Configuration Files

### `.github/workflows/default.yml`
Main CI pipeline for pull requests with comprehensive testing and quality checks.

### `.github/workflows/release.yml`
Automated release pipeline with semantic versioning and PyPI publishing.

### `.ci/mosquitto.conf`
MQTT broker configuration for integration testing in CI environment.

## Environment Variables

### CI/CD Environment
- `MQTT_BROKER_HOST=localhost` - Local broker for CI tests
- `MQTT_BROKER_PORT=1883` - Standard MQTT port
- `PYTEST_TIMEOUT=30` - Test timeout configuration
- `LOG_LEVEL` - Logging verbosity control

### Secrets (GitHub)
- `GITHUB_TOKEN` - Automatic token for repository access
- No PyPI API tokens required (uses Trusted Publishers)

## Semantic Versioning

### Conventional Commit Format
```bash
# Patch release (0.1.0 → 0.1.1) - Bug fixes
fix: handle connection timeout properly
fix: resolve SSL certificate validation issue

# Minor release (0.1.0 → 0.2.0) - New features  
feat: add message throttling capability
feat: support custom SSL context configuration

# Major release (0.x.x → 1.0.0) - Breaking changes
feat!: redesign connection API for stability

BREAKING CHANGE: Connection method signature changed.
```

### Release Artifacts
- **Git Tags:** `v{version}` format (e.g., `v0.1.1`)
- **GitHub Releases:** Auto-generated with changelog
- **PyPI Packages:** Wheel and source distributions
- **Build Artifacts:** Stored for 90 days in GitHub Actions

## Troubleshooting

### Common CI Failures

#### Commitlint Failures
```bash
# Fix commit message format
git commit --amend -m "feat: add new feature description"

# Valid types: feat, fix, docs, style, refactor, test, chore, build, ci
```

#### Code Quality Failures
```bash
# Auto-format code
black .

# Fix linting issues
ruff check . --fix

# Manual security review may be required for Bandit findings
```

#### Test Failures
```bash
# Local debugging
LOG_LEVEL=DEBUG pytest tests/test_connector.py -v

# Check MQTT broker accessibility
telnet test.mosquitto.org 1883
```

#### Build Failures
```bash
# Verify package structure
python -m build
twine check dist/*

# Check version format in __init__.py
```

### Security Considerations

#### Secret Detection
- **Never ignore** TruffleHog failures
- Remove secrets immediately if detected
- Consider credentials compromised if in git history
- Use environment variables for configuration

#### Dependency Vulnerabilities
- Review `pip-audit` findings carefully
- Update vulnerable packages promptly
- Consider security implications of all changes

#### Access Control
- Use least-privilege permissions in workflows
- Monitor PyPI download statistics
- Review GitHub Actions usage regularly

## Monitoring and Maintenance

### Performance Metrics
- **Build Time:** Monitor workflow duration trends
- **Test Coverage:** Review coverage reports in artifacts
- **Success Rate:** Track workflow success/failure ratios

### Regular Maintenance
- **Dependencies:** Monitor Renovate PRs for updates
- **Security:** Review security scan results weekly
- **Performance:** Optimize slow tests or CI steps
- **Documentation:** Keep workflow docs current with changes

### Alerts and Notifications
- **Failed Builds:** GitHub notifications to maintainers
- **Security Issues:** Immediate attention required
- **Release Success:** Monitor PyPI package availability

## Development Workflow Integration

### For Contributors
1. **Branch Creation:** `git checkout -b feat/new-feature`
2. **Development:** Follow code quality standards
3. **Local Testing:** Run tests and quality checks locally
4. **Commit:** Use conventional commit format
5. **Push:** Create pull request to trigger CI
6. **Review:** Address any CI failures

### For Maintainers
1. **PR Review:** Ensure all required checks pass
2. **Merge:** Use squash and merge for clean history
3. **Release:** Automatic on merge to master with releasable commits
4. **Monitor:** Verify successful PyPI publication

This CI/CD pipeline ensures high-quality, secure, and reliable package releases while maintaining developer productivity and code maintainability.