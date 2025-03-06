from models.command import Command
from models.info import Info
from models.out import Out
from models.title import Title
from models.container import Container

class ParserJson:

    @staticmethod
    def parse_sub_items(parent_item, sub_item):
        new_obj = None
        if sub_item["type"] == "command":
            new_obj = Command(
                text=sub_item["text"],
                comment=sub_item.get("comment"),
                icon=sub_item.get("icon"),
                tool_link=sub_item.get("tool_link"),
                link=sub_item.get("link"),
                out=sub_item.get("out"),
                is_cve=sub_item.get("is_cve")
            )
        if sub_item["type"] == "info":
            new_obj = Info(
                text=sub_item["text"],
                comment=sub_item.get("comment"),
                link=sub_item.get("link"),
                is_cve=sub_item.get("is_cve")
            )

        if sub_item["type"] == "command" or sub_item["type"] == "info":
            for out_item in sub_item.get("out", []):
                ParserJson.parse_out_items(new_obj, out_item)

        if sub_item.get("content") is not None:
            for sub_sub_item in sub_item.get("content"):
                if new_obj is not None:
                    ParserJson.parse_sub_items(new_obj, sub_sub_item)
        parent_item.content.append(new_obj)

    @staticmethod
    def parse_out_items(parent_item, sub_item):
        new_obj = None
        if sub_item["type"] == "out":
            new_obj = Out(
                text=sub_item.get("text"),
                object_id=sub_item.get("id"),
                color=sub_item.get("color")
            )
        parent_item.out.append(new_obj)

    @staticmethod
    def parse_json_to_objects(json_data):
        container = Container(
            text=json_data["text"],
            color=json_data["color"],
            position=json_data["position"],
            content=[]
        )

        for item in json_data["content"]:
            is_cve = False
            if "is_cve" in item.keys():
                is_cve = item["is_cve"]
            title_obj = Title(text=item["text"], is_cve=is_cve, content=[], out=[])

            for sub_item in item.get("content", []):
                ParserJson.parse_sub_items(title_obj, sub_item)

            for out_item in item.get("out", []):
                ParserJson.parse_out_items(title_obj, out_item)

            container.content.append(title_obj)

        return container
