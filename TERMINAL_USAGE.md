# 💬 ChatApp Terminal Usage Guide

Complete guide to using ChatApp from your terminal.

---

## 🚀 Quick Start

### 1. Start the Terminal Chat Client

```bash
cd C:\Users\siddh\OneDrive\Desktop\chatapp
python chat.py
```

### 2. Create an Account or Login

You'll see:
```
============================================================
💬 ChatApp - Secure Ephemeral Messaging
============================================================
📡 Connected to: https://chatapp-cd3r.onrender.com
============================================================

Please login or create an account

Enter 'login' or 'signup' (or 'quit' to exit):
```

**For new users:**
```
Enter 'login' or 'signup': signup
Username: alice
Password: MySecure123!
✅ Account created successfully! Welcome alice!
```

**For existing users:**
```
Enter 'login' or 'signup': login
Username: alice
Password: MySecure123!
✅ Logged in successfully! Welcome back alice!
```

---

## 📖 Available Commands

Once logged in, you'll see a prompt like `alice>`. Here are all available commands:

### 1. Send a Message

```bash
alice> send bob Hello Bob! How are you?
✅ Message sent to bob at 2025-11-23T12:30:45
```

**Syntax:** `send <username> <message>`

### 2. Read Messages

```bash
alice> read bob

💬 Messages with bob:
============================================================
[2025-11-23 12:25:30] bob → You
  Hey Alice! Long time no see!

[2025-11-23 12:30:45] You → bob
  Hello Bob! How are you?

============================================================
```

**Syntax:** `read <username>`

### 3. List Contacts

```bash
alice> contacts

👥 Your contacts (2):
  1. bob
  2. charlie
```

**Syntax:** `contacts`

### 4. Show Help

```bash
alice> help

📖 Available Commands:
  send <username> <message>  - Send a message
  read <username>            - Read messages with a user
  contacts                   - List your contacts
  help                       - Show this help
  quit / exit                - Exit the app
```

### 5. Exit

```bash
alice> quit
👋 Goodbye!
```

**Syntax:** `quit` or `exit` or `q`

---

## 🎯 Usage Examples

### Example 1: Full Conversation

```bash
# Terminal 1 - Alice
$ python chat.py
Enter 'login' or 'signup': signup
Username: alice
Password: SecurePass123!
✅ Account created successfully! Welcome alice!

alice> send bob Hey Bob! Want to grab coffee?
✅ Message sent to bob at 2025-11-23T12:00:00

alice> read bob

💬 Messages with bob:
============================================================
[2025-11-23 12:00:00] You → bob
  Hey Bob! Want to grab coffee?

============================================================
```

```bash
# Terminal 2 - Bob
$ python chat.py
Enter 'login' or 'signup': signup
Username: bob
Password: BobPass456!
✅ Account created successfully! Welcome bob!

bob> read alice

💬 Messages with alice:
============================================================
[2025-11-23 12:00:00] alice → You
  Hey Bob! Want to grab coffee?

============================================================

bob> send alice Sure! 3pm at the usual spot?
✅ Message sent to alice at 2025-11-23T12:01:30
```

### Example 2: Group Chat Simulation

```bash
alice> send bob Meeting at 3pm
✅ Message sent to bob

alice> send charlie Meeting at 3pm
✅ Message sent to charlie

alice> send dave Meeting at 3pm
✅ Message sent to dave

alice> contacts
👥 Your contacts (3):
  1. bob
  2. charlie
  3. dave
```

---

## ⚙️ Configuration

### Change API URL (Local vs Production)

Edit `chat.py` line 11:

**For Production (Render):**
```python
API_URL = "https://chatapp-cd3r.onrender.com"
```

**For Local Development:**
```python
API_URL = "http://127.0.0.1:8000"
```

---

## 🔧 Advanced Usage

### Using with curl (Command Line)

#### 1. Create Account
```bash
curl -X POST https://chatapp-cd3r.onrender.com/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"SecurePass123!"}'
```

**Response:**
```json
{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGc..."}
```

#### 2. Login
```bash
curl -X POST https://chatapp-cd3r.onrender.com/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"SecurePass123!"}'
```

#### 3. Send Message
```bash
curl -X POST "https://chatapp-cd3r.onrender.com/messages?token=YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"recipient":"bob","encrypted_content":"Hello!"}'
```

#### 4. Get Messages
```bash
curl "https://chatapp-cd3r.onrender.com/messages/bob?token=YOUR_TOKEN"
```

#### 5. Get Contacts
```bash
curl "https://chatapp-cd3r.onrender.com/contacts?token=YOUR_TOKEN"
```

---

## 🐍 Using with Python Requests

### Basic Example

