import datetime
import glob
import json
import os
import subprocess
import sys
import urllib.request
import shutil

"""Script downloads and sets up the inc typing library"""

db_url = 'https://bitbucket.org/genomicepidemiology/plasmidfinder_db/get/master.zip'
data_dir = 'db'
reps_db_name = 'plasmidfinder_db.zip'

if not os.path.exists(data_dir):
    os.makedirs(data_dir, exist_ok=True)

gp_data_dir = data_dir + '/gram_positive'
if not os.path.exists(gp_data_dir):
    os.makedirs(gp_data_dir, exist_ok=True)

gn_data_dir = data_dir + '/gram_negative'
if not os.path.exists(gn_data_dir):
    os.makedirs(gn_data_dir, exist_ok=True)

urllib.request.urlretrieve(db_url, reps_db_name)

# makeblastdb.
subprocess.run(['unzip', '-o', reps_db_name])

for file in glob.glob('genomic*'):
    source_dir = file

# Gram positive database list
gp_libs = []
with open(source_dir + '/config', 'r') as config_fh:
    for line in config_fh.readlines():
        if 'Gram Positive' in line:
            gp_libs.append(line.split('\t')[0])

# Create gram negative files
print('Building', ', '.join(gp_libs), file=sys.stderr)
gp_build_lib = gn_data_dir + '/all.fna'
shutil.move(source_dir + '/' + 'enterobacteriales.fsa', gn_data_dir)
os.chdir(gn_data_dir)
subprocess.run(['makeblastdb', '-in', 'enterobacteriales.fsa', '-out', 'all', '-dbtype', 'nucl'])
os.chdir('../..')

# Create gram positive files
os.chdir(gp_data_dir)
for gp_lib in gp_libs:
    print('Moving ' + gp_lib, file=sys.stderr)
    shutil.move('../../' + source_dir + '/' + gp_lib + '.fsa', '.')
    subprocess.run(['makeblastdb', '-in', gp_lib + '.fsa', '-out', gp_lib, '-dbtype', 'nucl'])
os.chdir('../..')

os.chdir(data_dir)
# Write the metadata out.
metadata = {'url': db_url, 'timestamp': '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())}
with open('metadata.jsn', 'w') as m_fh:
    print(json.dumps(metadata, indent=4), file=m_fh)
os.chdir('..')

subprocess.run('rm -rf genomicepidemiology* inc_reps.fna.zip', shell=True)
