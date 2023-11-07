import os
import socket
import time
import uuid

from constants import *


class Node:
    def __init__(self):
        # generate 4-byte address
        self.address = uuid.UUID(int=uuid.getnode()).bytes[-4:]
        self.format_address = ':'.join(['{:02x}'.format(b) for b in self.address])

        # initialize container name and networks the container is connected to
        self.container_name = CONTAINERS[os.environ.get('HOSTNAME')]
        self.connected_networks = BROADCAST_NETWORKS[self.container_name]
        if isinstance(self.connected_networks, tuple):
            self.broadcast_ip_port = tuple(NETWORKS[network] for network in self.connected_networks)
        else:
            self.broadcast_ip_port = NETWORKS[self.connected_networks]

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(('', 50000))
        self.buffer_size = 65536

    def print_info(self):
        print("Container: " + self.container_name)
        print("Address: " + self.format_address)
        print("Connected to networks: " + str(self.connected_networks))
        print("Broadcast to these addresses " + str(self.broadcast_ip_port))

    def broadcast(self, payload):
        self.socket.sendto(payload, ('<broadcast>', 50000))

    def receive_broadcast_and_reply(self):
        data, sender_address = self.socket.recvfrom(self.buffer_size)
        if sender_address != self.socket.getsockname():
            print(data.decode())
            payload = ("Hi I am your edge " + str(self.address) + str(self.socket.getsockname()[0]) + str(
                self.socket.getsockname()[1])).encode()
            self.socket.sendto(payload, sender_address)

    def receive_edge_address(self):
        addresses = []
        start_time = time.time()
        while (time.time() - start_time) < 1:
            data, sender_address = self.socket.recvfrom(self.buffer_size)
            if sender_address != self.socket.getsockname():
                print(data.decode())
                addresses.append(sender_address)
        return addresses


class Router(Node):
    def __init__(self):
        super().__init__()
        self.forwarding_table = []

    def add_entry_to_forwarding_table(self, destination, next_hop, timer):
        entry = ForwardingTableEntry(destination, next_hop, timer)
        self.forwarding_table.append(entry)

    def remove_entry_from_forwarding_table(self, destination):
        self.forwarding_table = [entry for entry in self.forwarding_table if entry.destination != destination]


class Endpoint(Node):
    def __init__(self):
        super().__init__()


class ForwardingTableEntry:
    def __init__(self, destination, next_hop, timer):
        self.destination = destination
        self.next_hop = next_hop
        self.timer = timer
