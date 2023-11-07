from input import input_address
from node import Router
import select
import sys

address = input_address()
router = Router(address)

input_sockets = [sys.stdin, router.socket]
output_sockets = []

menu = "Choose action:\n   1 --> Find Edges\n   2 --> Continue\n"
print(menu)

quit = False
while not quit:
    readable, writable, _ = select.select(input_sockets, output_sockets, [])
    for sock in readable:
        if sock is sys.stdin:
            input_action = input()
            if input_action == '1':
                print("Searching for edges")
                router.broadcast("looking for my edges".encode())
                router.add_edges(router.receive_edge_address())
            elif input_action == '2':
                quit = True
            else:
                print("Invalid selection")

        elif sock is router.socket:
            router.receive_broadcast_and_reply()
