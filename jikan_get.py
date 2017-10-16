# -------
# imports
# -------

import sys
import requests
import json
import os
import errno
import filecmp
import re

# -------
# methods
# -------


def test():
    print("This is a test")
    r = requests.get('https://api.github.com/events').json()
    print(r)


def jikanget(url_type, num_items, folder_name, filter_porn=True):

    id = 1
    count = 1

    while count <= num_items:
        url = url_type + str(id) + '/characters_staff'
        r = requests.get(url)
        print(r.status_code)

        if r.status_code != 404:
            r = r.json()

            has_porn = False
            # checks if the anime is pornographic, but only if filter_porn
            # is set to true
            if filter_porn :
	            for x in r['genre'] :
	            	if x[1] == 'Hentai' :
	            		has_porn = True
            
            # only add the anime if it's not porn, will always run if filter_porn
            # is set to false
            if has_porn != True :
	            file_name = folder_name + '/' + str(id)
	            print(file_name)
	            if not os.path.exists(os.path.dirname(file_name)):
	                try:
	                    os.makedirs(os.path.dirname(file_name))
	                except OSError as exc:  # Guard against race condition
	                    if exc.errno != errno.EEXIST:
	                        raise

	            with open(str(file_name), 'w') as outfile:
	                json.dump(r, outfile)
	            count += 1

        id += 1

def get_matches(read_match, write_match, read_folder, write_folder, url_type, additional_data=''):

    id = 220
    count = 0
    num_items = 100

    while count <= num_items:

        # get a json page based off of id
        url = url_type + str(id) + additional_data
        r = requests.get(url)
        print(r.status_code)
        print(id)
        print(count)
        add_outcome = 'FAILED'

        # if the daily limit is not exceeded
        if r.status_code == 429:
        	raise StopIteration

        # if the page returns something
        if r.status_code != 404:
        	# turn the json page into a dict
            r = r.json()
            # make sure our match field exists
            if write_match in r:
                match_data = r[write_match]
                # check to see if that item's match field matches any of the titles in anime
                # runs through all the files in the give folder
                for filename in os.listdir(read_folder):
                    with open(read_folder + '/' + filename) as datafile:
                        data = json.load(datafile)
                        if read_match in data:
                            # if the field matches between files
                            if data[read_match] == match_data:
                                # name the file after it's id
                                file_name = write_folder + '/' + str(id)
                                # create the folder if it does not exist in this dir
                                if not os.path.exists(os.path.dirname(file_name)):
                					try:
                						os.makedirs(os.path.dirname(file_name))
                					except OSError as exc:  # Guard against race condition
                						if exc.errno != errno.EEXIST:
                							raise
                				# write the file
                                with open(file_name, 'w') as outfile:
                                    json.dump(r, outfile)
                                    add_outcome = 'SUCCESS'
                                count += 1
        id += 1
        print(add_outcome)
        print('')

def get_matches_people(read_match, write_match, read_folder, write_folder, url_type, additional_data=''):

    # highest manga id = 2034
    # num manga = 41

    # highest person id 220
    # num people = 0

    id = 1
    count = 0
    num_items = 100

    while count <= num_items:

        # get a json page based off of id
        url = url_type + str(id) + additional_data
        r = requests.get(url)
        print(r.status_code)
        print(id)
        print(count)
        add_outcome = 'FAILED'

        # if the daily limit is not exceeded
        if r.status_code == 429:
            raise StopIteration

        # if the page returns something
        if r.status_code != 404:
            # turn the json page into a dict
            r = r.json()
            # make sure our match field exists
            if write_match in r:
                match_data = r[write_match]
                print(match_data)
                # check to see if that item's match field matches any of the titles in anime
                # runs through all the files in the give folder
                for readfile in os.listdir(read_folder):
                    with open(read_folder + '/' + readfile) as datafile:
                        data = json.load(datafile)

                        for character in data['character']:
                            if 'voice-actor' in character:
                                for actor in character['voice-actor']:
                                    if 'url' in actor:
                                        if actor['url'] == match_data:
                                            # if the field matches between file
                                                # name the file after it's id
                                            writefile = write_folder + '/' + str(id)
                                            # create the folder if it does not exist in this dir
                                            if not os.path.exists(os.path.dirname(writefile)):
                                                try:
                                                    os.makedirs(os.path.dirname(writefile))
                                                except OSError as exc:  # Guard against race condition
                                                    if exc.errno != errno.EEXIST:
                                                        raise
                                            duplicate = False            
                                            for file in os.listdir(write_folder):
                                                if file == str(id):
                                                    duplicate = True
                                            # write the file
                                            if duplicate != True:
                                                with open(writefile, 'w') as outfile:
                                                    json.dump(r, outfile)
                                                    add_outcome = 'SUCCESS'
                                                count += 1
        id += 1
        print(add_outcome)
        print('')

def get_matches_character(read_match, write_match, read_folder, write_folder, url_type, additional_data=''):

    # highest manga id = 2034
    # num manga = 41

    # highest person id 220
    # num people = 0

    id = 127
    count = 56
    num_items = 100

    while count <= num_items:
        print('here 1')
        # get a json page based off of id
        url = url_type + str(id) + additional_data
        print('here 2')
        r = requests.get(url)
        print(r.status_code)
        print(id)
        print(count)
        add_outcome = 'FAILED'

        # if the daily limit is not exceeded
        if r.status_code == 429:
            raise StopIteration

        # if the page returns something
        if r.status_code == 200:
            # turn the json page into a dict
            r = r.json()
            if r != False:
                # make sure our match field exists
                if write_match in r:
                    match_data = r[write_match]
                    match_data = re.findall(r"[\w']+", match_data)
                    match_set = set(match_data)
                    print(match_set)
                    # check to see if that item's match field matches any of the titles in anime
                    # runs through all the files in the give folder
                    for readfile in os.listdir(read_folder):
                        with open(read_folder + '/' + readfile) as datafile:
                            data = json.load(datafile)
                            for character in data['character']:
                                if 'name' in character:
                                    char_name = re.findall(r"[\w']+", character['name'])
                                    name_set = set(char_name)
                                    if name_set == match_set:
                                        # if the field matches between file
                                            # name the file after it's id
                                        writefile = write_folder + '/' + str(id)
                                        # create the folder if it does not exist in this dir
                                        if not os.path.exists(os.path.dirname(writefile)):
                                            try:
                                                os.makedirs(os.path.dirname(writefile))
                                            except OSError as exc:  # Guard against race condition
                                                if exc.errno != errno.EEXIST:
                                                    raise
                                        duplicate = False            
                                        for file in os.listdir(write_folder):
                                            if file == str(id):
                                                duplicate = True
                                        # write the file
                                        if duplicate != True:
                                            with open(writefile, 'w') as outfile:
                                                json.dump(r, outfile)
                                                add_outcome = 'SUCCESS'
                                            count += 1
        id += 1
        print(add_outcome)
        print('')


# ----
# main
# ----

if __name__ == "__main__":
    # titles used to match anime and manga
    # voice actor page links used to match anime and people

    # jikanget('http://jikan.me/api/anime/', 100, 'jikan_anime', True)
    # get_matches('title', 'title', 'jikan_anime', 'jikan_manga', 'http://jikan.me/api/manga/', '/characters_staff')
    get_matches_character('character', 'name', 'jikan_anime', 'jikan_character', 'http://jikan.me/api/character/')
