# Introduction

This project aims to fetch Spotify historical listened tracks periodically.

The final goal is to be able to make my own Spotify annual visualization or more finer granularity with any Visualization tools. 

The fetch job is simple. However, I am currently struggling with mapping JSON files to tabular format. May be I was too obsessed with SqlAlchemy, which is Python ORM. I will try to change my thought and try another approach when I have time.

# Instruction

## Setup Dependencies

```sh
$ python3 -m virtualenv .venv
$ source ./.venv/bin/activate
$ pip3 install -r requirements.txt
```

## Setup Cronjob
```sh
# Schedule to fetch 20 recently played songs every 50 minutes.

# Edit cron job list
crontab -e 

# Add the following cronjob to Vim console.  <Cron job schedule> <command>
*/3 * * * * cd ~/Desktop/programming/yet-another-spotify-scraping-attempt/ && ./.venv/bin/python ./get-recently-played.py

# View existsing cron job
crontab -l
```