from transformers import CLIPModel

model = CLIPModel.from_pretrained("openai/clip-rn50")
print(model.vision_model)
