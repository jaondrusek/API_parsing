import fileinput

def fix():
    for filename in os.listdir('jikan_anime'):
        read_file = 'jikan_anime/' + filename
        with open(read_file) as datafile:
            with fileinput.FileInput(datafile, inplace=True, backup='.bak') as file:
                for line in file:
                    print(line.replace('&#039', '\''), end='')

if __name__ == "__main__":
    fix()