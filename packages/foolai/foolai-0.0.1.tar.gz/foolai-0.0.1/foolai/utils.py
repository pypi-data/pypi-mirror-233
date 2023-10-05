from huggingface_hub import HfFileSystem
from importlib import import_module
from PIL import Image
from rich.console import Console
import torch
from torchvision import transforms
from typing import Any, Optional
import json

console = Console()

# Hugging Face File System to find specific files in repository.
hffs = HfFileSystem()


# Mean and standard deviation for pytorch pretrained models (torchvision)
MEAN_IMAGENET = [0.485, 0.456, 0.406]
STD_IMAGENET = [0.229, 0.224, 0.225]


def load_model_from_huggingface(repo_id: str, supported_hf_architectures: list[tuple[str, str]]) -> Optional[tuple[Any, list[str], str]]:
    """
    Load ML model from Hugging Face Hub.
    """
    try:
        config = json.loads(hffs.read_text(f"{repo_id}/config.json"))
        if config.get("architectures"):
            archs = config["architectures"]
        else:
            console.print(f"Architectures not found on {repo_id}.")
            return None
        
        arch = archs[0]
        for sa in supported_hf_architectures:
            sa_arch, sa_lib = sa
            if sa_arch in arch:
                module = import_module("transformers")
                class_obj = getattr(module, sa_lib)
                # Load pretrained model
                model = class_obj.from_pretrained(repo_id)
                # Load labels
                labels = list(model.config.id2label.values())
                return model, labels, sa_arch
        console.print(f"{arch} is not supported yet")
    except FileNotFoundError as e:
        console.print(f"File/path not found on Hugging Face: {e}", style="red")
    except Exception as e:
        console.print(f"Error loading model from Hugging Face: {e}", style="red")

    return None


def load_image(img: Optional[str] = None) -> Optional[Image.Image]:
    """
    Load image from file path
    """
    if img is None:
        console.print("Image file is not set. Please use `--img/-i` option to specify the image file.", style="red")
        return None
    
    try:
        image = Image.open(img)
    except FileNotFoundError as e:
        console.print(f"Image file not found: {e}", style="red")
        return None
    except Exception as e:
        console.print(f"Error loading an image: {e}", style="red")
        return None
    
    return image


def preprocess_image(image: Image.Image, device: str = 'cpu') -> torch.Tensor:
    """
    Preprocess an image.
    """
    # Adjust number of channels
    image = image.convert('RGB') if image.mode == 'RGBA' else image

    preprocess = create_preprocess()
    image_tensor = preprocess(image)

    # Prepend one dimension to the tensor for inference
    image_batch = image_tensor.unsqueeze(0)
    image_batch = image_batch.to(device)
    return image_batch


def create_preprocess() -> transforms.Compose:
    """
    Create a preprocessor.
    """
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=MEAN_IMAGENET, std=STD_IMAGENET),
    ])
