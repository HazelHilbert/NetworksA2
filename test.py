from node import *
import unittest
import sys

container_list = ['endpoint1', 'endpoint2', 'router1', 'router2', 'router3']
all_networks = {
    'edge1': ('172.20.1.255', 24),
    'access1': ('10.20.10.255', 24),
    'access2': ('10.20.20.255', 24),
    'edge2': ('192.168.17.255', 24)
}


class ElementTest(unittest.TestCase):

    def test_endpoint1(self):
        endpoint1 = Endpoint([
            all_networks.get('edge1')
        ])
        endpoint1.send_request("This is endpoint1")

    def test_router1(self):
        router1 = Router([
            all_networks.get('edge1'),
            all_networks.get('access1')
        ])
        while True:
            router1.receive_response()

    def test_router2(self):
        router2 = Router([
            all_networks.get('access1'),
            all_networks.get('access2')
        ])
        router2.send_request("This is router2")
        while True:
            router2.receive_response()

    def test_router3(self):
        router3 = Router([
            all_networks.get('access2'),
            all_networks.get('edge2')
        ])
        while True:
            router3.receive_response()

    def test_endpoint2(self):
        endpoint2 = Endpoint([
            all_networks.get('edge2')
        ])
        endpoint2.send_request("This is endpoint2")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        container_name = sys.argv[1]
        suite = unittest.TestSuite()
        if container_list.__contains__(container_name):
            suite.addTest(ElementTest('test_' + container_name))
        else:
            print("Terminating script. Wrong container name.")
        unittest.TextTestRunner().run(suite)
    else:
        print("No container name specified.")
        unittest.main()
