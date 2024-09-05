# Fantasy Screen Scraper
Allows you to check what players are injured in
- Premier Leagure
- Bundesliga

It currently has two sources:
- onlinebetting.com
- sportsgambler.com

Choose league and source when you run the script.


## Setup
### On Mac:
1. Run
```
brew install geckodriver
```
2. Run
```
pip install -r requirements.txt
```


## Use it
To run the program call the script.

1.
Edit your team file:
premierleague-team.txt for Premier League
bundesliga-team.txt for Bundesliga

2.
```
./scrape.py
```

## Dependencies
These are the foundations.

### Gecko drivers
https://github.com/mozilla/geckodriver/releases
