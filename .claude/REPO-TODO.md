# Repository Configuration TODO

This file documents recommended next steps for standardizing CI/CD and repository settings across the ICSIA project repositories.

## Current Status

✅ **Completed for mqtt-connector:**
- GitHub Actions CI workflow (`default.yml`) with commitlint, code quality, tests, and build
- GitHub Actions release workflow (`release.yml`) with semantic-release
- Semantic versioning with automatic changelog generation
- Renovate dependency management configuration
- MQTT broker testing with Docker in CI
- **✅ Security scanning suite integrated:**
  - Bandit for Python security vulnerabilities
  - pip-audit for dependency vulnerability scanning
  - TruffleHog for secret detection
  - Enhanced CI/CD pipeline with comprehensive security reporting

## Pending Repository Configuration

### 1. Branch Protection Rules

**Need to configure via GitHub UI or CLI for each repository:**

Required status checks for `master` and `maint` branches:
- `commit-check` (renamed from commitlint)
- `code-quality` (includes security scanning: Bandit, pip-audit, TruffleHog)
- `test (3.8, ubuntu-latest)`
- `test (3.9, ubuntu-latest)`
- `test (3.10, ubuntu-latest)`
- `test (3.11, ubuntu-latest)`
- `test (3.12, ubuntu-latest)`
- `build`

**GitHub CLI command:**
```bash
gh api repos/muxu-io/mqtt-connector/branches/master/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"checks":[{"context":"commit-check"},{"context":"code-quality"},{"context":"test (3.8, ubuntu-latest)"},{"context":"test (3.9, ubuntu-latest)"},{"context":"test (3.10, ubuntu-latest)"},{"context":"test (3.11, ubuntu-latest)"},{"context":"test (3.12, ubuntu-latest)"},{"context":"build"}]}'' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

### 2. Repository Settings

Configure merge settings:
- ✅ Allow squash merge
- ❌ Disable merge commits
- ❌ Disable rebase merge
- ✅ Delete branches after merge

## Scaling to Other ICSIA Repositories

### Target Repositories:
- `mqtt-application/`
- `mqtt-logger/`
- `dummy-icsia/` (if separate repos)

### Recommended Approach: GitHub CLI + Scripts

**Create a configuration management script:**

```bash
#!/bin/bash
# scripts/apply-repo-settings.sh

REPOS=("mqtt-connector" "mqtt-logger" "mqtt-application")
ORG="muxu-io"

