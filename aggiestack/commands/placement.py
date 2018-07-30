from helpers import parse_images
from helpers import parse_instances
from helpers import parse_hardware
from helpers import parse_image_rack

def placement_algorithm(arg1, arg2):
    # arg1 : image name
    # arg2 : flavor name

    hardware = parse_hardware('current')
    images = parse_images()
   
    # obtain images to rack
    im2rack = parse_image_rack()
    
    # if image not in rack, check space of rack and install image in rack with more space among racks that have a server which can host the instance
    if arg1 not in im2rack.keys():
        usable_racks = []
        servers = hardware['server']
        for server in servers.keys():
            if admin_can_host_command(server, arg2, ''):
                usable_racks.append(servers[server]['rack'])
        usable_racks = set(usable_racks)
        if usable_racks:
            hostable_racks = []
            for rack in usable_racks:
                if hardware['rack'][rack] - images[key]['size'] < 0:
                    hostable_racks.append(rack)
            if hostable_racks:
                hostable_servers = []
                for server in servers.keys():
                    if servers[server]['rack'] in hostable_racks:
                        if admin_can_host_command(server, arg2, ''):
                            hostable_servers.append(server)
                if hostable_servers:
                    server = hostable_servers[0]
                    # update server-config file, im2rack-config file
                    hardware['rack'][hardware['server'][server]['rack']] -= images[arg1]['size']
                    update_hardware(hardware)
                    temp = []
                    temp.append(hardware['server'][server]['rack'])
                    im2rack[arg1] = temp
                    update_image_rack(im2rack)
                    return server
                else:
                    return 'CANT_ACCOMMODATE'
            else:
                # clear an old image and update new image (change server-config)
        else:
            return 'CANT_ACCOMMODATE'
        
    # if image in rack but no server to host, then follow same procedure as mentioned above
    else:
        # search servers in hostable racks
        hostable_servers = []
        for server in hardware['server'].keys():
            if hardware['server'][server]['rack'] in im2rack[arg1]:
                if admin_can_host_command(server, arg2, ''):
                    hostable_servers.append(server)

        if hostable_servers:
            server = hostable_servers[0]
            hardware['rack'][hardware['server'][server]['rack']] -= images[arg1]['size']
            update_hardware(hardware)
            im2rack[arg1].append(hardware['server'][server]['rack'])
            update_image_rack(im2rack)
            return server
        else:
            return 'CANT_ACCOMMODATE'
