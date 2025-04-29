#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import io
import re
import sys
import json
import time
import random

from colorama import Fore, Back, Style

import simple_term_menu as stm
from prettytable import PrettyTable

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from fake_useragent import UserAgent

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

debug = False

separator = "<>"

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
    'user-agent': UserAgent().random, #random.choice(user_agents),
    'method': 'POST',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'en',
    'cache-control':'max-age=0',
    'content-type' : 'application/x-www-form-urlencoded; charset=UTF-8'
}

sources = {
    "httpbin" : "http://httpbin.org/status/200",
    "bundesliga-sportsgambler" : "https://www.sportsgambler.com/football/injuries-suspensions/germany-bundesliga/",
    "bundesliga-onlinebetting" : "https://www.online-betting.me.uk/injuries/germany-bundesliga-injuries-and-suspensions/",
    "bundesliga-betinf" : "https://www.betinf.com/germany_injured.htm",
    "premierleague-sportsgambler" : "https://www.sportsgambler.com/injuries/football/england-premier-league/",
    "premierleague-onlinebetting" : "https://www.online-betting.me.uk/injuries/english-premier-league-injuries-and-suspensions",
    "premierleague-betinf" : "https://www.betinf.com/england_injured.htm",
    "bundesliga-stats-goals" : "https://www.bundesliga.com/en/bundesliga/stats/players/goals",
    "bundesliga-stats-assists" : "https://www.bundesliga.com/en/bundesliga/stats/players/assists",
    "bundesliga-stats-duelswon" : "https://www.bundesliga.com/en/bundesliga/stats/players/duels-won",
    "bundesliga-stats-crosses" : "https://www.bundesliga.com/en/bundesliga/stats/players/crosses",
    "bundesliga-stats-passes" : "https://www.bundesliga.com/en/bundesliga/stats/players/passes",
    "bundesliga-stats-intensiveruns" : "https://www.bundesliga.com/en/bundesliga/stats/players/intensive-runs",
    "bundesliga-stats-saves" : "https://www.bundesliga.com/en/bundesliga/stats/players/goalkeeper-saves"
}

stat_headers = [
    "Goals",
    "Assists",
    "Shots",
    "Shots against post and bar",
    "Top speed (km/h)",
    "Own goals",
    "Penalties",
    "Penalties scored",
    "Successful passes from open play (%)",
    "Aerial duels won",
    "Crosses from open play",
    "Yellow cards",
    "Cards",
    "Fouls committed",
    "Distance covered (km)",
    "Sprints",
    "Intensive runs",
    "Shots saved"
]

