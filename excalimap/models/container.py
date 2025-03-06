from config import Config
from models.mapobject import MapObject
from utils import Utils

class Container(MapObject):
    def __init__(self, text, color, position, content=None, object_id=None):
        super().__init__(text, object_id, content)
        self.color = color
        self.position = position

    def __repr__(self):
        return f"Container(text={self.text}, content={self.content})\n"

    def draw(self, x, y, color=None):
        elements = []
        start_x = x
        start_y = y
        end_x = x
        end_y = y

        # add padding arround container
        x = x + Config.padding_width
        y = y + Config.padding_height

        # draw container content
        for content in self.content:
            # draw each element vertically
            (element, element_end_x, element_end_y) = content.draw(x, y, self.color)
            Utils.flat_and_add_to_list(elements, element)
            y = element_end_y + Config.space_height
            if element_end_y > end_y:
                end_y = element_end_y
            if element_end_x > end_x:
                end_x = element_end_x

        element = [
            {
                "type": "rectangle",
                "id": f"{self.object_id}_title_rectangle",
                "x": start_x,
                "y": start_y - Config.container_title_height,
                "width": Config.container_title_width,
                "height": Config.container_title_height,
                "angle": 0,
                "strokeColor": self.color,
                "backgroundColor": self.color,
                "fillStyle": "solid",
                "strokeWidth": Config.container_line_width,
                "strokeStyle": Config.container_line,
                "roughness": 1,
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
                "x": start_x,
                "y": start_y - Config.container_title_height,
                "width": Config.container_title_width,
                "height": Config.container_title_height,
                "angle": 0,
                "strokeColor": Config.container_title_text_color,
                "backgroundColor": "transparent",
                "fillStyle": "solid",
                "strokeWidth": Config.container_line_width,
                "strokeStyle": Config.container_line,
                "fontSize": Config.title_font_size,
                "fontFamily": Config.font_family,
                "textAlign": "center",
                "verticalAlign": "middle",
                "containerId": f"{self.object_id}",
                "isDeleted": False, }
            ,{
                "type": "rectangle",
                "id": f"{self.object_id}",
                "x": start_x,
                "y": start_y,
                "width": end_x - start_x   + Config.padding_width,
                "height": end_y - start_y  + Config.padding_height,
                "angle": 0,
                "strokeColor": self.color,
                "backgroundColor": Config.container_background,
                "fillStyle": "solid",
                "strokeWidth": Config.container_line_width,
                "strokeStyle": Config.container_line,
                "roughness": 0,
                "opacity": 100,
                "roundness": None,
                "isDeleted": False,
                "locked": False
            }]
        Utils.flat_and_add_to_list(elements, element)
        return elements, end_x, end_y
