#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import date
from dateutil.relativedelta import relativedelta

class DateFinder:
    def __init__(self):
        #pass
        #self.start_date = date.today()
        self.start_date = date(2023, 3, 1)
        self.number_of_months = 6
    
    def get_start_date(self):
        return self.start_date
        
    def get_offset(self):
        return self.number_of_months

    def calculate_day(self):
        calculated_date =  \
            self.get_start_date() + \
            relativedelta(months=+self.get_offset())
        return calculated_date

if __name__ == "__main__":
    df = DateFinder()
    print(df.calculate_day())
    sys.exit(0)
