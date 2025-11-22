#!/usr/bin/env python3
"""
Pre-commit security and quality check.
Ensures no secrets are committed and code is ready for deployment.
"""
import os
import re
from pathlib import Path

# ANSI color codes (Windows compatible)
GREEN = ""
RED = ""
YELLOW = ""
BLUE = ""
RESET = ""

print("=" * 60)
print("PRE-COMMIT SECURITY & QUALITY CHECK")
print("=" * 60)
print()

errors = []
warnings = []
passed = []

# 1. Check for .env files in git staging
print("[1/7] Checking for .env files...")
env_files = list(Path(".").rglob(".env"))
env_files_not_example = [f for f in env_files if not str(f).endswith(".env.example")]

if env_files_not_example:
    if os.path.exists(".gitignore"):
        gitignore = open(".gitignore").read()
        if ".env" in gitignore:
            for f in env_files_not_example:
                passed.append(f"Found {f} but .env is in .gitignore")
        else:
            errors.append(".env files found but .env pattern not in .gitignore!")
    else:
        errors.append(".env files found but no .gitignore exists!")
else:
    passed.append("No .env files found")

# 2. Check for hardcoded secrets
print("[2/7] Scanning for hardcoded secrets...")
secret_patterns = [
    (r'mongodb\+srv://[^:]+:[^@]+@', "MongoDB URI with credentials"),
    (r'redis://[^:]+:[^@]+@', "Redis URL with credentials"),
    (r'password\s*=\s*["\'][^"\']{8,}["\']', "Hardcoded password"),
    (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "API key"),
]

excluded_files = {".env", ".env.example", "pre_commit_check.py", ".git", "__pycache__", "node_modules"}

for root, dirs, files in os.walk("."):
    # Exclude certain directories
    dirs[:] = [d for d in dirs if d not in excluded_files]

    for file in files:
        if file.endswith(('.py', '.js', '.json', '.yml', '.yaml', '.toml', '.ini')):
            filepath = os.path.join(root, file)

            # Skip excluded files
            if any(excl in filepath for excl in excluded_files):
                continue

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    for pattern, desc in secret_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            # Check if it's in a comment or example
                            if "example" in filepath.lower() or "sample" in filepath.lower():
                                continue
                            warnings.append(f"Possible {desc} in {filepath}")
            except Exception:
                pass

if not warnings:
    passed.append("No hardcoded secrets detected")

# 3. Check .gitignore exists and has required patterns
print("[3/7] Validating .gitignore...")
if os.path.exists(".gitignore"):
    with open(".gitignore") as f:
        gitignore_content = f.read()

    required_patterns = [".env", "__pycache__", "*.pyc", ".venv", "venv/"]
    missing = [p for p in required_patterns if p not in gitignore_content]

    if missing:
        errors.append(f".gitignore missing patterns: {', '.join(missing)}")
    else:
        passed.append(".gitignore has all required patterns")
else:
    errors.append(".gitignore file not found!")

# 4. Check for TODO/FIXME/HACK comments
print("[4/7] Checking for TODO/FIXME markers...")
todo_count = 0
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in excluded_files]

    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if re.search(r'#\s*(TODO|FIXME|HACK|XXX)', line, re.IGNORECASE):
                            todo_count += 1
            except Exception:
                pass

if todo_count > 0:
    warnings.append(f"Found {todo_count} TODO/FIXME/HACK comments")
else:
    passed.append("No TODO/FIXME markers found")

# 5. Check required files exist
print("[5/7] Verifying required files...")
required_files = [
    "README.md",
    "backend/requirements.txt",
    "backend/app.py",
    "backend/Procfile",
    "backend/Dockerfile",
    "chatapp/requirements.txt",
    "chatapp/main.py",
]

for req_file in required_files:
    if os.path.exists(req_file):
        passed.append(f"Required file exists: {req_file}")
    else:
        errors.append(f"Missing required file: {req_file}")

# 6. Check Python syntax
print("[6/7] Checking Python syntax...")
import py_compile
python_files = list(Path(".").rglob("*.py"))
syntax_errors = []

for py_file in python_files:
    if any(excl in str(py_file) for excl in excluded_files):
        continue

    try:
        py_compile.compile(str(py_file), doraise=True)
    except py_compile.PyCompileError as e:
        syntax_errors.append(f"{py_file}: {e}")

if syntax_errors:
    for err in syntax_errors:
        errors.append(f"Syntax error: {err}")
else:
    passed.append(f"All {len(python_files)} Python files have valid syntax")

# 7. Check for large files
print("[7/7] Checking for large files...")
large_files = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in excluded_files]

    for file in files:
        filepath = os.path.join(root, file)
        try:
            size = os.path.getsize(filepath)
            if size > 10_000_000:  # 10 MB
                large_files.append(f"{filepath} ({size / 1_000_000:.1f} MB)")
        except Exception:
            pass

if large_files:
    for lf in large_files:
        warnings.append(f"Large file: {lf}")
else:
    passed.append("No files larger than 10 MB")

# Print results
print()
print("=" * 60)
print("RESULTS")
print("=" * 60)
print()

if passed:
    print(f"PASSED ({len(passed)}):")
    for p in passed:
        print(f"  [OK] {p}")
    print()

if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  [WARN] {w}")
    print()

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  [FAIL] {e}")
    print()

# Final verdict
print("=" * 60)
if errors:
    print("STATUS: FAILED - Fix errors before committing!")
    print("=" * 60)
    exit(1)
elif warnings:
    print("STATUS: WARNING - Review warnings before committing")
    print("=" * 60)
    exit(0)
else:
    print("STATUS: PASSED - Ready to commit!")
    print("=" * 60)
    exit(0)
