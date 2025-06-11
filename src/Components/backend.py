import cv2
import uvicorn
from flask import request, send_file
from starlette.responses import StreamingResponse

from src.Components.comic_reader import ComicReader
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from skimage.color import rgb2gray
from skimage.feature import canny
from skimage.morphology import dilation, square
from scipy import ndimage as ndi
from skimage.measure import label, regionprops
from skimage.draw import rectangle_perimeter

import io
import base64
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.Components.cv_panel import detect_panels, detect_speech_bubbles

app = FastAPI()
ComicReader = ComicReader()

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


@app.post("/get-comic")
async def get_comic(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    if not isinstance(image, np.ndarray):
        image = np.array(image)

    comic = ComicReader.read_comic("uploaded_comic", [image])

    base64_image = image_to_base64_np(image)

    xml_element = comic.to_xml()  # likely an Element object
    xml_bytes = ET.tostring(xml_element, encoding='utf-8')
    xml_str = xml_bytes.decode('utf-8')

    return JSONResponse({
        "image": base64_image,
        "annotations": xml_str  # now a JSON-serializable string
    })


@app.post("/api/process")
async def process_image(
    file: UploadFile = File(...),
    threshold: int = Form(200),
    blur: int = Form(5),
    morph: int = Form(5),
    min_size: int = Form(50)
):
    contents = await file.read()
    data = np.frombuffer(contents, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)

    panel_img = detect_panels(img, blur, threshold, morph, min_size)
    result_img = detect_speech_bubbles(panel_img)

    _, img_encoded = cv2.imencode('.png', result_img)

    return StreamingResponse(
        io.BytesIO(img_encoded.tobytes()),
        media_type='image/png'
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)