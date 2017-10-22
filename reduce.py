import os
import json

def reduce_anime():
    # count = 1
    for filename in os.listdir('jikan_anime'):
        read_file = 'jikan_anime/' + filename
        with open(read_file) as datafile:
            print('filename: ' + filename)
            # print(count)
            # print('')
            data = json.load(datafile)
            reduced_data = {}
            reduced_data['id'] = filename
            reduced_data['title'] = data['title']
            dates = data['aired'].split('to')
            premiered = dates[0]
            reduced_data['year'] = premiered.strip()
            reduced_data['genre'] = data['genre']
            reduced_data['score'] = data['score']
            reduced_data['num_episodes'] = data['episodes']
            reduced_data['synopsis'] = data['synopsis']
            reduced_data['media_type'] = data['type']
            reduced_data['picture'] = data['image']
            reduced_data['status'] = data['status']
            if 'youtubeVideoId' in data:
                reduced_data['youtube_id'] = data['youtubeVideoId']
            else:
                reduced_data['youtube_id'] = 'null'
            # count += 1
            if not os.path.exists('reduced_anime'):
                    try:
                        os.makedirs('reduced_anime')
                    except OSError, exc:

                                # Guard against race condition

                        if exc.errno != errno.EEXIST:
                            raise
            filename = 'reduced_anime/' + filename + '.txt'
            if os.path.isfile(filename) == False:
                    with open(str(filename), 'w') as outfile:
                        json.dump(reduced_data, outfile)
                    

def reduce_manga():
    for filename in os.listdir('jikan_manga'):
        read_file = 'jikan_manga/' + filename
        with open(read_file) as datafile:
            data = json.load(datafile)
            # print('filename: ' + filename)
            reduced_data = {}
            reduced_data['id'] = filename
            reduced_data['title'] = data['title']
            reduced_data['author'] = data['author']
            dates = data['published'].split('to')
            premiered = dates[0]
            reduced_data['year'] = premiered.strip()
            reduced_data['genre'] = data['genre']
            if 'score' in data:
                reduced_data['score'] = data['score']
            else:
                reduced_data['score'] = 'null'
            reduced_data['num_chapters'] = data['chapters']
            reduced_data['synopsis'] = data['synopsis']
            reduced_data['media_type'] = data['type']
            reduced_data['picture'] = data['image']
            reduced_data['status'] = data['status']
            if not os.path.exists('reduced_manga'):
                    try:
                        os.makedirs('reduced_manga')
                    except OSError, exc:

                                # Guard against race condition

                        if exc.errno != errno.EEXIST:
                            raise
            filename = 'reduced_manga/' + filename + '.txt'
            if os.path.isfile(filename) == False:
                    with open(str(filename), 'w') as outfile:
                        json.dump(reduced_data, outfile)

def reduce_character():
    for filename in os.listdir('jikan_character'):
        read_file = 'jikan_character/' + filename
        with open(read_file) as datafile:
            data = json.load(datafile)
            print('filename: ' + filename)
            reduced_data = {}
            reduced_data['id'] = filename
            reduced_data['name'] = data['name']
            reduced_data['about'] = data['about']
            reduced_data['japanese_name'] = data['name-japanese']
            reduced_data['picture'] = data['image']

def reduce_person():
    for filename in os.listdir('jikan_person'):
        read_file = 'jikan_person/' + filename
        with open(read_file) as datafile:
            data = json.load(datafile)
            reduced_data = {}
            reduced_data['id'] = filename
            name_tokens = data['link-canonical'].split('/')
            name = name_tokens[5]
            name = name.replace('_', ' ')
            reduced_data['name'] = name
            # reduced_data['language'] =
            if data['birthday'] in data:
                reduced_data['birthday'] = data['birthday']
            else:
                reduced_data['birthday'] = 'null'
            reduced_data['picture'] = data['image']


if __name__ == "__main__":
    # reduce_anime()
    # reduce_manga()
    # reduce_character()
    # reduce_person()