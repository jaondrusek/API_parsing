

def reduce_anime:
    for filename in os.listdir('jikan_anime'):
        read_file = 'jikan_anime/' + filename
        with open(read_file) as datafile:
            data = json.load(datafile)
            reduced_data = {}
            reduced_data['id'] = data['id']
            reduced_data['title'] = data['title']
            reduced_data['year'] = 
            reduced_data['genre'] =
            reduced_data['score'] =
            reduced_data['num_episodes'] =
            reduced_data['synopsis'] =
            reduced_data['showType'] =
            reduced_data['picture'] =
            reduced_data['status'] =

def reduce_manga:


def reduce_character:


def reduce_person:


if __name__ == "__main__":
    