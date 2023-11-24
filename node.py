import os
import socket
import threading
import time
import uuid

from constants import *
from fowarding_table import ForwardingTable
from header import *


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

    def __str__(self):
        s = self.container_name + ' connected to: ' + str(self.connected_networks) + '\n'
        s += 'Address: ' + self.format_address
        return s


class Router(Node):
    def __init__(self):
        super().__init__()
        self.forwarding_table = ForwardingTable()
        self.broadcast_ip_port = tuple(NETWORKS[network] for network in self.connected_networks)
        # create list of listening UDP sockets
        self.listening_sockets = []
        for ip_port in self.broadcast_ip_port:
            new_socket = self.create_broadcasting_socket()
            new_socket.bind(ip_port)
            #print(new_socket.getsockname())
            self.listening_sockets.append(new_socket)

    def broadcast(self, data, dont_send_to_address=None):
        for ip_port in self.broadcast_ip_port:
            if ip_port[0] != dont_send_to_address[0]:
                self.broadcast_socket.sendto(data, ip_port)

    def broadcast_to(self, data, destination_ip):
        self.broadcast_socket.sendto(data, destination_ip)

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
            packet_type, header, payload, sender_ip_port = parse_datagram(sock.recvfrom(BUFFER_SIZE))
            # discards messages from itself
            if sender_ip_port not in LISTENING_SOCKET_ADDRESS[self.container_name]:
                print(payload.decode())

                ip_parts = sender_ip_port[0].split('.')
                ip_parts[-1] = '255'
                dont_sent_to_address = ('.'.join(ip_parts), 24)
                time.sleep(0.5)

                if packet_type == 1:
                    # look up in forwarding table. If there is a path send a path_response to sender.
                    # Else broadcast and keep track of who sent the request?
                    self.forwarding_table.add_entry(get_source(header), dont_sent_to_address, 5)
                    #print("adding to ft: " + str(get_source(header)) + str(dont_sent_to_address))
                    next_hop = self.forwarding_table.get_next_hop(get_destination(header))
                    if next_hop is None:
                        #print("dont know where that is, will broadcast")
                        self.broadcast(header + payload, dont_sent_to_address)
                    else:
                        print("Found path")
                        header = make_header(2, get_destination(header), get_source(header))
                        payload = ("I know where " + format_address(get_destination(header)) + " is").encode()
                        self.broadcast_to(header + payload, dont_sent_to_address)
                elif packet_type == 2:
                    # add to forwarding table and broadcast
                    self.forwarding_table.add_entry(get_source(header), sender_ip_port, 5)
                    next_hop = self.forwarding_table.get_next_hop(get_destination(header))
                    #print("sending data back to: " + str(next_hop))
                    self.broadcast_to(header + payload, next_hop)

                elif packet_type == 3:
                    # look up in forwarding table and forward
                    print("now i need to forward")


class Endpoint(Node):
    def __init__(self):
        super().__init__()
        self.broadcast_ip_port = NETWORKS[self.connected_networks]
        # listening UDP sockets
        self.listening_socket = self.create_broadcasting_socket()
        self.listening_socket.bind(self.broadcast_ip_port)
        #print(self.listening_socket.getsockname())

    def broadcast(self, data):
        self.broadcast_socket.sendto(data, self.broadcast_ip_port)

    def listen(self):
        while True:
            packet_type, header, payload, sender_ip_port = parse_datagram(self.listening_socket.recvfrom(BUFFER_SIZE))
            if sender_ip_port not in LISTENING_SOCKET_ADDRESS[self.container_name]:
                return packet_type, header, payload, sender_ip_port
            else:
                return None, None, None, None
