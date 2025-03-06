from config import Config
from models.mapobject import MapObject
from utils import Utils


class Out(MapObject):
    def __init__(self, text, content=None, out=None, object_id=None, color=None):
        super().__init__(text, object_id, content, out)
        self.object_width = Config.title_width
        self.color = color

    def __repr__(self):
        return f"{self.__class__.__name__}(text={self.text}, object_id={self.object_id})\n"

    def draw_out_line(self, x, y, height):
        end_x = x + Config.out_line_width
        end_y = y + height
        element = {
            "id": f"{self.object_id}-line",
            "type": "line",
            "x": x,
            "y": y,
            "width": Config.out_line_width,
            "height": height,
            "angle": 0,
            "strokeColor": Config.arrow_color,
            "backgroundColor": "#ffc9c9",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": None,
            "isDeleted": False,
            "boundElements": None,
            "link": None,
            "locked": False,
            "points": [
                [
                    0,
                    0
                ],
                [
                    Config.out_line_width/2,
                    height/2
                ],
                [
                    Config.out_line_width/2,
                    height/2
                ],
                [
                    0,
                    height
                ]
            ],
            "lastCommittedPoint": None,
            "startBinding": None,
            "endBinding": None,
            "startArrowhead": None,
            "endArrowhead": None
            }

        # "points": [
        #     [
        #         0,
        #         0
        #     ],
        #     [
        #         Config.out_line_width,
        #         0
        #     ],
        #     [
        #         Config.out_line_width,
        #         height
        #     ],
        #     [
        #         0,
        #         height
        #     ]
        # ],
        return element, end_x, end_y

    def draw_out_element(self, x, y, color):
        end_x = x + Config.out_width
        end_y = y + Config.out_height

        elements = []

        if self.out is not None:
            total_size = end_y - y
            center_y = y + total_size / 2
            element, child_end_x, child_end_y = self.draw_out(self.content, y, center_y, total_size, end_x, end_y, color)
            Utils.flat_and_add_to_list(elements, element)
            end_x = max(end_x, child_end_x)
            end_y = max(end_y, child_end_y)

        # element, child_end_x, child_end_y = self.draw_child(self.content, x, y, end_x, end_y)

        if self.color is None:
            self.color = color
        element = [{
            "type": "rectangle",
            "id": f"{self.object_id}{self.text}",
            "x": x,
            "y": y,
            "width": Config.out_width,
            "height": Config.out_height,
            "angle": 0,
            "strokeColor": "#1e1e1e",
            "backgroundColor": self.color,
            "fillStyle": "solid",
            "strokeWidth": Config.out_line_line_width,
            "strokeStyle": "solid",
            "roughness": Config.out_roughness,
            "opacity": 100,
            "roundness": None,
            "boundElements": [
                {
                    "type": "text",
                    "id": f"{self.object_id}{hash(self.text)}"
                }
            ],
            "isDeleted": False,
            "locked": False
        },
            {
                "type": "text",
                "text": self.text,
                "id": f"{self.object_id}{hash(self.text)}",
                "x": x + 5,
                "y": y,
                "width": Config.out_width - 5,
                "height": Config.out_height,
                "angle": 0,
                "strokeColor": Config.out_text_color,
                "backgroundColor": None,
                "fillStyle": "solid",
                "strokeWidth": Config.out_line_line_width,
                "strokeStyle": "solid",
                "fontSize": 16,
                "fontFamily": Config.out_font_family,
                "textAlign": "center",
                "verticalAlign": "middle",
                "containerId": f"{self.object_id}",
                "isDeleted": False, }]
        Utils.flat_and_add_to_list(elements, element)
        return elements, end_x, end_y