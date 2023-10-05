from pathlib import Path
import torch
from typing import Union


class AdversarialExample:
    """
    Class for generated adversarial example
    """
    def __init__(
        self,
        img: torch.Tensor,
        epsilon: float,
        top_label: str,
        fooled: bool,
    ) -> None:
        self.img = img
        self.epsilon = epsilon
        self.top_label = top_label
        self.fooled = fooled
        self.filename = f"adv_eps_{epsilon}_fooled.png" if fooled else f"adv_eps_{epsilon}.png"
