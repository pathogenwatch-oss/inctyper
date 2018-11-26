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
    if match1['Contig Start'] <= match2['Contig End'] <= match1['Contig End']:
        overlap_length = match2['Contig End'] - match1['Contig Start'] + 1
    elif match2['Contig Start'] <= match1['Contig End'] <= match2['Contig End']:
        overlap_length = match1['Contig End'] - match2['Contig Start'] + 1
    else:
        overlap_length = 0

    return threshold < overlap_length


def select_matches(matches: list) -> list:
    sorted_matches = sorted(matches, key=lambda match: match['Percent Identity'], reverse=True)
    kept = list()
    skip = set()
    for i in range(0, len(sorted_matches)):
        if i not in skip:
            kept.append(sorted_matches[i])
            for j in range(i + 1, len(sorted_matches)):
                if overlapping(sorted_matches[i], sorted_matches[j], 20):
                    skip.add(j)
    return kept
