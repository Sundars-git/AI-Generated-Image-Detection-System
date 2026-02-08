# Deployment Guide for AI Image Detection System

This guide explains how to deploy your full-stack application. Since this project has a Python backend and a React/Next.js frontend, it cannot be hosted entirely on GitHub Pages (which only supports static sites).

## Architecture Overview

We will use two free services that integrate perfectly with GitHub:
1.  **Backend (FastAPI/Python)**: Deployed on **Render** (Offers free Python hosting).
2.  **Frontend (Next.js)**: Deployed on **Vercel** (Creators of Next.js).

---

## Part 1: Backend Deployment (Render)

1.  **Create a Render Account**:
    -   Go to [https://render.com](https://render.com) and sign up with your GitHub account.

2.  **Create a New Web Service**:
    -   Click "New +" -> "Web Service".
    -   Select "Build and deploy from a Git repository".
    -   Connect your `AI-Generated-Image-Detection-System` repository.

3.  **Configure the Service**:
    -   **Name**: `ai-image-detector-backend` (or similar).
    -   **Region**: Choose the one closest to you.
    -   **Branch**: `main`
    -   **Root Directory**: `backend` (Important! This tells Render where your python code lives).
    -   **Runtime**: `Python 3`
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
    -   **Instance Type**: Free

4.  **Deploy**:
    -   Click "Create Web Service".
    -   Render will build your app. This might take a few minutes as it installs PyTorch.
    -   **Note**: The first time it runs, it will download the AI model (~600MB).
    -   Once successful, copy the **Service URL** (e.g., `https://ai-image-detector-backend.onrender.com`).

---

## Part 2: Frontend Deployment (Vercel)

1.  **Create a Vercel Account**:
    -   Go to [https://vercel.com](https://vercel.com) and sign up with GitHub.

2.  **Import Project**:
    -   Click "Add New..." -> "Project".
    -   Import your `AI-Generated-Image-Detection-System` repository.

3.  **Configure Project**:
    -   **Framework Preset**: Next.js (Should be auto-detected).
    -   **Root Directory**: Click "Edit" and select `frontend`.
    -   **Environment Variables**:
        -   Add a new variable named `NEXT_PUBLIC_API_URL`.
        -   Value: The **Backend Service URL** you got from Render (e.g., `https://ai-image-detector-backend.onrender.com`).
        -   **Important**: Do NOT add a trailing slash `/` at the end of the URL.
        
4.  **Deploy**:
    -   Click "Deploy".
    -   Vercel will build your frontend and give you a live URL (e.g., `https://ai-generated-image-detection-system.vercel.app`).

---

## Part 3: Final Testing

1.  Open your Vercel URL.
2.  Upload an image.
3.  The frontend will send the image to your Render backend and display the result.

## Troubleshooting

-   **Backend Timeout/Memory**: The AI model is large. If the free tier of Render runs out of memory, you might need to try a smaller model or upgrade to a paid instance.
-   **CORS Errors on Frontend**: If you see network errors, check the "Console" in your browser developer tools (F12). Ensure your backend allows requests from your frontend URL. (We configured `allow_origins=["*"]` in `main.py`, so this should work by default).
