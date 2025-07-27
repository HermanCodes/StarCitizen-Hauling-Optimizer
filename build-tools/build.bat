@echo off
echo Building Container Allocator...
echo.

REM Change to project root directory
cd /d "%~dp0\.."

REM Activate virtual environment and build
.venv\Scripts\pyinstaller.exe --clean build-tools\ContainerAllocator.spec

echo.
if exist "dist\ContainerAllocator.exe" (
    echo ✅ Build successful! 
    echo Executable created: dist\ContainerAllocator.exe
    echo.
    echo Updating deployment folder...
    copy "dist\ContainerAllocator.exe" "deployment\" >nul
    copy "docs\EXECUTABLE_README.md" "deployment\README.md" >nul
    echo ✅ Deployment folder updated!
) else (
    echo ❌ Build failed!
)

pause
