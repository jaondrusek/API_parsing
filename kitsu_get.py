import sys
import requests
import json
import os
import errno
import filecmp
import re

# Incomplete, plan to use to get youtube video links from kitsu
def get_anime_video() :
    url = 'https://kitsu.io/api/edge'
    for filename in os.listdir('jikan_anime'):
        with open('jikan_anime/' + filename) as datafile:
            data = json.load(datafile)
                if 'title' in data:

if __name__ == "__main__":
    get_anime_vids()
