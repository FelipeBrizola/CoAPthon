import sys
import docker
import threading
import tarfile
import os

docker_client = docker.from_env()
container_prefix_name = 'container_'
docker_image = 'python:2.7.15-alpine3.8'
network_name = 'myfarm'
containers_quantity = 5

def remove_containers(containers):

    print 'Remove all containers: IN PROGRESS'

    threads_to_stop = []
    threads_to_remove = []

    # threads to stop containers
    for container in containers:
        thread = threading.Thread(target=container.stop, name=container.name)
        threads_to_stop.append(thread)
        print '    Start thread to stop ' + str(thread.name)
        thread.start()
    for thread in threads_to_stop:
        thread.join()

    # threads to remove containers
    for container in containers:
        thread = threading.Thread(target=container.remove, name=container.name)
        threads_to_remove.append(thread)
        print '    Start thead to remove ' + str(thread.name)
        thread.start()
    for thread in threads_to_remove:
        thread.join()

    print 'Remove all containers: DONE'


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def deploy_containers(docker_image, network_name, container_prefix_name, containers_quantity):

    print 'Deploy containers: IN PROGRESS'

    containers = []

    for index in range(0, containers_quantity):
        name = container_prefix_name + str(index)

        # $ docker run -i -t python:2.7.15-alpine3.8 /bin/sh
        containers.append(docker_client.containers.run(image=docker_image, command='/bin/sh', tty=True, stdin_open=True, network=network_name, detach=True, name=name))
        print '    ' + name + ' is running!'

    print 'Deploy containers: DONE'

    return containers

def push_project(containers):

    print 'Send project folder to containers: IN PROGRESS'

    # generate tar file
    make_tarfile('CoAPthon.tar', './CoAPthon')

    # put on containers
    for container in containers:
        project = open('./CoAPthon.tar', 'r')
        container.put_archive(path='/', data=project)
        project.close()
        print '    sent to ' + container.name

    os.remove('./CoAPthon.tar')

    print 'Send project folder to containers: DONE'

def create_network(network_name):

    print 'Create network: IN PROGRESS'

    ipam_pool = docker.types.IPAMPool(subnet='192.168.0.0/24')
    ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
    docker_client.networks.create(name=network_name, driver='bridge', ipam=ipam_config)

    print 'Create network: DONE'

def run_coap_servers(containers):

    print 'Run coap servers: IN PROGRESS'

    for container in containers:
        container.exec_run(workdir='/CoAPthon', cmd='python coapserver.py', detach=True)
        print '    coap server is running on ' + container.name

    print 'Run coap servers: DONE'


def main(argv):

    print 'build_farm.py: IN PROGRESS'

    # Remove all container(stoped or not)
    containers = docker_client.containers.list()
    thread = threading.Thread(target=remove_containers, args=(containers,))
    thread.start()
    thread.join()

    # Remove stopped containers
    docker_client.containers.prune(filters=None)
    # Remove unused networks
    docker_client.networks.prune(filters=None)

    # create network
    create_network(network_name)
    
    # run containers
    containers = deploy_containers(docker_image, network_name, container_prefix_name, containers_quantity)

    # put project on each container
    push_project(containers)

    # run coap server on each container
    run_coap_servers(containers)

    print 'build_farm.py: DONE'


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
