#!/bin/bash

# first build docker image
# https://github.com/realazthat/excalidraw-brute-export-cli/tree/master?tab=readme-ov-file#-docker-image
# need also convert

if [ -z "$1" ]; then
    echo "Error : need mindmap md folder"
    echo "Usage : $0 <argument>"
    exit 1
fi

echo "generate all excalidraw files"
./gen_all.sh $1

echo "generate all svg files"
cd output/
maps=`ls *.excalidraw`
rm -rf svg
mkdir svg
sudo chmod -R 777 svg/

for map in $maps
do
  sudo docker run --rm --tty -v "${PWD}:/data" my-excalidraw-brute-export-cli-image \
    -i ./$map \
    --background 1 \
    --embed-scene 0 \
    --dark-mode 0 \
    --scale 1 \
    --format svg \
    -o "./svg/$map.svg"
  sudo docker run --rm --tty -v "${PWD}:/data" my-excalidraw-brute-export-cli-image \
    -i ./$map \
    --background 1 \
    --embed-scene 0 \
    --dark-mode 0 \
    --scale 1 \
    --format png \
    -o "./svg/$map.png"
done
sudo chmod 755 svg/
sudo chmod 644 svg/*
sudo chown -R $(id -u):$(id -g) svg/

cd svg/
for map in $maps
do
  mogrify -resize 500x ${map}.png
  mv ${map}.png thumbnail_${map}.png
done
