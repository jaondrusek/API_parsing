import sys
import requests
import json
import os
import errno
import filecmp
import re

# Runs through every anime in jikan_anime and searches kitsu's api for an exact match to that anime's
# title, if it finds a match, it adds the youtube id to the local file
def get_anime_video() :
    url = 'https://kitsu.io/api/edge/anime?filter[text]='
    for filename in os.listdir('jikan_anime'):
        readwrite_file = 'jikan_anime/' + filename
        print(readwrite_file)
        with open(readwrite_file) as datafile:
            data = json.load(datafile)
            jikan_name = data['title']
            search_url = url + jikan_name
            r = requests.get(search_url)
            add_outcome = 'FAILED'
            print(r.status_code)
            if r.status_code != 404:
                r = r.json()
                found = False
                for anime in r['data']:
                    if 'attributes' in anime:
                        attr = anime['attributes']
                        if attr['canonicalTitle'] == jikan_name and found != True:
                            print(attr['canonicalTitle'])
                            data['youtubeVideoId'] = attr['youtubeVideoId']
                            if os.path.isfile(readwrite_file) == True:
                                with open(str(readwrite_file), 'w') as outfile:
                                    json.dump(data, outfile)
                                    # os.rename(readwrite_file, readwrite_file + '.txt')
                                    add_outcome = 'SUCCESS'
                                    found = True
                print(add_outcome)
                print('')

if __name__ == "__main__":
    get_anime_video()
