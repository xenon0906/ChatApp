@echo off
REM Build and prepare for PyPI publishing (Windows)

echo ================================================
echo   Building ChattingWorld for PyPI
echo ================================================
echo.

echo [1/5] Installing build tools...
pip install --upgrade build twine

echo.
echo [2/5] Cleaning previous builds...
if exist dist\ rd /s /q dist
if exist build\ rd /s /q build
if exist *.egg-info rd /s /q *.egg-info

echo.
echo [3/5] Building package...
python -m build

echo.
echo [4/5] Checking package...
python -m twine check dist/*

echo.
echo [5/5] Package built successfully!
echo.
echo ================================================
echo   Ready to publish!
echo ================================================
echo.
echo Built files:
dir /b dist\
echo.
echo To publish to TestPyPI (recommended first):
echo   python -m twine upload --repository testpypi dist/*
echo.
echo To publish to PyPI:
echo   python -m twine upload dist/*
echo.
echo You'll need:
echo   - PyPI account: https://pypi.org/account/register/
echo   - API token: https://pypi.org/manage/account/token/
echo.
pause
