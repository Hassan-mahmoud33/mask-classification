import io
from pathlib import Path

import numpy as np
from PIL import Image
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tensorflow.keras.models import load_model

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "mask_best_model.keras"

app = FastAPI(title="Mask Check API")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
model = load_model(MODEL_PATH)


def predict_mask(image: Image.Image) -> tuple[str, float]:
    image = image.convert("RGB").resize((224, 224))
    image_array = np.asarray(image, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)

    probability = float(model.predict(image_array, verbose=0)[0][0])
    label = "with_mask" if probability >= 0.5 else "without_mask"
    confidence = probability if label == "with_mask" else 1 - probability
    return label, confidence


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/api/predict")
async def predict(image: UploadFile = File(...)):
    if not image.filename:
        raise HTTPException(status_code=400, detail="Please choose an image first.")

    try:
        image_data = await image.read()
        uploaded_image = Image.open(io.BytesIO(image_data))
        label, confidence = predict_mask(uploaded_image)
    except (OSError, ValueError):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid image.")

    return {
        "label": label,
        "has_mask": label == "with_mask",
        "confidence": round(confidence * 100, 2),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
