import sys
import docker

container_prefix_name = 'container_'

image = 'alpine'
network_name = 'myfarm'
commands = ['ifconfig']

client = docker.from_env()

client.containers.prune(filters=None)
client.networks.prune(filters=None)

# network config
ipam_pool = docker.types.IPAMPool(subnet='192.168.0.0/24')
ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
network = client.networks.create(name=network_name, driver='bridge', ipam=ipam_config)

for index in range(1, 4):
    name = container_prefix_name + str(index)

    container = client.containers.run(image=image, command=commands, network=network_name, detach=True, name=name)
    print container.logs()



# https://docker-py.readthedocs.io/en/stable/client.html
