#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import datetime

from datetime import date
from dateutil.relativedelta import relativedelta
from colorama import Fore, Back, Style

import simple_term_menu as stm

def is_valid_date(string_to_check):
    try:
        datetime.date.fromisoformat(string_to_check)
    except ValueError:
        return False
    return True

if __name__ == "__main__":

    thedate = date.today()
    offsetvalue = 1

    title = "Datefinder 1.0"
    mapping = \
    { \
        "Set date" : "setdate",
        "Set offset value": "offsetvalue",
        "-": "-",
        "Days" : "days", \
        "Months" : "months", \
        "Years" : "years", \
        "Quit" : "quit"
    }
    info = "Please choose your request below:"
    caption = "Welcome to Datefinder."
    main_menu_cursor = "> "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")

    print(Fore.CYAN + title + Style.RESET_ALL)

    while True:

        print(Fore.GREEN + caption + Style.RESET_ALL)
        
        terminal_menu = stm.TerminalMenu \
        (
            mapping.keys(), 
            title=info,
            menu_cursor=main_menu_cursor,
            menu_cursor_style=main_menu_cursor_style,
            menu_highlight_style=main_menu_style
        )
        
        selected = terminal_menu.show()

        print("Selected: {}".format(list(mapping.keys())[selected]))

        if list(mapping.values())[selected] == "quit":
            print("Thanks for using Datefinder 1.0")
            break

        if list(mapping.values())[selected] == "setdate":
            while True:
                read_value = input("Enter from date (YYYY-MM-DD) or leave blank for today :> ")
                if read_value == "":
                    break

                if is_valid_date(read_value):
                    thedate = datetime.date.fromisoformat(read_value)
                    break
        
        if list(mapping.values())[selected] == "offsetvalue":
            while True:
                read_value = input("Enter the value you wish to offset by :> ")
                if read_value == "":
                    break

                if read_value.isnumeric():
                    offsetvalue = int(read_value)
                    break
        
        if selected > 2:
            choice = list(mapping.values())[selected]

            result = \
            {
                "days": lambda result: thedate + relativedelta(days=+offsetvalue),
                "months": lambda result: thedate + relativedelta(months=+offsetvalue),
                "years": lambda result: thedate + relativedelta(years=+offsetvalue),
            }[choice](0)
            
            print("The date that is {} {} from {} is {}{}{}{}".format(
                offsetvalue,
                choice,
                thedate,
                Fore.BLACK,
                Back.LIGHTGREEN_EX,
                result,
                Style.RESET_ALL
            ))
            print("")
    
    sys.exit(0)
