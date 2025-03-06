from config import Config

class Arrow:

    @staticmethod
    def draw_arrow_title_command(start, end, x, y, x_end, y_end):
        element = {
            "id": f"{hash(start + end)}",
            "type": "arrow",
            "x": x,
            "y": y,
            "width": abs(x_end - x),
            "height": abs(y_end - y),
            "angle": 0,
            "strokeColor": Config.arrow_color,
            "backgroundColor": "#a5d8ff",
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
                    (x_end - x) / 2,
                    0
                ],
                [
                    (x_end - x) / 2,
                    y_end - y
                ],
                [
                    x_end - x,
                    y_end - y
                ]
            ],
            "lastCommittedPoint": None,
            "startBinding": {
                "elementId": start,
                "gap": 5,
                "fixedPoint": [0, 0]
            },
            "endBinding": {
                "elementId": end,
                "focus": 0,
                "gap": 5,
                "fixedPoint": [0, 0]
            },
            "startArrowhead": None,
            "endArrowhead": Config.title_command_arrow_end,
            "elbowed": True,
            "fixedSegments": None,
            "startIsSpecial": None,
            "endIsSpecial": None
        }
        return element
