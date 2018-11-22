# For dealing with the species mapping.

map_file = 'genus_to_db.map'


def read_map(resource_dir) -> dict:
    genus_to_db = dict()

    with open(resource_dir + '/' + map_file, 'r') as map_fh:
        for line in map_fh.readlines():
            data = line.rstrip().split(' ')
            genus_to_db[data[0]] = data[1]
    return genus_to_db

