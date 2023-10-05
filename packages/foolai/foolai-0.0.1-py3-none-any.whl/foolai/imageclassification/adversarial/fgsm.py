from rich.console import Console
from rich.prompt import Prompt
import torch
import torch.nn.functional as F
from torchvision import transforms
from typing import Any, Optional

from foolai.config import Config
from foolai.imageclassification.adversarial.examples import AdversarialExample
from foolai.target import TargetModel
from foolai.utils import MEAN_IMAGENET, STD_IMAGENET

console = Console()


class FGSM:
    """
    Generate adversarial examples with FGSM (Fast Gradient Sign Method)
    """
    
    def __init__(
        self,
        config: Config,
        target_model: TargetModel,
        inputs: torch.Tensor,
        target_idx: torch.Tensor
    ) -> None:
        self.config = config
        self.target_model = target_model
        self.inputs = inputs
        self.target_idx = target_idx # Target label index to be used for prediction, calculate perturbations, etc.
        self.epsilons: Optional[list[float]] = None


    def generate(self) -> list[Any]:
        """
        The main function to generate adversarial examples
        """
        epsilons = Prompt.ask("Set custom epsilons if you like", default='0, 0.01, 0.05, 0.1, 0.2')
        try:
            self.epsilons = [float(x.strip()) for x in epsilons.split(',')]
        except:
            self.epsilons = [0, 0.01, 0.05, 0.1, 0.2]
        console.print("Epsilons: ", self.epsilons)

        perturbations = self.calc_perturbations()

        adv_examples: list[AdversarialExample] = []

        for eps in self.epsilons:
            inputs_denorm = self.denormalize(batch=self.inputs)
            adv_img = inputs_denorm + eps * perturbations
            adv_img = torch.clamp(adv_img, 0, 1)
            # Normalize the adversarial image
            adv_img_norm = transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))(adv_img)

            # Predict adversarial example
            adv_preds = self.target_model.predict(inputs=adv_img_norm)
            adv_top_probs, adv_top_indices = adv_preds

            # Add to the list
            adv_top_idx = adv_top_indices[0]
            adv_top_label = self.target_model.labels[adv_top_idx]

            # Check if the adversarial example could fool the target model.
            fooled = False
            if adv_top_idx != self.target_idx:
                fooled = True

            # Initiate the adversarial example
            adv_example = AdversarialExample(img=adv_img, epsilon=eps, top_label=adv_top_label, fooled=fooled)
            adv_examples.append(adv_example)      

        return adv_examples


    def calc_perturbations(self) -> torch.Tensor:
        """
        Calculate perturbations which is used for generating adversarial examples.
        """
        # Assign a variable because of changing the `requires_grad` state.
        inputs = self.inputs

        inputs.requires_grad = True

        preds = self.target_model.model(inputs).logits
        loss = F.nll_loss(preds, torch.tensor([self.target_idx]))
        gradient = torch.autograd.grad(loss, inputs)[0]

        return gradient.sign()


    def denormalize(
        self,
        batch: torch.Tensor,
        mean=MEAN_IMAGENET,
        std=STD_IMAGENET,
    ) -> torch.Tensor:
        """
        Denormalize inputs
        """
        if isinstance(mean, list):
            mean = torch.tensor(mean).to(self.config.device)
        if isinstance(std, list):
            std = torch.tensor(std).to(self.config.device)

        return batch * std.view(1, -1, 1, 1) + mean.view(1, -1, 1, 1)
