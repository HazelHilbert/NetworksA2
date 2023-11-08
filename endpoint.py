from header import *
from node import *

endpoint = Endpoint()
endpoint.print_info()
print("Broadcasting to: " + str(endpoint.broadcast_ip_port))
payload = ("Hi I am " + endpoint.container_name).encode()
endpoint.broadcast(payload)

