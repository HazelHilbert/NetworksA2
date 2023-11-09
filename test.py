from header import *
'''
node = Node()
node.print_info()
print(node.broadcast_socket.getsockname())

print(node.address)
print(node.format_address)

addr = input_address()
print(addr)
print(format_address(addr))
'''

# Example usage:
header = make_header(3, bytes.fromhex("aaaaaaaa"), bytes.fromhex("bbbbbbbb"), 23, 2)
print(header)

print(get_packet_type(header))
print(get_sender(header))
print(get_destination(header))
print(get_stream_number(header))
print(get_frame(header))

