import re
import yaml

from config import Config
from models.command import Command
from models.info import Info
from models.out import Out
from models.title import Title
from models.container import Container
from utils import Utils


class ParserMD:

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
                ParserMD.parse_out_items(new_obj, out_item)

        if sub_item.get("content") is not None:
            for sub_sub_item in sub_item.get("content"):
                if new_obj is not None:
                    ParserMD.parse_sub_items(new_obj, sub_sub_item)
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
    def parse_md_to_objects(md_data, conf):
        # # load yml
        # with open("mindmap/conf.yml", "r", encoding="utf-8") as file:
        #     conf = yaml.safe_load(file)

        colors = conf['color_id']

        parent = {}
        level = 0
        id = 0
        for line in md_data:
            cve = False
            id = id + 1
            out = []
            url = None
            if ">>>" in line:
                id_out = 0
                outputs = line.split('>>>')[1:]
                column = 0
                for output in outputs:
                    for o in output.split('||'):
                        color = Config.default_out_color
                        if o.strip() in conf['out'].keys():
                            color_id = conf['out'][o.strip()]
                            color = colors[color_id]
                        text = o.strip().rstrip('\n')
                        text = Utils.split_text(text, Config.out_new_line_nb_chars)
                        new_out = Out(text=text, object_id=hash(f'{id}-{id_out}'), color=color)
                        # TODO dirty refactor
                        if column == 0:
                            out.append(new_out)
                        if column == 1:
                            if out[-1].out is not None:
                                out[-1].out.append(new_out)
                            else:
                                out[-1].out = [new_out]
                        if column == 2:
                            if out[0].out[-1].out is not None:
                                out[0].out[-1].out.append(new_out)
                            else:
                                out[0].out[-1].out = [new_out]
                        id_out += 1
                    column += 1
                line = line.split('>>>')[0]

            if "@CVE@" in line:
                cve = True
                line = line.replace('@CVE@','')

            if line.startswith('# '):
                match = re.search(r"# (.+)", line)
                color = Config.info_background_color
                text = match.group(1)
                if text.strip() in conf['container_color'].keys():
                    color_id = conf['container_color'][text.strip()]
                    color = colors[color_id]
                text = Utils.split_text(match.group(1), Config.container_new_line_nb_chars)
                container = Container(text=text, color=color, position=None, content=[], object_id=hash(f'{id}'))
                level = 1
                if level not in parent.keys():
                    parent[level] = container
                continue

            if line.startswith('## '):
                match = re.search(r"## (.+)", line)
                text = Utils.split_text(match.group(1), Config.title_new_line_nb_chars)
                title_obj = Title(text=text, is_cve=cve, content=[], out=out, object_id=hash(f'{id}'))
                level = 2
                parent[level] = title_obj
                parent[level-1].content.append(title_obj)
                continue

            if line.startswith('<!--'):
                match = re.search(r'<!--\s+cve\s+-->', line)
                if match:
                    parent[level].cve = True

            if line.strip().startswith('['):
                match = re.search(r"\((https?://[^\)]+)\)", line)
                if match:
                    url = match.group(1)
                    parent[level].link = url

            if line.strip().startswith('- `'):
                match = re.search(r"(\s*)- `(.+)`", line)
                spaces = len(match.group(1))
                level = int(3 + spaces/2)
                text = Utils.split_text(match.group(2), Config.command_new_line_nb_chars)

                # tool parsing
                cmd_to_parse = text.replace('proxychains ', '')
                tool = cmd_to_parse.split(' ')[0]
                icon = None
                tool_link = None
                if tool in conf['tools'].keys():
                    icon = conf['tools'][tool].get('icon')
                    tool_link = conf['tools'][tool].get('link')

                new_obj = Command(text=text,comment="",link=None,is_cve=cve, out=out, object_id=hash(f'{id}'), icon=icon, tool_link=tool_link)
                parent[level] = new_obj
                parent[level-1].content.append(new_obj)

            elif line.strip().startswith('- '):
                match = re.search(r"(\s*)- (.+)", line)
                spaces = len(match.group(1))
                level = int(3 + spaces / 2)
                text = Utils.split_text(match.group(2), Config.info_new_line_nb_chars)

                new_obj = Info(text=text,comment="",link=None,is_cve=cve, out=out, object_id=hash(f'{id}'))
                parent[level] = new_obj
                parent[level-1].content.append(new_obj)

        return container
