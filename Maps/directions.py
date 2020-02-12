#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import googlemaps
from datetime import datetime


FROM_ADDRESS='Miraallen 51', 'Göteborg', 'Sweden'
TO_ADDRESS='Ullevigatan 19,', 'Göteborg', 'Sweden'

class Maps():
    def __init__(self):
        pass

    def retrieve_key(self):
        self.key = os.environ.get("MAPS_SECRET_KEY")
        #print(self.key)

    def do_lookup(self):
        gmaps = googlemaps.Client(key=self.key)

        #print(gmaps.key)
        #print(FROM_ADDRESS)
        #print(TO_ADDRESS[0])
        #print(TO_ADDRESS[1])

        geocode_result = gmaps.geocode(FROM_ADDRESS)

        reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

        now = datetime.now()
        directions_result = gmaps.directions(
            TO_ADDRESS[0],
            TO_ADDRESS[1],
            mode="transit",
            departure_time=now)

        res=json.dumps(directions_result[0])

        print(res)

if __name__ == "__main__":
    maps = Maps()
    maps.retrieve_key()
    maps.do_lookup()
    sys.exit(0)

