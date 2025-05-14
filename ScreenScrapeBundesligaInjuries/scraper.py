#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import simple_term_menu as stm
from colorama import Fore, Back, Style
from prettytable import PrettyTable

from fantasy_football_scraper import *

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

def generate_table_with_two_columns(data, headers):

    R = "\033[0;31;40m" # Red
    G = "\033[0;32;40m" # Green
    B = "\033[0;34;40m" # Blue
    Y = "\033[0;33;40m" # Yellow
    N = "\033[0m" # Reset

    t = PrettyTable(headers)
    for row in data:
        cols = row.split(separator)
        t.add_row([cols[0], cols[1]])
    print(t)

def generate_table_with_five_columns(data, headers):
    t = PrettyTable(headers)
    for row in data:
        cols = row.split(separator)
        t.add_row([cols[0], cols[1], cols[2], cols[3], cols[4]])
    print(t)

def show_stats(selectedLeagueAndSource):
    s = FantasyFootballScraper(selectedLeagueAndSource)

    for header_key in bundesliga_stat_headers.keys():
        data = s.read_bundesliga_stats(url=sources[header_key], filename=header_key)
        generate_table_with_two_columns(data, headers=bundesliga_stat_headers[header_key])

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
    injured_squad=[]
    for injury in injuries:
        if injury[1] in players and injury[1] != "":
            injured_squad.append(
                f"{injury[1].strip()}{separator} \
                {injury[0].strip()}{separator} \
                {injury[3].strip()}{separator} \
                {injury[4].strip()}{separator} \
                {injury[2].strip()}{separator}"
            )
            number_of_injuries_in_squad += 1
    if number_of_injuries_in_squad > 0:
        print(Fore.RED)
        generate_table_with_five_columns(
            headers=injury_and_suspension_headers,
            data=injured_squad
        )
        print(Style.RESET_ALL)
        print("There are a total of {} injuries in the squad." \
            .format(number_of_injuries_in_squad))
    else:
        print("No injuries in squad.")
    
    print("")
    print("- Prospects -")
    injured_prospects=[]
    for injury in injuries:
        if injury[1] in prospects and injury[1] != "":
            injured_prospects.append(
                f"{injury[1].strip()}{separator} \
                {injury[0].strip()}{separator} \
                {injury[3].strip()}{separator} \
                {injury[4].strip()}{separator} \
                {injury[2].strip()}{separator}"
            )
            number_of_injuries_in_prospects += 1
    if number_of_injuries_in_prospects > 0:
        print(Style.YELLOW)
        generate_table_with_five_columns(
            headers=injury_and_suspension_headers,
            data=injured_prospects
        )
        print(Style.RESET_ALL)
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