class FantasyFootballScraper:

    CONST_MAX_AGE_OF_DATA_FILE_IN_MINUTES = 60
    
    def __init__(self, sls, url=None, filename=None):
        self.source = sls.split("-")[1]

        if url == None:
            try:
                self.pageurl = sources[sls]
            except:
                self.pageurl = None
        else:
            self.pageurl = url

        if filename == None:
            self.tempfilename = "temp/temp-{}.txt".format(sls)
        else:
            self.tempfilename = "temp/temp-{}.txt".format(filename)

        # FireFox Options
        self.FIREFOX_OPTS = Options()
        self.FIREFOX_OPTS.log.level = "trace"
        self.FIREFOX_OPTS.add_argument("--headless")
        self.FIREFOX_OPTS.set_preference("browser.cache.disk.enable", False)
        self.FIREFOX_OPTS.set_preference("browser.cache.memory.enable", False)
        self.FIREFOX_OPTS.set_preference("browser.cache.offline.enable", False)
        self.FIREFOX_OPTS.set_preference("network.http.use-cache", False)
        self.FIREFOX_OPTS.set_preference("javascript.enabled", True)
        self.FIREFOX_OPTS.set_preference("general.useragent.override", UserAgent().random)

        # Gecko
        self.GECKODRIVER_LOG = "logs/geckodriver.log"

    def _save_to_file(self, content):
        f = open(self.tempfilename, "w", encoding="utf-8")
        f.write(content)
        f.close()

    def _read_from_file(self):
        text = None
        with io.open(self.tempfilename, "r", encoding="utf8") as f:
            text = f.read()
        return text
    
    def read_bundesliga_stats(self, url, filename):
        driver = None
        stats = []
        read_from_remote = True

        self.pageurl = url
        self.tempfilename = "temp/temp-{}.txt".format(filename)

        if os.path.exists(self.tempfilename):
            fileLastUpdatedTime = os.stat(self.tempfilename).st_mtime
            ageOfFileInMinutes = (time.time() - fileLastUpdatedTime) / 240
            if ageOfFileInMinutes < self.CONST_MAX_AGE_OF_DATA_FILE_IN_MINUTES:
                read_from_remote = False
        
        if not read_from_remote:
            with open(self.tempfilename) as f:
                encoded_str = json.load(f)
                return encoded_str

        service = Service(
            service_log_path=self.GECKODRIVER_LOG,
        )

        options = self.FIREFOX_OPTS
        options.add_argument("window-size=441, 795")

        driver = webdriver.Firefox(
            service=service,
            options=options
        )
        driver.get(self.pageurl)

        rows = driver.find_elements(By.XPATH, "//div[@class='footer']")
        for p in rows:

            tags = p.get_attribute("innerHTML")
            soup = BeautifulSoup(tags, 'html.parser')
            
            first_name = soup.find("span", {"class": "first"})
            if first_name != None:
                first_name = first_name.get_text().strip()

            last_name = soup.find("span", {"class": "last"})
            if last_name != None:
                last_name = last_name.get_text().strip()

            number = soup.find("span", {"class" : "value"})
            if number != None:
                number = number.get_text().strip()
            
            stats.append(
                "{} {} {} {}".format(
                first_name,
                last_name,
                separator,
                number
            ))
            break
        
        rows = driver.find_elements(By.CLASS_NAME, "rankingMetric")
        rows += driver.find_elements(By.TAG_NAME, "a")
        
        for p in rows:

            tags = p.get_attribute("innerHTML")
            soup = BeautifulSoup(tags, 'html.parser')

            footer = soup.find("div", {"class": "footer"})
            if footer != None:
                footer = footer.get_text().strip()
            
            first_name = soup.find("span", {"class": "first"})
            if first_name != None:
                first_name = first_name.get_text().strip()

            last_name = soup.find("span", {"class": "last"})
            if last_name != None:
                last_name = last_name.get_text().strip()

            number = soup.find("span", {"class" : "value fixed fixed-large"})
            if number != None:
                number = number.get_text().strip()
            
            metric = soup.find("span", {"class" : "metric"})
            if metric != None:
                metric = metric.get_text().strip()
            
            playerRows = soup.find("a", {"class" : "playerRow"})
            if playerRows != None:
                playerRows = playerRows.get_text().strip()
            
            if  (playerRows == metric and number is not None) or \
                (footer is not None and number is not None):
                name = f"{first_name} {last_name}"
                found = any(name in word for word in stats)
                if not found:
                    stats.append(
                        "{} {} {} {}".format(
                        first_name,
                        last_name,
                        separator,
                        number
                    ))
        
        json_str = json.dumps(stats, indent=4, sort_keys=True)
        encoded_str = json_str.encode('latin-1').decode('unicode-escape')
        self._save_to_file(encoded_str)
        driver.quit()

        with open(self.tempfilename) as f:
            data = json.load(f)
        return data
        

    def _read_from_remote_source(self):
        data = {}

        service = Service(
            service_log_path=self.GECKODRIVER_LOG,
        )
        
        driver = webdriver.Firefox(
            service=service,
            options=self.FIREFOX_OPTS
        )
        
        driver.get(self.pageurl)
        
        if self.source == "onlinebetting":
            elements_teams = driver.find_elements('xpath', '//h2[@class="injury-container__team-name"]')
            elements_injuries = driver.find_elements('xpath', '//div[@class="injury-table-container"]')
            for i in range(0, len(elements_teams)):
                team_name = elements_teams[i].get_attribute("innerText")
                injured_players = elements_injuries[i].get_attribute("innerHTML")
                data[team_name] = injured_players
        elif self.source == "sportsgambler":
            injury_blocks = driver.find_elements('xpath', '//div[@class="injury-block"]')
            elements_teams = driver.find_elements('xpath', '//h3[@class="injuries-title"]')
            for i in range(0, len(elements_teams)):
                team_name = elements_teams[i].get_attribute("innerText")
                injured_players = injury_blocks[i].get_attribute("innerHTML")
                data[team_name] = injured_players
        elif self.source == "betinf":
            injury_blocks = driver.find_elements('xpath', '//table[@class="tbl tblc1"]')
            elements_teams = driver.find_elements('xpath', '//h3[@class="exph" and @id]')
            for i in range(0, len(elements_teams)):
                team_name = elements_teams[i].get_attribute("innerText")
                injured_players = injury_blocks[i].get_attribute("innerHTML")
                data[team_name] = injured_players

        self._save_to_file(json.dumps(data, indent=4, sort_keys=True))
        driver.quit()

    def _getteams(self):
        read_from_remote = True
        teams = []

        if os.path.exists(self.tempfilename):
            fileLastUpdatedTime = os.stat(self.tempfilename).st_mtime
            ageOfFileInMinutes = (time.time() - fileLastUpdatedTime) / 240
            if ageOfFileInMinutes < self.CONST_MAX_AGE_OF_DATA_FILE_IN_MINUTES:
                read_from_remote = False

        if read_from_remote:
            self._read_from_remote_source()

        with open(self.tempfilename) as f:
            json_data = json.load(f)
            for part in json_data:
                teams.append(part)
        return teams

    def _separate_player_name_from_position(self, data):
        N=3
        name = ""
        position = ""
        for i in range(0, len(data)):
            if data[i] == "(":
                position = data[-N:]
                name = data[:-N].strip()
        return name, position

    def _find_injuried_players(self):
        injured_reserve = []

        with open(self.tempfilename) as f:
            parts = json.load(f)
            if self.source == "onlinebetting":
                for part in parts:
                    teams = BeautifulSoup(parts[part], "html.parser")
                    tables = teams.find_all("table")
                    for i in range(0, len(tables)):
                        rows = tables[i].find_all("tr")
                        for j in range(0, len(rows)):
                            columns = rows[j].find_all("td")
                            for k in range(0, len(columns)):
                                playerinfo = []
                                playerinfo.append(part)
                                playerinfo.append(columns[1].get_text())
                                playerinfo.append(columns[2].get_text())
                                playerinfo.append(columns[3].get_text())
                                playerinfo.append(columns[4].get_text())
                                injured_reserve.append(playerinfo)
                                break
            elif self.source == "sportsgambler":
                for part in parts:
                    driver = BeautifulSoup(parts[part], "html.parser")
                    #spans = driver.find_all("span")
                    injury_containers = driver.find_all(attrs={"class" : "inj-container"})
                    for injury_container in injury_containers:
                        spans = injury_container.find_all("span")
                        if len(spans) <= 7:
                            continue
                        playerinfo = []
                        playerinfo.append(part)
                        playerinfo.append(spans[1].get_text())
                        playerinfo.append(spans[2].get_text())
                        playerinfo.append(spans[7].get_text())
                        playerinfo.append(spans[6].get_text())
                        injured_reserve.append(playerinfo)
            elif self.source == "betinf":
                for part in parts:
                    table = BeautifulSoup(parts[part], "html.parser")
                    rows = table.find_all("tr")
                    for row in rows:
                        columns = row.find_all("td")
                        if len(columns) <= 0:
                            continue
                        for i in range(0, len(columns)):
                            name, pos = self._separate_player_name_from_position(columns[1].get_text())
                            playerinfo = []
                            playerinfo.append(part) # Team
                            playerinfo.append(name) # Player                            
                            playerinfo.append(columns[4].get_text()) # Type
                            playerinfo.append(columns[2].get_text()) # Return
                            playerinfo.append(columns[3].get_text()+ " " + pos) # Info
                            playerinfo.append(columns[4].get_text())
                            playerinfo.append(columns[5].get_text())
                            injured_reserve.append(playerinfo)
                            break
        return injured_reserve
    
    def get_injuries(self):
        read_from_remote = True

        if os.path.exists(self.tempfilename):
            fileLastUpdatedTime = os.stat(self.tempfilename).st_mtime
            ageOfFileInMinutes = (time.time() - fileLastUpdatedTime) / 240
            if ageOfFileInMinutes < self.CONST_MAX_AGE_OF_DATA_FILE_IN_MINUTES:
                read_from_remote = False

        if read_from_remote:
            self._read_from_remote_source()

        return self._find_injuried_players()

