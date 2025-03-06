#!/bin/bash
version="2025.03"

if [ -z "$1" ]; then
    echo "Error : need mindmap md folder"
    echo "Usage : $0 <argument>"
    exit 1
fi
name=$(echo "$1" | sed 's|/|_|g')
python3 main.py -f $1 -t dark  -s classic -o output/${name}_dark_classic_${version}.excalidraw
#python3 main.py -f $1 -t light -s classic -o output/${name}_light_classic_${version}.excalidraw
#python3 main.py -f $1 -t dark  -s handraw -o output/${name}_dark_handraw_${version}.excalidraw
#python3 main.py -f $1 -t light -s handraw -o output/${name}_light_handraw_${version}.excalidraw
