from node import *

# Initialize network elements
endpoint1 = Endpoint()
endpoint2 = Endpoint()
router1 = Router()
router2 = Router()
router3 = Router()

# Specify network connections
endpoint1.set_gateway(router1.socket.getsockname())
endpoint1.set_gateway(router3.socket.getsockname())
router1.add_edge(endpoint1.socket.getsockname())
router1.add_edge(router2.socket.getsockname())
router2.add_edge(router1.socket.getsockname())
router2.add_edge(router3.socket.getsockname())
router3.add_edge(router2.socket.getsockname())
router3.add_edge(endpoint2.socket.getsockname())

elements = [endpoint1, endpoint2, router1, router2, router3]

for el in elements:
    print(el.node_address)