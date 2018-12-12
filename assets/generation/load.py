#!/usr/bin/env python

# Copyright (C) 2018 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import logging
from multiprocessing import Pool
import os
from queue import Queue
import sys
from uuid import uuid4

from data import simple_schema

from aether.client import Client, AetherAPIException

log = logging.getLogger("AssetGeneration:")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s [AssetGeneration:] %(levelname)-8s %(message)s'))
log.addHandler(handler)
log.setLevel(logging.DEBUG)

def env(key):
    return os.environ.get(key, False)


def create_load(client, project):
    out_queue = Queue()
    pool = Pool(processes=LOAD_PARALLELISM)
    results = []
    loads = tuple([ i for i in range(LOAD_PARALLELISM)])
    res = pool.map(load_handler ,loads)
    log.debug('done')
        
def log_completion(i):
    log.info(f'{i} completed')

def load_handler(process_id):
    # create artifacts
    
    name = f'testchannel{RUN_NUMBER}{process_id}'
    log.info(f'{name} started')
    try:
        definition = dict(simple_schema)
        def gen():
            return {
                'id': str(uuid4()),
                'rev': '1',
                'name': str(uuid4())
            }

        definition['name'] = name 
        tpl = {
            'id': str(uuid4()),
            'name': name,
            'type': 'record',
            'revision': '1',
            'definition': definition
        }
        Schema = client.get_model('Schema')
        schema = Schema(**tpl)
        client.schemas.create(data=schema)
        PS = client.get_model('ProjectSchema')
        ps = PS(
            id=str(uuid4()),
            name=schema.name,
            revision='1',
            project=project.id,
            schema=schema.id)
        project_schema = client.projectschemas.create(data=ps)
    except AetherAPIException as err:
        # schema exists, look it up
        project_schema = [i for i in client.projectschemas.paginated('list', name=name)][0]
        
    ps_id = project_schema.id
    for x in range(LOAD_ENTITIES):
        if (x % 100 == 0):
            log.debug(f'{name} : {x}')
        payload = gen()
        data = {
            "id": payload['id'],
            "payload": payload,
            "projectschema": ps_id,
            "mapping_revision": "None",
            "status": "Publishable"
        }
        client.entities.create(data=data)
        #out_queue.put(obj.id)
    return process_id

def check_arg(pos, args):
    try:
        if len(args) > (pos) and isinstance(int(args[pos]), int):
            return int(args[pos])
    except ValueError:
        log.error(args[pos] + ' was a bad value for position ' + pos)
        return None

if __name__ == "__main__":
    global LOAD_ENTITIES, LOAD_PARALLELISM, RUN_NUMBER
    reqs = ['KERNEL_URL', 'KERNEL_USER', 'KERNEL_PASSWORD']
    if False in [env(r) for r in reqs]:
        log.error('Required Environment Variable is missing.')
        log.error('Required: %s' % (reqs,))
        sys.exit(1)
    args = sys.argv
    url = env('KERNEL_URL')
    username = env('KERNEL_USER')
    password = env('KERNEL_PASSWORD')
    log.debug(args)
    LOAD_ENTITIES = check_arg(1, args) or 100
    LOAD_PARALLELISM = check_arg(2, args) or 1
    RUN_NUMBER = check_arg(3, args) or 1

    log.debug(f'{LOAD_PARALLELISM} threads creating {LOAD_ENTITIES} for run# {RUN_NUMBER}')

    global client
    client = Client(url, username, password)
    global project
    project = [i for i in client.projects.paginated('list')][0]
    create_load(client, project)
