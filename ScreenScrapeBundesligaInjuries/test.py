#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytesseract as tess
from PIL import Image

def get_all_players():
    players=[]
    with open(r"data/allplayers.txt", "r") as file:
        for line in file:
            parts = line.split("	")
            if len(parts) > 5 and parts[2] != "Name":
                players.append(parts[2])
    return players

def read_players_from_image():
    players=[]
    img_path = "img/team.png"
    img = Image.open(img_path)
    text= tess.image_to_string(img)

    with open(r"data/das.txt", "w") as file:
        print(text, file=file)

    with open(r"data/das.txt", "r") as file:
        for line in file:
            line = line.strip()
            if len(line) > 1:
                parts = line.split(" ")
                for part in parts:
                    if len(part) > 3:
                        players.append(part)
                        #print(f"{len(part)}: --{part}--")
                #print(f":{len(line)}:-{line.strip()}-")
    return players

if __name__ == "__main__":
    confirmed_players=[]
    all_players = get_all_players()
    read_players = read_players_from_image()
    for p in read_players:
        for a in all_players:
            pa = a.split(" ")
            if p in pa and len(pa) > 1:
                confirmed_players.append(f"{pa[0]} {pa[1]}")
    #print(len(confirmed_players))
    for c in confirmed_players: print(c)