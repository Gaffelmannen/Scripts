#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pytesseract as tess
from PIL import Image

title =  r"""
    ______            __
   / ____/___ _____  / /_____ ________  __
  / /_  / __ `/ __ \/ __/ __ `/ ___/ / / /
 / __/ / /_/ / / / / /_/ /_/ (__  ) /_/ /
/_/    \__,_/_/ /_/\__/\__,_/____/\__, /
                                 /____/
    ______            __  __          ____
   / ____/___  ____  / /_/ /_  ____ _/ / /
  / /_  / __ \/ __ \/ __/ __ \/ __ `/ / /
 / __/ / /_/ / /_/ / /_/ /_/ / /_/ / / /
/_/    \____/\____/\__/_.___/\__,_/_/_/

   _____
  / ___/______________ _____  ___  _____
  \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
 ___/ / /__/ /  / /_/ / /_/ /  __/ /
/____/\___/_/   \__,_/ .___/\___/_/
                    /_/
        """

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