# this is an endpoint
import select
import sys

from node import *

endpoint = Endpoint()

input_sockets = [sys.stdin, endpoint.socket]
output_sockets = []

menu = "Choose action:\n   1 --> Publish Content\n   2 --> Quit\n"
print(menu)

quit = False
while not quit:
    readable, writable, _ = select.select(input_sockets, output_sockets, [])

    for sock in readable:
        if sock is sys.stdin:
            action_input = input()

            if action_input == '1':
                payload = str.encode("This is sending some data")
                #endpoint.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                #network_address = endpoint.socket.getsockname()[0]
                #broadcast_address = network_address[:network_address.rfind('.')] + '.255'
                endpoint.socket.sendto(payload, endpoint.gateway)

            elif action_input == '2':
                quit = True
                break
            else:
                print("Invalid action")

            print(menu)

        elif sock is endpoint.socket:
            try:
                data = endpoint.socket.recvfrom(65536)
                print(data[0].decode())
            except:
                continue




