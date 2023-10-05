import torch
import torch.nn.functional as F
from typing import Any, Optional


class TargetModel:
    """
    Target model class.
    """

    def __init__(self, model: Any, labels: list[str], arch: str) -> None:
        self.model = model
        self.labels = labels
        self.arch = arch


    def predict(self, inputs: torch.Tensor, top_k: int = 5) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Prediction by target model. It returns the top K probabilities and class indices
        """
        with torch.no_grad():
            preds = self.model(inputs).logits

        probs = F.softmax(preds[0], dim=0)
        top_probs, top_indices = torch.topk(probs, top_k)

        return top_probs, top_indices
