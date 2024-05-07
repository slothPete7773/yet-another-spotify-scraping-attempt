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
*/50 * * * * cd ~/Desktop/programming/yet-another-spotify-scraping-attempt/ && ./.venv/bin/python ./get-recently-played.py

*/60 * * * * cd ~/Desktop/programming/yet-another-spotify-scraping-attempt/ && ./.venv/bin/python ./extract-recently-played.py

# View existsing cron job
crontab -l
```


# Issues

1. **[Solved]** Problem while inserting Album Images. Iterating through Album images list but the AlbumImage Object is not instantiate for each iteration. Making the previous iteration object entangled with new iteration object. 
   1. I tried manually provide UUID, the UUIDs are different for each iteration, but when look closely, a new iteration object still hold on to previous UUID. WTF?
   2. Having concern about the Artists field, because it is a list as well, and might affect by this problem too.

2. Track item from Spotify has field `popularity` updated, while the database is not update accordingly. The query to find existing data is wrong, use all fields to find is too strict. 