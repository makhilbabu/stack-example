# command server

# help documentation
# commands possible :
# aggiestack server create --image IMAGE --flavor FLAVOR_NAME INSTANCE_NAME ---> creates instance INSTANCE_NAME, boots from IMAGE, configured as FLAVOR_NAME

# aggiestack server delete INSTANCE_NAME ---> delete the instance INSTANCE_NAME

# aggiestack server list ---> list all running servers (name, image and flavor)

import os
from shutil import copyfile
from admin import parse_hardware
from admin import parse_flavors
from admin import admin_can_host_command
from helpers import log
from helpers import parse_images
from helpers import parse_instances
from helpers import update_instances
from helpers import parse_hardware
from helpers import update_hardware

def server_create_command(arg1, arg2, arg3, arg4 = ''):
    # arg1 => IMAGE_NAME
    # arg2 => FLAVOR_NAME
    # arg3 => INSTANCE_NAME
    # arg4 => executed command

    directory = os.path.dirname(os.path.realpath(__file__)) 
    src_path = os.path.join(os.getcwd(), arg2)
    
    images = parse_images()
    flavors = parse_flavors()
    instances = parse_instances()
    if arg1 in images:
        if agr2 in flavors:
            instances[arg3] = {'image': arg1, 'flavor': arg2}
            # search for a server (verify if it can_host)
            hardware = parse_hardware('current')
            servers = hardware['server']
            flavors = parse_flavors()
            
            runnable_servers = []
            for server in servers.keys():
                if admin_can_host_command(server, arg2, executed_command):
                    runnable_servers.append(server)
            
            # re do a sophisticated strategy for choosing server
            if runnable_servers:
                server = runnable_servers[0]
            else:
                ERR_MSG = 'ERROR: ' + str(arg3) + ' cannot be instantiated now due to shortage of resources'
                log(arg4, 'FAILURE\n', ERR_MSG)
                return
            
            instances[arg3]['server'] = servers[server]
            updated = update_instances(instances)
            
            # update server config file
            runnable_servers[0]['mem'] -= flavors[instances[arg3]['flavor']]['mem']
            runnable_servers[0]['ndisks'] -= flavors[instances[arg3]['flavor']]['ndisks']
            runnable_servers[0]['vcpus'] -= flavors[instances[arg3]['flavor']]['vcpus']
            update_hardware(runnable_servers, hardware['rack'])
            log(arg4, 'SUCCESS\n')
        else:
            ERR_MSG = 'ERROR: specified wrong flavor name'
            log(arg4, 'FAILURE\n', ERR_MSG)
    else:
        ERR_MSG = 'ERROR: specified wrong image name'
        log(arg4, 'FAILURE\n', ERR_MSG)

def server_delete_command(arg1, arg2 = ''):
    # arg1 => INSTANCE_NAME
    # arg2 => executed command
    
    # delete instance
    instances = parse_instances('instance2imageflavor')
    if instances.has_key(arg1):
        hardware = parse_hardware('current')
        servers = hardware['server']
        servers['mem'] += flavors[instances[arg1]['flavor']]['mem']
        servers['ndisks'] += flavors[instances[arg1]['flavor']]['ndisks']
        servers['vcpus'] += flavors[instances[arg1]['flavor']]['vcpus']
        instances.pop(arg1, None)
        updated = update_instances(instances)
        update_hardware(servers, hardware['rack'])
        log(arg2, 'SUCCESS\n')
    else:
        ERR_MSG = 'ERROR: specified instance name does not exist'
        log(arg2, 'FAILURE\n', ERR_MSG)

def server_list_command(arg1 = ''):
    # arg1 => executed command

    instaces = parse_instances('instance2imageflavor')
    for key in instances.keys():
        if arg1:
            print key + ' ' + instances[key]['image'] + ' ' + instances[key]['flavor']
    log(arg1, 'SUCCESS\n')
