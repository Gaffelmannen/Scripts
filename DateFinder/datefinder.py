#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import date
from dateutil.relativedelta import relativedelta
from colorama import Fore, Back, Style

import simple_term_menu as stm

if __name__ == "__main__":

    title = "Datefinder 1.0"
    mapping = \
    { \
        "One month" : "one-month", \
        "Three months" : "three-months", \
        "Six months" : "six-months", \
        "Quit" : "Quit"
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

        if list(mapping.keys())[selected] == "Quit":
            print("Thanks for using Datefinder 1.0")
            break

        choice = list(mapping.values())[selected]
        result = \
        {
            "one-month": lambda result: date.today() + relativedelta(months=+1),
            "three-months": lambda result: date.today() + relativedelta(months=+3),
            "six-months": lambda result: date.today() + relativedelta(months=+6)
        }["one-month"](choice)
        
        print("The calculated date is: {}".format(result))
        print("")
    
    sys.exit(0)
