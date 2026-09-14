# Mask Classification

This project detects whether a person is wearing a face mask. It uses a trained TensorFlow/Keras model and provides two ways to test it:

- A FastAPI web app with an image upload page
- A simple Streamlit app

## Project structure

```text
mask_classification/
├── app.py                  # FastAPI application
├── streamlit.py            # Streamlit application
├── mask1.jpg               # Sample image
├── mask2.jpg               # Sample image
├── no_mask1.jpg            # Sample image
├── no_mask2.jpg            # Sample image
├── models/
│   └── mask_best_model.keras
├── dataset/                # Training images
├── notebooks/              # Training notebooks
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Requirements

Install the required packages with:

```powershell
python -m pip install fastapi uvicorn python-multipart streamlit tensorflow pillow numpy opencv-python jinja2
```

## Model location

The trained model is stored in `models/mask_best_model.keras`.

The FastAPI and Streamlit scripts load the model from the `models` folder:

```python
MODEL_PATH = BASE_DIR / "models" / "mask_best_model.keras"
```

For `streamlit.py`, use:

```python
model = load_model("models/mask_best_model.keras")
```

## Run with Docker

Build the image from the project folder:

```powershell
docker build -t mask-classification .
```

Start the container:

```powershell
docker run --rm -p 8000:8000 mask-classification
```

Open the web page at `http://127.0.0.1:8000/`.

## Run the FastAPI app

Open a terminal inside the project folder:

```powershell
cd "C:\Users\B-UNIT\Desktop\computer_vision\image_classification\mask_classification"
python -m uvicorn app:app --reload
```

Then open the web page:

```text
http://127.0.0.1:8000/
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The prediction endpoint is:

```text
POST /api/predict
```

It expects an image in a multipart form field named `image`.

Example with PowerShell:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/predict" -F "image=@mask1.jpg"
```

Example response:

```json
{
  "label": "with_mask",
  "has_mask": true,
  "confidence": 98.42
}
```

## Run the Streamlit app

```powershell
cd "C:\Users\B-UNIT\Desktop\computer_vision\image_classification\mask_classification"
python -m streamlit run streamlit.py
```

Streamlit will print the local URL in the terminal, usually:

```text
http://localhost:8501
```

## Notes

- The model resizes uploaded images to `224 x 224` before prediction.
- Use a clear image where the face is visible.
- `with_mask` means a mask was detected.
- `without_mask` means no mask was detected.
- If port `8000` is already in use, start FastAPI on another port:

  ```powershell
  python -m uvicorn app:app --reload --port 8001
  ```
