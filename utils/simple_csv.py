import glob
import os.path as op
import sys

import jsonpickle


def write_line(data_file: str):
    name = op.splitext(op.splitext(op.basename(data_file))[0])[0]

    with open(data_file, 'r') as blob_fh:
        content = blob_fh.read()

    match_data = jsonpickle.decode(content)

    inc_types = list()
    for match in match_data['Inc Matches']:
        inc_types.append(match['Inc Type'])

    print(name, '"' + ', '.join(sorted(inc_types)) + '"', sep=',')


data_directory = sys.argv[1]
# print(data_directory, file=sys.stderr)

print('id', 'Inc Types')
for file in glob.glob(data_directory + '*.out'):
    # print(file, file=sys.stderr)
    write_line(file)
