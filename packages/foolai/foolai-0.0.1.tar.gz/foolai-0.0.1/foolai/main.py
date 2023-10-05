import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import typer
from typing import Optional
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table

from foolai.__version__ import __version__
from foolai.banner import banner
from foolai.config import Config
from foolai.fool import Fool

console = Console()

app = typer.Typer()


@app.command(name="fool", help="The main command to fool an AI/ML model with various ways.", rich_help_panel="Fool")
def fool(
    model: Annotated[
        Optional[str], typer.Option("--model", "-m", help="Target model you want to fool.")
    ],
    img: Annotated[
        Optional[str], typer.Option("--img", "-i", help="Original image to be used for generating adversarial examples.")
    ] = None,
    text: Annotated[
        Optional[str], typer.Option("--text", "-t", help="Original text to be used for generating adversarial text.")
    ] = None,
    technique: Annotated[
        Optional[str], typer.Option("--technique", "-T", help="")
    ] = None,
    outdir: Annotated[
        str, typer.Option("--outdir", "-o", help="Output directory where generated examples to be stored.")
    ] = ".",
) -> None:
    app_dir = typer.get_app_dir("foolai")
    banner()

    config = Config(model=model, img=img, text=text, technique=technique, outdir=outdir)
    config.show()

    fool = Fool(config)
    fool.attack()


@app.command(name="list", help="List techniques to attack models for each task", rich_help_panel="Fool")
def list() -> None:
    table = Table(title="List Techniques to Attack Models")

    table.add_column("Tasks")
    table.add_column("Techniques")
    table.add_column("Option IDs")

    for key, val in Fool.supported_techniques().items():
        for i in range(len(val)):
            if i == 0:
                table.add_row(key, val[i][0], val[i][1])
            else:
                table.add_row("", val[i][0], val[i][1])

    # table.add_row("Image Classification", "Adversarial Examples (FGSM)", "adv, adv-fgsm")

    console.print(table)


@app.command(name="version", help="Display the version of FoolAI", rich_help_panel="General")
def version() -> None:
    console.print(f"FoolAI version {__version__}")


@app.callback()
def main() -> None:
    """
    FoolAI
    """
    pass
