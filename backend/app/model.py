import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# global model and processor to load once
model = None
processor = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_model():
    """Loads the CLIP model and processor."""
    global model, processor, device
    if model is None:
        print(f"Loading CLIP model on {device}...")
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        model.to(device)
        model.eval()
        print("Model loaded.")
    return model, processor

def predict_single_image(image: Image.Image):
    """
    Predicts if the image is AI-generated or Real using Zero-Shot CLIP.
    Returns dictionary with probabilities.
    """
    global model, processor, device
    if model is None:
        load_model()
    
    # Define labels for zero-shot classification
    labels = ["a real photo", "an ai generated image"]
    
    # Process inputs
    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get probabilities
    logits_per_image = outputs.logits_per_image  # image-text similarity score
    probs = logits_per_image.softmax(dim=1)  # softmax to get probabilities
    
    # Convert to list
    probs_list = probs.cpu().numpy().tolist()[0]
    
    return {
        "real_probability": probs_list[0],
        "ai_probability": probs_list[1]
    }
