# Developer Guide

## Overview

Container Allocator is built with Python 3.13+ using Tkinter for the GUI and PuLP for linear programming optimization. This guide covers the architecture, development setup, and contribution guidelines.

## Architecture

### Project Structure
```
container-allocator/
├── src/                    # Source code
│   ├── main.py            # Application entry point
│   ├── container_app.py   # Main application logic
│   ├── solver.py          # Optimization solver
│   ├── ui_components.py   # GUI components
│   ├── dialogs.py         # Dialog windows
│   ├── settings.py        # Settings management
│   └── simple_config_dialogs.py # Configuration dialogs
├── build-tools/           # Build configuration
│   └── ContainerAllocator.spec # PyInstaller spec
├── examples/              # Example configurations
├── docs/                  # Documentation
├── deployment/            # Distribution files
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

### Core Components

#### `container_app.py` - Main Application
- **Purpose**: Coordinates all components and manages application state
- **Key Classes**: `ContainerAllocatorApp`
- **Responsibilities**: UI coordination, event handling, configuration management

#### `solver.py` - Optimization Engine
- **Purpose**: Handles linear programming optimization
- **Key Classes**: `ContainerSolver`
- **Dependencies**: PuLP library with CBC solver
- **Algorithm**: Mixed Integer Linear Programming (MILP)

#### `ui_components.py` - GUI Components
- **Purpose**: Reusable UI components and table formatting
- **Key Classes**: `InputGrids`, `OutputDisplay`, `ManagementButtons`
- **Features**: Professional table layouts, dynamic grid management

#### `settings.py` - Settings Management
- **Purpose**: Persistent application settings
- **Key Classes**: `SettingsManager`, `SettingsDialog`
- **Storage**: JSON file in user's home directory

#### `simple_config_dialogs.py` - Configuration UI
- **Purpose**: Simplified save/load dialogs
- **Key Classes**: `SimpleConfigDialogs`, `SimpleLoadDialog`
- **Features**: Text input for save, file list for load

## Development Setup

### Prerequisites
- Python 3.13 or higher
- Git for version control
- Virtual environment support

### Environment Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/container-allocator.git
cd container-allocator

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running from Source
```bash
# Run the application
python src/main.py

# Run with debug output
python src/main.py --debug
```

### Building Executable
```bash
# Build standalone executable
pyinstaller build-tools/ContainerAllocator.spec

# Clean build (recommended)
pyinstaller --clean build-tools/ContainerAllocator.spec

# Output will be in dist/ContainerAllocator.exe
```

## Code Style and Standards

### Python Style Guide
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Documentation Standards
- All public methods must have docstrings
- Use Google-style docstrings
- Include parameter types and return values
- Provide usage examples for complex functions

### Example Code Style
```python
def calculate_optimal_allocation(
    requirements: Dict[Tuple[str, str], int],
    availability: Dict[Tuple[str, int], int],
    materials: List[str],
    locations: List[str],
    sizes: List[int]
) -> Dict[str, Any]:
    """
    Calculate optimal container allocation using linear programming.
    
    Args:
        requirements: Dictionary mapping (location, material) to required SCU
        availability: Dictionary mapping (material, size) to available containers
        materials: List of material names
        locations: List of location names
        sizes: List of container sizes
        
    Returns:
        Dictionary containing optimization results and solution details
        
    Raises:
        OptimizationError: If no feasible solution exists
    """
    # Implementation here
    pass
```

## Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src/

# Run specific test file
python -m pytest tests/test_solver.py
```

### Test Structure
- Unit tests for core logic
- Integration tests for UI components
- End-to-end tests for complete workflows

### Writing Tests
```python
import unittest
from src.solver import ContainerSolver

class TestContainerSolver(unittest.TestCase):
    def setUp(self):
        self.solver = ContainerSolver()
    
    def test_basic_allocation(self):
        # Test implementation
        pass
```

## Contributing

### Getting Started
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Pull Request Guidelines
- **Clear description**: Explain what your changes do and why
- **Tests included**: Add tests for new features or bug fixes
- **Documentation updated**: Update relevant documentation
- **Code style**: Follow the established style guidelines
- **Small, focused changes**: Keep PRs manageable and focused

### Issue Reporting
When reporting bugs or requesting features:
- Use the provided issue templates
- Include steps to reproduce (for bugs)
- Provide system information (OS, Python version)
- Include relevant error messages or screenshots

## Architecture Decisions

### Linear Programming Solver
- **Choice**: PuLP with CBC solver
- **Rationale**: Open source, reliable, handles MILP problems efficiently
- **Alternatives**: OR-Tools, Gurobi (commercial)

### GUI Framework
- **Choice**: Tkinter
- **Rationale**: Built into Python, cross-platform, sufficient for our needs
- **Alternatives**: PyQt, wxPython, web-based interface

### Configuration Storage
- **Choice**: JSON files
- **Rationale**: Human-readable, easy to parse, version control friendly
- **Alternatives**: SQLite, YAML, binary formats

### Build System
- **Choice**: PyInstaller
- **Rationale**: Creates standalone executables, good Python support
- **Alternatives**: cx_Freeze, Nuitka, Docker containers

## Performance Considerations

### Optimization Performance
- **Small problems** (< 10 locations, < 5 materials): < 1 second
- **Medium problems** (< 100 locations, < 20 materials): < 10 seconds
- **Large problems** (> 100 locations): May require solver tuning

### Memory Usage
- **Typical usage**: < 50MB RAM
- **Large problems**: May use several hundred MB
- **Optimization**: Consider problem decomposition for very large scenarios

### UI Responsiveness
- Long-running optimizations run in background
- Progress indicators for user feedback
- Cancellation support for long operations

## Debugging

### Common Issues
- **Import errors**: Check virtual environment activation
- **Solver failures**: Verify PuLP and CBC installation
- **UI freezing**: Check for blocking operations in main thread
- **Build failures**: Ensure all dependencies are included in spec file

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug flag
python src/main.py --debug
```

### Profiling
```python
# Profile optimization performance
import cProfile
cProfile.run('solver.solve(requirements, availability)')
```

## Release Process

### Version Management
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Update version in relevant files before release
- Tag releases in Git

### Release Checklist
1. Update version numbers
2. Update CHANGELOG.md
3. Run full test suite
4. Build and test executable
5. Create Git tag
6. Create GitHub release
7. Upload executable as release asset

## Future Enhancements

### Planned Features
- **Multi-objective optimization**: Cost, time, and efficiency optimization
- **Batch processing**: Handle multiple scenarios simultaneously
- **Advanced reporting**: Export results to Excel, PDF
- **API interface**: REST API for integration with other systems

### Technical Improvements
- **Performance optimization**: Faster solver algorithms
- **Better error handling**: More informative error messages
- **Internationalization**: Support for multiple languages
- **Plugin system**: Allow custom optimization algorithms

## Getting Help

- **Documentation**: Check the `docs/` folder
- **Issues**: Create GitHub issues for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Code Review**: Submit PRs for feedback and collaboration
