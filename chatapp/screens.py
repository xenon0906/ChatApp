"""
Textual TUI screens for the chat app.
Enhanced with beautiful UI, message bubbles, and visual feedback.
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer, Center
from textual.widgets import Header, Footer, Input, Button, Label, Static, LoadingIndicator
from textual.binding import Binding
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from datetime import datetime
import asyncio
import json

from api import api_client, ws_client, WebSocketClient
from crypto import get_or_create_chat_crypto, encrypt_for_peer, decrypt_from_peer


class MessageBubble(Static):
    """A styled message bubble for chat messages."""

    def __init__(self, sender: str, text: str, timestamp: str, is_mine: bool = False):
        self.sender = sender
        self.text = text
        self.timestamp = timestamp
        self.is_mine = is_mine
        super().__init__()

    def render(self) -> Panel:
        """Render message as a styled panel."""
        # Format timestamp
        try:
            dt = datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))
            time_str = dt.strftime("%H:%M")
        except:
            time_str = ""

        # Create message content
        content = Text()

        if self.is_mine:
            content.append(f"{self.text}\n", style="bold cyan")
            content.append(f"{time_str} ✓", style="dim")
            panel = Panel(
                content,
                border_style="cyan",
                title=f"[bold cyan]You[/]",
                title_align="right",
                padding=(0, 1),
            )
        else:
            content.append(f"{self.text}\n", style="bold green")
            content.append(f"{time_str}", style="dim")
            panel = Panel(
                content,
                border_style="green",
                title=f"[bold green]{self.sender}[/]",
                title_align="left",
                padding=(0, 1),
            )

        return panel


class SystemMessage(Static):
    """A system message for notifications."""

    def __init__(self, text: str):
        self.text = text
        super().__init__()

    def render(self) -> Text:
        """Render as centered italic text."""
        msg = Text()
        msg.append("● ", style="yellow")
        msg.append(self.text, style="italic yellow dim")
        return msg


class LoginScreen(Screen):
    """Beautiful login/signup screen with gradients and animations."""

    BINDINGS = [
        Binding("escape", "quit", "Quit", priority=True),
        Binding("ctrl+c", "quit", "Quit", priority=True),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Center(
            Container(
                Static("", id="logo"),
                Label("🔐 EPHEMERAL CHAT", id="title"),
                Static("", id="divider"),
                Label("Secure • Encrypted • Private", id="subtitle"),
                Label("Messages auto-delete after 24 hours", id="description"),
                Static("", id="spacer1"),
                Input(
                    placeholder="👤 Username (min 3 characters)",
                    id="username",
                ),
                Input(
                    placeholder="🔒 Password (min 8 characters)",
                    password=True,
                    id="password",
                ),
                Static("", id="spacer2"),
                Horizontal(
                    Button("Login", variant="primary", id="login"),
                    Button("Sign Up", variant="success", id="signup"),
                    id="button_row"
                ),
                Label("", id="status"),
                Static("", id="footer_info"),
                id="login_container"
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        """Add welcome message on mount."""
        footer = self.query_one("#footer_info", Static)
        footer.update("[dim]Press ESC to quit • Secure E2EE • Open Source[/]")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle login/signup button presses."""
        username_input = self.query_one("#username", Input)
        password_input = self.query_one("#password", Input)
        status_label = self.query_one("#status", Label)

        username = username_input.value.strip()
        password = password_input.value

        # Validation
        if not username or not password:
            status_label.update("[red]⚠ Username and password required[/]")
            return

        if len(username) < 3:
            status_label.update("[red]⚠ Username must be at least 3 characters[/]")
            return

        if len(password) < 8:
            status_label.update("[red]⚠ Password must be at least 8 characters[/]")
            return

        # Disable inputs while processing
        username_input.disabled = True
        password_input.disabled = True
        event.button.disabled = True

        success = False
        if event.button.id == "login":
            status_label.update("[yellow]🔄 Authenticating...[/]")
            success = await api_client.login(username, password)
        else:  # signup
            status_label.update("[yellow]🔄 Creating your account...[/]")
            success = await api_client.signup(username, password)

        if success:
            status_label.update(f"[green]✓ Welcome, {username}![/]")
            await asyncio.sleep(0.5)  # Brief pause for effect
            self.app.push_screen(MenuScreen())
        else:
            if event.button.id == "login":
                status_label.update("[red]✗ Invalid credentials[/]")
            else:
                status_label.update("[red]✗ Username already taken[/]")
            username_input.disabled = False
            password_input.disabled = False
            event.button.disabled = False


