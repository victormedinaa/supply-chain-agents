# Contributing to Supply Chain Agents

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Use the issue template
3. Provide clear reproduction steps
4. Include relevant logs or screenshots

### Submitting Changes

1. Fork the repository
2. Create a descriptive branch name
3. Write clear commit messages
4. Include tests for new functionality
5. Update documentation as needed
6. Submit a pull request

## Development Setup

```bash
cd backend
pip install -e ".[dev]"
pytest tests/unit/ -v
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for public functions
- Keep functions focused and small

## Testing

All new features should include unit tests:

```bash
pytest tests/unit/ -v --cov=src
```

## Questions?

Open an issue for discussion.
