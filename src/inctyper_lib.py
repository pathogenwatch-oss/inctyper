# For dealing with the species mapping.

map_file = 'genus_to_db.map'


def read_map(resource_dir: str) -> dict:
    genus_to_db = dict()

    with open(resource_dir + '/' + map_file, 'r') as map_fh:
        for line in map_fh.readlines():
            data = line.rstrip().split(' ')
            genus_to_db[data[0]] = data[1]
    return genus_to_db


def overlapping(match1, match2, threshold) -> bool:
    if match1['qstart'] <= match2['qend'] <= match1['qend']:
        overlap_length = match2['qend'] - match1['qstart'] + 1
    elif match2['qstart'] <= match1['qend'] <= match2['qend']:
        overlap_length = match1['qend'] - match2['qstart'] + 1
    else:
        overlap_length = 0

    return threshold < overlap_length


def select_matches(matches: list) -> list:
    sorted_matches = sorted(matches, key=lambda match: match['pid'], reverse=True)
    kept = list()
    skip = set()
    for i in range(0, len(sorted_matches)):
        if i not in skip:
            kept.append(sorted_matches[i])
            for j in range(i + 1, len(sorted_matches)):
                if overlapping(sorted_matches[i], sorted_matches[j], 20):
                    skip.add(j)
    return kept
