import math

from config import Config
from models.arrow import Arrow
from models.mapobject import MapObject
from utils import Utils

class Info(MapObject):
    def __init__(self, text, comment=None, icon=None, tool_link=None, link=None, out=None, object_id=None, content=None, is_cve=False):
        super().__init__(text, object_id, content, out, is_cve)
        self.comment = comment
        self.icon = icon
        self.tool_link = tool_link
        self.link = link
        self.object_width = Config.info_width

    def __repr__(self):
        return f"Info(text={self.text}, comment={self.comment})\n"

    def draw(self, x, y):
        elements = []
        # end_x and end_y will be minimum to title draw size
        calc_width = math.ceil(Utils.len_text(self.text) * 10)
        self.object_width = max(calc_width,self.object_width)

        end_x = x + self.object_width
        end_y = y + Config.info_height

        # draw all the content
        elements, end_x, end_y = self.draw_child(elements, x, y, end_x, end_y)
        total_size = end_y - y
        center_y = y + total_size / 2
        title_y = center_y - Config.info_height / 2
        # draw out
        elements, end_x, end_y = self.draw_out(elements, y, center_y, total_size, end_x, end_y, Config.default_out_color)

        # color
        background_color =  Config.info_background_color
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
                       "height": Config.info_height,
                       "angle": 0,
                       "strokeColor": Config.border_color,
                       "backgroundColor": background_color,
                       "fillStyle": "solid",
                       "strokeWidth": Config.info_line_width,
                       "strokeStyle": "solid",
                       "roughness": Config.info_roughness,
                       "opacity": 100,
                       "roundness": None,
                       "boundElements": [
                           {
                               "type": "text",
                               "id": f"{self.object_id + hash(self.text)}"
                           }
                       ],
                       "isDeleted": False,
                       "link": self.link,
                       "locked": False
                   },
                   {
                       "type": "text",
                       "text": self.text,
                       "id": f"{self.object_id + hash(self.text)}",
                       "x": x + 5,
                       "y": title_y,
                       "width": self.object_width-5,
                       "height": Config.info_height,
                       "angle": 0,
                       "strokeColor": text_color,
                       "backgroundColor": None,
                       "fillStyle": "solid",
                       "strokeWidth": Config.info_line_width,
                       "strokeStyle": "solid",
                       "fontSize": 16,
                       "fontFamily": Config.info_font_family,
                       "textAlign": "left",
                       "verticalAlign": "middle",
                       "containerId": f"{self.object_id}",
                       "link": self.link,
                       "isDeleted": False, }]

        Utils.flat_and_add_to_list(elements, element)
        return elements, end_x, end_y
