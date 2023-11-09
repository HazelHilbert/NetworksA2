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


endpoint = Endpoint()
endpoint.print_info()
print("Broadcasting to: " + str(endpoint.broadcast_ip_port))

input_sockets = [sys.stdin, endpoint.listening_socket]
output_sockets = []

menu = "Choose action:\n   1 --> Send data\n   2 --> Quit\n"
print(menu)

quit = False
while not quit:
    readable, writable, _ = select.select(input_sockets, output_sockets, [])
    for sock in readable:
        if sock is sys.stdin:
            input_action = input()
            if input_action == '1':
                receiver_address = input_address()

                payload = ("Hi I am " + endpoint.format_address + " trying to find " + str(format_address(receiver_address))).encode()
                endpoint.broadcast(payload)

            elif input_action == '2':
                quit = True
            else:
                print("Invalid selection")

        elif sock is endpoint.listening_socket:
            endpoint.listen()
            #print("I received something lolz")


