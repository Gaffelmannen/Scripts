#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import datetime

from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer

from fantasy_football_scraper \
    import \
    FantasyFootballScraper, \
    leagues_and_sources_map, \
    bundesliga_stat_headers, \
    sources

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    return render_template("index.html",
                           rows=leagues_and_sources_map,
                           target="stats")

@app.route("/injuries", methods=["POST"])
def info():
    sls = request.form.get("sls")
    league = sls.split("-")[0]
    
    ffs = FantasyFootballScraper(sls)
    squad_json = ffs.get_injured_players_in_squad(sls)
    prospect_json = ffs.get_injured_players_in_prospects(sls)

    return render_template("injuries.html", 
                           injuries_squad=squad_json,
                           injuries_prospects=prospect_json,
                           utc_dt=datetime.datetime.utcnow(),
                           league=league)

@app.route("/stats", methods=["POST"])
def stats():
    sls = request.form.get("sls")
    print(sls)
    print(sources)
    league = sls.split("-")[0]
    source = sls.split("-")[1]
    ffs = FantasyFootballScraper(sls)

    data = []
    captions = []
    for key, value in bundesliga_stat_headers.items():
        data.append(ffs.read_bundesliga_stats_as_json(url=sources[key], filename=key))
        captions.append(value)

    return render_template("stats.html", 
                           stats=data,
                           utc_dt=datetime.datetime.utcnow(),
                           league=league,
                           captions=captions)

if __name__ == "__main__":
    app.run(debug=True)

    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")

    # Production
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()