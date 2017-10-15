# -------
# imports
# -------

import sys
import requests
import json
import os
import errno

# -------
# methods
# -------


def test():
    print("This is a test")
    r = requests.get('https://api.github.com/events').json()
    print(r)


def jikanget(url_type, num_items, folder_name):

    id = 1
    count = 1

    while count <= num_items:
    	url = url_type + str(id) + '/characters_staff'
    	r = requests.get(url)
    	print(r.status_code)

        if r.status_code != 404:
            r = r.json()
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

def get_manga() :

	id = 1
	count = 1
	num_items = 100

	while count <= num_items:

		# get a manga based off of id
		url = 'http://jikan.me/api/manga/' + str(id)
		r = requests.get(url)
		print(r.status_code)

		if r.status_code != 404:
			r = r.json()
			if 'title' in data:
				manga_name = r['title']

					# check to see if that manga's title matches any of the titles in anime
					for filename in os.listdir('jikan_anime'):
						with (filename) as datafile:
							data = json.load(datafile)
							if 'title' in data:
								if data['title'] == manga_name:
									with open(str(id), 'w') as outfile:
										json.dump(r, outfile)
									count += 1
		id += 1


        		

# ----
# main
# ----

if __name__ == "__main__":
    # jikanget('http://jikan.me/api/anime/', 100, 'jikan_anime')
    get_manga()
    # jikanget('http://jikan.me/api/manga/', 100, 'jikan_manga')
    # jikanget('http://jikan.me/api/character/', 100, 'jikan_character')
    # jikanget('http://jikan.me/api/person/', 100, 'jikan_person')
