"""Module 3: Food Recognition Module.
Loads a Vision Transformer (ViT) fine-tuned on the Food-101 dataset
(101 food classes) and predicts the food category in an input image.

Model: nateraw/vit-base-food101 (pre-trained, downloaded to ./model)
Preprocessing uses OpenCV as specified in the project proposal.
"""
import os
import cv2
import torch
import numpy as np
from transformers import ViTImageProcessor, AutoModelForImageClassification

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
# Public fallback if the local model folder is not shipped with the code.
HF_MODEL_ID = "nateraw/vit-base-food101"

_processor = None
_model = None
_labels = None


def _load_processor():
    if os.path.isdir(MODEL_DIR):
        return ViTImageProcessor.from_pretrained(MODEL_DIR)
    # Fallback: download from Hugging Face Hub (needs internet on first run)
    from transformers import AutoImageProcessor
    return AutoImageProcessor.from_pretrained(HF_MODEL_ID)


def load_model():
    """Load (once) the image processor, model and label list."""
    global _processor, _model, _labels
    if _model is not None:
        return _processor, _model, _labels
    _processor = _load_processor()
    if os.path.isdir(MODEL_DIR):
        _model = AutoModelForImageClassification.from_pretrained(MODEL_DIR)
    else:
        _model = AutoModelForImageClassification.from_pretrained(HF_MODEL_ID)
    _model.eval()
    _labels = [_model.config.id2label[i] for i in range(len(_model.config.id2label))]
    return _processor, _model, _labels


def preprocess_image(image_path):
    """Read an image with OpenCV and prepare it for the model.

    Steps: read (BGR) -> convert to RGB -> resize to 224x224.
    The ViTImageProcessor then handles normalization.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (224, 224), interpolation=cv2.INTER_AREA)
    return img_resized


def predict(image_path, top_k=3):
    """Predict the food category. Returns list of (label, confidence) tuples."""
    processor, model, labels = load_model()
    img = preprocess_image(image_path)
    inputs = processor(images=img, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]
    top = torch.topk(probs, k=min(top_k, len(labels)))
    return [(labels[i], float(probs[i])) for i in top.indices]


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if not path:
        print("Usage: python3 food_classifier.py <image_path>")
    else:
        for label, conf in predict(path):
            print(f"{label}: {conf * 100:.1f}%")
