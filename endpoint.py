import select
import sys

from input import input_address
from node import Endpoint

address = input_address()

endpoint = Endpoint(address)

input_sockets = [sys.stdin, endpoint.socket]
output_sockets = []

menu = "Choose action:\n   1 --> Find Gateway\n   2 --> Continue\n"
print(menu)

quit = False
while not quit:
    readable, writable, _ = select.select(input_sockets, output_sockets, [])
    for sock in readable:
        if sock is sys.stdin:
            input_action = input()
            if input_action == '1':
                print("Searching for gateway")
                endpoint.broadcast("are you my gateway?".encode())
                endpoint.set_gateway(endpoint.receive_edge_address()[0])
            elif input_action == '2':
                quit = True
            else:
                print("Invalid selection")

        elif sock is endpoint.socket:
            endpoint.receive_broadcast_and_reply()
