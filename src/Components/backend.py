from src.Components.comic_reader import ComicReader
from fastapi import FastAPI
from src.Utils import image_utils as iu
from src.Utils import io_utils as iou
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
ComicReader = ComicReader()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Serve static files (e.g., images, xml) from a folder
STATIC_DIR = r"C:\Users\derra\PycharmProjects\ComicToNarration\Data"
app.mount("/static", StaticFiles(directory=r"C:\Users\derra\PycharmProjects\ComicToNarration\Data"), name="static")


@app.get("/get-comic")
def get_comic():
    image_name = "Starting_page.png"
    image_path = rf"C:\Users\derra\PycharmProjects\ComicToNarration\Data\{image_name}"

    image = iu.read_image(image_path)
    comic = ComicReader.read_comic("tester", [image])

    xml_name = f"{comic.name}.xml"
    xml_path = rf"C:\Users\derra\PycharmProjects\ComicToNarration\Data\{xml_name}"
    iou.export_as_xml(export_path=xml_path, comic=comic)

    return {
        "image_url": f"/static/{image_name}",
        "xml_url": f"/static/{xml_name}"
    }

