import math

from config import Config
from models.mapobject import MapObject
from utils import Utils
from models.icon import Icon
import os.path

class Command(MapObject):
    def __init__(self, text, comment=None, icon=None, tool_link=None, link=None, out=None, object_id=None, content=None, is_cve=False):
        super().__init__(text, object_id, content, out, is_cve)
        self.comment = comment
        self.icon = icon
        self.tool_link = tool_link
        self.link = link
        self.object_width = Config.command_width

    def __repr__(self):
        return f"Command(text={self.text}, comment={self.comment})\n"

    def draw(self, x, y):
        elements = []

        text_padding = 5
        # end_x and end_y will be minimum to element size

        calc_width = text_padding + Config.image_width + text_padding + math.ceil(Utils.len_text(self.text) * 8.75)
        self.object_width = max(self.object_width, calc_width)
        end_x = x + self.object_width
        end_y = y + Config.command_height

        # draw all the content
        elements, end_x, end_y = self.draw_child(elements, x, y, end_x, end_y)
        total_size = end_y - y
        center_y = y + total_size / 2
        title_y = center_y - Config.command_height / 2

        # draw out
        elements, out_end_x, out_end_y = self.draw_out(elements, y, center_y, total_size, end_x, end_y, Config.default_out_color)
        end_x = max(end_x, out_end_x)
        end_y = max(end_y, out_end_y)

        # images
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
            image_y_pos = title_y + (Config.command_height-Config.image_height)/2
            element_id = f"{image_hash}-{Utils.id_counter}"
            image_element = Icon.draw(x+ text_padding, image_y_pos, element_id ,image_hash, self.tool_link)
            Utils.id_counter += 1

            # add block to elements
            Utils.flat_and_add_to_list(elements, image_element)

            # add padding before image
            text_padding = text_padding + Config.image_width + text_padding

        # block

        # color
        background_color =  Config.command_background_color
        text_color = Config.text_color
        if self.is_cve:
            background_color = Config.cve_color
            text_color = Config.cve_text_color

        element = [{
                       "type": "rectangle",
                       "id": f"{self.object_id}",
                       "x": x,
                       "y": title_y,
                       "width": self.object_width,
                       "height": Config.command_height,
                       "angle": 0,
                       "strokeColor": Config.border_color,
                       "backgroundColor": background_color,
                       "fillStyle": "solid",
                       "strokeWidth": Config.command_line_width,
                       "strokeStyle": "solid",
                       "roughness": Config.command_roughness,
                       "opacity": 100,
                       "roundness": None,
                       "boundElements": [
                           {
                               "type": "text",
                               "id": f"{self.object_id + hash(self.text)}"
                           }
                       ],
                       "isDeleted": False,
                       "locked": False,
                       "link": self.link
                   },
                   {
                       "type": "text",
                       "text": self.text,
                       "id": f"{self.object_id + hash(self.text)}",
                       "x": x + text_padding,
                       "y": title_y,
                       "width": self.object_width-5,
                       "height": Config.command_height,
                       "angle": 0,
                       "strokeColor": text_color,
                       "backgroundColor": None,
                       "fillStyle": "solid",
                       "strokeWidth": Config.command_line_width,
                       "strokeStyle": "solid",
                       "fontSize": 16,
                       "fontFamily": Config.command_font_family,
                       "textAlign": "left",
                       "verticalAlign": "middle",
                       "containerId": f"{self.object_id}",
                       "isDeleted": False,
                       "link": self.link
                  }]

        Utils.flat_and_add_to_list(elements, element)

        return elements, end_x, end_y
