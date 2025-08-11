import os

import cv2
import uvicorn
from starlette.responses import StreamingResponse

from src.Components.comic_reader import ComicReader
import numpy as np
from PIL import Image
import io
import base64
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.Components.cv_panel import detect_panels, detect_speech_bubbles

app = FastAPI()
#ComicReader = ComicReader()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", r"Data/comics"))

app.mount("/comics", StaticFiles(directory=DATA_DIR), name="comics")

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def image_to_base64_pil(img: Image.Image) -> str:
    """Convert PIL Image to base64 string."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def image_to_base64_np(array: np.ndarray) -> str:
    """Convert numpy image array (HWC, uint8 or bool) to base64 string."""
    if array.dtype == bool:
        array = (array * 255).astype(np.uint8)
    if array.ndim == 2:  # grayscale
        pil_img = Image.fromarray(array, mode='L')
    elif array.shape[2] == 3:
        pil_img = Image.fromarray(array, mode='RGB')
    else:
        raise ValueError("Unsupported image shape for base64 conversion")
    return image_to_base64_pil(pil_img)

@app.post("/api/process")
async def process_image(
    comic: str = Form(...),
    page: str = Form(...),
    threshold: int = Form(200),
    blur: int = Form(5),
    morph: int = Form(5),
    min_size: int = Form(50),
    bubble_thresh: int = Form(220),
    bubble_min_area: float = Form(0.005),
    bubble_max_area: float = Form(0.05),
    min_circularity: float = Form(0.4),
    use_adaptive: bool = Form(False)
):
    # Build the full path to the image
    img_path = os.path.join(DATA_DIR, comic, page)
    if not os.path.exists(img_path):
        return JSONResponse(status_code=404, content={"error": "Page not found"})

    # Read image directly from disk
    img = cv2.imread(img_path)
    if img is None:
        return JSONResponse(status_code=400, content={"error": "Invalid image"})

    # Run detection
    panel_img = detect_panels(img, blur, threshold, morph, min_size)
    result_img = detect_speech_bubbles(
        panel_img,
        bubble_thresh=bubble_thresh,
        min_area_ratio=bubble_min_area,
        max_area_ratio=bubble_max_area,
        use_adaptive=use_adaptive,
        min_circularity=min_circularity
    )

    _, img_encoded = cv2.imencode('.png', result_img)
    return StreamingResponse(io.BytesIO(img_encoded.tobytes()), media_type='image/png')


@app.get("/comics")
def list_comics():
    comics = []
    if not os.path.exists(DATA_DIR):
        return JSONResponse(status_code=500, content={"error": f"DATA_DIR not found: {DATA_DIR}"})

    for comic_name in os.listdir(DATA_DIR):
        if comic_name == "static":
            continue
        comic_path = os.path.join(DATA_DIR, comic_name)
        if not os.path.isdir(comic_path):
            continue

        pages = sorted([
            f for f in os.listdir(comic_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ])
        if not pages:
            continue

        xml_content = os.path.join(DATA_DIR, comic_name + ".xml")
        comics.append({
            "name": comic_name,
            "pages": pages,
            "annotations": xml_content,
            "previewImage": pages[0]
        })
    return comics


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)