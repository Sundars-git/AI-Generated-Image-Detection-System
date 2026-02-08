import torch
from PIL import Image
from transformers import ViTForImageClassification, ViTImageProcessor
import torch.nn.functional as F

# Global model and processor
model = None
processor = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_model():
    """Loads the ViT model and processor."""
    global model, processor, device
    if model is None:
        print(f"Loading ViT model (`google/vit-tiny-patch16-224`) on {device}...")
        
        # Load Processor (handles resizing to 224x224 and normalization)
        processor = ViTImageProcessor.from_pretrained("google/vit-tiny-patch16-224")
        
        # Load Model with head replacement for binary classification (2 classes)
        # ignore_mismatched_sizes=True is required to replace the 1000-class head
        model = ViTForImageClassification.from_pretrained(
            "google/vit-tiny-patch16-224",
            num_labels=2,
            ignore_mismatched_sizes=True
        )
        
        model.to(device)
        model.eval()
        print("ViT Model loaded successfully.")
    return model, processor

def predict_single_image(image: Image.Image):
    """
    Predicts if the image is AI-generated or Real using ViT.
    Returns dictionary with probabilities.
    """
    global model, processor, device
    if model is None:
        load_model()
    
    # Preprocess inputs (resizes to 224x224, normalizes)
    inputs = processor(images=image, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Apply Softmax to get probabilities
    probs = F.softmax(outputs.logits, dim=1)
    probs_list = probs.cpu().numpy().tolist()[0]
    
    # Mapping indices to classes
    # Index 0: Real (Arbitrary assignment since untrained)
    # Index 1: AI Generated
    real_score = probs_list[0]
    ai_score = probs_list[1]
    
    return {
        # Requested keys
        "real": real_score,
        "ai_generated": ai_score,
        
        # Backward compatibility keys for Frontend
        "real_probability": real_score,
        "ai_probability": ai_score
    }
