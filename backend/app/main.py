from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import base64
import io

from .model import predict_single_image
from .gradcam import generate_heatmap
from .utils import validate_image, process_image

app = FastAPI(title="AI-Generated Image Detection API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Image Detection API is running."}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        content = await file.read()
        validate_image(content, file.filename)
        
        image = process_image(content)
        
        # Prediction
        probs = predict_single_image(image)
        
        # Grad-CAM (Placeholder for now)
        try:
            heatmap_b64 = generate_heatmap(image)
        except Exception as e:
            print(f"GradCAM error: {e}")
            heatmap_b64 = None
        
        return JSONResponse(content={
            "ai_generated": probs["ai_generated"],
            "real": probs["real"],
            # Backward compatibility for Frontend
            "ai_probability": probs["ai_probability"],
            "real_probability": probs["real_probability"],
            "heatmap_image": heatmap_b64
        })

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Server error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
