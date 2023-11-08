import os
import socket
import threading
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

        # create broadcast UDP sockets
        self.broadcast_socket = self.create_broadcasting_socket()
        self.broadcast_socket.bind(BROADCAST_SOCKET_ADDRESS[self.container_name])


    def create_broadcasting_socket(self):
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        return new_socket

    def print_info(self):
        print("Container: " + self.container_name)
        print("Address: " + self.format_address)
        print("Connected to networks: " + str(self.connected_networks))


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

    def broadcast(self, payload):
        for ip_port in self.broadcast_ip_port:
            self.broadcast_socket.sendto(payload, ip_port)

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
            response, sender_address = sock.recvfrom(BUFFER_SIZE)
            if not response:
                break  # Socket closed or error occurred

            # discards messages from itself
            if sender_address not in LISTENING_SOCKET_ADDRESS[self.container_name]:
                print(response)
                '''
                print("From: " + str(sender_address))
                print("I am: " + str(self.broadcast_socket.getsockname()))
                print("FIRST: " + str(LISTENING_SOCKET_ADDRESS[self.container_name][0]))
                print("scond: " + str(LISTENING_SOCKET_ADDRESS[self.container_name][1]))
                '''

                ip_parts = sender_address[0].split('.')
                ip_parts[-1] = '255'
                dont_sent_to_address = ('.'.join(ip_parts), 24)

                #print("dont send to: " + str(dont_sent_to_address))
                time.sleep(1.0)
                self.forward(response, dont_sent_to_address)

    def forward(self, payload, dont_send_to_address):
        for ip_port in self.broadcast_ip_port:
            if ip_port[0] != dont_send_to_address[0]:
                #print(str(ip_port) + " vs " + str(dont_send_to_address))
                self.broadcast_socket.sendto(payload, ip_port)

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

    def broadcast(self, payload):
        self.broadcast_socket.sendto(payload, self.broadcast_ip_port)

    def listen(self):
        response, address = self.listening_socket.recvfrom(BUFFER_SIZE)
        print(response.decode())


class ForwardingTableEntry:
    def __init__(self, destination, next_hop, timer):
        self.destination = destination
        self.next_hop = next_hop
        self.timer = timer
