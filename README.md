# Creating networks:
docker network create --subnet 192.168.17.0/24 edge1
docker network create --subnet 172.20.1.0/24 edge2
docker network create --subnet 10.20.10.0/24 access1
docker network create --subnet 10.20.20.0/24 access2

# Making containers:
docker create -ti --name endpoint1 --cap-add=all -v /Users/hazelhilbert/PycharmProjects/NetworksA2:/compnets myimage /bin/bash
docker create -ti --name endpoint2 --cap-add=all -v /Users/hazelhilbert/PycharmProjects/NetworksA2:/compnets myimage /bin/bash
docker create -ti --name router1 --cap-add=all -v /Users/hazelhilbert/PycharmProjects/NetworksA2:/compnets myimage /bin/bash
docker create -ti --name router2 --cap-add=all -v /Users/hazelhilbert/PycharmProjects/NetworksA2:/compnets myimage /bin/bash
docker create -ti --name router3 --cap-add=all -v /Users/hazelhilbert/PycharmProjects/NetworksA2:/compnets myimage /bin/bash

# Connecting containers to networks:
docker network connect edge1 endpoint1
docker network connect edge1 router1
docker network connect access1 router1
docker network connect access1 router2
docker network connect access2 router2
docker network connect access2 router3
docker network connect edge2 router3
docker network connect edge2 endpoint2

## or
docker network connect edge1 endpoint1 ; docker network connect edge1 router1 ; docker network connect access1 router1 ; docker network connect access1 router2 ; docker network connect access2 router2 ; docker network connect access2 router3 ; docker network connect edge2 router3 ; docker network connect edge2 endpoint2


# Start containers:
docker start -i endpoint1
...