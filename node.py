import os
import socket
import threading
import time
import uuid

from constants import *
from header import parse_datagram


def format_address(hex_address):
    return ':'.join(['{:02x}'.format(b) for b in hex_address])


class Node:
    def __init__(self):
        # generate 4-byte address
        self.address = uuid.UUID(int=uuid.getnode()).bytes[-4:]
        self.format_address = format_address(self.address)

        # initialize container name and networks the container is connected to
        self.container_name = CONTAINERS[os.environ.get('HOSTNAME')]
        self.connected_networks = BROADCAST_NETWORKS[self.container_name]

        # create broadcast UDP sockets
        self.broadcast_socket = self.create_broadcasting_socket()
        self.broadcast_socket.bind(BROADCAST_SOCKET_ADDRESS[self.container_name])

    def create_broadcasting_socket(self):
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        return new_socket

    def print_info(self):
        print(self.container_name + " connected to: " + str(self.connected_networks))
        print("Address: " + self.format_address)


class Router(Node):
    def __init__(self):
        super().__init__()
        self.forwarding_table = []
        self.broadcast_ip_port = tuple(NETWORKS[network] for network in self.connected_networks)
        # create list of listening UDP sockets
        self.listening_sockets = []
        for ip_port in self.broadcast_ip_port:
            new_socket = self.create_broadcasting_socket()
            new_socket.bind(ip_port)
            self.listening_sockets.append(new_socket)

    def broadcast(self, data):
        for ip_port in self.broadcast_ip_port:
            self.broadcast_socket.sendto(data, ip_port)

    def listen_concurrently(self):
        threads = []
        for sock in self.listening_sockets:
            thread = threading.Thread(target=self.listen, args=(sock,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def listen(self, sock):
        while True:
            packet_type, header, payload, sender_address = parse_datagram(sock.recvfrom(BUFFER_SIZE))

            # discards messages from itself
            if sender_address not in LISTENING_SOCKET_ADDRESS[self.container_name]:
                print(payload.decode())

                ip_parts = sender_address[0].split('.')
                ip_parts[-1] = '255'
                dont_sent_to_address = ('.'.join(ip_parts), 24)

                time.sleep(0.5)
                self.forward(header+payload, dont_sent_to_address)

    def forward(self, data, dont_send_to_address):
        for ip_port in self.broadcast_ip_port:
            if ip_port[0] != dont_send_to_address[0]:
                # print(str(ip_port) + " vs " + str(dont_send_to_address))
                self.broadcast_socket.sendto(data, ip_port)

    def add_entry_to_forwarding_table(self, destination, next_hop, timer):
        entry = ForwardingTableEntry(destination, next_hop, timer)
        self.forwarding_table.append(entry)

    def remove_entry_from_forwarding_table(self, destination):
        self.forwarding_table = [entry for entry in self.forwarding_table if entry.destination != destination]


class Endpoint(Node):
    def __init__(self):
        super().__init__()
        self.broadcast_ip_port = NETWORKS[self.connected_networks]
        # listening UDP sockets
        self.listening_socket = self.create_broadcasting_socket()
        self.listening_socket.bind(self.broadcast_ip_port)

    def broadcast(self, data):
        self.broadcast_socket.sendto(data, self.broadcast_ip_port)

    def listen(self):
        while True:
            packet_type, header, payload, sender_address = parse_datagram(self.listening_socket.recvfrom(BUFFER_SIZE))
            if sender_address not in LISTENING_SOCKET_ADDRESS[self.container_name]:
                return packet_type, header, payload, sender_address
            else:
                return None, None, None, None


class ForwardingTableEntry:
    def __init__(self, destination, next_hop, timer):
        self.destination = destination
        self.next_hop = next_hop
        self.timer = timer
