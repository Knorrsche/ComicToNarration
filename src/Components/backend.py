from src.Components.comic_reader import ComicReader
from fastapi import FastAPI
from src.Utils import image_utils as iu
from src.Utils import io_utils as iou

app = FastAPI()

comic_reader = ComicReader()

@app.get("/")
def read_root():
    image = iu.read_image(r"C:\Users\derra\PycharmProjects\ComicToNarration\Data\Edgecase_bubble_no_entity.png")
    comic = comic_reader.read_comic("tester", [image])
    iou.export_as_xml(export_path=rf"C:\Users\derra\PycharmProjects\ComicToNarration\Data\{comic.name}.xml",comic=comic)
    return {"message": "Comic processed"}
