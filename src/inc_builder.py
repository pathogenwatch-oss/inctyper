import datetime
import json
import os
import subprocess
import urllib.request

"""Script downloads and sets up the inc typing library"""

db_url = 'https://bitbucket.org/genomicepidemiology/plasmidfinder_db/get/master.zip'
data_dir = 'db'
reps_db_name = 'inc_reps'

if not os.path.exists(data_dir):
    os.makedirs(data_dir, exist_ok=True)

os.chdir(data_dir)

urllib.request.urlretrieve(db_url, reps_db_name + '.fna.zip')

# makeblastdb.
unzip_cmd = ['unzip', '-o', reps_db_name + '.fna.zip']

mv_cmd1 = 'mv gen*/enterobacteriaceae.fsa ' + 'gram_negative_inc_reps' + '.fna && mv gen*/gram_positive.fsa ' + \
          'gram_positive_inc_reps' + '.fna'

makedb_cmd1 = ['makeblastdb', '-in', 'gram_negative_inc_reps' + '.fna', '-out', 'gram_negative_inc_reps', '-dbtype', 'nucl']
makedb_cmd2 = ['makeblastdb', '-in', 'gram_positive_inc_reps' + '.fna', '-out', 'gram_positive_inc_reps', '-dbtype', 'nucl']

subprocess.run(unzip_cmd)
subprocess.run(mv_cmd1, shell=True)
subprocess.run(makedb_cmd1)
subprocess.run(makedb_cmd2)
subprocess.run('rm -rf genomicepidemiology* inc_reps.fna.zip', shell=True)
# Write the metadata out.
metadata = {'url': db_url, 'timestamp': '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())}

with open('metadata.jsn', 'w') as m_fh:
    print(json.dumps(metadata, indent=4), file=m_fh)

os.chdir('..')
