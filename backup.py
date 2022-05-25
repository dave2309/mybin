#!/usr/bin/env python3

import argparse
import logging
from juju import loop
from juju.controller import Controller
from juju.unit import Unit
from juju.model import Model

log = logging.getLogger(__name__)

async def backup():
    # logging.debug('unit %s', unit.name)
    log.info('Trying to connect to juju')

    # controller = Controller()
    # await controller.connect(endpoint=args.endpoint, username=args.username, password=args.password, cacert=args.certificate)
    # model = await controller.get_model(args.model)

    # Get current model from
    model = Model()
    await model.connect_current()

    # Elect one non leader percona server
    found = False
    for unit in model.units:
        if args.application in unit and 'hacluster' not in unit:
            unit_instance = Unit(unit, model)
            if False == await unit_instance.is_leader_from_status():
                found = True;
                break

    if not found:
        log.info('No suitable server to perform backup on found, exiting...')
        return

    # Perform the backup
    log.info('Backing up from: %s', unit_instance.name)
    action = await unit_instance.run_action('backup')
    log.info('Backup on: %s, done', unit_instance.name)

    # Get backup date
    log.info('Last backup checking...')
    action = await unit_instance.run('ls -1rd ' + args.inputdir + '/* |head -n1')
    folder = action.results['Stdout'].rstrip()
    date = folder.split('/')[-1]
    log.info('Last backup found at: %s', folder)
    log.info('Last backup date: %s', date)

    # Create tar file
    filename = '/home/ubuntu/mysql-backups-' + date + '.tar.xz'
    log.info('Compressing data to: %s', filename)
    action = await unit_instance.run('nice -n19 ionice -c2 -n7 tar -zcf ' + filename + ' ' + folder + '/')
    if int(action.results['Code']) > 0:
        log.error('Can not create backup tar file')
        return

    # action = await unit.run('tar -Jcf mysql-backups-
    machine = model.machines[unit_instance.machine.id]
    log.info('Copying file %s to %s', filename, args.outputdir)
    await machine.scp_from(filename, args.outputdir)
    log.info('done')

    log.info('Backup Terminated')

if __name__ == '__main__':
    # Set logger level
    logging.basicConfig(level=logging.INFO)

    # Parse command line options
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--application', help='application to filter units from', default='mysql')
    parser.add_argument('-c', '--certificate', help='PEM certificate file', default='.local/share/juju/cacert.pem')
    parser.add_argument('-e', '--endpoint', help='endpoint to connect to', default='127.0.0.1:8443')
    parser.add_argument('-i', '--inputdir', help='where backup files are dump', default='/opt/backups/mysql')
    parser.add_argument('-m', '--model', help='model name', default='default')
    parser.add_argument('-o', '--outputdir', help='where backup files are stored', default='/tmp')
    parser.add_argument('-p', '--password', help='password', default='juju')
    parser.add_argument('-u', '--username', help='username', default='juju')

    args = parser.parse_args()

    # read the certificate
    if args.certificate:
        with open(args.certificate, 'r') as juju_id_rsa:
            args.certificate = juju_id_rsa.read()

    # Enter the main loop
    loop.run(backup())
