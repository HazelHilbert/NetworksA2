from header import *
from node import *

endpoint = Endpoint()
endpoint.print_info()
print("Broadcasting to: " + str(endpoint.broadcast_ip_port))

#header = make_header(1, endpoint.address, b'ac:11:00:03')
payload = ("Hi I am " + endpoint.container_name).encode()

endpoint.broadcast(payload)

