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
    ffs = FantasyFootballScraper("test-testsson")
    fileages = ffs.get_age_of_all_source_files()

    return render_template("index.html",
                           utc_dt=datetime.datetime.now(),
                           rows=leagues_and_sources_map,
                           target="stats",
                           fileages=fileages,
                           bsh=bundesliga_stat_headers,
                           sls=["bundesliga-players", "premierleague-players"])

@app.route("/injuries", methods=["GET", "POST"])
def injuries():
    sls = None

    if request.method == "POST":
        sls = request.form.get("sls")
    elif request.method == "GET":
        sls = request.args.get("sls")

    ffs = FantasyFootballScraper(sls)
    squad_json = ffs.get_injured_players_in_squad(sls)
    prospect_json = ffs.get_injured_players_in_prospects(sls)

    league = sls.split("-")[0]

    return render_template("injuries.html", 
                        utc_dt=datetime.datetime.now(),
                        injuries_squad=squad_json,
                        injuries_prospects=prospect_json,
                        league=league)
    

@app.route("/stats", methods=["GET", "POST"])
def stats():
    sls = None

    if request.method == "POST":
        sls = request.form.get("sls")
    elif request.method == "GET":
        sls = request.args.get("sls")
    
    league = sls.split("-")[0]
    ffs = FantasyFootballScraper(sls)

    data = []
    captions = []
    for key, value in bundesliga_stat_headers.items():
        data.append(ffs.read_bundesliga_stats_as_json(url=sources[key], filename=key))
        captions.append(value)

    return render_template("stats.html",
                           utc_dt=datetime.datetime.now(),
                           stats=data,
                           league=league,
                           captions=captions)

@app.route("/team", methods=["POST"])
def team():
    sls = request.form.get("sls")
    league = sls.split("-")[0]
    ffs = FantasyFootballScraper(sls)
    players = ffs.get_team_players_as_json(league=league)
    prospects = ffs.get_prospect_players_as_json(league=league)
    return render_template("team.html",
                           utc_dt=datetime.datetime.now(),
                           league=league,
                           team_players=players,
                           prospect_players=prospects)

@app.route("/saveteam", methods=["POST"])
def saveteam():
    data = request.get_json()
    league = data.get('league')
    player_type = data.get('type')
    player_data = data.get('data')

    ffs = FantasyFootballScraper("bundesliga-sportsgambler")
    ffs.save_team_players_as_json(league=league, type=player_type, content=player_data)

    return {
        "outcome" : "success"
    }

if __name__ == "__main__":
    app.run(debug=True)

    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")

    # Production
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()