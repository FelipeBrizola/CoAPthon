import sys
import docker

container_prefix_name = 'container_'

image = 'alpine'
network_name = 'myfarm'
commands = ['ls', 'pwd', 'ifconfig']

client = docker.from_env()

client.containers.prune(filters=None)
client.networks.prune(filters=None)

# network config
ipam_pool = docker.types.IPAMPool(subnet='192.168.0.0/24')
ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
network = client.networks.create(name=network_name, driver='bridge', ipam=ipam_config)

# start faz sair de stopped -- sai do docker ps -a para o docker ps
# attach faz entrar no container nao stopado

for index in range(1, 10):
    name = container_prefix_name + str(index)

    # simular a: docker run -i -t alpine
    container = client.containers.run(image=image, tty=True, stdin_open=True, network=network_name, detach=True, name=name)
    print container.logs()
    print container.exec_run('ifconfig')
    print container.logs()


        # for command in commands:
        #     container.exec_run(command)
        #     print container.logs()