```python
import requests

API_URL = "https://chatapp-cd3r.onrender.com"

# Signup
response = requests.post(
    f"{API_URL}/signup",
    json={"username": "alice", "password": "SecurePass123!"}
)
token = response.json()["access_token"]

# Send message
requests.post(
    f"{API_URL}/messages?token={token}",
    json={"recipient": "bob", "encrypted_content": "Hello Bob!"}
)

# Read messages
messages = requests.get(
    f"{API_URL}/messages/bob?token={token}"
).json()

for msg in messages:
    print(f"{msg['sender']}: {msg['encrypted_content']}")
```

---

## 🎨 Enhanced Terminal Client Features

### Auto-refresh Messages

Create a script that auto-refreshes messages every few seconds:

```python
import time
import os

def watch_messages(client, username):
    """Auto-refresh messages"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        client.get_messages(username)
        print("\n🔄 Refreshing in 5 seconds... (Ctrl+C to stop)")
        time.sleep(5)
```

### Colored Output (Optional)

Install `colorama` for colored terminal output:

```bash
pip install colorama
```

Then add to `chat.py`:

```python
from colorama import init, Fore, Style
init()

# In send_message:
print(f"{Fore.GREEN}✅ Message sent!{Style.RESET_ALL}")

# In get_messages:
if sender == self.username:
    print(f"{Fore.BLUE}You: {content}{Style.RESET_ALL}")
else:
    print(f"{Fore.MAGENTA}{sender}: {content}{Style.RESET_ALL}")
```

---

## 📋 Password Requirements

Your password must:
- Be at least 8 characters long
- Contain at least one uppercase letter
- Contain at least one lowercase letter
- Contain at least one number
- Optionally contain special characters

**Good passwords:**
- `SecurePass123!`
- `MyPassword2025`
- `ChatApp2025!`

**Bad passwords:**
- `password` (too weak)
- `12345678` (no letters)
- `short` (too short)

---

## 🐛 Troubleshooting

### Error: "Connection refused"

**Problem:** Can't connect to API

**Solutions:**
1. Check if backend is running:
   ```bash
   curl https://chatapp-cd3r.onrender.com/
   ```
2. For local dev, start backend first:
   ```bash
   start-dev.bat  # or ./start-dev.sh
   ```
3. Change `API_URL` in `chat.py` to local if testing locally

### Error: "Invalid credentials"

**Problem:** Wrong username or password

**Solutions:**
1. Make sure username is lowercase
2. Check password is correct
3. Create new account if you forgot password

### Error: "Username already exists"

**Problem:** Account already created

**Solution:** Use `login` instead of `signup`

### No messages showing

**Problem:** Messages might be older than 24 hours

**Solution:** Messages auto-delete after 24 hours (ephemeral chat feature)

---

## 🎯 Pro Tips

### Tip 1: Create Aliases (Windows)

Create a batch file `chat.bat`:
```batch
@echo off
cd C:\Users\siddh\OneDrive\Desktop\chatapp
python chat.py
```

Then run from anywhere:
```bash
chat
```

### Tip 2: Create Aliases (Linux/Mac)

Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias chat='cd ~/chatapp && python chat.py'
```

Then run from anywhere:
```bash
chat
```

### Tip 3: Use Environment Variables for Token

Save your token to avoid logging in every time:

```python
import os

# Save token
with open('.token', 'w') as f:
    f.write(token)

# Load token
if os.path.exists('.token'):
    with open('.token', 'r') as f:
        token = f.read().strip()
```

### Tip 4: Multiple Windows/Terminals

Open multiple terminal windows to chat with yourself:
- Window 1: Login as `alice`
- Window 2: Login as `bob`
- Chat between them in real-time!

---

## 📊 Command Reference Table

| Command | Syntax | Example | Description |
|---------|--------|---------|-------------|
| **Send** | `send <user> <msg>` | `send bob Hi!` | Send a message |
| **Read** | `read <user>` | `read bob` | View conversation |
| **Contacts** | `contacts` | `contacts` | List all contacts |
| **Help** | `help` | `help` | Show help menu |
| **Quit** | `quit` or `exit` | `quit` | Exit application |

---

## 🚀 Next Steps

1. **Try it out:**
   ```bash
   python chat.py
   ```

2. **Create multiple accounts:**
   - Open multiple terminals
   - Create different users
   - Chat between them!

3. **Customize the client:**
   - Edit `chat.py` to add features
   - Add colors, sounds, notifications
   - Create your own commands

4. **Use with your friends:**
   - Share your Render URL
   - They can use the same `chat.py`
   - Just change `API_URL` to your Render URL

---

## 📚 Related Documentation

- **API Documentation:** https://chatapp-cd3r.onrender.com/docs
- **Startup Commands:** `STARTUP_COMMANDS.md`
- **Optimization Guide:** `RENDER_OPTIMIZATION.md`
- **Deployment Guide:** `FINAL_RENDER_DEPLOYMENT.md`

---

## 🎉 You're Ready!

Your ChatApp is fully functional and ready to use from the terminal!

**Start chatting:**
```bash
python chat.py
```

Enjoy your secure, ephemeral messaging app! 💬🚀
