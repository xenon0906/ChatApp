# 📦 ChatApp Installation Guide

Install ChatApp as a command-line tool on **any operating system**!

---

## ⚡ Quick Install (Recommended)

### Option 1: Install from GitHub (Easiest)

```bash
pip install git+https://github.com/xenon0906/ChatApp.git
```

**That's it!** Now just run:
```bash
chatapp
```

---

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/xenon0906/ChatApp.git
cd ChatApp

# Install
pip install .
```

**Now run:**
```bash
chatapp
```

---

### Option 3: Development Install (For Contributing)

```bash
git clone https://github.com/xenon0906/ChatApp.git
cd ChatApp
pip install -e .
```

This installs in "editable" mode - changes to code take effect immediately.

---

## 🖥️ Platform-Specific Instructions

### Windows

**Method 1: Using pip (Recommended)**
```cmd
pip install git+https://github.com/xenon0906/ChatApp.git
```

**Method 2: Using PowerShell**
```powershell
# Install Python first if not installed
winget install Python.Python.3.12

# Install ChatApp
pip install git+https://github.com/xenon0906/ChatApp.git

# Run
chatapp
```

**Method 3: Using Windows Terminal**
```cmd
pip install git+https://github.com/xenon0906/ChatApp.git
chatapp
```

---

### Linux (Ubuntu/Debian)

**Method 1: Using pip**
```bash
# Install Python and pip if not installed
sudo apt update
sudo apt install python3 python3-pip git -y

# Install ChatApp
pip3 install git+https://github.com/xenon0906/ChatApp.git

# Run
chatapp
```

**Method 2: Add to PATH permanently**
```bash
# Install
pip3 install --user git+https://github.com/xenon0906/ChatApp.git

# Add to PATH in ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Run
chatapp
```

---

### macOS

**Method 1: Using Homebrew**
```bash
# Install Python
brew install python3

# Install ChatApp
pip3 install git+https://github.com/xenon0906/ChatApp.git

# Run
chatapp
```

**Method 2: Using pip directly**
```bash
pip3 install git+https://github.com/xenon0906/ChatApp.git
chatapp
```

---

## 🐧 Creating System Package (Advanced)

### For Debian/Ubuntu (.deb package)

Create a `.deb` package that can be installed with `sudo apt install`:

**1. Install build tools:**
```bash
sudo apt install python3-stdeb dh-python -y
```

**2. Build the package:**
```bash
cd ChatApp
python3 setup.py --command-packages=stdeb.command bdist_deb
```

**3. Install:**
```bash
sudo dpkg -i deb_dist/python3-chatapp-cli_1.0.0-1_all.deb
```

**4. Now users can install with:**
```bash
sudo dpkg -i chatapp-cli_1.0.0-1_all.deb
chatapp
```

---

### For Arch Linux (AUR)

Create a PKGBUILD for the AUR:

**1. Create PKGBUILD:**
```bash
# pkgname=chatapp-cli
# pkgver=1.0.0
# pkgrel=1
# pkgdesc="Secure ephemeral messaging"
# arch=('any')
# url="https://github.com/xenon0906/ChatApp"
# license=('MIT')
# depends=('python' 'python-requests')
# source=("git+https://github.com/xenon0906/ChatApp.git")
# md5sums=('SKIP')

# package() {
#   cd "$srcdir/ChatApp"
#   python setup.py install --root="$pkgdir" --optimize=1
# }
```

**2. Users install with:**
```bash
yay -S chatapp-cli
chatapp
```

---

### For Fedora/RHEL (.rpm package)

```bash
python3 setup.py bdist_rpm
sudo rpm -i dist/chatapp-cli-1.0.0-1.noarch.rpm
chatapp
```

---

## 📱 Mobile Installation

### Android (Termux)

```bash
# Install Termux from F-Droid
# Open Termux and run:

pkg update
pkg install python git
pip install git+https://github.com/xenon0906/ChatApp.git
chatapp
```

### iOS (Pythonista)

1. Install Pythonista from App Store
2. Download the files from GitHub
3. Run `main.py` in Pythonista

---

## 🔧 Verify Installation

After installing, verify it works:

```bash
# Check installation
chatapp --help

# Or just run
chatapp
```

You should see:
```
============================================================
💬 ChatApp - Secure Ephemeral Messaging
============================================================
📡 Connected to: https://chatapp-cd3r.onrender.com
============================================================
```

---

## 🚀 Usage After Installation

Once installed, simply run from **any directory**:

```bash
chatapp
```

**That's it!** No need to navigate to the project folder or run `python chat.py`.

---

## 📦 Publishing to PyPI (For Maintainers)

To make it installable with just `pip install chatapp-cli`:

**1. Create PyPI account:**
- Go to https://pypi.org/account/register/

**2. Install build tools:**
```bash
pip install build twine
```

**3. Build the package:**
```bash
python -m build
```

**4. Upload to PyPI:**
```bash
python -m twine upload dist/*
```

**5. Now anyone can install with:**
```bash
pip install chatapp-cli
chatapp
```

---

## 🔄 Updating ChatApp

### If installed from GitHub:
```bash
pip install --upgrade git+https://github.com/xenon0906/ChatApp.git
```

### If installed from PyPI (future):
```bash
pip install --upgrade chatapp-cli
```

---

## 🗑️ Uninstalling

```bash
pip uninstall chatapp-cli
```

---

## 🐛 Troubleshooting

### "chatapp: command not found"

**Problem:** Python scripts directory not in PATH

**Solution (Linux/Mac):**
```bash
# Find where pip installed it
pip show chatapp-cli | grep Location

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Make permanent
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Solution (Windows):**
```cmd
# Run as administrator
pip install --user git+https://github.com/xenon0906/ChatApp.git

# Python Scripts should be in PATH automatically
# If not, add: C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts
```

### "Permission denied"

**Linux/Mac:**
```bash
# Install for current user only
pip install --user git+https://github.com/xenon0906/ChatApp.git
```

**Windows:**
```cmd
# Run terminal as Administrator
```

### "No module named 'requests'"

```bash
pip install requests
```

---

## ✨ What Gets Installed

After installation, you get:

1. **Command:** `chatapp` - Available from any directory
2. **Package:** `chatapp_package` - Python package with all functionality
3. **Dependencies:** `requests` - Automatically installed

---

## 🎯 Quick Reference

| Command | Description |
|---------|-------------|
| `pip install git+https://github.com/xenon0906/ChatApp.git` | Install from GitHub |
| `chatapp` | Run the app |
| `pip uninstall chatapp-cli` | Uninstall |
| `pip install --upgrade git+https://github.com/xenon0906/ChatApp.git` | Update |

---

## 🌍 Share with Others

**Tell your friends:**

```
Install ChatApp:

pip install git+https://github.com/xenon0906/ChatApp.git

Then just run:

chatapp
```

---

## 📚 Related Documentation

- **Usage Guide:** `TERMINAL_USAGE.md`
- **Remote Access:** `REMOTE_ACCESS.md`
- **Deployment:** `FINAL_RENDER_DEPLOYMENT.md`

---

## 🎉 You're Ready!

After installation, just type:

```bash
chatapp
```

**Anywhere, anytime!** 🚀
