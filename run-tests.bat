@echo off
REM Test runner script for Windows

echo ========================================
echo   Running ChatApp Test Suite
echo ========================================
echo.

echo [1/2] Running all tests...
python -m pytest tests/ -v

echo.
echo [2/2] Test Summary
echo ========================================
echo Total tests: 35
echo Run 'python -m pytest tests/ -v' to see details
echo.
pause
