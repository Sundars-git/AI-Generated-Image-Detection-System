import torch
import numpy as np
import cv2
import base64
import io
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

from .model import load_model, device

class CLIPWrapper(torch.nn.Module):
    """
    Wraps CLIP model to behave like a standard classifier for Grad-CAM.
    Output: logits_per_image (Text-Image similarity scores)
    """
    def __init__(self, model, processor, text_labels):
        super().__init__()
        self.model = model
        self.processor = processor
        self.text_labels = text_labels
        self.text_inputs = None 

    def forward(self, x):
        if self.text_inputs is None:
            self.text_inputs = self.processor(text=self.text_labels, return_tensors="pt", padding=True).to(device)
        
        # Check if x is tensor or dict. GradCAM passes validation tensor.
        # But CLIP expects pixel_values.
        outputs = self.model(pixel_values=x, input_ids=self.text_inputs["input_ids"], attention_mask=self.text_inputs["attention_mask"])
        return outputs.logits_per_image

def reshape_transform(tensor, height=7, width=7):
    # Dims: (Batch, N_tokens, Channels)
    # CLIP ViT-B/32: 224x224 img / 32 patch = 7x7 grid.
    # Total tokens = 1 (im_start/cls) + 49 (patches) = 50.
    
    # Exclude cls token
    result = tensor[:, 1:, :].reshape(tensor.size(0), height, width, tensor.size(2))
    
    # Bring channels to first dim: (B, C, H, W)
    result = result.transpose(2, 3).transpose(1, 2)
    return result

def generate_heatmap(image: Image.Image):
    """
    Generates Grad-CAM heatmap for the 'AI generated' class (index 1).
    """
    model, processor = load_model()
    
    labels = ["a real photo", "an ai generated image"] 
    wrapper = CLIPWrapper(model, processor, labels)
    wrapper.eval()
    
    # Target Layer for ViT: last encoder layer's LayerNorm before attention or MLP?
    # Usually `model.vision_model.encoder.layers[-1].layer_norm1` works well for attention.
    # Transformers CLIP structure:
    # model.vision_model.encoder.layers is a list of CLIPEncoderLayer.
    target_layers = [model.vision_model.encoder.layers[-1].layer_norm1]

    # Construct GradCAM with reshape_transform
    cam = GradCAM(model=wrapper, target_layers=target_layers, reshape_transform=reshape_transform)

    # Preprocess image
    inputs = processor(images=image, return_tensors="pt").to(device)
    input_tensor = inputs["pixel_values"] 
    
    # Generate CAM for class 1 (AI)
    targets = [ClassifierOutputTarget(1)]
    grayscale_cam = cam(input_tensor=input_tensor, targets=targets)
    grayscale_cam = grayscale_cam[0, :]
    
    # Overlay
    image_np = np.array(image.resize((224, 224))) / 255.0 # Resize to match input_tensor resolution approximately
    # Actually simpler to resize image to input_tensor H,W
    h, w = input_tensor.shape[2], input_tensor.shape[3]
    if image.size != (w, h):
         image_np = np.array(image.resize((w, h))) / 255.0
    else:
         image_np = np.array(image) / 255.0

    visualization = show_cam_on_image(image_np, grayscale_cam, use_rgb=True)
    
    # Convert to Base64
    img_pil = Image.fromarray(visualization)
    buff = io.BytesIO()
    img_pil.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")
