# Contributing to Bob-QA Gatekeeper

Thank you for your interest in contributing to Bob-QA Gatekeeper! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit your changes: `git commit -m "Description of changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Initialize the database**
   ```bash
   python setup_db.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## Code Style Guidelines

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Comment complex logic

## Security Guidelines

⚠️ **CRITICAL**: Never commit sensitive information:
- API keys
- Passwords
- Database credentials
- Personal information

Always use environment variables for sensitive data.

## Testing

Before submitting a pull request:
1. Test all new features thoroughly
2. Ensure existing functionality still works
3. Test with and without API keys (template mode)
4. Verify database operations work correctly

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation for any new features
3. Ensure your code follows the style guidelines
4. Write clear commit messages
5. Reference any related issues in your PR description

## Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Error messages or logs

## Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists
- Clearly describe the feature and its benefits
- Explain the use case
- Consider EU AI Act compliance implications

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Maintain professional communication

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Questions?

If you have questions, please open an issue with the "question" label.

---

Thank you for contributing to Bob-QA Gatekeeper!