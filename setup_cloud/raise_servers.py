#!/usr/bin/python27

from shade import *

conn = openstack_cloud(cloud='osic-hackathon')

server1_name = "slads_s1"
server2_name = "slads_s2"

servers = conn.list_servers()
servers = [str(server.name) for server in servers]
if server1_name in servers:
	conn.delete_server(server1_name)

if server2_name in servers:
	conn.delete_server(server2_name)


#images = conn.list_images()
#image_name="ubuntu"
#image_version="14"
#for x in images:
#    if image_name in str(x.name) and image_version in str(x.name):
#        image_id = str(x.id)
#print image_id

# INSTANCE IMAGE AND FLAVOR
image_id = "95576f28-afed-4b63-93b4-1d07928930da"
flavor_name = "m1.tiny"
external_network="7004a83a-13d3-4dcd-8cf5-52af1ace4cae"
ex_userdata = '''#!/usr/bin/env bash
curl -L -s https://raw.githubusercontent.com/SerDigital/OpenStack/master/script.sh | bash -s --
'''


sec_group_name = 'iot'
#if conn.search_security_groups(sec_group_name):
#    pass #print('Security group already exists. Skipping creation.')
#else:
#    #print('Creating security group.')
#    conn.create_security_group(sec_group_name, 'Network access for SLADS IoT application.')
#    conn.create_security_group_rule(sec_group_name, 80, 80, 'TCP')
#    conn.create_security_group_rule(sec_group_name, 5000, 5000, 'TCP')
#    conn.create_security_group_rule(sec_group_name, 9000, 9000, 'TCP')

print "\nServer 1 creation:"
testing_instance = conn.create_server(wait=True, auto_ip=True,
    name=server1_name,
    image=image_id,
    flavor=flavor_name,
#    userdata=ex_userdata,
    network=external_network,
    security_groups=['default',sec_group_name])





