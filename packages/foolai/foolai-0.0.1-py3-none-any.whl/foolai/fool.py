from pathlib import Path
from rich.console import Console
from torchvision.utils import save_image
from typing import Optional

from foolai.imageclassification.adversarial.attacker import AdversarialAttacker
from foolai.imageclassification.adversarial.examples import AdversarialExample
from foolai.config import Config
from foolai.result import show_result_panel
from foolai.target import TargetModel
from foolai.utils import load_model_from_huggingface

console = Console()


class Fool:
    """
    Base class for fooling ML models
    """
    def __init__(self, config: Config) -> None:
        self.config = config
        self.target_model: Optional[TargetModel] = None


    def attack(self) -> None:
        """
        The main method to attack a ML model.
        """
        loaded_model = load_model_from_huggingface(
            repo_id=self.config.model,
            supported_hf_architectures=Fool.supported_hf_architectures())

        if loaded_model is None:
            return

        model, labels, arch = loaded_model
        self.target_model = TargetModel(model=model, labels=labels, arch=arch)

        if self.target_model.arch == "ImageClassification":
            self.attack_image_classification()


    def attack_image_classification(self) -> None:
        """
        Attack against an image classification model.
        """
        # Set technique
        self.config.technique = "adv-fgsm" if self.config.technique is None else self.config.technique

        # Generate adversarial examples
        if "adv" in self.config.technique:
            attacker = AdversarialAttacker(self.config, self.target_model)
            adv_examples = attacker.generate()
            if adv_examples is None or len(adv_examples) == 0:
                console.print(f"Adversarial examples were not generated.", style="red")
                return
        else:
            console.print(f"Unsupported Technique: {self.config.technique} is not supported.", style="red")
            return
        
        # Create "adversarial_examples" folder under `outdir`
        adv_dir = self.config.outdir / "adversarial_examples"
        adv_dir.mkdir(parents=True, exist_ok=True)

        self.save_adversarial_examples(adv_examples, adv_dir)

        show_result_panel(
            title=f"Congrats!",
            description=f"\
Adversarial examples generated successfully!\n\
Now go to the [cyan]'{self.config.outdir}/{adv_dir.name}'[/cyan] directory to see them.\n\
In addition, try to fool [cyan]'{self.config.model}'[/cyan] on Hugging Face Hub, using these examples!"
        )


    def save_adversarial_examples(self, adv_examples: list[AdversarialExample], adv_dir: Path) -> None:
        """
        Save generated adversarial examples.
        """
        for adv_example in adv_examples:
            save_image(adv_example.img, f"{self.config.outdir}/{adv_dir.name}/{adv_example.filename}")


    @staticmethod
    def supported_techniques() -> dict[str, list[tuple[str, str]]]:
        """
        Supported fool techniques
        """
        return {
            "Image Classification": [
                ("Adversarial Examples (FGSM)", "adv-fgsm"),
            ]
        }


    @staticmethod
    def supported_hf_architectures() -> list[tuple[str, str]]:
        """
        Supported Hugging Face architectures
        """
        return [
            ("ImageClassification", "AutoModelForImageClassification")
        ]

