"""
Main entry point for the chatapp TUI.
Launches the Textual app with enhanced beautiful styling.
"""
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from textual.app import App
from screens import LoginScreen


class ChatApp(App):
    """Ephemeral chat application with beautiful UI."""

    CSS = """
    Screen {
        align: center middle;
        background: $surface;
    }

    /* Centered containers */
    Center {
        width: 100%;
        height: 100%;
        align: center middle;
    }

    /* Login Screen Styling */
    #login_container {
        width: 70;
        height: auto;
        border: heavy $primary;
        padding: 2;
        background: $panel;
        box-sizing: border-box;
    }

    #login_container #title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin: 1 0;
        text-style: bold;
    }

    #login_container #subtitle {
        text-align: center;
        color: $success;
        margin-bottom: 1;
    }

    #login_container #description {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    #login_container #divider {
        height: 1;
        background: $primary-darken-2;
        margin: 1 0;
    }

    #login_container #spacer1, #login_container #spacer2 {
        height: 1;
    }

    #login_container Input {
        margin: 1 0;
        border: tall $primary;
    }

    #login_container Input:focus {
        border: tall $accent;
    }

    #login_container #button_row {
        height: auto;
        align: center middle;
        margin: 1 0;
    }

    #login_container #button_row Button {
        width: auto;
        min-width: 20;
        margin: 0 1;
    }

    #login_container #status {
        text-align: center;
        margin: 1 0;
        min-height: 2;
    }

    #login_container #footer_info {
        text-align: center;
        margin-top: 2;
    }

    /* Menu Screen Styling */
    #menu_container {
        width: 60;
        height: auto;
        border: heavy $primary;
        padding: 3;
        background: $panel;
    }

    #menu_container #user_badge {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 1 0;
    }

    #menu_container #menu_title {
        text-align: center;
        text-style: bold;
        color: $primary;
        margin: 1 0 2 0;
    }

    #menu_container #menu_divider {
        height: 1;
        background: $primary-darken-2;
        margin: 1 0;
    }

    #menu_container #spacer1, #menu_container #spacer2 {
        height: 1;
    }

    #menu_container Button {
        width: 100%;
        margin: 1 0;
    }

    #menu_container #menu_footer {
        text-align: center;
        margin-top: 2;
    }

    /* Start Chat Screen */
    #start_chat_container {
        width: 70;
        height: auto;
        border: heavy $primary;
        padding: 2;
        background: $panel;
    }

    #start_chat_container #title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin: 1 0;
    }

    #start_chat_container #subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    #start_chat_container #divider {
        height: 1;
        background: $primary-darken-2;
        margin: 1 0;
    }

    #start_chat_container #spacer1, #start_chat_container #spacer2 {
        height: 1;
    }

    #start_chat_container Input {
        margin: 1 0;
        border: tall $primary;
    }

    #start_chat_container Input:focus {
        border: tall $accent;
    }

    #start_chat_container #button_row {
        height: auto;
        align: center middle;
        margin: 1 0;
    }

    #start_chat_container #button_row Button {
        width: auto;
        min-width: 20;
        margin: 0 1;
    }

    #start_chat_container #status {
        text-align: center;
        margin: 1 0;
        min-height: 2;
    }

    #start_chat_container #footer_info {
        text-align: center;
        margin-top: 1;
    }

    /* Recent Chats Screen */
    #recent_chats_container {
        width: 70;
        height: auto;
        max-height: 90%;
        border: heavy $primary;
        padding: 2;
        background: $panel;
    }

    #recent_chats_container #title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin: 1 0;
    }

    #recent_chats_container #divider {
        height: 1;
        background: $primary-darken-2;
        margin: 1 0;
    }

    #recent_chats_container #loading {
        margin: 2 0;
        align: center middle;
    }

    #recent_chats_container #contacts_list {
        height: 25;
        border: solid $primary;
        padding: 1;
        margin: 1 0;
        background: $surface;
    }

    #recent_chats_container #empty_state {
        text-align: center;
        padding: 5 2;
    }

    #recent_chats_container #contacts_list Button {
        width: 100%;
        margin: 0 0 1 0;
    }

    #recent_chats_container #spacer {
        height: 1;
    }

    #recent_chats_container #back {
        width: 100%;
    }

    /* Chat Screen Styling */
    #chat_container {
        width: 100%;
        height: 100%;
        border: none;
        padding: 0;
        background: $surface;
    }

    #chat_container #chat_header_row {
        height: auto;
        padding: 1 2;
        background: $primary-darken-3;
        border-bottom: wide $primary;
    }

    #chat_container #chat_header {
        text-style: bold;
        color: $accent;
        width: auto;
    }

    #chat_container #encryption_badge {
        text-align: right;
        color: $success;
        width: auto;
        margin-left: auto;
    }

    #chat_container #divider, #chat_container #input_divider {
        height: 1;
        background: $primary-darken-2;
    }

    #chat_container #messages {
        height: 1fr;
        padding: 1 2;
        background: $surface;
        border: none;
    }

    #chat_container MessageBubble {
        margin: 1 0;
    }

    #chat_container SystemMessage {
        text-align: center;
        margin: 1 0;
    }

    #chat_container #input_row {
        height: auto;
        padding: 1 2;
        background: $panel;
        align: center middle;
    }

    #chat_container #message_input {
        width: 4fr;
        border: tall $primary;
    }

    #chat_container #message_input:focus {
        border: tall $accent;
    }

    #chat_container #send {
        width: 1fr;
        margin-left: 1;
        min-width: 15;
    }

    #chat_container #chat_footer {
        padding: 1 2;
        text-align: center;
        background: $panel-darken-1;
        height: auto;
    }

    /* Global button styling */
    Button {
        min-width: 10;
    }

    Button:hover {
        background: $accent;
    }
    """

    TITLE = "Ephemeral Chat"
    SUB_TITLE = "Secure E2E Encrypted Messaging"

    def on_mount(self) -> None:
        """Start with login screen."""
        self.push_screen(LoginScreen())


def run():
    """Entry point for console script."""
    app = ChatApp()
    app.run()


if __name__ == "__main__":
    run()
