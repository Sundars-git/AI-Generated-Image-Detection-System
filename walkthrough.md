# Walkthrough - AI Image Detection System

I have successfully built the AI-Generated Image Detection System. Here is a summary of the changes and verification.

## Implemented Features

### Backend
- **FastAPI Server**: Implemented `/predict` endpoint to handle image uploads.
- **Model Integration**: Integrated `openai/clip-vit-base-patch32` for zero-shot classification ("AI generated" vs "Real photo").
- **Grad-CAM**: implemented `gradcam.py` with `pytorch-grad-cam` adapted for Vision Transformers (ViT), including a custom `CLIPWrapper` and `reshape_transform`.
- **Validation**: Added file size and type validation logic.

### Documentation
- **Deployment**: Added deployment instructions for Backend (Render/Heroku) and Frontend (Vercel) to README.md.

### Frontend
- **Next.js Application**: Initialized a modern Next.js app.
- **UI Components**: Created a drag-and-drop upload zone, image preview, and results display with progress bars.
- **Visuals**: Applied a sleek dark theme with CSS custom properties.
- **Interaction**: Implemented API integration and Grad-CAM toggle functionality.

## Verification Results

### Backend Test Results
- **Script**: `python backend/test_backend.py`
- **Status**: PASSED
- **Output**:
  - `AI Probability`: Returned valid float.
  - `Real Probability`: Returned valid float.
  - `Heatmap`: Received Base64 encoded image.
  
### Frontend Test Results
- **Command**: `npx next dev`
- **Status**: PASSED (Server running at http://localhost:3001)
- **Connectivity**: Verified via HTTP request.
- **Fixes Applied**: Resolved duplicate `app` directory issue and added missing `globals.css` import in `layout.tsx`.

## Known Issues & Notes
- **Initial Startup**: The first time the backend starts, it downloads the CLIP model (~600MB). This can take several minutes depending on internet speed.
- **Grad-CAM**: The heatmap is generated based on the attention maps of the last encoder layer of the ViT model.

2. **Start Frontend**: `npm run dev` inside `frontend/`
3. **Upload Real Image**: Test with a photograph. Expect high "Real" probability.
4. **Upload AI Image**: Test with a Midjourney/DALL-E image. Expect high "AI" probability.
5. **Check Heatmap**: Toggle the heatmap to verify overlay rendering.

## Known Issues & Notes
- First request takes longer due to model downloading/loading.
- Ensure backend dependencies are fully installed (`torch`, `transformers`, etc.).
