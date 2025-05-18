import random

from PIL import Image
import numpy as np
from transformers import AutoModel
import torch
import warnings
from torch.nn.modules.module import Module


class MagiModel:
    def __init__(self):
        warnings.filterwarnings("ignore",
                                message="for .*: copying from a non-meta parameter in the checkpoint to a meta parameter.*")
        self.model = AutoModel.from_pretrained("ragavsachdeva/magiv2", trust_remote_code=True).eval()

    def detect_objects(self,image, debug=False):
        images = [image]
        character_bank = {
            "images": [],
            "names": []
        }
        with torch.no_grad():
            page_results = self.model.do_chapter_wide_prediction(images, character_bank, use_tqdm=True,
                                                            do_ocr=False)
            print(page_results)
            if debug:
                for i, (image, page_result) in enumerate(zip(image, page_results)):
                    self.model.visualise_single_image_prediction(image, page_result, f"page_{random.randint(0, 10000)}.png")

        return page_results
