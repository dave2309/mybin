import sys
from juju import loop
from juju.controller import Controller


async def status(endpoint, username, password, cacert):
    with open(cacert, 'r') as juju_id_rsa:
        cert = juju_id_rsa.read()

    controller = Controller()
    await controller.connect(endpoint=endpoint, username=username, password=password, cacert=cert)
    v5_prod = await controller.get_model('v5-prod')
    tom_model = await v5_prod.get_status()
    print(tom_model.applications['tomcms']['units']['tomcms/0']['public-address'])


if __name__ == '__main__':
    print(sys.argv)
    assert len(sys.argv) == 5, 'Invalid number of arguments'
    loop.run(status(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
