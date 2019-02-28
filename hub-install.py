#!/usr/bin/env python3

import os,requests,platform,json,subprocess
import tarfile
from zipfile import ZipFile

debug=False
os_type=platform.system().lower()
machine_type=platform.machine().lower()

if debug:print(f'Your OS and Machine Type is {os_type} and {machine_type}')

if machine_type in ['x64', 'x86_64', 'amd64']: machine_type='amd64'
if machine_type in ['386', '686']: machine_type='386'


LIB_URL='https://api.github.com/repos/github/hub/releases/latest'
def get_urls(LIB_URL,cache=True):
    # Caching done to avoid rate limiting : Atleast during the script development phase
    if os.path.isfile('cache.json'):
        temp=json.loads(open('cache.json','r').read())
    else:
        response = requests.get(LIB_URL)
        temp=json.loads(response.content)
        cache=True
    links=[temp['assets'][i]['browser_download_url'] for i in range(len(temp['assets']))]
    version=temp['tag_name']
    if cache:
        with open('cache.json', 'w') as outfile:
            json.dump(temp, outfile)
    return links,version

def download_data(url, dest_dir='.'):
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    base = os.path.basename(url)
    temp_dest_path = os.path.join(dest_dir, base)

    # Download only if file doesnt exist
    if not os.path.isfile(temp_dest_path):
        with open(temp_dest_path, "wb") as f:
            r = requests.get(url)
            f.write(r.content)
            if debug: print('Completed Downloading') #debug

    if base.endswith('.tgz'):
        obj = tarfile.open(temp_dest_path)
        dest=temp_dest_path.rstrip('.tgz')

    elif base.endswith('.zip'):
        obj = ZipFile(temp_dest_path, 'r')
        dest=temp_dest_path.rstrip('.zip')
    else:
            raise ValueError("Unknown File Type: {0}.".format(base))

    if debug: print("Extracting the Archive")

    obj.extractall(dest_dir)
    obj.close()
    os.remove(temp_dest_path)
    return dest


# Identify the Corresponding URL
links,version=get_urls(LIB_URL)
if debug: print(f"Latest Version of Hub {version}")

download_link=[link for link in links if ((os_type in link ) & (machine_type in link)) ]
if len(download_link)==0:
  print('Platform not Supported.')
  sys.exit()

if debug : print(f'Downloading the Archive from :{download_link[0]}')
loc=download_data(download_link[0])

env = {}
#Call OS Specific Installation Script:
if os_type =='linux' or os_type =='mac':
    cmd=f'{loc}/install'
    # Check for Conda Based Environment
    if 'CONDA_DEFAULT_ENV' in os.environ.keys():
        if debug : print('Script Executed inside Conda Environment')
        env["prefix"] = os.environ['CONDA_PREFIX']
elif os_type=='windows':
    cmd=f'install.bat'

# Installation of hub library

print(f"running: {cmd} (env={env})")
my_env = {**os.environ, **env}
subprocess.run(cmd.split(),shell=False, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)

print("hub installed")