for repo in "${REPOS[@]}"; do
  echo "Configuring $repo..."
  
  # Branch protection for master
  gh api "repos/$ORG/$repo/branches/master/protection" \
    --method PUT \
    --input - <<EOF
{
  "required_status_checks": {
    "strict": true,
    "checks": [
      {"context": "commit-check"},
      {"context": "code-quality"},
      {"context": "test (3.8, ubuntu-latest)"},
      {"context": "test (3.9, ubuntu-latest)"},
      {"context": "test (3.10, ubuntu-latest)"},
      {"context": "test (3.11, ubuntu-latest)"},
      {"context": "test (3.12, ubuntu-latest)"},
      {"context": "build"}
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true
  },
  "restrictions": null
}
EOF

  # Repository settings
  gh api "repos/$ORG/$repo" \
    --method PATCH \
    --field allow_squash_merge=true \
    --field allow_merge_commit=false \
    --field allow_rebase_merge=false \
    --field delete_branch_on_merge=true
    
done
```

### Alternative Approaches:

#### 1. GitHub Organization Templates
- Create `.github` repository in organization
- Add workflow templates in `workflow-templates/`
- Templates appear when creating workflows in any org repository

#### 2. Repository Templates
- Create template repository with complete CI/CD setup
- Mark as "Template repository" in Settings
- Use "Use this template" for new repositories

#### 3. Terraform GitHub Provider
```hcl
variable "repositories" {
  default = ["mqtt-connector", "mqtt-logger", "mqtt-application"]
}

resource "github_branch_protection" "main" {
  for_each = toset(var.repositories)
  
  repository_id = each.value
  pattern       = "master"
  
  required_status_checks {
    strict = true
    checks = [
      "commit-check",
      "code-quality", 
      "test (3.8, ubuntu-latest)",
      "test (3.9, ubuntu-latest)",
      "test (3.10, ubuntu-latest)",
      "test (3.11, ubuntu-latest)",
      "test (3.12, ubuntu-latest)",
      "build"
    ]
  }
  
  required_pull_request_reviews {
    required_approving_review_count = 1
    dismiss_stale_reviews          = true
  }
  
  enforce_admins = true
}
```

#### 4. Reusable Workflows
Create shared workflows that can be called from other repositories:
```yaml
# .github/workflows/reusable-python-ci.yml
on:
  workflow_call:
    inputs:
      python-versions:
        required: false
        type: string
        default: '["3.8", "3.9", "3.10", "3.11", "3.12"]'
```

## File Templates to Copy

### Essential Files for Each Repository:
- `.github/workflows/default.yml` - CI workflow (with security scanning)
- `.github/workflows/release.yml` - Release workflow
- `.ci/mosquitto.conf` - MQTT broker config for testing
- `.commitlintrc.json` - Commitlint configuration
- `renovate.json` - Dependency management
- `pyproject.toml` - Tool configurations (semantic-release, black, ruff, pytest, bandit)
- `CONTRIBUTING.md` - Contributor guidelines with security practices

### Semantic Release Configuration:
```toml
[tool.semantic_release]
version_variable = "src/{package_name}/__init__.py:__version__"
build_command = "python -m build"
upload_to_vcs_release = true
upload_to_repository = false
commit_message = "chore(release): {version}\n\n[skip ci]"
tag_format = "v{version}"
major_on_zero = true

[tool.semantic_release.changelog]
exclude_commit_patterns = [
  '''chore(?:\([^)]*?\))?: .+''',
  '''ci(?:\([^)]*?\))?: .+''',
  '''docs(?:\([^)]*?\))?: .+''',
  '''style(?:\([^)]*?\))?: .+''',
  '''refactor(?:\([^)]*?\))?: .+''',
  '''test(?:\([^)]*?\))?: .+''',
  '''Merge pull request.*''',
  '''Merge branch.*''',
]

[tool.semantic_release.changelog.default_templates]
changelog_file = "CHANGELOG.md"
```

## Action Items

### Immediate:
1. [ ] Configure branch protection rules for mqtt-connector
2. ✅ Test the complete CI/CD pipeline with security scanning
3. [ ] Verify security scanning results and fix any issues

### Short-term:
1. [ ] Apply same CI/CD setup to mqtt-logger
2. [ ] Apply same CI/CD setup to mqtt-application
3. [ ] Create repository configuration script
4. [ ] Document conventional commit standards for the team

### Long-term:
1. [ ] Consider organization-wide templates
2. [ ] Evaluate Terraform for infrastructure as code
3. [ ] Set up monitoring for CI/CD pipeline health

## Conventional Commit Reminders

**Correct format:** `type(scope): description`
- ✅ `fix(ci): changelog generation`
- ❌ `fix (ci): changelog generation` (no space before parentheses)

**Common types:**
- `feat`: New features (minor version bump)
- `fix`: Bug fixes (patch version bump)  
- `perf`: Performance improvements (patch version bump)
- `docs`: Documentation changes
- `ci`: CI/CD changes
- `chore`: Maintenance tasks
- `test`: Test additions/modifications
- `refactor`: Code refactoring

## Security Enhancements Added

### Implemented Security Scanning:
1. **Bandit**: Static security analysis for Python code
   - Scans for common security vulnerabilities (SQL injection, hardcoded secrets, etc.)
   - Generates JSON reports with detailed findings
   - Integrated into code-quality job

2. **pip-audit**: Dependency vulnerability scanning
   - Replaces deprecated Safety tool
   - Checks all installed packages against known CVE database
   - No authentication required, maintained by PyPA

3. **TruffleHog**: Secret detection
   - Scans entire repository for exposed credentials
   - Uses `--only-verified` flag to reduce false positives
   - Full repository scan (not differential)

4. **Setuptools Security Fix**:
   - Updated from vulnerable 65.5.0 to secure >=65.5.1
   - Resolves PYSEC-2022-43012 and partially addresses PYSEC-2025-49
   - Maintains Python 3.8+ compatibility

### Security Workflow Integration:
- Security scans run on every PR and push
- JSON reports generated for automated processing
- Human-readable fallback outputs
- Non-blocking secret scanning with proper error handling
- Comprehensive troubleshooting documentation

## Notes

- All repositories should use Python 3.8+ (3.7 is EOL)
- MQTT tests use local Mosquitto broker in CI with external broker for SSL tests
- Semantic-release automatically manages versions, changelogs, and GitHub releases
- Branch protection prevents merging until all CI checks pass
- Renovate handles dependency updates with auto-merge for patches
- **Security-first approach**: All security scans must pass before merge
- **Zero tolerance for secrets**: TruffleHog failures must be investigated
- **Dependency hygiene**: pip-audit ensures no known vulnerabilities in dependencies
