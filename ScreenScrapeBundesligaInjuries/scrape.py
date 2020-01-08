#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import urllib.request
import time

from bs4 import BeautifulSoup

debug = False

squad = {  
    "Robert Lewandowski",
    "Timo Werner",
    "Alassane Plea",
    "Serge Gnabry",
    "Jadon Sancho",
    "Marcel Sabitzer",
    "Amine Harit",
    "Joshua Kimmich",
    "Christain Günter",
    "Marvin Friedrich",
    "Yann Sommer" 
}

types = {
    "/images/injury/red.png" : "Suspended",
    "/images/injury/cross.png" : "Injured"
}

sources = {
    "httpbin" : "http://httpbin.org/status/200",
    "sportsgambler" : "https://www.sportsgambler.com/football/injuries-suspensions/germany-bundesliga/"
}

class BundesligaFantasyScraper:
    
    def __init__(self):
        self.pageurl = sources["sportsgambler"]

    def scrapeteams(self):
        teamlist = {}
        response = requests.get(self.pageurl)
        if response.status_code != 200:
            print("Failed.")
            print("========")
            print(response)
        soup = BeautifulSoup(response.text, "html.parser")
        teams = soup.findAll(attrs={"class" : "injuries-title"})
        for i in range(0, len(teams)):
            teamlist[i] = teams[i].contents[0].string
        return teamlist
    
    def getinjuries(self):
        injured_reserve = []
        count = 0
        response = requests.get(self.pageurl)
        if debug:
            print(response.apparent_encoding)
            print(response.headers.get('Content-Type', ''))
        if response.status_code != 200:
            print("Failed.")
            print("========")
            print(response)
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.findAll(attrs={"class" : "home-team"})
        for i in range(0, len(tables)):
            table_body = tables[i].find_all("tbody")
            players = table_body[0]
            for player in players:
                if player == None:
                    continue
                playerinfo = []
                player = BeautifulSoup(str(player), "html.parser")
                data = player.findAll("a")
                if len(data) == 0:
                    continue
                playerinfo.append(data[1].string)
                playerinfo.append(i)
                playerinfo.append(data[2].string)
                playerinfo.append(data[3].string)
                injury_type = "Unkown"
                if len(data[0].findAll("img")) > 0:
                    t = data[0].img["src"]
                    if t in types:
                        injury_type = types[t]
                playerinfo.append(injury_type)

                injured_reserve.append(playerinfo)
        return injured_reserve

def runit():
    bfs = BundesligaFantasyScraper()
    teams = bfs.scrapeteams()
    injuries = bfs.getinjuries()
    number_of_injuries_in_squad = 0
    for injury in injuries:
        if injury[0] in squad:
            print("Note")
            print("\tPlayer:\t{}".format(injury[0]))
            print("\tTeam:\t{}".format(teams[int(injury[1])]))
            print("\tInfo:\t{}".format(injury[2]))
            print("\tReturn:\t{}".format(injury[3]))
            print("\tType:\t{}".format(injury[4]))
            number_of_injuries_in_squad += 1
    if number_of_injuries_in_squad > 0:
        print("There are a total of {} injuries in squad." \
            .format(number_of_injuries_in_squad))
    else:
        print("No injuries in squad.")

if __name__ == "__main__":
    print("Begin Check")
    runit()
    print("Done")
    sys.exit(0)
