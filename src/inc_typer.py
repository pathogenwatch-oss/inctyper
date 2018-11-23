"""Script uses database from PlasmidFinder to identify inc types"""
import json
import subprocess
import sys
from collections import defaultdict

import inctyper_lib as lib

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
             '-perc_identity', '95',
             '-max_target_seqs', '1000']

p = subprocess.Popen(blast_cmd, stdout=subprocess.PIPE)

return_code = p.returncode

# Read result file and write as json blob
matches = defaultdict(list)

for line in p.stdout.readlines():
    data = line.decode('UTF-8').rstrip().split('\t')
    # Check the length coverage
    coords = sorted([int(data[6]), int(data[7])])

    cov = (coords[1] - coords[0] + 1) / float(data[3])

    if cov < 0.6:
        # Fragment match
        continue

    matches[data[0]].append(
        {'contig': data[0], 'id': data[1], 'qstart': int(data[4]), 'qend': int(data[5]), 'sstart': int(data[6]),
         'send': int(data[7]), 'pid': float(data[8]), 'cov': float(cov)})

results = list()

for contig in matches.keys():
    results.extend(sorted(lib.select_matches(matches[contig]), key=lambda match: match['qstart']))

print(json.dumps(results, indent=4), file=sys.stdout)
