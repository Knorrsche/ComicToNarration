from .page import Page
from typing import Optional, List
import xml.etree.ElementTree as eT
import numpy as np
import cv2


class Comic:
    def __init__(self, name: str,page_pairs: List[tuple[Optional[Page], Optional[Page]]]):
        self.name = name
        self.page_pairs = page_pairs
        self.scenes = []
        self.scene_data = ''

    def to_narrative(self) -> str:
        script = ''
        white_spaces = '     '
        for i,scene in enumerate(self.scenes):
            script +=  f'Scene {i+1} \n'
            for j,panel in enumerate(scene):
                script += white_spaces + f'Panel {j+1}: {panel.description}\n'
                for speechbubble in panel.speech_bubbles:
                    script += white_spaces * 2 + speechbubble.get_string() + '\n'
        return script

    def to_xml(self):
        element = eT.Element('Comic')
        eT.SubElement(element, 'Name').text = self.name

        page_pairs_element = eT.SubElement(element, 'PagePairs')
        for pair in self.page_pairs:
            pair_element = eT.SubElement(page_pairs_element, 'PagePair')
            if pair[0] is not None:
                pair_element_left = eT.SubElement(pair_element, 'LeftPage')
                pair_element_left.append(pair[0].to_xml())
            if pair[1] is not None:
                pair_element_right = eT.SubElement(pair_element, 'RightPage')
                pair_element_right.append(pair[1].to_xml())

        return element

    def reset_scenes(self):
        for scene in self.scenes:
            for panel in scene:
                panel.starting_tag = False
                panel.scene_id = 0
        self.scenes = []

    def reset_entities(self):
        for scene in self.scenes:
            for panel in scene:
                panel.entities.clear()

    def get_scene_images(self):
        comic_pages = []
        scene_images = []
        for page_pair in self.page_pairs:
            for page in page_pair:
                if page is not None and page not in comic_pages:
                    comic_pages.append(page)

        for idx, scene in enumerate(self.scenes):
            scene_pages = []
            used_pages = []

            for panel in scene:
                if comic_pages[panel.page_id]not in used_pages:
                    page_image = comic_pages[panel.page_id].page_image

                    if page_image.shape[2] == 3:
                        page_image = cv2.cvtColor(page_image, cv2.COLOR_RGB2BGR)

                    page_image = page_image.astype(np.uint8)

                    scene_pages.append(page_image)
                    used_pages.append(comic_pages[panel.page_id])

            if scene_pages:
                try:
                    scene_image = np.hstack(scene_pages)
                    scene_images.append((scene_image,used_pages))
                    cv2.imwrite(f'scene_{idx}.png', scene_image)
                except ValueError as e:
                    print(f"Error stacking images for scene {idx}: {e}")
        return scene_images


