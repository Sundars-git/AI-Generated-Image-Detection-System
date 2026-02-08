# Implementation Plan - Switch to Vision Transformer (ViT)

## Goal Description
Replace the existing CLIP-based zero-shot model with a standard Vision Transformer (`google/vit-base-patch16-224`) for binary classification (AI-generated vs Real). The backend will be updated to load this model, replace its classification head, and serve predictions via the existing API.

## User Review Required
> [!IMPORTANT]
> **Model Accuracy Warning**: The requested model (`google/vit-base-patch16-224`) is pre-trained on ImageNet (1000 classes). We are replacing the classification head with a binary one (2 classes), which means **the weights for this new head will be randomly initialized**.
> Without fine-tuning on a labeled dataset of "Real vs AI" images, **the model's predictions will be random (approx 50/50)**.
> This implementation provides the *architecture* and *pipeline* for a ViT-based detector, but it requires training to be functional.

## Proposed Changes

### Backend

#### [MODIFY] [model.py](file:///c:/Users/kamac/OneDrive/Pictures/Documents/TRIAL1/backend/app/model.py)
- Remove `CLIPModel` and `CLIPProcessor`.
- Import `ViTForImageClassification` and `ViTImageProcessor` from `transformers`.
- Update `load_model` to load `google/vit-base-patch16-224`.
- **Key Step**: Use `num_labels=2` and `ignore_mismatched_sizes=True` to replace the 1000-class head with a 2-class head.
- Update `predict_single_image` to:
    - Preprocess image using `ViTImageProcessor`.
    - Run inference.
    - Apply `softmax` to logits.
    - Return probabilities mapping index 0/1 to Real/AI (arbitrary assignment required since untrained).

#### [MODIFY] [main.py](file:///c:/Users/kamac/OneDrive/Pictures/Documents/TRIAL1/backend/app/main.py)
- Update the `/predict` endpoint to use the new `predict_single_image` return values.
- Ensure the JSON response maintains `ai_probability` and `real_probability` for Frontend compatibility.
- *Optionally* add `ai_generated` and `real` keys to satisfy the specific prompt request format.

#### [MODIFY] [requirements.txt](file:///c:/Users/kamac/OneDrive/Pictures/Documents/TRIAL1/backend/requirements.txt)
- Ensure `transformers` and `torch` are present (already are).

## Verification Plan

### Automated Tests
- Run `backend/test_backend.py`. It calls the API and checks for valid float probabilities.
    - Update `test_backend.py` to expect the new model behavior (random but valid floats).

### Manual Verification
1. Start backend: `python -m uvicorn app.main:app --reload`
2. Start frontend: `npm run dev`
3. Upload an image.
4. Verify the backend returns a response (even if random prediction).
5. Verify checks of "heatmap" functionality (might be disabled/broken, check logs).
