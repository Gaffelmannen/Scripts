#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import urllib.request
import time
import random

from bs4 import BeautifulSoup

debug = False
#selectedLeagueAndSource = "bundesliga-onlinebetting"
#selectedLeagueAndSource = "bundesliga-sportsgambler"
selectedLeagueAndSource = "premierleague-sportsgambler"

types = {
    "/images/injury/red.png" : "Suspended",
    "/images/injury/cross.png" : "Injured"
}

user_agents = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
]  

headers = {
    'authority': 'www.online-betting.me.uk',
    'user-agent': random.choice(user_agents),
    'method': 'POST',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'en',
    'cache-control':'max-age=0',
    'content-type' : 'application/x-www-form-urlencoded; charset=UTF-8'
    #'origin': 'https://www.online-betting.me.uk',
    #'referer' : 'https://www.online-betting.me.uk/injuries/germany-bundesliga-injuries-and-suspensions'
}

sources = {
    "httpbin" : "http://httpbin.org/status/200",
    "bundesliga-sportsgambler" : "https://www.sportsgambler.com/football/injuries-suspensions/germany-bundesliga/",
    "bundesliga-onlinebetting" : "https://www.online-betting.me.uk/injuries/germany-bundesliga-injuries-and-suspensions/",
    "premierleague-sportsgambler" : "https://www.sportsgambler.com/injuries/football/england-premier-league/",
    "premierleague-onlinebetting" : "https://www.online-betting.me.uk/injuries/english-premier-league-injuries-and-suspensions"
}

class BundesligaFantasyScraper:

    def __init__(self):
        self.pageurl = sources[selectedLeagueAndSource]

    def scrapeteams(self):
        teams = {}
        teamlist = {}
        response = requests.get(self.pageurl, headers=headers)
        if response.status_code != 200:
            print("Failed.")
            print("========")
            print(self.pageurl)
            print(response)

        soup = BeautifulSoup(response.text, "html.parser")
        selectedSource = selectedLeagueAndSource.split("-")[1]

        if selectedSource == "sportsgambler":
            teams = soup.findAll(attrs={"class" : "injuries-title"})
            for i in range(0, len(teams)):
                teamlist[i] = teams[i].contents[0].string
        elif selectedSource == "onlinebetting":
            teams = soup.findAll(attrs={"class" : "injury-container__team-name"})
            for i in range(0, len(teams)):
                teamlist[i] = teams[i].contents[0].string
        if debug:
            print(teamlist)

        if len(teamlist) == 0:
            print("Something went horribly wrong.")
        
        return teamlist

    def getinjuries(self):
        injured_reserve = []
        count = 0
        response = requests.get(self.pageurl, headers=headers)
        if debug:
            print(response.apparent_encoding)
            print(response.headers.get('Content-Type', ''))
        if response.status_code != 200:
            print("Failed.")
            print("========")
            print(response)
        
        soup = BeautifulSoup(response.text, "html.parser")
        selectedSource = selectedLeagueAndSource.split("-")[1]

        if  selectedSource == "sportsgambler":
            injuries = soup.find_all(attrs={"class" : "injury-block"})
            for injury in injuries:
                team = injury.find_all(attrs={"class" : "injuries-title"})[0].text
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
            print(selectedSource)
            tables = soup.findAll(attrs={"class" : "injury-table"})
            for i in range(0, len(tables)):
                rows = tables[i].findAll(attrs={"class" : "table-row"})
                for j in range(0, len(rows)):
                    columns = rows[j].text.split('\n')
                    for k in range(0, len(columns)):
                        if debug:
                            print("{0} :: {1}".format(k, columns[k]))
                        playerinfo = []
                        playerinfo.append(columns[2])
                        playerinfo.append(i)
                        playerinfo.append(columns[3])
                        playerinfo.append(columns[5])
                        playerinfo.append(columns[4])
                        injured_reserve.append(playerinfo)
                        break
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

            selectedSource = selectedLeagueAndSource.split("-")[1]

            if selectedSource == "onlinebetting":
                print("\tTeam:\t{}".format(teams[int(injury[1])]))
            else:
                print("\tTeam:\t{}".format(injury[1]))

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

    league = selectedLeagueAndSource.split("-")[0]

    if debug:    
        print("")
        print(league)
        print("")
    
    team_filename = "{0}-team.txt".format(league)
    prospects_filename = "{}-prospects.txt".format(league)
    players = {}

    print("Team:")
    with open(team_filename, "r") as f:
        players = [line.strip() for line in f]
    runit(players, "team")

    print("")
    print("Prospects:")

    with open(prospects_filename, "r") as f:
        players = [line.strip() for line in f]
    runit(players, "team prospects")

    print("")
    print("Done")
    sys.exit(0)
