#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import urllib.request
import time

from bs4 import BeautifulSoup

debug = False
#selectedSource = "onlinebetting"
selectedSource = "sportsgambler"

#squad = {}

types = {
    "/images/injury/red.png" : "Suspended",
    "/images/injury/cross.png" : "Injured"
}

sources = {
    "httpbin" : "http://httpbin.org/status/200",
    "sportsgambler" : "https://www.sportsgambler.com/football/injuries-suspensions/germany-bundesliga/",
    "onlinebetting" : "https://www.online-betting.me.uk/injuries/germany-bundesliga-injuries-and-suspensions/"
}

class BundesligaFantasyScraper:

    def __init__(self):
        self.pageurl = sources[selectedSource]

    def scrapeteams(self):
        teams = {}
        teamlist = {}
        response = requests.get(self.pageurl)
        if response.status_code != 200:
            print("Failed.")
            print("========")
            print(self.pageurl)
            print(response)
        soup = BeautifulSoup(response.text, "html.parser")
        if selectedSource == "sportsgambler":
            teams = soup.findAll(attrs={"class" : "injuries-title"})
            for i in range(0, len(teams)):
                teamlist[i] = teams[i].contents[0].string
        elif selectedSource == "onlinebetting":
            teams = soup.find_all('h3')
            for i in range(0, len(teams)):
                teamlist[i] = teams[i].contents[0].string
        if debug:
            print(teamlist)
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
        if  selectedSource == "sportsgambler":
            injuries = soup.find_all(attrs={"class" : "injury-block"})
            for injury in injuries:
                team = injury.find_all(attrs={"class" : "injuries-title"})[0].text
                #print(team)
                rows = injury.findAll(attrs={"class" : "inj-row"})
                for i in range(0, len(rows)):
                    playerinfo = []
                    playerinfo.append(rows[i].findAll(attrs={"class" : "inj-player"})[0].text)
                    playerinfo.append(team)
                    playerinfo.append(rows[i].findAll(attrs={"class" : "inj-info"})[0].text)
                    playerinfo.append(rows[i].findAll(attrs={"class" : "inj-return h-sm"})[0].text)
                    injury_type = "Unkown"
                    playerinfo.append(injury_type)
                    if debug:
                        print(playerinfo)
                    injured_reserve.append(playerinfo)
        elif selectedSource == "onlinebetting":
            tables = soup.findAll(attrs={"class" : "injurytable"})
            for i in range(0, len(tables)):
                rows = tables[i]
                for row in rows:
                    columns = row.findAll('td')
                    playerinfo = []
                    try:
                        playerinfo.append(columns[1].text)
                        playerinfo.append(i)
                        playerinfo.append("Incident date - {}" \
                            .format(columns[3].text))
                        playerinfo.append(columns[4].text)
                        playerinfo.append(columns[2].text)
                        injured_reserve.append(playerinfo)
                        if debug:
                            print(columns[1].text)
                            print(columns[2].text)
                            print(columns[3].text)
                    except:
                        pass
                    if debug:
                        print("")
        return injured_reserve

def runit(squad, listtype):
    bfs = BundesligaFantasyScraper()
    teams = bfs.scrapeteams()
    injuries = bfs.getinjuries()
    number_of_injuries_in_squad = 0
    for injury in injuries:
        if injury[0] in squad:
            print("Note")
            print("\tPlayer:\t{}".format(injury[0]))
            print("\tTeam:\t{}".format(injury[1]))
            #print("\tTeam:\t{}".format(teams[int(injury[1])]))
            print("\tInfo:\t{}".format(injury[2]))
            print("\tReturn:\t{}".format(injury[3]))
            print("\tType:\t{}".format(injury[4]))
            number_of_injuries_in_squad += 1
    if number_of_injuries_in_squad > 0:
        print("There are a total of {} injuries in the {}." \
            .format(number_of_injuries_in_squad, listtype))
    else:
        print("No injuries in squad.")

if __name__ == "__main__":
    print("Begin Check")
    print("")

    players = {}

    print("Team:")
    with open("team.txt", "r") as f:
        players = [line.strip() for line in f]
    runit(players, "team")

    print("")
    print("Prospects")

    with open("prospects.txt", "r") as f:
        players = [line.strip() for line in f]
    runit(players, "team prospects")

    print("")
    print("Done")
    sys.exit(0)
