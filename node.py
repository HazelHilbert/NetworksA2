import socket
import time
import uuid


class Node:
    def __init__(self, address):
        self.address = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(('', 50000))
        self.buffer_size = 65536

    def broadcast(self, payload):
        self.socket.sendto(payload, ('<broadcast>', 50000))

    def receive_broadcast_and_reply(self):
        data, sender_address = self.socket.recvfrom(self.buffer_size)
        if sender_address != self.socket.getsockname():
            print(data.decode())
            payload = ("Hi I am your edge " + str(self.address) + str(self.socket.getsockname()[0]) + str(self.socket.getsockname()[1])).encode()
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


class ForwardingTableEntry:
    def __init__(self, destination, next_hop, timer):
        self.destination = destination
        self.next_hop = next_hop
        self.timer = timer


class Router(Node):
    def __init__(self, address):
        super().__init__(address)
        self.forwarding_table = []
        self.edges = []

    def add_edge(self, address_port):
        self.edges.append(address_port)

    def add_edges(self, address_ports):
        for addr in address_ports:
            self.edges.append(addr)

    def add_entry_to_forwarding_table(self, destination, next_hop, timer):
        entry = ForwardingTableEntry(destination, next_hop, timer)
        self.forwarding_table.append(entry)

    def remove_entry_from_forwarding_table(self, destination):
        self.forwarding_table = [entry for entry in self.forwarding_table if entry.destination != destination]


class Endpoint(Node):
    def __init__(self, address):
        super().__init__(address)
        self.gateway = None

    def set_gateway(self, address_port):
        self.gateway = address_port




