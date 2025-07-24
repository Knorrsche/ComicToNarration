import base64
import io
import os

import numpy as np
import xml.etree.ElementTree as ET

from src.Utils import image_utils as iu
from src.Classes.comic import Comic
from src.Classes.page import Page,PageType
from src.Classes.panel import Panel
from src.Classes.speech_bubble import SpeechBubble,SpeechBubbleType
from src.Classes.entity import Entity
from Models import magi
from PIL import Image

class ComicReader:
    def __init__(self):
        self.model = magi.MagiModel()

    def read_comic(self, name, images):
        comic = Comic(name=name, page_pairs=[])
        pages = []

        for i, image in enumerate(images):
            page = Page(
                page_index=i + 1,
                page_type=PageType(3),
                page_image=image
            )
            self.handle_detect_objects(page)

            if i == 0:
                comic.page_pairs.append((None,page))
            else:
                pages.append(page)

        for i in range(0, len(pages), 2):
            if i + 1 < len(pages):
                page_pair = (pages[i], pages[i + 1])
            else:
                page_pair = (pages[i],None)
            comic.page_pairs.append(page_pair)

        return comic

    def handle_panels(self, panel_list, page, y_tolerance=50):
        panels = []

        for panel in panel_list:
            bbox = iu.x1y1x2y2_to_xywh(panel)
            print(bbox)
            panel_image = iu.image_from_bbox(page.page_image, bbox)

            description = ""
            panel = Panel(description, bbox, panel_image)
            panel.page_id = page.page_index
            panel.descriptions.append(panel.description)
            panels.append(panel)

            sorted_panels = sorted(
                panels,
                key=lambda p: (p.bounding_box['y'] // y_tolerance, p.bounding_box['x'])
            )
            page.panels = sorted_panels

    def handle_entities(self, entity_list, character_cluster_labels, page):
        for i, entity_ in enumerate(entity_list):
            bbox = iu.x1y1x2y2_to_xywh(entity_)
            entity = Entity(bbox)
            entity.named_entity_id = character_cluster_labels[i]
            entity.image = iu.image_from_bbox(page.page_image, bbox)

            for panel in page.panels:
                best_panel = None
                highest_iou = 0

                for panel in page.panels:
                    iou_value = iu.calculate_iou(panel.bounding_box, entity.bounding_box)

                    if iou_value > highest_iou:
                        highest_iou = iou_value
                        best_panel = panel

                if best_panel is not None and highest_iou > 0:
                    if not any(iu.calculate_iou(existing_entity.bounding_box, entity.bounding_box) > 0.6
                               for existing_entity in best_panel.entities):
                        best_panel.entities.append(entity)

                for panel in page.panels:
                    entities = panel.entities
                    panel.entities = sorted(entities,
                                            key=lambda p: ((p.bounding_box['y'] - p.bounding_box['height']),
                                                           (p.bounding_box['x']) - p.bounding_box['width']))

    def handle_speechbubbles(self, speechbubble_list, is_essential_text, page):
        essential_counter = 0
        for i, speechbubble in enumerate(speechbubble_list):
            bbox = iu.x1y1x2y2_to_xywh(speechbubble)
            speech_bubble_image = iu.image_from_bbox(page.page_image, bbox)
            description = ""
            speech_bubble = SpeechBubble(SpeechBubbleType.SPEECH, description, bbox, speech_bubble_image)
            speech_bubble.type = 'dialogue'
            speech_bubble.person_list = []

            if is_essential_text[i]:
                speech_bubble.speaker_id = 1
                essential_counter += 1
            else:
                speech_bubble.speaker_id = 0

            max_overlap = 0
            best_panel = None
            for panel in page.panels:
                overlap = iu.calculate_overlap_percentage(speech_bubble.bounding_box, panel.bounding_box)
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_panel = panel

            if best_panel:
                best_panel.speech_bubbles.append(speech_bubble)

        for panel in page.panels:
            speech_bubbles = panel.speech_bubbles
            panel.speech_bubbles = sorted(
                speech_bubbles,
                key=lambda p: ((p.bounding_box['y'] - p.bounding_box['height']),
                               (p.bounding_box['x'] - p.bounding_box['width']))
            )

    def handle_detect_objects(self, page):
        data = self.model.detect_objects(image=page.page_image)
        panel_list = data[0]['panels']
        speechbubble_list = data[0]['texts']
        entity_list = data[0]['characters']
        tails = data[0]['tails']
        text_character_associations = data[0]['text_character_associations']
        text_tail_associations = data[0]['text_tail_associations']
        character_cluster_labels = data[0]['character_cluster_labels']
        is_essential_text = data[0]['is_essential_text']
        character_names = data[0]['character_names']

        self.handle_panels(panel_list, page)
        self.handle_entities(entity_list, character_cluster_labels, page)
        self.handle_speechbubbles(speechbubble_list, is_essential_text, page)


def read_comics():

    comic = ComicReader()
    comic_dir = r"C:\Users\derra\PycharmProjects\ComicToNarration\Data\comics"
    for root, dirs, files in os.walk(comic_dir):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            images = []

            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)

                if os.path.isfile(file_path):
                    try:
                        img = Image.open(file_path).convert("RGB")
                        image = np.array(img)
                        images.append(image)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

            comic_reader = ComicReader()
            comic = comic_reader.read_comic(dir_path, images)

            xml_element = comic.to_xml()
            xml_bytes = ET.tostring(xml_element, encoding='utf-8')
            xml_str = xml_bytes.decode('utf-8')

            with open(os.path.join(root, f"{dir_name}.xml"), "w", encoding="utf-8") as f:
                f.write(xml_str)