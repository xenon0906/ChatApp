"""
Beautiful loading animations and UI enhancements for the terminal.
Provides smooth, modern loading indicators similar to Claude or other modern CLIs.
"""
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.text import Text
from rich import box
from typing import Optional
import time
import asyncio

console = Console()


class LoadingAnimation:
    """Beautiful loading animations with various styles."""

    SPINNERS = {
        "dots": "dots",
        "line": "line",
        "arc": "arc",
        "arrow": "arrow3",
        "bounce": "bouncingBar",
        "clock": "clock",
        "earth": "earth",
        "moon": "moon",
        "dots12": "dots12",
        "aesthetic": "aesthetic"
    }

    @staticmethod
    def spinner(text: str, spinner_type: str = "dots12", style: str = "cyan"):
        """
        Create a spinner context manager.

        Usage:
            with LoadingAnimation.spinner("Loading..."):
                # do work
                time.sleep(2)
        """
        return console.status(text, spinner=spinner_type, spinner_style=style)

    @staticmethod
    def show_progress(description: str, total: int = 100):
        """
        Create a progress bar.

        Returns:
            Progress object to use with context manager
        """
        return Progress(
            SpinnerColumn(spinner_name="dots12"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
            transient=True
        )


class MessageBox:
    """Beautiful message boxes for status updates."""

    @staticmethod
    def success(message: str, title: str = "Success"):
        """Display a success message."""
        console.print(Panel(
            f"[green]{message}[/green]",
            title=f"[bold green]{title}[/bold green]",
            border_style="green",
            box=box.ROUNDED
        ))

    @staticmethod
    def error(message: str, title: str = "Error"):
        """Display an error message."""
        console.print(Panel(
            f"[red]{message}[/red]",
            title=f"[bold red]{title}[/bold red]",
            border_style="red",
            box=box.ROUNDED
        ))

    @staticmethod
    def info(message: str, title: str = "Info"):
        """Display an info message."""
        console.print(Panel(
            f"[cyan]{message}[/cyan]",
            title=f"[bold cyan]{title}[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        ))

    @staticmethod
    def warning(message: str, title: str = "Warning"):
        """Display a warning message."""
        console.print(Panel(
            f"[yellow]{message}[/yellow]",
            title=f"[bold yellow]{title}[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED
        ))


class Banner:
    """Beautiful ASCII banners for the app."""

    @staticmethod
    def show_welcome():
        """Display welcome banner."""
        banner = Text()
        banner.append("╔═══════════════════════════════════════════════════════════╗\n", style="bold cyan")
        banner.append("║                                                           ║\n", style="bold cyan")
        banner.append("║          ", style="bold cyan")
        banner.append("✨ EPHEMERAL CHAT", style="bold magenta")
        banner.append("                         ║\n", style="bold cyan")
        banner.append("║                                                           ║\n", style="bold cyan")
        banner.append("║          ", style="bold cyan")
        banner.append("Secure • Private • Self-Destructing", style="bold green")
        banner.append("        ║\n", style="bold cyan")
        banner.append("║                                                           ║\n", style="bold cyan")
        banner.append("╚═══════════════════════════════════════════════════════════╝", style="bold cyan")

        console.print(banner)
        console.print()

    @staticmethod
    def show_connecting():
        """Display connecting animation."""
        frames = [
            "⠋ Connecting to server",
            "⠙ Connecting to server",
            "⠹ Connecting to server",
            "⠸ Connecting to server",
            "⠼ Connecting to server",
            "⠴ Connecting to server",
            "⠦ Connecting to server",
            "⠧ Connecting to server",
            "⠇ Connecting to server",
            "⠏ Connecting to server"
        ]
        return frames


class StatusDisplay:
    """Display connection status and system info."""

    @staticmethod
    def show_status(backend_url: str, connected: bool = True):
        """Show current connection status."""
        table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))

        table.add_column("Key", style="cyan")
        table.add_column("Value")

        status_icon = "✓" if connected else "✗"
        status_color = "green" if connected else "red"
        status_text = "Connected" if connected else "Disconnected"

        table.add_row("Status", f"[{status_color}]{status_icon} {status_text}[/{status_color}]")
        table.add_row("Backend", f"[blue]{backend_url}[/blue]")
        table.add_row("Encryption", "[green]✓ End-to-End (X25519)[/green]")
        table.add_row("Message TTL", "[yellow]24 hours[/yellow]")

        console.print(Panel(
            table,
            title="[bold cyan]Connection Status[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        ))


# Example usage functions
async def demo_loading():
    """Demo of loading animations."""
    with LoadingAnimation.spinner("Connecting to server...", "dots12", "cyan"):
        await asyncio.sleep(2)

    MessageBox.success("Connected successfully!", "Connection")

    with LoadingAnimation.show_progress("Initializing encryption") as progress:
        task = progress.add_task("[cyan]Setting up...", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            await asyncio.sleep(0.02)

    MessageBox.success("Encryption initialized!", "Security")


if __name__ == "__main__":
    # Demo
    Banner.show_welcome()
    time.sleep(1)
    asyncio.run(demo_loading())
    StatusDisplay.show_status("https://chatapp.onrender.com", connected=True)
