NETWORKS = {
    'edge1': ('192.168.17.255', 24),
    'access1': ('10.20.10.255', 24),
    'access2': ('10.20.20.255', 24),
    'edge2': ('172.20.1.255', 24)
}

CONTAINERS = {
    '5816e53d1d28': 'endpoint1',
    'aa05304517ab': 'router1',
    '8a2e750d2943': 'router2',
    '19f13edd4ece': 'router3',
    'c69437103918': 'endpoint2'
}

BROADCAST_NETWORKS = {
    'endpoint1': 'edge1',
    'router1': ('edge1', 'access1'),
    'router2': ('access1', 'access2'),
    'router3': ('access2', 'edge2'),
    'endpoint2': 'edge2'
}

BROADCAST_SOCKET_ADDRESS = {
    'endpoint1': ('192.168.17.2', 50000),
    'router1': ('10.20.10.2', 50000),
    'router2': ('10.20.10.3', 50000),
    'router3': ('10.20.20.3', 50000),
    'endpoint2': ('172.20.1.2', 50000)
}

LISTENING_SOCKET_ADDRESS = {
    'endpoint1': (('192.168.17.2', 50000),),
    'router1': (('10.20.10.2', 50000), ('192.168.17.1', 50000)),
    'router2': (('10.20.10.3', 50000), ('10.20.20.1', 50000)),
    'router3': (('10.20.20.3', 50000), ('172.20.1.1', 50000)),
    'endpoint2': (('172.20.1.2', 50000),)
}

BUFFER_SIZE = 65536
