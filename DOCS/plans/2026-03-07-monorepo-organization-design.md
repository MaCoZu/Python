# Python & Data Science Monorepo Organization Design

**Date:** 2026-03-07
**Status:** Approved

## Overview

Transform the Python learning repository into a comprehensive, well-organized monorepo for data science exploration with professional tooling, efficient dependency management, and reusable utilities following DRY/KISS principles.

## Goals

1. **Comprehensive learning platform** - Cover all major Python/data science topics with clear organization
2. **Efficient dependency management** - Use uv for fast, workspace-based dependency handling
3. **Strict code quality** - Enforce best practices with ruff, mypy, and pre-commit hooks from day one
4. **Reusable utilities** - Build a DRY toolbox of utilities following KISS principles
5. **Scalable structure** - Organize for both current needs and future exploration

## Design Decisions

### 1. Directory Structure

**Approach:** Comprehensive learning platform with flat topic folders

```
Python/
├── pandas/                    # DataFrame manipulation & analysis
├── numpy/                     # Array computing & numerical operations
├── python/                    # Core Python language features
├── sklearn/                   # Machine learning with scikit-learn
├── visualization/             # Plotting libraries
├── statistics/                # Statistical methods & theory
├── sql/                       # SQL & database interactions
├── utils/                     # Reusable utilities package
├── docs/                      # Documentation & planning
│   ├── plans/                # Design documents
│   └── notes/                # Learning notes & references
├── data/                      # Datasets (gitignored)
├── tests/                     # Tests for utils package
├── .github/workflows/        # CI/CD
├── pyproject.toml            # Project config & dependencies
├── uv.lock                   # Locked dependencies
├── Makefile                  # Helper commands
└── README.md
```

**Rationale:**
- Flat topic folders are easy to navigate and understand
- Each topic has a clear home for notebooks and scripts
- Utils package is separate for cross-topic reuse
- Empty folders guide exploration without cluttering
- Professional structure that scales with learning

### 2. Dependency Management

**Approach:** Workspace monorepo with shared dependencies using uv

**Key features:**
- Single `pyproject.toml` with base dependencies (pandas, numpy, jupyter)
- Optional dependency groups for specific topics (ml, viz, db, web)
- Development tools in separate `dev` group
- uv.lock ensures reproducible installations
- Fast installs (10-100x faster than pip)

**Dependencies structure:**
```toml
[project.dependencies]
# Core data science stack always installed

[project.optional-dependencies]
ml = [...]      # Machine learning packages
viz = [...]     # Advanced visualization
db = [...]      # Database & SQL tools
web = [...]     # Web scraping & APIs
dev = [...]     # Development tools
```

**Common commands:**
```bash
uv sync                    # Install base dependencies
uv sync --extra ml        # Install with ML packages
uv sync --all-extras      # Install everything
uv add package-name       # Add new dependency
```

**Rationale:**
- Single environment is simple and fast
- Optional groups keep base install lean
- uv's speed encourages frequent syncing
- Lock file ensures reproducibility

### 3. Code Quality & Linting

**Approach:** Strict from the start

**Tools:**
- **ruff** - Fast linter + formatter (replaces black, isort, flake8)
- **mypy** - Strict type checking
- **pre-commit** - Git hooks to catch issues early
- **pytest** - Testing framework

