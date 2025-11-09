import argparse
import json
import os.path
import sys
import yaml
from config import Config
from models.maintitle import MainTitle
from parsermd import ParserMD
from utils import Utils
from types import SimpleNamespace

def fix_broken_container_ids(elements):
    id_map = {el.get("id"): el for el in elements if isinstance(el, dict) and "id" in el}
    MAX_DIST = 300

    for el in elements:
        if not isinstance(el, dict):
            continue
        cid = el.get("containerId")
        if not cid:
            continue

        parent = id_map.get(cid)
        if parent is None or parent.get("isDeleted") or parent.get("type") == "text":
            el["containerId"] = None
            continue

        ex, ey = el.get("x"), el.get("y")
        px, py = parent.get("x"), parent.get("y")
        if all(isinstance(v, (int, float)) for v in (ex, ey, px, py)):
            if abs(ex - px) > MAX_DIST or abs(ey - py) > MAX_DIST:
                el["containerId"] = None


def draw(matrix, main_title="", main_title_logo=""):
    elements = []
    x = end_x = 0
    y = 0

    # draw main title
    main_title = MainTitle(text=main_title, icon=main_title_logo)
    element, main_title_end_x, main_title_end_y = main_title.draw(x, y)
    Utils.flat_and_add_to_list(elements, element)

    main_title_end_y += Config.container_title_height + Config.padding_height

    # draw matrix
    for container_col in matrix:
        y = end_y = main_title_end_y
        for container in container_col:
            element, container_end_x, container_end_y = container.draw(x, y)
            Utils.flat_and_add_to_list(elements, element)
            end_y = max(end_y, container_end_y)
            end_x = max(end_x, container_end_x)
            y = end_y + Config.space_height * 2 + Config.container_title_height
        x = end_x + Config.space_width * 2

    fix_broken_container_ids(elements)

    appstate = {
        "gridSize": 20,
        "gridStep": 5,
        "gridModeEnabled": False,
        "viewBackgroundColor": Config.background_color
    }

    json_output = json.dumps({"type": "excalidraw",
                           "version": 2,
                           "source": "https://excalidraw.com",
                           "elements": elements,
                           "appState": appstate,
                           "files": Utils.images_catalog}, indent=2)
    return json_output.replace('\\\\n', '\\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='excalimap')
    parser.add_argument('-f', '--input_folder', help='folder containing the mindmap .md and conf.yml file', required=True)
    parser.add_argument('-t', '--theme', choices=['light', 'dark'], default='dark', help='Theme to use')
    parser.add_argument('-s','--style', choices=['classic', 'handraw'], default='classic', help='Style to use')
    parser.add_argument('-o', '--output', default='output/mindmap.excalidraw', help='output file')
    args = parser.parse_args()

    # set config
    Config.set_style(args.style)
    Config.set_theme(args.theme)

    mm_folder = args.input_folder
    conf_file = f'{mm_folder}/conf.yml'

    if not os.path.isfile(conf_file):
        print(f"configuration file not found : {conf_file}")
        sys.exit(1)

    try:
        with open(conf_file, "r", encoding="utf-8") as file:
            conf = yaml.safe_load(file)
    except Exception as e:
        print(f"Exception during configuration file loading {e}")
        sys.exit(1)

    try:
        file_matrix = conf['matrix']
    except Exception as e:
        print(f"Matrix not found {e}")
        sys.exit(1)

    containers_matrix = []
    for col in zip(*file_matrix):
        containers_col = []
        for md_file in col:
            if md_file != '':
                with open(f'{mm_folder}/{md_file}.md', "r", encoding="utf-8") as file:
                    print(f'[+] parse file : {md_file}')
                    data = file.readlines()
                    container_obj = ParserMD.parse_md_to_objects(data, conf)
                    containers_col.append(container_obj)
        containers_matrix.append(containers_col)

    json_output = draw(containers_matrix, conf['main_title'], conf['main_title_logo'])

    try:
        f = open(args.output, "w", encoding="utf-8")
        f.write(json_output)
        f.close()
        print(f'Mindmap result in file : {args.output}')
    except Exception as e:
        print(f"Exception during file creation {e}")
        sys.exit(1)
