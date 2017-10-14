# -------
# imports
# -------

import sys
import requests
import json

# -------
# methods
# -------

def test():
    print("This is a test")
    r = requests.get('https://api.github.com/events').json()
    print(r)

def jikanget(url_type, num_items, folder_name):

	id = 1
	url = url_type + str(id)
	r = requests.get(url)
	print(r.status_code)
	count = 1

	while count <= num_items :
		if r.status_code !=  404:
			r = r.json()
			file_name = folder_name + str(id)
			if not os.path.exists(os.path.dirname(file_name)):
    			try:
    				os.makedirs(os.path.dirname(file_name))
    			except OSError as exc: # Guard against race condition
        	if exc.errno != errno.EEXIST:
            	raise
			with open(str(file_name), 'w') as outfile:
				json.dump(r, outfile)
			count += 1
		id += 1
		url = url_type + str(id)
		r = requests.get(url)
		print(r.status_code)
		print(url)
	

# ----
# main
# ----

if __name__ == "__main__":
    # jikanget('http://jikan.me/api/anime/', 100, 'jikan_anime')
    jikanget('http://jikan.me/api/manga/', 100, 'jikan_manga')
    # test()