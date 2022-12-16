import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from chatgpt import OpenAI

app = typer.Typer()


@app.command()
def explain():
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)
        progress.add_task(description="Preparing...", total=None)
        response = OpenAI().get_response()
        print("\n")
        print(response)


@app.command()
def debug(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
