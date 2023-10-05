import os
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
import torch

console = Console()


class Config:
    def __init__(
        self,
        model: str,
        img: Optional[str],
        text: Optional[str],
        technique: Optional[str],
        outdir: str = '.',
    ) -> None:
        self.model = model
        self.img = img
        self.text = text
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.technique = technique
        self.outdir = Path(os.getcwd()) if outdir is None else Path(outdir)


    def show(self) -> None:
        table = Table(title="Configurations", show_header=False, show_lines=True)

        table.add_row("Target model", self.model)
        if self.img is not None:
            table.add_row("Original image", self.img)
        if self.text is not None:
            table.add_row("Original text", self.text)
        if self.technique is not None:
            table.add_row("Technique", self.technique)
        table.add_row("Output directory", str(self.outdir))

        console.print()
        console.print(table)
        console.print()
