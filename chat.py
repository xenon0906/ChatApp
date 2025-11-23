#!/usr/bin/env python3
"""
Simple terminal-based chat client for ChatApp
Usage: python chat.py
"""
import requests
import json
import sys
from datetime import datetime

# API Configuration
API_URL = "https://chatapp-cd3r.onrender.com"  # Change to local for dev: http://127.0.0.1:8000

class ChatClient:
    def __init__(self):
        self.token = None
        self.username = None

    def signup(self, username, password):
        """Create a new account"""
        try:
            response = requests.post(
                f"{API_URL}/signup",
                json={"username": username, "password": password}
            )
            if response.status_code == 201:
                data = response.json()
                self.token = data["access_token"]
                self.username = username
                print(f"✅ Account created successfully! Welcome {username}!")
                return True
            else:
                print(f"❌ Signup failed: {response.json().get('detail', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def login(self, username, password):
        """Login to existing account"""
        try:
            response = requests.post(
                f"{API_URL}/login",
                json={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.username = username
                print(f"✅ Logged in successfully! Welcome back {username}!")
                return True
            else:
                print(f"❌ Login failed: {response.json().get('detail', 'Invalid credentials')}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def send_message(self, recipient, message):
        """Send a message to another user"""
        try:
            response = requests.post(
                f"{API_URL}/messages?token={self.token}",
                json={
                    "recipient": recipient,
                    "encrypted_content": message  # In real app, this would be encrypted
                }
            )
            if response.status_code == 201:
                data = response.json()
                timestamp = data.get("timestamp", datetime.now().isoformat())
                print(f"✅ Message sent to {recipient} at {timestamp}")
                return True
            else:
                print(f"❌ Failed to send: {response.json().get('detail', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def get_messages(self, other_user):
        """Get messages with another user"""
        try:
            response = requests.get(
                f"{API_URL}/messages/{other_user}?token={self.token}"
            )
            if response.status_code == 200:
                messages = response.json()
                if not messages:
                    print(f"📭 No messages with {other_user}")
                    return []

                print(f"\n💬 Messages with {other_user}:")
                print("=" * 60)
                for msg in messages:
                    sender = msg["sender"]
                    content = msg["encrypted_content"]
                    timestamp = msg.get("timestamp", "")

                    # Format timestamp
                    if timestamp:
                        try:
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            time_str = timestamp
                    else:
                        time_str = "Unknown time"

                    # Display message
                    if sender == self.username:
                        print(f"[{time_str}] You → {other_user}")
                        print(f"  {content}")
                    else:
                        print(f"[{time_str}] {sender} → You")
                        print(f"  {content}")
                    print()

                print("=" * 60)
                return messages
            else:
                print(f"❌ Failed to get messages: {response.json().get('detail', 'Unknown error')}")
                return []
        except Exception as e:
            print(f"❌ Error: {e}")
            return []

    def get_contacts(self):
        """Get list of contacts"""
        try:
            response = requests.get(
                f"{API_URL}/contacts?token={self.token}"
            )
            if response.status_code == 200:
                contacts = response.json()
                if not contacts:
                    print("📭 No contacts yet")
                    return []

                print(f"\n👥 Your contacts ({len(contacts)}):")
                for i, contact in enumerate(contacts, 1):
                    print(f"  {i}. {contact}")
                return contacts
            else:
                print(f"❌ Failed to get contacts: {response.json().get('detail', 'Unknown error')}")
                return []
        except Exception as e:
            print(f"❌ Error: {e}")
            return []


def print_banner():
    """Print app banner"""
    print("\n" + "=" * 60)
    print("💬 ChatApp - Secure Ephemeral Messaging")
    print("=" * 60)
    print(f"📡 Connected to: {API_URL}")
    print("=" * 60 + "\n")


def print_help():
    """Print help menu"""
    print("\n📖 Available Commands:")
    print("  send <username> <message>  - Send a message")
    print("  read <username>            - Read messages with a user")
    print("  contacts                   - List your contacts")
    print("  help                       - Show this help")
    print("  quit / exit                - Exit the app")
    print()


def main():
    """Main application loop"""
    print_banner()

    client = ChatClient()

    # Login or Signup
    print("Please login or create an account\n")

    while True:
        choice = input("Enter 'login' or 'signup' (or 'quit' to exit): ").strip().lower()

        if choice in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            sys.exit(0)

        if choice not in ['login', 'signup']:
            print("❌ Invalid choice. Please enter 'login' or 'signup'\n")
            continue

        username = input("Username: ").strip().lower()
        password = input("Password: ").strip()

        if not username or not password:
            print("❌ Username and password cannot be empty\n")
            continue

        if choice == 'signup':
            if client.signup(username, password):
                break
        else:  # login
            if client.login(username, password):
                break
        print()

    # Main menu
    print_help()

    while True:
        try:
            command = input(f"{client.username}> ").strip()

            if not command:
                continue

            parts = command.split(maxsplit=2)
            cmd = parts[0].lower()

            if cmd in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break

            elif cmd == 'help':
                print_help()

            elif cmd == 'send':
                if len(parts) < 3:
                    print("❌ Usage: send <username> <message>")
                    continue
                recipient = parts[1].lower()
                message = parts[2]
                client.send_message(recipient, message)

            elif cmd == 'read':
                if len(parts) < 2:
                    print("❌ Usage: read <username>")
                    continue
                other_user = parts[1].lower()
                client.get_messages(other_user)

            elif cmd == 'contacts':
                client.get_contacts()

            else:
                print(f"❌ Unknown command: {cmd}")
                print("💡 Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
