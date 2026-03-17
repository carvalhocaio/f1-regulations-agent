"""
Interactive terminal chat for the F1 Technical Regulations Assistant.
"""

import asyncio

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

from src.agent import ask
from src.models import RegulationAnswer

console = Console()

BANNER = """
[bold red]🏎  F1 Technical Regulations Assistant[/bold red]
[dim]Powered by PydanticAI + Gemini + LangChain RAG[/dim]
[dim]Regulations: FIA 2026 Formula 1 Technical Regulations[/dim]

Type [bold]'exit'[/bold] or [bold]'quit'[/bold] to leave.
"""

EXAMPLE_QUESTIONS = [
    "What is the maximum power unit energy deployment per lap?",
    "What are the dimensions allowed for the front wing?",
    "Can the DRS be used during the formation lap?",
    "What materials are prohibited in car construction?",
]


def _render_answer(answer: RegulationAnswer) -> None:
    """Render a structured RegulationAnswer in the terminal."""

    # Main answer
    console.print()
    console.print(
        Panel(
            Markdown(answer.answer),
            title="[bold green]Answer[/bold green]",
            border_style="green",
        )
    )

    # References
    if answer.references:
        console.print()
        console.print("[bold yellow] Regulation References[/bold yellow]")
        for ref in answer.references:
            console.print(
                Panel(
                    f"[italic]{ref.excerpt}[/italic]",
                    title=f"[cyan]Art. {ref.article} — {ref.title}[/cyan]",
                    border_style="cyan",
                    padding=(0, 1),
                )
            )

    # Confidence
    confidence_pct = int(answer.confidence * 100)
    if answer.confidence >= 0.8:
        confidence_style = "bold green"
        icon = "✅"
    elif answer.confidence >= 0.5:
        confidence_style = "bold yellow"
        icon = "⚠️ "
    else:
        confidence_style = "bold red"
        icon = "❓"

    console.print()
    console.print(
        f"{icon} Confidence: [{confidence_style}]{confidence_pct}%[/{confidence_style}]"
    )

    # Disclaimer
    if answer.disclaimer:
        console.print()
        console.print(
            Panel(
                Text(answer.disclaimer, style="italic"),
                title="[yellow]⚠️  Disclaimer[/yellow]",
                border_style="yellow",
            )
        )


def _show_examples() -> None:
    console.print("\n[dim]Example questions you can ask:[/dim]")
    for i, q in enumerate(EXAMPLE_QUESTIONS, 1):
        console.print(f"  [dim]{i}. {q}[/dim]")
    console.print()


async def chat_loop() -> None:
    """Main interactive loop."""
    console.print(BANNER)
    _show_examples()

    while True:
        try:
            console.print(Rule(style="dim"))
            question = console.input("[bold blue]You:[/bold blue] ").strip()

            if not question:
                continue

            if question.lower() in {"exit", "quit", "q"}:
                console.print("\n[dim]Goodbye! 🏁[/dim]\n")
                break

            console.print("\n[dim]Searching the regulations...[/dim]")

            answer = await ask(question)
            _render_answer(answer)

        except KeyboardInterrupt:
            console.print("\n\n[dim]Interrupted. Goodbye! 🏁[/dim]\n")
            break
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}\n")


def main() -> None:
    asyncio.run(chat_loop())


if __name__ == "__main__":
    main()
