# Container Allocator - Standalone Executable

## What's Included

- **ContainerAllocator.exe** (13MB) - The complete standalone application
- **run_container_allocator.bat** - Optional batch file to launch the application

## How to Use

### Option 1: Direct Launch
Simply double-click `dist/ContainerAllocator.exe` to run the application.

### Option 2: Using Batch File
Double-click `run_container_allocator.bat` to launch the application.

## System Requirements

- **Operating System**: Windows 7 or later (64-bit)
- **Memory**: At least 100MB RAM available
- **Disk Space**: 15MB free space
- **No Python Installation Required** - Everything is bundled!

## Features

The executable includes all necessary components:
- Python runtime
- Tkinter GUI framework
- PuLP optimization library
- Tabulate formatting library
- All application modules

## Getting Started

1. Launch the application using either method above
2. Add materials using the "+" button under Materials
3. Add locations using the "+" button under Locations
4. Configure your requirements and container availability
5. Click "Calculate Allocation" to find the optimal solution

## Distribution

This single executable file can be:
- Copied to any Windows computer
- Run without installing Python or any dependencies
- Shared with others who need the Container Allocator tool
- Placed on network drives for shared access

## File Structure After Build

```
container-allocator/
├── dist/
│   └── ContainerAllocator.exe    # ← The standalone executable (13MB)
├── build/                        # Build artifacts (can be deleted)
├── ContainerAllocator.spec       # PyInstaller specification
├── run_container_allocator.bat   # Launch helper
└── [source files...]            # Original Python source code
```

## Notes

- The executable is larger (13MB) because it contains the entire Python runtime
- First launch may be slightly slower as the executable unpacks itself
- The application runs entirely from memory - no temporary files are created
- All original functionality is preserved in the standalone version

## Troubleshooting

If the executable doesn't start:
1. Make sure you have Windows 7 or later
2. Check that antivirus software isn't blocking the file
3. Try running as administrator if needed
4. Ensure you have sufficient disk space and memory

## Building Your Own

If you want to rebuild the executable:
1. Install PyInstaller: `pip install pyinstaller`
2. Run: `pyinstaller --onefile --windowed --name "ContainerAllocator" main.py`
3. Find the new executable in the `dist/` folder
