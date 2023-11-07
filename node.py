import socket
import uuid


class Node:
    def __init__(self):
        self.node_address = bytes.fromhex(uuid.UUID(int=uuid.getnode()).hex)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(('', 50000))
        self.buffer_size = 65536

    def broadcast(self, payload):
        self.socket.sendto(payload, ('<broadcast>', 50000))


class ForwardingTableEntry:
    def __init__(self, destination, next_hop, timer):
        self.destination = destination
        self.next_hop = next_hop
        self.timer = timer


class Router(Node):
    def __init__(self):
        super().__init__()
        self.forwarding_table = []
        self.edges = []

    def add_edge(self, address_port):
        self.edges.append(address_port)

    def add_entry_to_forwarding_table(self, destination, next_hop, timer):
        entry = ForwardingTableEntry(destination, next_hop, timer)
        self.forwarding_table.append(entry)

    def remove_entry_from_forwarding_table(self, destination):
        self.forwarding_table = [entry for entry in self.forwarding_table if entry.destination != destination]


class Endpoint(Node):
    def __init__(self):
        super().__init__()
        self.gateway = None

    def set_gateway(self, address_port):
        self.gateway = address_port




