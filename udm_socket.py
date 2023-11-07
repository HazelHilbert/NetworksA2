import socket, random, zlib
from header import *


class UDMSocket:
    def __init__(self, name):
        self.UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.bufferSize = 65536
        self.name = name

    def bind_to_address(self, address_port):
        self.UDPSocket.bind(address_port)

    def set_timeout(self, timeout):
        self.UDPSocket.settimeout(timeout)

    def send_data_to(self, bytes_to_send, address_port):
        self.UDPSocket.sendto(bytes_to_send, address_port)

    def receive_data(self):
        return self.UDPSocket.recvfrom(self.bufferSize)[0]

    def receive_data_parsed(self):
        data = self.UDPSocket.recvfrom(self.bufferSize)

        packet_type = data[0][0]
        header = data[0][:get_header_length(packet_type)]
        payload = data[0][get_header_length(packet_type):]
        address = data[1]

        return packet_type, header, payload, address