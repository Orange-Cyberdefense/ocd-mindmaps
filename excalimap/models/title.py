from config import Config
from models.mapobject import MapObject
from models.command import Command
from models.arrow import Arrow
from utils import Utils

class Title(MapObject):
    def __init__(self, text, content=None, out=None, object_id=None, is_cve=False):
        super().__init__(text, object_id, content, out, is_cve)
        self.object_width = Config.title_width


    def __repr__(self):
        return f"Title(text={self.text}, content={self.content}, out={self.out})\n"

    def draw(self, x, y, color):
        elements = []
        # end_x and end_y will be minimum to title draw size
        end_x = x + Config.title_width
        end_y = y + Config.title_height

        # draw all the content
        elements, end_x, end_y = self.draw_child(elements, x, y, end_x, end_y)
        total_size = end_y - y
        center_y = y + total_size / 2
        title_y = center_y - Config.title_height / 2

        # draw out
        elements, end_x, end_y = self.draw_out(elements, y, center_y, total_size, end_x, end_y, color)

        title_element =[
            {
                "type": "rectangle",
                "id": f"{self.object_id}",
                "x": x,
                "y": title_y,
                "width": Config.title_width,
                "height": Config.title_height,
                "angle": 0,
                "strokeColor": Config.border_color,
                "backgroundColor": color,
                "fillStyle": "solid",
                "strokeWidth": 2,
                "strokeStyle": "solid",
                "roughness": Config.title_roughness,
                "opacity": 100,
                "roundness": None,
                "boundElements": [
                    {
                        "type": "text",
                        "id": f"{self.object_id + hash(self.text)}"
                    }
                ],
                "isDeleted": False,
                "locked": False
            },
            {
                "type": "text",
                "text": self.text,
                "id": f"{self.object_id + hash(self.text)}",
                "x": x,
                "y": title_y,
                "width": Config.title_width,
                "height": Config.title_height,
                "angle": 0,
                "strokeColor": Config.title_text_color,
                "backgroundColor": "transparent",
                "fillStyle": "solid",
                "strokeWidth": 2,
                "strokeStyle": "solid",
                "fontSize": Config.title_font_size,
                "fontFamily": Config.font_family,
                "textAlign": "center",
                "verticalAlign": "middle",
                "containerId": f"{self.object_id}",
                "isDeleted": False, }]

        Utils.flat_and_add_to_list(elements, title_element)
        return elements, end_x, end_y
