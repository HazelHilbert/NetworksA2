from node import *

endpoint = Endpoint()
endpoint.print_info()
print("Broadcasting to: " + str(endpoint.broadcast_ip_port))
endpoint.broadcast(("Hi I am " + endpoint.container_name).encode())

