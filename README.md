# AI-Generated Image Detection System

This full-stack web application determines whether an uploaded image is AI-generated or real. It utilizes a CLIP-based Vision Transformer model for Zero-Shot classification and provides explainability through Grad-CAM heatmaps.

## Features

- **AI vs Real Detection**: Classifies images with probability scores.
- **Explainability**: Visualizes decision regions using Grad-CAM heatmaps.
- **Modern UI**: Dark-themed, responsive interface built with Next.js.
- **Secure Backend**: Fast and robust API using FastAPI and PyTorch.

## Tech Stack

- **Frontend**: Next.js, React, CSS Modules
- **Backend**: FastAPI, PyTorch, Transformers (Hugging Face), OpenCV
- **Model**: `openai/clip-vit-base-patch32` (Zero-Shot Classification)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   The API will run at `http://127.0.0.1:8000`.

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The app will typically run at `http://localhost:3000`.

## Usage

1. Open the web interface (`http://localhost:3000`).
2. Drag and drop an image or click to upload.
3. Click "Detect Image".
4. View the probability scores and toggle the Heatmap to see which parts of the image influenced the prediction.

## Limitations

- **Probabilistic Nature**: Results are not 100% guaranteed. The system uses zero-shot classification which is versatile but may be less accurate than specialized trained models.
- **Explainability**: Grad-CAM on ViT models interprets attention/activation maps, which can sometimes be abstract.

## Deployment

### Backend (Render/Railway/Heroku)
1. Add a `Procfile` (for Heroku) or start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
2. Ensure `requirements.txt` is present.
3. Set environment variable `PORT` if needed.
4. Note: The model download (approx 600MB) happens on first startup. Persistent storage or caching is recommended to avoid download on every restart.

### Frontend (Vercel/Netlify)
1. Push `frontend` directory to a repository.
2. Import into Vercel.
3. Set `NEXT_PUBLIC_API_URL` environment variable if you modify the API endpoint.
4. Vercel automatically detects Next.js and deploys.
