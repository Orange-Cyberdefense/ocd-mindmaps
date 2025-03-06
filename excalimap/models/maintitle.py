import math

from config import Config
from models.mapobject import MapObject
from utils import Utils
from models.icon import Icon
import os.path

class MainTitle(MapObject):

    def __init__(self, text, icon=None):
        super().__init__(text, 'main_title', content=None, out=None, is_cve=None)
        self.icon = icon
        self.object_width = Config.main_title_width

    def __repr__(self):
        return f"MainTitle(text={self.text})\n"

    def draw(self, x, y):
        elements = []

        text_padding = 20
        end_x = x + self.object_width
        end_y = y + Config.main_title_height

        center_y = y + Config.main_title_height / 2

        # title image
        file_path = f'{Config.icon_path}/cmd.png'
        if self.icon is not None:
            file_path = f'{Config.icon_path}/{self.icon}.png'
        image_hash = hash(file_path)
        if os.path.isfile(file_path):
            if image_hash not in Utils.images_catalog.keys():
                base64_image = Icon.image_to_base64(file_path, (Config.image_width,Config.image_height) )
                file_element = Icon.file_element(image_hash, base64_image)
                # add file to images list
                Utils.images_catalog[image_hash] = file_element

            # add image element block
            image_y_pos = center_y - Config.main_image_height/2
            element_id = f"{image_hash}-{Utils.id_counter}"
            image_element = Icon.draw(x+ text_padding, image_y_pos, element_id ,image_hash, None, Config.main_image_width, Config.main_image_height)

            # add block to elements
            Utils.flat_and_add_to_list(elements, image_element)

            # add padding before image
            text_padding = text_padding + Config.main_image_width + text_padding

        element = [{
                       "type": "rectangle",
                       "id": f"{self.object_id}",
                       "x": x,
                       "y": y,
                       "width": self.object_width,
                       "height": Config.main_title_height,
                       "angle": 0,
                       "strokeColor": Config.main_title_border_color,
                       "backgroundColor": None,
                       "fillStyle": "solid",
                       "strokeWidth": Config.main_title_line_width,
                       "strokeStyle": Config.main_title_line,
                       "roughness": Config.main_title_roughness,
                       "opacity": 100,
                       "roundness": None,
                       "boundElements": [
                           {
                               "type": "text",
                               "id": f"{str(self.object_id) + str(hash(self.text))}"
                           }
                       ],
                       "isDeleted": False,
                       "locked": False,
                       "link": None
                   },
                   {
                       "type": "text",
                       "text": self.text,
                       "id": f"{str(self.object_id) + str(hash(self.text))}",
                       "x": x + text_padding,
                       "y": y,
                       "width": self.object_width-5,
                       "height": Config.main_title_height,
                       "angle": 0,
                       "strokeColor": Config.text_color,
                       "backgroundColor": None,
                       "fillStyle": "solid",
                       "strokeWidth": Config.main_title_line_width,
                       "strokeStyle": "solid",
                       "fontSize": Config.main_title_font_size,
                       "fontFamily": Config.main_title_font_family,
                       "textAlign": "left",
                       "verticalAlign": "middle",
                       "containerId": f"{self.object_id}",
                       "isDeleted": False,
                       "link": None
                  }]

        Utils.flat_and_add_to_list(elements, element)

        return elements, end_x, end_y