# Changelog

All notable changes to Container Allocator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-27

### Added
- **Linear Programming Optimization**: Uses PuLP with CBC solver for optimal container allocation
- **Multi-Location Support**: Distribute containers across unlimited locations
- **Multi-Material Handling**: Support for different material types (Aluminum, Titanium, Carbon, etc.)
- **Container Size Optimization**: Works with 1, 2, and 4 SCU container sizes
- **Professional Table Layouts**: Three detailed tables showing allocation, usage summary, and efficiency
- **Container Usage Summary Table**: New table showing total container usage by material and size
- **Settings System**: Persistent configuration folder setup with user-friendly dialogs
- **Simplified Configuration Management**: 
  - Save: Simple text input popup for naming configurations
  - Load: File list popup showing saved configurations with timestamps
  - Delete: Remove unwanted configurations from the interface
- **Menu System**: Professional menu bar with File and Settings menus
- **Cross-Platform Executable**: Single-file executable requiring no installation
- **Professional UI**: Improved table formatting with fancy grid borders and center alignment
- **Status Indicators**: Usage percentages with clear status labels (USED, FULL, UNUSED)
- **Error Handling**: Comprehensive error messages and user guidance
- **Documentation**: Complete user and developer guides with Star Citizen examples

### Star Citizen Integration
- **Mission-Specific Design**: Created to solve Star Citizen's multi-location delivery optimization problem
- **Gaming Context**: Addresses the challenge where missions give you more containers than needed without specifying exact amounts per location
- **Cargo Hold Optimization**: Minimizes containers used for maximum cargo efficiency
- **Mission Configuration**: Save and load different mission types (e.g., "Crusader_Aluminum_Daily")
- **Location Names**: Supports Star Citizen location names (Port Olisar, Lorville, Area18, etc.)
- **Material Types**: Handles Star Citizen materials (Aluminum, Titanium, Medical Supplies, etc.)

### Technical Details
- **GUI Framework**: Tkinter with professional styling
- **Optimization Engine**: PuLP library with CBC solver
- **Data Format**: JSON configuration files
- **Build System**: PyInstaller for standalone executables
- **Architecture**: Modular design with separate solver, UI, and settings components
- **Settings Storage**: JSON file in user's home directory for persistence
- **Cross-Platform**: Compatible with Windows, macOS, and Linux

### Use Cases
- **Star Citizen**: Multi-location delivery mission optimization
- **Gaming**: Elite Dangerous, EVE Online logistics planning
- **Real-World**: Logistics planning, inventory management, supply chain optimization
- **Academic**: Operations research and optimization studies
- **Manufacturing**: Material distribution across facilities

### Problem Solved
**Star Citizen Challenge**: Member missions ask you to deliver X SCU to locations A, B, and C, but don't give exact amounts required for each location. You always have more containers than needed, making manual optimization time-consuming and error-prone.

**Solution**: This application finds the mathematically optimal allocation, telling you exactly which containers to take to each location for maximum efficiency.

[1.0.0]: https://github.com/HermanCodes/container-allocator/releases/tag/v1.0.0
