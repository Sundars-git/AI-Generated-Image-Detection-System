from transformers import CLIPModel, CLIPProcessor

try:
    print("Loading processor...")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    print("Processor loaded.")
    
    print("Loading model...")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    print("Model loaded.")
except Exception as e:
    print("Error loading model:")
    print(e)
