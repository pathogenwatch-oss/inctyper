"""Script uses database from PlasmidFinder to identify inc types"""
import json
import subprocess
import sys
from collections import defaultdict

import inctyper_lib as lib


def resolve_inctype(header: str) -> str:
    # Anything after a double underscore is irrelevant.
    first_part = header.rstrip().split('__')[0]
    smaller_parts = first_part.split('_')
    # If there's only one part left, that is the Inc Type, otherwise it's the first two parts
    if 1 == len(smaller_parts):
        return smaller_parts[0]
    else:
        return '_'.join(smaller_parts[0:2])


query_file = sys.argv[1]

genus_id = sys.argv[2]

resource_dir = sys.argv[3] if len(sys.argv) == 4 else 'db/'

genus_map = lib.read_map(resource_dir)

if genus_id not in genus_map:
    print('{}', file=sys.stdout)
    exit(0)

inc_db = 'db/' + genus_map[genus_id] + '_inc_reps'

blast_cmd = ['blastn',
             '-query', query_file,
             '-db', inc_db,
             '-outfmt', '6 qseqid sseqid qlen slen qstart qend sstart send pident evalue',
             '-evalue', '1e-35',
             '-perc_identity', '90.0',
             '-max_target_seqs', '1000']

p = subprocess.Popen(blast_cmd, stdout=subprocess.PIPE)

return_code = p.returncode

# Read result file and write as json blob
matches = defaultdict(list)

for line in p.stdout.readlines():
    data = line.decode('UTF-8').rstrip().split('\t')
    # Check the length coverage
    coords = sorted([int(data[6]), int(data[7])])

    cov = ((coords[1] - coords[0] + 1) / float(data[3])) * 100

    if cov < 100.0:
        # Fragment match
        continue

    if float(data[8]) < 90:
        continue

    inc_type = resolve_inctype(data[1])

    matches[data[0]].append(
        {'Contig': data[0], 'Match ID': data[1], 'Inc Match': inc_type, 'Percent Identity': round(float(data[8]), 3),
         'Match Coverage': round(float(cov), 3), 'Contig Start': int(data[4]), 'Contig End': int(data[5]),
         'Reference Start': int(data[6]), 'Reference End': int(data[7])})

results = list()

for contig in matches.keys():
    results.extend(sorted(lib.select_matches(matches[contig]), key=lambda match: match['Contig Start']))

jsonResult = {'Inc Matches': results}
print(json.dumps(jsonResult, indent=4), file=sys.stdout)
