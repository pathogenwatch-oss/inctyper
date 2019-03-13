import subprocess
import sys
from pathlib import Path


# Map genus to gram+/-


def extract_genus_id(record):
    return record.lstrip().rstrip().split(' ')[0]


def read_lists(config_dir) -> dict:
    taxon_to_gram_type = dict()

    for file in config_dir.glob('*_taxon_ids.txt'):
        gram_type = str(file.name).replace('_taxon_ids.txt', '')
        with open(file, 'r') as src_fh:
            for line in src_fh.readlines():
                taxon_to_gram_type[line.rstrip()] = gram_type

    return taxon_to_gram_type


# Genus example (one line from grep)
# mirko-air:bin coriny$ ./taxonkit list --ids 570 --show-rank --show-name | grep "\[genus\]"
# 570 [genus] Klebsiella
# Species example (no output from grep)
# mirko-air:bin coriny$ ./taxonkit list --ids 1280 --show-rank --show-name | grep "\[genus\]"
# mirko-air:bin coriny$
# High level example (lots of output)
# mirko-air:bin coriny$ ./taxonkit list --ids 1224 --show-rank --show-name | grep "\[genus\]" | head
# 262 [genus] Francisella
# 1234547 [genus] Candidatus Nebulobacter
# 1869285 [genus] Allofrancisella
# 330062 [genus] Candidatus Endoecteinascidia
def extract_genus_maps(taxid_dict):

    genus_to_gram_type = dict()

    for taxid in taxid_dict.keys():

        print(taxid, file=sys.stderr)
        command = [taxonkit_path, 'list', '--ids', taxid, '--show-rank', '--show-name']

        lookup_process = subprocess.Popen(command, stdout=subprocess.PIPE)

        genuses = list(filter(lambda x: '[genus]' in x,
                              [line.decode('UTF=8').lstrip().rstrip() for line in lookup_process.stdout.readlines()]))

        for line in genuses:
            print(line, file=sys.stderr)
            genus_id = extract_genus_id(line)
            genus_to_gram_type[genus_id] = taxid_dict[taxid]

    return genus_to_gram_type


library_directory = Path(sys.argv[1])

taxonkit_path = sys.argv[2] if 2 < len(sys.argv) else 'taxonkit'

library_taxids = read_lists(library_directory)

id_map = extract_genus_maps(library_taxids)

with open('genus_to_db.map', 'w') as db_map:
    for taxid in id_map.keys():
        print(taxid, id_map[taxid], file=db_map)
