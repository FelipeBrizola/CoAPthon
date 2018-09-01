import sys
import docker
import threading

def remove_containers(containers):

    print 'Purge all containers'

    threads_to_stop = []
    threads_to_remove = []

    # threads to stop containers 
    for container in containers:
        thread = threading.Thread(target=container.stop, name=container.name)
        threads_to_stop.append(thread)
        print 'Start thread to stop container ' + str(thread.name)
        thread.start()
    for thread in threads_to_stop:
        print 'Join from stop container. ThreadId: ' + str(thread.ident)
        thread.join()

    # threads to remove containers 
    for container in containers:
        thread = threading.Thread(target=container.remove, name=container.name)
        threads_to_remove.append(thread)
        print 'Start thead to remove container ' + str(thread.name)
        thread.start()
    for thread in threads_to_remove:
        print 'Join from remove container. ThreadId: ' + str(thread.ident)
        thread.join()


container_prefix_name = 'container_'
image = 'alpine'
network_name = 'myfarm'
commands = ['ls', 'pwd', 'ifconfig']

client = docker.from_env()

# Remove all container(stoped or not) and network
containers = client.containers.list()
thread = threading.Thread(target=remove_containers, args=(containers,))
thread.start()
thread.join()

client.containers.prune(filters=None)
client.networks.prune(filters=None)

# network config
ipam_pool = docker.types.IPAMPool(subnet='192.168.0.0/24')
ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
network = client.networks.create(name=network_name, driver='bridge', ipam=ipam_config)

for index in range(0, 2):
    name = container_prefix_name + str(index)

    # simular a: docker run -i -t alpine
    container = client.containers.run(image=image, tty=True, stdin_open=True, network=network_name, detach=True, name=name)
    print container.logs()
    print container.exec_run('ifconfig')
    print container.logs()


        # for command in commands:
        #     container.exec_run(command)
        #     print container.logs()