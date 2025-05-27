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
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
@app.post("/segment-panels")
async def segment_panels_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image_np = np.array(image)

    original_img = image

    gray = rgb2gray(image_np)

    edges = canny(gray)

    thick_edges = dilation(edges, square(3))
    thick_edges = dilation(thick_edges, square(3))

    filled = ndi.binary_fill_holes(thick_edges)

    label_image = label(filled)
    labeled_img_np = np.zeros_like(image_np)
    for region in regionprops(label_image):
        minr, minc, maxr, maxc = region.bbox
        rr, cc = rectangle_perimeter(start=(minr, minc), end=(maxr, maxc), shape=label_image.shape)
        labeled_img_np[rr, cc] = [255, 0, 0]  # Red box
    labeled_img = Image.fromarray(labeled_img_np)

    results = {
        "original": image_to_base64_pil(original_img),
        "grayscale": image_to_base64_np((gray * 255).astype(np.uint8)),
        "edges": image_to_base64_np(edges),
        "dilated_edges": image_to_base64_np(thick_edges),
        "filled": image_to_base64_np(filled),
        "labeled": image_to_base64_pil(labeled_img),
    }

    return JSONResponse(results)
