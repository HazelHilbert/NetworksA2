from endpoint import input_address
from node import *

node = Node()
node.print_info()
print(node.broadcast_socket.getsockname())

print(node.address)
print(node.format_address)

addr = input_address()
print(addr)
print(format_address(addr))
