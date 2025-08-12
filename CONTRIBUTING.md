# Contributing

We welcome contributions to this project! Please follow these guidelines to ensure smooth collaboration.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/project-name.git
cd project-name

# Install in development mode
pip install -e ".[dev]"

# Or install specific dependencies
pip install -e .
pip install pytest black ruff bandit[toml] safety build
```

## Commit Message Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automatic versioning and changelog generation. All commits must follow this format:

```
<type>: <description>

[optional body]

[optional footer]
```

**Commit Types:**
- `fix:` - Bug fixes (patch version bump: 0.1.0 → 0.1.1)
- `feat:` - New features (minor version bump: 0.1.0 → 0.2.0)
- `feat!:` or `BREAKING CHANGE:` - Breaking changes (major version bump: 0.x.x → 1.0.0)
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring without feature changes
- `test:` - Adding or modifying tests
- `chore:` - Maintenance tasks, dependency updates

**Examples:**
```bash
# Patch release (0.1.0 → 0.1.1)
git commit -m "fix: resolve connection timeout issue"

# Minor release (0.1.0 → 0.2.0)
git commit -m "feat: add new configuration option"

# Major release (0.x.x → 1.0.0)
git commit -m "feat!: stable v1.0.0 API release

BREAKING CHANGE: Official stable release with finalized public API."
```

## Pre-Submission Checklist

Before submitting your changes, ensure your code passes all local checks:

```bash
# 1. Format your code with Black
black .

# 2. Check for linting issues with Ruff
ruff check .

# 3. Run security scan with Bandit
bandit -r src/

# 4. Check for known vulnerabilities with Safety
safety check

# 5. Scan for secrets with TruffleHog
trufflehog git file://. --only-verified

# 6. Run the test suite
pytest

# 7. Run with coverage (optional)
pytest --cov=src --cov-report=html
```

**Quick validation script:**
```bash
# Run all pre-submission checks in sequence
black . && ruff check . && bandit -r src/ && safety check && trufflehog git file://. --only-verified && pytest && echo "✅ Ready for submission!"
```

## CI/CD Pipeline Overview

When you open a pull request, our CI/CD pipeline automatically runs several checks:

**Automated Checks (all must pass):**
1. **Commit Lint**: Validates all commit messages follow conventional format
2. **Code Quality & Security**: 
   - Black formatting check (no auto-fixing in CI)
   - Ruff linting for style and potential errors
   - Bandit security scanning for common vulnerabilities
   - Safety dependency vulnerability checks
   - TruffleHog secret scanning for exposed credentials
3. **Tests**: 
   - Matrix testing across Python versions
   - Comprehensive test suite execution
   - Integration and unit tests
4. **Build**: Validates package can be built successfully

**What to Expect:**
- ✅ **Green checks**: Your PR is ready for review
- ❌ **Red checks**: Review the failed job logs and fix issues
- 🟡 **Yellow checks**: Jobs are still running (be patient)

**Common CI Failures and Fixes:**
```bash
# Commit message format issues
git commit --amend -m "feat: your proper commit message"

# Code formatting issues  
black .

# Linting issues
ruff check . --fix

# Security issues (review and fix manually)
bandit -r src/ -v  # Verbose output for details

# Dependency vulnerabilities (update dependencies)
safety check --full-report
pip install --upgrade package-name

# Secret detection (remove or secure secrets)
trufflehog git file://. --debug  # Detailed output
# Remove secrets from code and git history if found

# Test failures
pytest -v  # Run locally to debug
```

## Pull Request Process

1. **Create Feature Branch:**
   ```bash
   git checkout -b feat/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make Your Changes:**
   - Write clean, well-documented code
   - Add tests for new functionality
   - Follow existing code patterns and conventions

3. **Validate Locally:**
   ```bash
   # Run the pre-submission checklist above
   black . && ruff check . && bandit -r src/ && safety check && trufflehog git file://. --only-verified && pytest
   ```

4. **Commit and Push:**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feat/your-feature-name
   ```

5. **Open Pull Request:**
   - Target the `master` branch
   - Provide clear description of changes
   - Link any relevant issues
   - Wait for CI checks to pass

## Release Process

Releases are fully automated via semantic-release:
- **Merge to master** → Automatic version bump and GitHub release
- **Version bumping** is based on conventional commit messages
- **Changelog** is auto-generated
- **Git tags** are created automatically (format: `v1.2.3`)

## Local Development Tips

**Environment Variables for Testing:**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Set custom test configuration (if applicable)
export TEST_CONFIG=local
```

**Security Tools Installation:**
```bash
# Install TruffleHog (requires Go or use Docker)
# Option 1: Install with Go
go install github.com/trufflesecurity/trufflehog/v3@latest

# Option 2: Use Docker (no local installation needed)
alias trufflehog='docker run --rm -v "$(pwd):/pwd" trufflesecurity/trufflehog:latest'

# Option 3: Download binary from GitHub releases
# https://github.com/trufflesecurity/trufflehog/releases
```

**Run Specific Test Categories:**
```bash
pytest tests/unit/        # Unit tests only
pytest tests/integration/ # Integration tests only  
pytest -k "test_name"     # Run specific test pattern
pytest -v                 # Verbose output
```

## Getting Help

- Check existing [issues](https://github.com/your-username/project-name/issues) for common problems
- Review the [CLAUDE.md](./CLAUDE.md) file for detailed development guidance
- Open a new issue for bugs or feature requests

Thank you for contributing! 🚀