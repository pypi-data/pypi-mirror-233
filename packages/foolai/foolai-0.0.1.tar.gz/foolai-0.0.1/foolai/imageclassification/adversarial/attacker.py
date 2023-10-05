from rich.console import Console
import torch.nn.functional as F
from typing import Optional
from typing_extensions import Any

from foolai.imageclassification.adversarial.fgsm import FGSM
from foolai.config import Config
from foolai.target import TargetModel
from foolai.utils import load_image, preprocess_image


console = Console()


class AdversarialAttacker:
    """
    Base class for generating adversarial examples.
    Reference: https://arxiv.org/abs/1412.6572
    """

    def __init__(self, config: Config, target_model: TargetModel) -> None:
        self.config = config
        self.target_model = target_model


    def generate(self) -> Optional[list[Any]]:
        """
        Generate adversarial examples
        """
        original_image = load_image(self.config.img)
        if original_image is None:
            return None
        
        inputs = preprocess_image(original_image, self.config.device)

        # Initial prediction and get target class index for comparing with the index of prediction for generated adversarial examples
        preds = self.target_model.predict(inputs=inputs)
        if preds is None:
            return None

        top_probs, top_indices = preds
        target_prob = top_probs[0]
        target_idx = top_indices[0]

        if self.config.technique == 'adv-fgsm':
            console.print("Generate adversarial examples with FGSM.")
            fgsm = FGSM(config=self.config, target_model=self.target_model, inputs=inputs, target_idx=target_idx)
            adv_examples = fgsm.generate()
        else:
            console.print(f"Unsupported Method: {self.config.technique} is not supported.", style="red")
            return None

        return adv_examples
