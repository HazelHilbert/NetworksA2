from header import *
from node import *
import select
import sys


def input_address():
    valid = False
    while not valid:
        id_input = input("Enter address: ")
        if len(id_input) == 8:
            try:
                address = bytes.fromhex(id_input)
                valid = True
            except:
                print("Invalid ID: enter 8 char string representing a 4 byte hexadecimal number")
                continue
        else:
            print("Invalid ID: enter 8 char string representing a 4 byte hexadecimal number")
    return address


def send_path_request(endpoint, receiver_address):
    header = make_header(1, endpoint.address, receiver_address, endpoint.address)
    payload = ("Hi I am " + endpoint.format_address + " trying to find " + str(
        format_address(receiver_address))).encode()
    endpoint.broadcast(header + payload)


def send_path_response(endpoint, requester_address):
    header = make_header(2, endpoint.address, requester_address, endpoint.address, NO_NEXT_HOP)
    payload = ("Yes, it is me, " + endpoint.format_address).encode()
    endpoint.broadcast(header + payload)


def send_forwarding_removal_request(endpoint):
    header = make_header(4, endpoint.address)
    payload = ("Please remove forwarding infromation about " + endpoint.format_address).encode()
    endpoint.broadcast(header + payload)


endpoint = Endpoint()
print(endpoint)
# print("Broadcasting to: " + str(endpoint.broadcast_ip_port))

input_sockets = [sys.stdin, endpoint.listening_socket]
output_sockets = []

menu = "Choose action:\n   1 --> Send data\n   2 --> Request to Remove Path Info\n   3 --> Quit"
print(menu)

quit_loop = False
while not quit_loop:
    readable, writable, _ = select.select(input_sockets, output_sockets, [])
    for sock in readable:
        if sock is sys.stdin:
            input_action = input()
            if input_action == '1':
                receiver_address = input_address()
                send_path_request(endpoint, receiver_address)
            elif input_action == '2':
                send_forwarding_removal_request(endpoint)
            elif input_action == '3':
                quit_loop = True
            else:
                print("Invalid selection")

        elif sock is endpoint.listening_socket:
            packet_type, header, payload, sender_ip_port = endpoint.listen()
            if packet_type is None:
                continue
            elif packet_type == 1:
                print(payload.decode())
                if get_destination(header) == endpoint.address:
                    send_path_response(endpoint, get_source(header))
                    print("That is me!")
                else:
                    print("Sorry not me!")
            elif packet_type == 2:
                print(payload.decode())
                if get_destination(header) == endpoint.address:
                    print("Now I can send the frames")
                else:
                    #print("This is not for me!")
                    continue
