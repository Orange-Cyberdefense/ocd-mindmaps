from config import Config
from utils import Utils
from models.arrow import Arrow

class MapObject:
    def __init__(self, text, object_id=None, content=None, out=None, is_cve=False):
        self.object_id = object_id if object_id is not None else hash(text)
        self.text = text
        self.content = content or []
        self.out = out or []
        self.object_width = 0
        if is_cve is None:
            self.is_cve = False
        else:
            self.is_cve = is_cve

    def __repr__(self):
        return f"{self.__class__.__name__}(text={self.text}, object_id={self.object_id})\n"

    def draw_out(self, elements, y, center_y, total_size, end_x, end_y, color):
        cpt_out = 0
        nb_out = len(self.out)

        total_out_size = nb_out * Config.out_height + (nb_out - 1) * Config.out_space_height
        out_y = center_y - total_out_size / 2
        out_x = end_x + Config.out_space_width

        for out_item in self.out:
            if cpt_out == 0:
                out_element, out_end_x, out_end_y = out_item.draw_out_line(out_x, y, total_size)
                end_y = max(end_y, out_end_y)
                end_x = max(end_x, out_end_x)
                Utils.flat_and_add_to_list(elements, out_element)
                out_x = end_x + Config.out_space_width
                cpt_out += 1
            out_element, out_end_x, out_end_y = out_item.draw_out_element(out_x, out_y, color)
            out_y += Config.out_height + Config.out_space_height
            end_y = max(end_y, out_end_y)
            end_x = max(end_x, out_end_x)
            Utils.flat_and_add_to_list(elements, out_element)
        return elements, end_x, end_y

    def draw_child(self, elements, x, y, end_x, end_y):
        #           branch
        #           branch    branch
        # title     branch
        #           branch    branch
        #           branch
        nb_branches = len(self.content)
        total_size = nb_branches * Config.command_height + (nb_branches - 1) * Config.space_height
        center_y = y + total_size / 2
        title_y = center_y - Config.command_height / 2

        start_x = x
        start_y = y
        # child of title x position
        child_x = x + self.object_width + Config.space_width

        for content in self.content:
            (element, element_end_x, element_end_y) = content.draw(child_x, y)
            Utils.flat_and_add_to_list(elements, element)

            # next y will be last child y + space
            y = element_end_y + Config.space_height

            # new end_x will be the bigger element_end_x
            if element_end_x > end_x:
                end_x = element_end_x

            # new end_x will be the bigger element_end_y
            if element_end_y > end_y:
                end_y = element_end_y

        total_size = end_y - start_y
        center_y = start_y + total_size / 2
        title_y = center_y - Config.title_height / 2

        # draw arrow parent->child
        x = start_x
        y = start_y
        for content in self.content:
            # call draw but will not be drawed
            (element, element_end_x, element_end_y) = content.draw(child_x, y)
            start_element_id = f"{self.object_id}"  # title id
            end_element_id = element[0]['id']  # first element result
            arrow_from_x = x + self.object_width
            arrow_from_y = title_y + Config.title_height / 2
            arrow_to_x = child_x
            arrow_to_y = y + (element_end_y - y) / 2
            arrow = Arrow.draw_arrow_title_command(start_element_id, end_element_id, arrow_from_x, arrow_from_y,
                                                   arrow_to_x, arrow_to_y)
            y = element_end_y + Config.space_height
            Utils.flat_and_add_to_list(elements, arrow)

        return elements, end_x, end_y
