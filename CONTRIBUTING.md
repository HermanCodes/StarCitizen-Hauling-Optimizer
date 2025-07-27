# Contributing to Container Allocator

Thank you for your interest in contributing to Container Allocator! This document provides guidelines and information for contributors.

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome newcomers and help them get started
- **Be constructive**: Provide helpful feedback and suggestions
- **Be professional**: Keep discussions focused and productive

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title**: Summarize the issue in the title
- **Steps to reproduce**: Detailed steps to reproduce the behavior
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: OS, Python version, application version
- **Screenshots**: If applicable, add screenshots to help explain

### Suggesting Features

Feature requests are welcome! Please provide:

- **Clear description**: Explain the feature and its benefits
- **Use case**: Describe when and why this feature would be useful
- **Implementation ideas**: If you have thoughts on how it could work
- **Alternatives**: Any alternative solutions you've considered

### Contributing Code

#### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/container-allocator.git
   cd container-allocator
   ```
3. **Set up development environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Making Changes

- **Follow the coding style**: See [Developer Guide](docs/DEVELOPER_GUIDE.md) for details
- **Write tests**: Add tests for new functionality
- **Update documentation**: Keep docs current with your changes
- **Test thoroughly**: Ensure all tests pass and the application works correctly

#### Submitting Changes

1. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: brief description of changes"
   ```
2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
3. **Create a Pull Request** on GitHub

### Pull Request Guidelines

#### Before Submitting
- [ ] Code follows the project's style guidelines
- [ ] Tests have been added for new functionality
- [ ] All tests pass locally
- [ ] Documentation has been updated
- [ ] Commit messages are clear and descriptive

#### Pull Request Description
Include in your PR description:
- **Summary**: What does this PR do?
- **Motivation**: Why is this change needed?
- **Changes**: List of specific changes made
- **Testing**: How was this tested?
- **Screenshots**: If UI changes, include before/after screenshots

#### Review Process
- Maintainers will review your PR and provide feedback
- Address any requested changes
- Once approved, your PR will be merged
- Thank you for your contribution!

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write clear, descriptive variable and function names
- Keep functions focused and reasonably sized
- Add docstrings to public methods

### Testing
- Write unit tests for new functionality
- Ensure existing tests continue to pass
- Test edge cases and error conditions
- Include integration tests for UI components

### Documentation
- Update relevant documentation for changes
- Use clear, concise language
- Include code examples where helpful
- Keep the README and user guides current

## Project Structure

Understanding the project structure helps with contributions:

```
container-allocator/
├── src/                    # Source code
│   ├── main.py            # Application entry point
│   ├── container_app.py   # Main application logic
│   ├── solver.py          # Optimization solver
│   ├── ui_components.py   # GUI components
│   └── ...                # Other modules
├── docs/                  # Documentation
├── examples/              # Example configurations
├── build-tools/           # Build configuration
└── tests/                 # Test files
```

## Areas for Contribution

We welcome contributions in these areas:

### High Priority
- **Bug fixes**: Address reported issues
- **Performance improvements**: Optimize solver performance
- **User experience**: Improve UI/UX based on feedback
- **Documentation**: Improve guides and examples

### Medium Priority
- **New features**: Add requested functionality
- **Testing**: Expand test coverage
- **Cross-platform**: Improve compatibility
- **Accessibility**: Make the application more accessible

### Future Enhancements
- **Multi-objective optimization**: Cost, time, efficiency
- **Advanced reporting**: Export capabilities
- **API interface**: REST API for integration
- **Internationalization**: Multiple language support

## Getting Help

If you need help with contributing:

- **Documentation**: Check the [Developer Guide](docs/DEVELOPER_GUIDE.md)
- **Issues**: Ask questions in GitHub Issues
- **Discussions**: Use GitHub Discussions for general questions
- **Code Review**: Submit draft PRs for early feedback

## Recognition

Contributors will be recognized in:
- **README**: Contributors section
- **Releases**: Release notes acknowledgments
- **Documentation**: Contributor credits

## License

By contributing to Container Allocator, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Container Allocator! Your efforts help make this project better for everyone.
