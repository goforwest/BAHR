# Golden Set Test Suite

This directory contains automated tests for the BAHR Golden Set dataset.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and configuration
├── test_golden_set_loader.py    # Data loading and filtering tests
├── test_schema_validation.py    # Schema validation tests
├── test_data_quality.py          # Data quality and integrity tests
├── test_prosody_engine.py        # Prosody engine integration tests
└── fixtures/
    └── sample_verses.json        # Test fixtures
```

## Running Tests

### Run all tests
```bash
pytest dataset/tests/ -v
```

### Run specific test file
```bash
pytest dataset/tests/test_golden_set_loader.py -v
```

### Run with coverage
```bash
pytest dataset/tests/ --cov=dataset --cov-report=html
```

### Run only fast tests (skip integration)
```bash
pytest dataset/tests/ -v -m "not integration"
```

## Test Markers

- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Integration tests with prosody engine
- `@pytest.mark.schema` - Schema validation tests
- `@pytest.mark.quality` - Data quality tests

## Requirements

```bash
pip install pytest pytest-cov jsonschema
```

## CI/CD Integration

Tests run automatically on:
- Every commit (GitHub Actions)
- Pull requests
- Pre-release builds

See `.github/workflows/test-golden-set.yml` for configuration.
