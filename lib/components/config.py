#!/usr/bin/python3

import json
import os
import sys

BROWNIE_FOLDER = sys.modules['__main__'].__file__.rsplit('/',maxsplit = 1)[0]
CONFIG = json.load(open(BROWNIE_FOLDER+'/config.json', 'r'))

conf_path = os.path.abspath('.')+"/brownie-config.json"
if os.path.exists(conf_path):
    for k,v in json.load(open(conf_path, 'r')).items():
        if type(v) is dict and k in CONFIG:
            CONFIG[k].update(v)
        else: CONFIG[k] = v

try:
    CONFIG['logging'] = CONFIG['logging'][sys.argv[1]]
    for k,v in [(k,v) for k,v in CONFIG['logging'].items() if type(v) is list]:
       CONFIG['logging'][k] = v[1 if '--verbose' in sys.argv else 0]
except:
    CONFIG['logging'] = {"tx":1 ,"exc":1}

if '--network' in sys.argv:
    CONFIG['active_network'] = sys.argv[sys.argv.index('--network')+1]
else:
    CONFIG['active_network'] = CONFIG['default_network']

print(CONFIG['active_network'])

if CONFIG['active_network'] not in CONFIG['networks']:
    sys.exit("ERROR: No network named '{}'".format(CONFIG['active_network']))