def show_stats(selectedLeagueAndSource):
    s = FantasyFootballScraper(selectedLeagueAndSource)
    goals = s.read_bundesliga_stats(url=sources["bundesliga-stats-goals"], filename="bundesliga-stats-goals")
    assists = s.read_bundesliga_stats(url=sources["bundesliga-stats-assists"], filename="bundesliga-stats-assists")
    duelswon = s.read_bundesliga_stats(url=sources["bundesliga-stats-duelswon"], filename="bundesliga-stats-duelswon")
    crosses = s.read_bundesliga_stats(url=sources["bundesliga-stats-crosses"], filename="bundesliga-stats-crosses")
    passes = s.read_bundesliga_stats(url=sources["bundesliga-stats-passes"], filename="bundesliga-stats-passes")
    intensiveruns = s.read_bundesliga_stats(url=sources["bundesliga-stats-intensiveruns"], filename="bundesliga-stats-intensiveruns")
    saves = s.read_bundesliga_stats(url=sources["bundesliga-stats-saves"], filename="bundesliga-stats-saves")

    goal_table = PrettyTable(["Player", "Goals"])
    for row in goals:
        cols = row.split(separator)
        goal_table.add_row([cols[0], cols[1]])
    print(goal_table)

    assist_table = PrettyTable(["Player", "Assists"])
    for row in assists:
        cols = row.split("<>")
        assist_table.add_row([cols[0], cols[1]])
    print(assist_table)

    duelswon_table = PrettyTable(["Player", "Duels won"])
    for row in duelswon:
        cols = row.split(separator)
        duelswon_table.add_row([cols[0], cols[1]])
    print(duelswon_table)

    crosses_table = PrettyTable(["Player", "Crosses"])
    for row in crosses:
        cols = row.split(separator)
        crosses_table.add_row([cols[0], cols[1]])
    print(crosses_table)

    passes_table = PrettyTable(["Player", "Passes"])
    for row in passes:
        cols = row.split(separator)
        passes_table.add_row([cols[0], cols[1]])
    print(passes_table)

    intensiveruns_table = PrettyTable(["Player", "Intensive runs"])
    for row in intensiveruns:
        cols = row.split(separator)
        intensiveruns_table.add_row([cols[0], cols[1]])
    print(intensiveruns_table)

    saves_table = PrettyTable(["Player", "Saves"])
    for row in saves:
        cols = row.split(separator)
        saves_table.add_row([cols[0], cols[1]])
    print(saves_table)


