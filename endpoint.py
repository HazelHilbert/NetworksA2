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


def input_frames():
    valid = False
    while not valid:
        try:
            folder_input = input("Enter folder with frames to broadcast: ")
            list_of_frames = os.listdir(os.getcwd() + '/' + folder_input)
            valid = True
        except:
            if (valid == False):
                print("Could not find folder")
    return (folder_input, list_of_frames)


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


def send_frame(endpoint, destination_address, frame_number, frame_payload):
    header = make_header(3, endpoint.address, destination_address, NO_NEXT_HOP, frame_number)
    endpoint.broadcast(header + frame_payload)


endpoint = Endpoint()
print(endpoint)
# print("Broadcasting to: " + str(endpoint.broadcast_ip_port))

input_sockets = [sys.stdin, endpoint.listening_socket]
output_sockets = []

menu = "Choose action:\n   1 --> Find Path\n   2 --> Send data\n   3 --> Request to Remove Path Info\n   4 --> Quit"
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
                destination_address = input_address()
                folder_input, list_of_frames = input_frames()
                for i in range(len(list_of_frames)):
                    current_frame_path = os.getcwd() + '/' + folder_input + '/' + list_of_frames[i]
                    with open(current_frame_path, 'rb') as file:
                        payload_frame = file.read()
                    print("Sending frame: " + str(i+1))
                    send_frame(endpoint, destination_address, i+1, payload_frame)
            elif input_action == '3':
                send_forwarding_removal_request(endpoint)
            elif input_action == '4':
                quit_loop = True
            else:
                print("Invalid selection")
                print(menu)

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
                    continue
            elif packet_type == 3:
                if get_last_hop(header) == endpoint.address:
                    print("Received frame: " + str(get_frame_or_next_hop(header)) + "; from: " + format_address(get_source(header)))