class MenuScreen(Screen):
    """Main menu with card-based layout."""

    BINDINGS = [
        Binding("1", "start_chat", "New Chat"),
        Binding("2", "recent_chats", "Recent"),
        Binding("3", "logout", "Logout"),
        Binding("escape", "logout", "Logout"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Center(
            Container(
                Label(f"👤 {api_client.username}", id="user_badge"),
                Static("", id="menu_divider"),
                Label("MAIN MENU", id="menu_title"),
                Static("", id="spacer1"),
                Button("💬 Start New Chat", id="start_chat", variant="primary"),
                Button("📜 View Recent Chats", id="recent_chats", variant="default"),
                Button("📊 Statistics", id="stats", variant="default"),
                Static("", id="spacer2"),
                Button("🚪 Logout", id="logout", variant="error"),
                Static("", id="menu_footer"),
                id="menu_container"
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        """Update footer on mount."""
        footer = self.query_one("#menu_footer", Static)
        footer.update("[dim]Press 1-3 for quick navigation • ESC to logout[/]")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle menu button presses."""
        if event.button.id == "start_chat":
            await self.action_start_chat()
        elif event.button.id == "recent_chats":
            await self.action_recent_chats()
        elif event.button.id == "stats":
            await self.action_stats()
        elif event.button.id == "logout":
            await self.action_logout()

    async def action_start_chat(self) -> None:
        """Prompt for username and start a chat."""
        self.app.push_screen(StartChatScreen())

    async def action_recent_chats(self) -> None:
        """Show recent contacts."""
        self.app.push_screen(RecentChatsScreen())

    async def action_stats(self) -> None:
        """Show user statistics."""
        # Placeholder for statistics screen
        contacts = await api_client.get_contacts()
        self.query_one("#menu_footer", Static).update(
            f"[cyan]📊 You have {len(contacts)} active conversations[/]"
        )

    async def action_logout(self) -> None:
        """Logout and return to login screen."""
        await api_client.close()
        self.app.pop_screen()


class StartChatScreen(Screen):
    """Screen to input username for starting a chat."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Center(
            Container(
                Label("💬 START NEW CHAT", id="title"),
                Static("", id="divider"),
                Label("Enter the username of the person you want to chat with", id="subtitle"),
                Static("", id="spacer1"),
                Input(
                    placeholder="👤 Enter username...",
                    id="chat_username"
                ),
                Static("", id="spacer2"),
                Horizontal(
                    Button("Start Chat", variant="primary", id="start"),
                    Button("Cancel", variant="default", id="cancel"),
                    id="button_row"
                ),
                Label("", id="status"),
                Static("", id="footer_info"),
                id="start_chat_container"
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        """Focus input and update footer."""
        self.query_one("#chat_username", Input).focus()
        self.query_one("#footer_info", Static).update(
            "[dim]Press ESC to go back • Messages are E2E encrypted[/]"
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle start/cancel."""
        if event.button.id == "cancel":
            self.action_cancel()
            return

        username_input = self.query_one("#chat_username", Input)
        other_user = username_input.value.strip().lower()
        status_label = self.query_one("#status", Label)

        if not other_user:
            status_label.update("[red]⚠ Username required[/]")
            return

        if other_user == api_client.username:
            status_label.update("[red]⚠ Cannot chat with yourself[/]")
            return

        status_label.update(f"[green]✓ Opening chat with {other_user}...[/]")
        await asyncio.sleep(0.3)

        # Open chat screen
        self.app.pop_screen()
        self.app.push_screen(ChatScreen(other_user))

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in input."""
        if event.input.id == "chat_username":
            # Trigger start button
            start_btn = self.query_one("#start", Button)
            await self.on_button_pressed(Button.Pressed(start_btn))

    def action_cancel(self) -> None:
        """Cancel and go back."""
        self.app.pop_screen()


class RecentChatsScreen(Screen):
    """Screen showing recent chat contacts with beautiful cards."""

    BINDINGS = [
        Binding("escape", "back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Label("📜 RECENT CHATS", id="title"),
            Static("", id="divider"),
            LoadingIndicator(id="loading"),
            ScrollableContainer(id="contacts_list"),
            Static("", id="spacer"),
            Button("← Back to Menu", id="back", variant="default"),
            id="recent_chats_container"
        )
        yield Footer()

    async def on_mount(self) -> None:
        """Load and display contacts."""
        loading = self.query_one("#loading", LoadingIndicator)
        container = self.query_one("#contacts_list", ScrollableContainer)

        try:
            contacts = await api_client.get_contacts()
            loading.remove()

            if not contacts:
                container.mount(
                    Static(
                        "[dim]No recent conversations\nStart a new chat to get started![/]",
                        id="empty_state"
                    )
                )
            else:
                for i, contact in enumerate(contacts):
                    btn = Button(
                        f"💬  {contact}",
                        id=f"contact_{contact}",
                        variant="primary" if i == 0 else "default"
                    )
                    container.mount(btn)

        except Exception as e:
            loading.remove()
            container.mount(
                Static(f"[red]Failed to load contacts: {str(e)}[/]")
            )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle contact selection or back."""
        if event.button.id == "back":
            self.action_back()
        elif event.button.id.startswith("contact_"):
            contact = event.button.id.replace("contact_", "")
            self.app.pop_screen()
            self.app.push_screen(ChatScreen(contact))

    def action_back(self) -> None:
        """Go back to menu."""
        self.app.pop_screen()


class ChatScreen(Screen):
    """
    Main chat screen with beautiful message bubbles and real-time updates.
    """

    BINDINGS = [
        Binding("escape", "back", "Back to Menu"),
    ]

    def __init__(self, other_user: str):
        super().__init__()
        self.other_user = other_user
        self.crypto = get_or_create_chat_crypto(other_user)
        self.ws_client = None
        self.message_count = 0

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Horizontal(
                Label(f"💬 {self.other_user}", id="chat_header"),
                Label("🔒 E2E Encrypted", id="encryption_badge"),
                id="chat_header_row"
            ),
            Static("", id="divider"),
            ScrollableContainer(id="messages"),
            Static("", id="input_divider"),
            Horizontal(
                Input(
                    placeholder="💭 Type your message... (Press Enter to send)",
                    id="message_input"
                ),
                Button("Send ➤", variant="primary", id="send"),
                id="input_row"
            ),
            Static("", id="chat_footer"),
            id="chat_container"
        )
        yield Footer()

    async def on_mount(self) -> None:
        """Load message history and start WebSocket."""
        messages_container = self.query_one("#messages", ScrollableContainer)
        footer = self.query_one("#chat_footer", Static)

        # Show loading state
        messages_container.mount(
            SystemMessage("Loading conversation history...")
        )

        try:
            # Load existing messages
            messages = await api_client.get_messages(self.other_user)

            # Clear loading message
            messages_container.remove_children()

            if not messages:
                messages_container.mount(
                    SystemMessage(f"Start of conversation with {self.other_user}")
                )
            else:
                for msg in messages:
                    try:
                        # Decrypt message
                        decrypted = decrypt_from_peer(msg["sender"], msg["encrypted_content"])
                        if decrypted:
                            self.display_message(
                                msg["sender"],
                                decrypted,
                                msg["timestamp"]
                            )
                    except Exception:
                        # Skip messages that can't be decrypted
                        continue

            footer.update(f"[dim]{self.message_count} messages • Press ESC to go back[/]")

        except Exception as e:
            messages_container.remove_children()
            messages_container.mount(
                SystemMessage(f"Failed to load messages: {str(e)}")
            )

        # Start WebSocket for real-time updates
        global ws_client
        if not ws_client:
            ws_client = WebSocketClient(
                api_client.username,
                api_client.token,
                self.on_websocket_message
            )
            asyncio.create_task(ws_client.connect())
            messages_container.mount(SystemMessage("Connected • Real-time messaging active"))

        # Focus message input
        self.query_one("#message_input", Input).focus()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle send button."""
        if event.button.id == "send":
            await self.send_message()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in input."""
        if event.input.id == "message_input":
            await self.send_message()

    async def send_message(self) -> None:
        """Encrypt and send a message."""
        message_input = self.query_one("#message_input", Input)
        text = message_input.value.strip()

        if not text:
            return

        try:
            # Encrypt message
            encrypted = encrypt_for_peer(self.other_user, text)

            # Send to backend
            success = await api_client.send_message(self.other_user, encrypted)

            if success:
                # Display locally
                self.display_message(api_client.username, text, datetime.now().isoformat())
                message_input.value = ""

                # Update footer
                footer = self.query_one("#chat_footer", Static)
                footer.update(f"[dim]{self.message_count} messages • Message sent ✓[/]")
            else:
                self.display_system_message("Failed to send message - please try again")

        except RuntimeError:
            # Key exchange needed
            self.display_system_message("Establishing secure connection...")

    def display_message(self, sender: str, text: str, timestamp: str):
        """Display a message bubble in the chat."""
        messages_container = self.query_one("#messages", ScrollableContainer)

        is_me = sender == api_client.username
        bubble = MessageBubble(sender, text, timestamp, is_me)

        messages_container.mount(bubble)
        messages_container.scroll_end()
        self.message_count += 1

    def display_system_message(self, text: str):
        """Display a system message."""
        messages_container = self.query_one("#messages", ScrollableContainer)
        messages_container.mount(SystemMessage(text))
        messages_container.scroll_end()

    async def on_websocket_message(self, message: str):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(message)

            if data.get("type") == "new_message":
                sender = data["sender"]
                if sender == self.other_user:
                    # Decrypt and display
                    decrypted = decrypt_from_peer(sender, data["encrypted_content"])
                    if decrypted:
                        self.display_message(sender, decrypted, data["timestamp"])

                        # Update footer
                        footer = self.query_one("#chat_footer", Static)
                        footer.update(f"[dim]{self.message_count} messages • New message received ✓[/]")

        except Exception:
            pass  # Ignore malformed messages

    def action_back(self) -> None:
        """Return to menu."""
        self.app.pop_screen()
