# Preparation of the image
docker create --name base -ti ubuntu /bin/bash
docker start -i base
apt update
apt install -y net-tools iputils-ping netcat tcpdump iptables
exit
docker commit base netimg

# Creating containers
docker create --name router1 -ti --cap-add=all netimg /bin/bash

# Creating networks
docker network create --subnet 172.20.1.0/24 net1
docker network create --subnet 172.20.2.0/24 net2

# Connecting the nodes
docker network connect net1 endpoint1
docker network connect net1 router1  
docker network connect net2 router1
docker network connect net2 router2
docker network connect net3 router2 
docker network connect net3 router3
docker network connect net4 router3
docker network connect net4 endpoint2

# On node1:
docker start -i node1
iptables -P FORWARD ACCEPT
route add -net 172.20.2.0/24 gw 172.20.1.3 eth1
route add -net 172.20.3.0/24 gw 172.20.1.3 eth1
nc -l -u 172.20.1.2 50000

# On node2:
docker start -i node2
iptables -P FORWARD ACCEPT
route add -net 172.20.3.0/24 gw 172.20.2.3 eth2
tcpdump -i eth1 -i eth2 -n -vv

# On node3:
docker start -i node3
iptables -P FORWARD ACCEPT
route add -net 172.20.1.0/24 gw 172.20.2.2 eth1
tcpdump -i eth1 -i eth2 -n -vv

# On node4:
docker start -i node4
iptables -P FORWARD ACCEPT
route add -net 172.20.1.0/24 gw 172.20.3.2 eth1
route add -net 172.20.2.0/24 gw 172.20.3.2 eth1
nc -u 172.20.1.2 50000


or
node1: tcpdump -i eth1 -w capture1.pcap &
node2: tcpdump -i eth1 -i eth2 -w capture2.pcap &
node3: tcpdump -i eth1 -i eth2 -w capture3.pcap &
node4: tcpdump -i eth1 -w capture4.pcap &
node1: nc -l -u 172.20.1.2 50000
node4: nc -u 172.20.1.2 50000
node4: hello world<Enter>
node1: same to you<Enter>
all: kill -2 %1


# Afterwards:
docker rm node1 node2 node3 node4
docker network rm net1 net2 net3
docker image rm netimg