def show_results(selectedLeagueAndSource):
    league = selectedLeagueAndSource.split("-")[0]
    team_filename = "data/{0}-team.txt".format(league)
    prospects_filename = "data/{}-prospects.txt".format(league)

    s = FantasyFootballScraper(selectedLeagueAndSource)
    injuries = s.get_injuries()

    with open(team_filename, "r") as f:
        players = [line.strip() for line in f]

    with open(prospects_filename, "r") as f:
        prospects = [line.strip() for line in f]
    
    number_of_injuries_in_squad = 0
    number_of_injuries_in_prospects = 0
    print("Number of injuries reported: {}".format(len(injuries)))

    print("")
    print("- Squad -")
    for injury in injuries:
        if injury[1] in players and injury[1] != "":
            print(Fore.RED)
            print("Note")
            print("\tPlayer:\t{}".format(injury[1]))
            print("\tType:\t{}".format(injury[2]))
            print("\tReturn:\t{}".format(injury[3]))
            print("\tInfo:\t{}".format(injury[4]))
            print("\tTeam:\t{}".format(injury[0]))
            print(Style.RESET_ALL)
            number_of_injuries_in_squad += 1
    if number_of_injuries_in_squad > 0:
        print("There are a total of {} injuries in the squad." \
            .format(number_of_injuries_in_squad))
    else:
        print("No injuries in squad.")
    
    print("")
    print("- Prospects -")
    for injury in injuries:
        if injury[1] in prospects and injury[1] != "":
            print("Note")
            print("\tPlayer:\t{}".format(injury[1]))
            print("\tType:\t{}".format(injury[2]))
            print("\tReturn:\t{}".format(injury[3]))
            print("\tInfo:\t{}".format(injury[4]))
            print("\tTeam:\t{}".format(injury[0]))
            number_of_injuries_in_prospects += 1
    if number_of_injuries_in_prospects > 0:
        print("There are a total of {} injuries in the prospect list." \
            .format(number_of_injuries_in_prospects))
    else:
        print("No injuries in the prospect list.")


if __name__ == "__main__":

    print(Fore.CYAN + title + Style.RESET_ALL)

    while True:
        mapping = \
                { \
                    "Injuries - Bundesliga - Sportsgambler" : "bundesliga-sportsgambler", \
                    "Injuries - Bundesliga - BetInf" : "bundesliga-betinf", \
                    #"Injuries - Bundesliga - Onlinebetting" : "bundesliga-onlinebetting", \
                    "Injuries - Premier League - Sportsgambler" : "premierleague-sportsgambler", \
                    "Injuries - Premier League - BetInf" : "premierleague-betinf", \
                    #"Injuries - Premier League - Onlinebetting" : "premierleague-onlinebetting", \
                    "Stats - Bundesliga" : "bundesliga-stats" , \
                    "Quit" : "Quit"
                }
        info = "Please choose league and source below:"
        caption = "Welcome to Screen Scraper for Fantasy football."
        main_menu_cursor = "> "
        main_menu_cursor_style = ("fg_red", "bold")
        main_menu_style = ("bg_red", "fg_yellow")

        print(Fore.GREEN + caption + Style.RESET_ALL)
        
        terminal_menu = stm.TerminalMenu(
            mapping.keys(), 
            title=info,
            menu_cursor=main_menu_cursor,
            menu_cursor_style=main_menu_cursor_style,
            menu_highlight_style=main_menu_style
        )
        
        selected = terminal_menu.show()

        print("Selected: {}".format(list(mapping.keys())[selected]))

        if list(mapping.keys())[selected] == "Quit":
            print("Thanks for using Screen Scraper for Fantasy football.")
            break
        elif list(mapping.values())[selected] == "bundesliga-stats":
            selectedLeagueAndSource = list(mapping.values())[selected]
            show_stats(selectedLeagueAndSource)
        else:
            selectedLeagueAndSource = list(mapping.values())[selected]
            show_results(selectedLeagueAndSource)


        print("")