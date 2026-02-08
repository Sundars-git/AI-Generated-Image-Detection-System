# Implementation Plan - AI-Generated Image Detection System

## Goal
Build a full-stack web application to detect if an image is AI-generated or real, providing a probability score and a Grad-CAM heatmap visualization.

## User Review Required
> [!IMPORTANT]
> **Model Selection**: I will use **`openai/clip-rn50`** in a Zero-Shot classification setting ("AI generated image" vs "Real image").
> - **Reasoning**: The requirements mandate a **CNN-based architecture** and **Grad-CAM**. Most dedicated state-of-the-art detection models are Transformers (ViT), which do not support standard Grad-CAM easy. `clip-rn50` uses a ResNet-50 visual backbone (CNN), allowing standard Grad-CAM, and is pre-trained.
> - **Trade-off**: Zero-shot detection is versatile but might have lower accuracy than a specialized fine-tuned ViT. However, it perfectly satisfies the architectural and explainability constraints without training.

## Proposed Changes

### Backend (`app/`)
I will create a FastAPI backend structure.
#### [NEW] [requirements.txt](file:///C:/Users/kamac/.gemini/antigravity/brain/9c361432-c1f4-4b4a-92be-45978681eadb/backend/requirements.txt)
- `fastapi`, `uvicorn`, `python-multipart`
- `torch`, `torchvision`, `transformers`, `pillow`, `numpy`, `opencv-python`
- `grad-cam` (pytorch-grad-cam library)

#### [NEW] [model.py](file:///C:/Users/kamac/.gemini/antigravity/brain/9c361432-c1f4-4b4a-92be-45978681eadb/backend/app/model.py)
- Load `openai/clip-rn50` using `transformers`.
- Implement `predict_image(image_bytes)`:
  - Preprocess image.
  - Run zero-shot classification with prompts: `["an ai generated image", "a real photo"]`.
  - Return probabilities.

#### [NEW] [gradcam.py](file:///C:/Users/kamac/.gemini/antigravity/brain/9c361432-c1f4-4b4a-92be-45978681eadb/backend/app/gradcam.py)
- Implement `generate_heatmap(image_tensor, model)`:
  - Target the last convolutional layer of the ResNet backbone (`model.vision_model.encoder.layers[-1]`).
  - Use `GradCAM` to generate the heatmap for the "AI generated" class index.
  - Overlay heatmap on the original image using OpenCV.
  - Convert to Base64.

#### [NEW] [main.py](file:///C:/Users/kamac/.gemini/antigravity/brain/9c361432-c1f4-4b4a-92be-45978681eadb/backend/app/main.py)
- Setup FastAPI app.
- CORS middleware.
- Endpoint `POST /predict`.

#### [NEW] [utils.py](file:///C:/Users/kamac/.gemini/antigravity/brain/9c361432-c1f4-4b4a-92be-45978681eadb/backend/app/utils.py)
- Image validation and resizing logic.

### Frontend (`frontend/`)
I will initialize a Next.js application.
#### [NEW] [frontend structure]
- `src/app/page.js`: Main UI.
- `src/components/ImageUpload.js`: Drag & Drop zone.
- `src/components/ResultSection.js`: Display probabilities and Heatmap toggle.
- `src/services/api.js`: Axios/Fetch calls to backend.
- `src/styles/globals.css`: Dark theme styling (Vanilla CSS/CSS Modules).

## Verification Plan

### Automated Tests
- I will write a simple `test_app.py` script to send a request to the local API with a dummy image and verify the JSON response contains `ai_probability` and `heatmap_image`.
- Command: `python test_app.py`

### Manual Verification
- Start Backend: `uvicorn app.main:app --reload`
- Start Frontend: `npm run dev`
- **User Action**: Upload a real image (e.g., photo of a person) -> Verify "Real" has higher probability.
- **User Action**: Upload an AI image (e.g., generated art) -> Verify "AI" has higher probability.
- **User Action**: Toggle "Show Heatmap" -> Verify heatmap overlay appears and looks like a heatmap (red/blue regions).
