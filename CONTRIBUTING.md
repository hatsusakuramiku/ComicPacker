# Contributing to ComicPacker

Thank you for your interest in contributing to ComicPacker! This document provides guidelines and information to help you contribute effectively.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request, please:

1. Check if the issue already exists in the [issue tracker](https://github.com/yourusername/ComicPacker/issues)
2. If not, create a new issue with:
   - A clear and descriptive title
   - Detailed steps to reproduce the problem (for bugs)
   - Expected and actual behavior
   - Screenshots or code examples, if applicable
   - Information about your environment (OS, Python version, etc.)

### Submitting Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Add or update tests if applicable
5. Ensure all tests pass
6. Commit your changes with a clear and descriptive commit message
7. Push your branch to your fork
8. Open a pull request to the main repository

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Write docstrings for all public functions and classes
- Add comments for complex logic
- Keep functions and classes focused on a single responsibility

### Testing

- Ensure existing tests pass before submitting changes
- Add new tests for new functionality
- Write clear, descriptive test names
- Test edge cases and error conditions

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ComicPacker.git
   cd ComicPacker
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests:
   ```bash
   python -m pytest
   ```

## Code of Conduct

Please be respectful and considerate in all interactions. We welcome contributions from everyone regardless of background or experience level.

## License

By contributing to ComicPacker, you agree that your contributions will be licensed under the MIT License.