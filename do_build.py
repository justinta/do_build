import argparse
import digitalocean
import sys


from ns1 import NS1


DO_TOKEN = ''
NS1_TOKEN = ''

manager = digitalocean.Manager(token=DO_TOKEN)
api = NS1(apiKey = NS1_TOKEN)



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--create', action='store_true', default=False, help='creates a droplet')
    parser.add_argument('--get', action='store_true', default=False, help='get droplet/zone info')
    parser.add_argument('--name', help='name to create')
    parser.add_argument('--size', default='s-2vcpu-2gb-intel', help='size of image')

    return parser.parse_args()

def create_droplet(droplet_name, size, image='centos-7-x64'):
    '''
    creates droplet
    '''
    keys = manager.get_all_sshkeys()
    droplet = digitalocean.Droplet(token=DO_TOKEN,
                                   name=droplet_name,
                                   region='sfo3',
                                   image=image,
                                   size_slug=size,
                                   ssh_keys=keys,
                                   backups=False)

    droplet.create()
    return droplet


def create_ns1_record(droplet_data):
    '''
    Update/create ns1 domain in justinta.com zone
    '''

    zone = api.loadZone('justinta.com')
    records = api.records()
    records.create(zone.zone, droplet_data.name, 'A', answers=droplet_data.ip_address)
    return 'DNS created'


def create(name, size, image='centos-7-x64'):

    drop = create_droplet(name, size, image)

    actions = drop.get_actions()
    status = 'in-progress'
    print(status)
    while status != 'completed':
        for action in actions:
            action.load()
            status = action.status

    print(status)
    droplet_data = manager.get_droplet(droplet.id)
    print(create_ns1_record(droplet_data))




def delete_ns1_record(zone, record):
    '''
    delete record in ns1
    '''
    pass


def main():

    args = parse_args()

    if args.create:
        if not args.name:
            sys.exit('use --name')
        droplet = create_droplet(args.name, args.size)

        actions = droplet.get_actions()
        status = 'in-progress'
        print(status)
        while status != 'completed':
            for action in actions:
                action.load()
                status = action.status

        print(status)
        droplet_data = manager.get_droplet(droplet.id)
        print(create_ns1_record(droplet_data))

    if args.get:
        droplets = manager.get_all_droplets()
        for droplet in droplets:
            if droplet.name == args.name:
                create_ns1_record(droplet)
    if args.delete:
        droplets = manager.get_all_droplets()
        for droplet in droplets:
            if droplet.name == args.name:
                droplet.destroy()



if __name__ == '__main__':
    main()



'''
Sizes:

[s-1vcpu-1gb, s-1vcpu-1gb-amd, s-1vcpu-1gb-intel, s-1vcpu-2gb, s-1vcpu-2gb-amd, s-1vcpu-2gb-intel, s-2vcpu-2gb, s-2vcpu-2gb-amd, s-2vcpu-2gb-intel, s-2vcpu-4gb, s-2vcpu-4gb-amd, s-2vcpu-4gb-intel, s-4vcpu-8gb, c-2, c2-2vcpu-4gb, s-4vcpu-8gb-amd, s-4vcpu-8gb-intel, g-2vcpu-8gb, gd-2vcpu-8gb, s-8vcpu-16gb, m-2vcpu-16gb, c-4, c2-4vcpu-8gb, s-8vcpu-16gb-amd, s-8vcpu-16gb-intel, m3-2vcpu-16gb, g-4vcpu-16gb, so-2vcpu-16gb, m6-2vcpu-16gb, gd-4vcpu-16gb, so1_5-2vcpu-16gb, m-4vcpu-32gb, c-8, c2-8vcpu-16gb, m3-4vcpu-32gb, g-8vcpu-32gb, so-4vcpu-32gb, m6-4vcpu-32gb, gd-8vcpu-32gb, so1_5-4vcpu-32gb, m-8vcpu-64gb, c-16, c2-16vcpu-32gb, m3-8vcpu-64gb, g-16vcpu-64gb, so-8vcpu-64gb, m6-8vcpu-64gb, gd-16vcpu-64gb, so1_5-8vcpu-64gb, m-16vcpu-128gb, c-32, c2-32vcpu-64gb, m3-16vcpu-128gb, m-24vcpu-192gb, g-32vcpu-128gb, so-16vcpu-128gb, m6-16vcpu-128gb, gd-32vcpu-128gb, m3-24vcpu-192gb, g-40vcpu-160gb, so1_5-16vcpu-128gb, m-32vcpu-256gb, gd-40vcpu-160gb, so-24vcpu-192gb, m6-24vcpu-192gb, m3-32vcpu-256gb, so1_5-24vcpu-192gb, so-32vcpu-256gb, m6-32vcpu-256gb, so1_5-32vcpu-256gb]


images (id, slug):
(69452245, 'freebsd-11-x64-zfs')
(69500386, 'freebsd-11-x64-ufs')
(72181180, 'ubuntu-20-10-x64')
(74885442, 'centos-8-x64')
(77558491, 'freebsd-12-x64-ufs')
(77558552, 'freebsd-12-x64-zfs')
(78547182, 'rancheros')
(84726136, 'fedora-33-x64')
(84729581, 'debian-9-x64')
(84729642, 'debian-10-x64')
(84780421, 'ubuntu-18-04-x64')
(84780478, 'ubuntu-20-04-x64')
(84780898, 'fedora-34-x64')
(84783446, 'ubuntu-21-04-x64')
(84783821, 'centos-7-x64')
(49506692, 'skaffolder-18-04')
(50270443, 'izenda-18-04')
(51476094, 'quickcorp-qcobjects-18-04')
(52318955, 'fathom-18-04')
(58037406, 'optimajet-workflowserver-18-04')
'''