**Configuration philosophy:**
- Strict rules for `utils/` package (it's your library)
- Notebooks excluded from strict linting (exploration-focused)
- Type hints required in utils, optional in notebooks
- Automatic formatting prevents bikeshedding
- Pre-commit catches issues before they hit git

**Ruff rules enabled:**
- E/W (pycodestyle)
- F (pyflakes)
- I (isort)
- N (pep8-naming)
- UP (pyupgrade)
- B (bugbear)
- C4 (comprehensions)
- SIM (simplify)
- PTH (use-pathlib)
- RUF (Ruff-specific)

**Mypy configuration:**
- Strict mode enabled
- ignore_missing_imports for data science libraries
- Relaxed rules for tests, strict for utils

**Rationale:**
- Learning good habits from day one
- Strict typing catches bugs early
- Automatic formatting saves time
- Professional setup teaches industry practices
- Tools are fast (ruff is 10-100x faster than pylint)

### 4. Utils Package Design

**Approach:** Single utils package with topical modules

**Structure:**
```
utils/
├── __init__.py              # Package exports
├── cleaning.py              # Data cleaning utilities
├── plotting.py              # Custom plotting helpers
├── stats.py                 # Statistical utilities
├── io.py                    # File I/O helpers
└── text.py                  # Text processing
```

**Design principles:**
- **Type hints everywhere** - Full typing for IDE support and error catching
- **Docstrings** - Clear documentation with Args, Returns, Examples
- **Pure functions** - No side effects, always return new data
- **Composable** - Small, focused functions that do one thing well
- **Testable** - Easy to write unit tests

**Example function signature:**
```python
def handle_missing(
    df: pd.DataFrame,
    strategy: Literal["drop", "mean", "median", "mode", "forward_fill"] = "drop",
    threshold: float = 0.5,
) -> pd.DataFrame:
    """Handle missing values with various strategies.

    Args:
        df: Input DataFrame
        strategy: How to handle missing values
        threshold: For 'drop' strategy, drop columns with >threshold proportion missing

    Returns:
        DataFrame with missing values handled
    """
```

**Usage in notebooks:**
```python
from utils.cleaning import clean_columns, handle_missing
from utils.plotting import quick_hist

df = clean_columns(df)
df = handle_missing(df, strategy="median")
quick_hist(df['age'])
```

**Rationale:**
- DRY - Write utilities once, use everywhere
- KISS - Small, focused functions are easy to understand
- Type safety prevents bugs
- Organized by topic for easy discovery
- Professional package structure teaches Python best practices

### 5. Testing Strategy

**Approach:** Test utils package, notebooks are exploratory

**Structure:**
```
tests/
├── conftest.py              # Shared fixtures
├── test_cleaning.py         # Test cleaning utilities
├── test_plotting.py         # Test plotting utilities
├── test_stats.py            # Test stats utilities
└── fixtures/                # Test data files
```

**Philosophy:**
- Utils package is tested (it's your library)
- Notebooks are not tested (they're for exploration)
- Tests use pytest with fixtures
- Fast tests encourage frequent running
- CI runs tests on every push

**Rationale:**
- Testing utils ensures reliability
- Tests document expected behavior
- Encourages thinking about edge cases
- Professional practice for coding

### 6. Workflow Automation

**Approach:** Makefile + pre-commit + GitHub Actions

**Makefile commands:**
```bash
make install           # Install all dependencies
make format            # Format code with ruff
make lint              # Check code with ruff
make type              # Run mypy type checking
make test              # Run pytest tests
make all               # Run all checks
make clean             # Remove cache files
```

**Pre-commit hooks:**
- Ruff formatting
- Ruff linting with auto-fixes
- Trailing whitespace removal
- Large file checks
- Mypy type checking (utils only)

**GitHub Actions CI:**
- Runs on every push/PR
- Checks formatting, linting, types, tests
- Fast feedback loop

**Rationale:**
- Simple commands reduce friction
- Pre-commit prevents bad commits
- CI ensures quality in shared repo
- Automation teaches professional workflows

## Migration Strategy

The existing content will be reorganized:

1. **Current Pandas notebooks** → `pandas/` (keep numbering)
2. **Current Python scripts** → `python/`
3. **Misc/toolbox.py** → `utils/cleaning.py` (expand and add types)
4. **Misc/Polars_cheatsheet.py** → decide on location (pandas/ or new polars/)
5. **Code Challenges** → `challenges/` or merge into topic folders
6. **data/** → Already correct location
7. **Create empty** → numpy/, sklearn/, visualization/, statistics/, sql/

## Success Criteria

1. Clean folder structure with all topic directories created
2. pyproject.toml configured with uv workspace
3. Ruff + mypy + pre-commit hooks working
4. Utils package importable from notebooks
5. Tests passing for existing utilities
6. Makefile commands functional
7. CI pipeline running on GitHub
8. Documentation updated (README, docs/)
9. Existing code reformatted and type-checked

## Non-Goals

- Migrating to a different Python version (staying on 3.14.2)
- Converting notebooks to scripts
- Adding complex build systems
- Creating installable packages for distribution
- Setting up documentation hosting

## Future Enhancements

- Add more topic folders as needed (web-scraping/, nlp/, deep-learning/)
- Expand utils package with more utilities
- Add notebook templates for common patterns
- Create learning path guides in docs/
- Add performance benchmarking utilities
- Consider adding Jupyter extensions for better notebook experience

## Summary

This design creates a professional, scalable learning repository that:
- Organizes content clearly by topic
- Enforces best practices from day one
- Provides reusable utilities following DRY/KISS
- Uses modern, fast tooling (uv, ruff)
- Teaches professional development workflows
- Scales from beginner to advanced topics
