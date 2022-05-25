#!/usr/bin/env python3

import sys
from juju import loop
from juju.controller import Controller


async def status(endpoint, username, password, cacert, model, apps):
    with open(cacert, 'r') as juju_id_rsa:
        cert = juju_id_rsa.read()

    controller = Controller()
    await controller.connect(endpoint=endpoint, username=username, password=password, cacert=cert)
    v5_prod = await controller.get_model(model)
    tom_model = await v5_prod.get_status()
    # print(tom_model.applications['tomcms']['units']['tomcms/0']['public-address'])
    for app in tom_model.applications:
        if app in apps.split(','):
            for instance in tom_model.applications[app]['units']:
                print(instance + '@' + tom_model.applications[app]['units'][instance]['public-address']);

if __name__ == '__main__':
    #print(sys.argv)
    assert len(sys.argv) == 7, 'Invalid number of arguments'
    loop.run(status(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]))
