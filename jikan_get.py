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

# def test():
#     url = 'http://jikan.me/api/anime/1/characters_staff'
#     r = requests.get(url).json()
#     for x in r:
#         print(x)

#     datafile = open('jikan_anime/1')
#     data = json.load(datafile)
#     print('Written file')
#     dump(data)
#     for x in data:
#         print(x)


# def dump(obj, nested_level=0, output=sys.stdout):
#     spacing = '   '
#     if type(obj) == dict:
#         print >> output, '%s{' % ((nested_level) * spacing)
#         for k, v in obj.items():
#             if hasattr(v, '__iter__'):
#                 print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
#                 dump(v, nested_level + 1, output)
#             else:
#                 print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)
#         print >> output, '%s}' % (nested_level * spacing)
#     elif type(obj) == list:
#         print >> output, '%s[' % ((nested_level) * spacing)
#         for v in obj:
#             if hasattr(v, '__iter__'):
#                 dump(v, nested_level + 1, output)
#             else:
#                 print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
#         print >> output, '%s]' % ((nested_level) * spacing)
#     else:
#         print >> output, '%s%s' % (nested_level * spacing, obj)

# Counts the number of files in the given folder
def count_files(folder):
    print len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])

# Used to get anime, starting at id 1 and going until you have num_items
def jikanget(url_type, num_items, folder_name, filter_porn=True):

    id = 1
    if os.path.exists(folder_name) :
        count = len([name for name in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, name))])
    else :
        count = 0;

    while count <= num_items:
        url = url_type + str(id) + '/characters_staff'
        r = requests.get(url)
        print(r.status_code)
        print(count)
        add_outcome = 'FAILED'

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
            if has_porn != True:
                file_name = folder_name + '/' + str(id)
                print file_name
                if not os.path.exists(os.path.dirname(file_name)):
                    try:
                        os.makedirs(os.path.dirname(file_name))
                    except OSError, exc:

                                # Guard against race condition

                        if exc.errno != errno.EEXIST:
                            raise
                if os.path.isfile(file_name) == False:
                    with open(str(file_name), 'w') as outfile:
                        json.dump(r, outfile)
                        add_outcome = 'SUCCESS'
                    count += 1

        id += 1
        print(add_outcome)
        print('')

# Used to get each anime's matching manga, used to check and compare the title attribute of each one.
# Was not used for characters or people because this only checks top level dict keys
def get_matches(read_match, write_match, read_folder, write_folder, url_type, *additional_data):

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

def get_manga_matches():
    count = 0
    for filename in os.listdir('jikan_anime'):
        read_file = 'jikan_anime/' + filename
        with open(read_file) as datafile:
            data = json.load(datafile)
            print(filename)
            if count < 100:
                if 'related' in data:
                    related = data['related']
                    if 'Adaptation' in related:
                        check_obj = related['Adaptation']
                        if isinstance(check_obj[0], list):
                            for list_obj in related['Adaptation']:
                                # print(list_obj)
                                tokens = list_obj[1].split('/')
                                manga_id = tokens[2]
                                # print('ID: ' + manga_id)
                                r = requests.get('http://jikan.me/api/manga/' + manga_id).json()

                                write_file = 'jikan_manga/' + manga_id
                                if not os.path.exists(os.path.dirname(write_file)):
                                    try:
                                        os.makedirs(os.path.dirname(write_file))
                                    except OSError as exc:  # Guard against race condition
                                        if exc.errno != errno.EEXIST:
                                            raise
                                # write the file
                                with open(write_file, 'w') as outfile:
                                    json.dump(r, outfile)
                                    print(r['title'])
                                    count += 1
                        else:
                            manga = related['Adaptation']
                            manga = manga[1].split('/')
                            manga_id = manga[2]
                            # print('ID: ' + manga_id)
                            r = requests.get('http://jikan.me/api/manga/' + manga_id).json()
                            write_file = 'jikan_manga/' + manga_id
                            if not os.path.exists(os.path.dirname(write_file)):
                                try:
                                    os.makedirs(os.path.dirname(write_file))
                                except OSError as exc:  # Guard against race condition
                                    if exc.errno != errno.EEXIST:
                                        raise
                            # write the file
                            with open(write_file, 'w') as outfile:
                                json.dump(r, outfile)
                                print(r['title'])
                                count += 1

# Runs through the anime we have locally, gets the first main character, gets the Japanese voice actor for that character
# Limited to one per show
def get_matches_people(read_folder, write_folder, url_type):

    count = 0

    for filename in os.listdir(read_folder):
        found = False
        with open(read_folder + '/' + filename) as datafile:
            data = json.load(datafile)
            if 'character' in data:
                for character in data['character']:
                    if 'role' in character:
                        if character['role'] == 'Main':
                            if 'voice-actor' in character:
                                for actor in character['voice-actor']:
                                    if actor['role'] == 'Japanese' and found != True:
                                        if 'url' in actor:
                                            tokenized_id = (actor['url'].split('/'))[4]

                                            url = url_type + tokenized_id
                                            r = requests.get(url).json()

                                            file_name = write_folder + '/' + tokenized_id
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
                                                print(data['title'])
                                                found = True
                                            count += 1
                                            print('Count: ' + str(count))
                                            print('')


# Runs through the anime we have locally, gets the first main character, and adds them to jikan_character
# Limited to one per show
def get_matches_character(read_folder, write_folder, url_type):

    count = 0

    for filename in os.listdir(read_folder):
        found = False
        with open(read_folder + '/' + filename) as datafile:
            data = json.load(datafile)
            if 'character' in data:
                for character in data['character']:
                    if 'role' in character:
                        if character['role'] == 'Main' and found != True:
                            if 'url' in character:
                                tokenized_id = (character['url'].split('/'))[4]

                                url = url_type + tokenized_id
                                r = requests.get(url).json()

                                file_name = write_folder + '/' + tokenized_id
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
                                    print(data['title'])
                                    found = True
                                count += 1
                                print('Count: ' + str(count))
                                print('')


# ----
# main
# ----

if __name__ == "__main__":

    # test()

    # count_files('jikan_anime')

    get_manga_matches()

    # jikanget('http://jikan.me/api/anime/', 100, 'jikan_anime', True)
    # jikanget('http://jikan.me/api/manga/', 100, 'jikan_manga', True)
    # get_matches('title', 'title', 'jikan_anime', 'jikan_manga', 'http://jikan.me/api/manga/', '/characters_staff')
    # get_matches_people("jikan_anime", "jikan_person", 'http://jikan.me/api/person/')    
    # get_matches_character('jikan_anime', 'jikan_character', 'http://jikan.me/api/character/')
