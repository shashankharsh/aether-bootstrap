
import logging
import os
from queue import Queue
from multiprocessing import Pool
from uuid import uuid4

from data import simple_schema

from aether.client import Client

LOAD_PARALLELISM = 25
LOAD_ENTITIES = 1000

log = logging.getLogger("AssetGeneration:")

def env(key):
    return os.environ.get(key, False)


def create_load(client, project):
    out_queue = Queue()
    pool = Pool(processes=LOAD_PARALLELISM)
    for i in range(LOAD_PARALLELISM):
        print(f'launch {i}')
        pool.apply_async(load_handler ,args=(i,))
    pool.close()
    pool.join()
    print('done')
        
def log_completion(i):
    print(f'{i} completed')

def load_handler(process_id):
    # create artifacts
    print(f'{process_id} started')
    name = f'testchannel5{process_id}'
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
    ps_id = project_schema.id
    for x in range(LOAD_ENTITIES):
        print(f'{process_id} : {x}')
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

if __name__ == "__main__":
    reqs = ['KERNEL_URL', 'KERNEL_USER', 'KERNEL_PASSWORD']
    if False in [env(r) for r in reqs]:
        log.error('Required Environment Variable is missing.')
        log.error('Required: %s' % (reqs,))
        sys.exit(1)
    # args = sys.argv
    # seed = 1000
    # try:
    #     if len(args) > 1 and isinstance(int(args[1]), int):
    #         seed = int(args[1])
    # except ValueError:
    #     pass
    url = env('KERNEL_URL')
    username = env('KERNEL_USER')
    password = env('KERNEL_PASSWORD')
    global client
    client = Client(url, username, password)
    global project
    project = [i for i in client.projects.paginated('list')][0]
    create_load(client, project)


