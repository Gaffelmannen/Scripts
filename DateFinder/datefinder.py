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

    title = "Datefinder 1.0"
    mapping = \
    { \
        "Set date" : "setdate",
        "-": "-",
        "One month" : "one-month", \
        "Three months" : "three-months", \
        "Six months" : "six-months", \
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
        
        if selected > 1:
            choice = list(mapping.values())[selected]

            result = \
            {
                "one-month": lambda result: thedate + relativedelta(months=+1),
                "three-months": lambda result: thedate + relativedelta(months=+3),
                "six-months": lambda result: thedate + relativedelta(months=+6)
            }[choice](0)
            
            print("{}The date that is {} from {} is {}{}".format(
                Fore.BLUE,
                list(mapping.keys())[selected].lower(),
                thedate,
                result,
                Style.RESET_ALL
            ))
            print("")
    
    sys.exit(0)
