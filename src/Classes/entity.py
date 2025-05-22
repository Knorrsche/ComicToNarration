from typing import Tuple
import xml.etree.ElementTree as eT


class Entity:

    def __init__(self, bounding_box: Tuple[float, float, float, float]):
        self.bounding_box = bounding_box
        self.image = None
        self.named_entity_id = 0
        self.tags = []
        self.active_tag = True

    def to_xml(self):
        element = eT.Element('Entity')
        #TODO: Implement naming system
        eT.SubElement(element, 'Name').text = "Placeholder"
        eT.SubElement(element,'Named_Entity_Id').text = str(self.named_entity_id)
        eT.SubElement(element, 'Active_Tag').text = str(self.active_tag)
        bbox = eT.SubElement(element, 'BoundingBox')
        bbox.text = ','.join(f"{key}:{value}" for key, value in self.bounding_box.items())

        tags_element = eT.SubElement(element, 'Tags')

        for tag, confidence in self.tags:
            tag_element = eT.SubElement(tags_element, 'Tag')
            eT.SubElement(tag_element, 'Label').text = str(tag)
            eT.SubElement(tag_element, 'Value').text = str(confidence)

        return element


