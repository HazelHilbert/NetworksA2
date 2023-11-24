NETWORKS = {
    'edge1': ('192.168.17.255', 24),
    'access1': ('10.20.10.255', 24),
    'edge4': ('10.20.30.255', 24),
    'access2': ('10.20.20.255', 24),
    'edge2': ('172.20.1.255', 24),
    'edge3': ('172.20.2.255', 24),
}

CONTAINERS = {
    '5816e53d1d28': 'endpoint1',
    'aa05304517ab': 'router1',
    '6bf16cc4700b': 'router4',
    '2505fe55ce36': 'endpoint4',
    '8a2e750d2943': 'router2',
    '19f13edd4ece': 'router3',
    'c69437103918': 'endpoint2',
    '38d74bc8b1c2': 'endpoint3'
}

BROADCAST_NETWORKS = {
    'endpoint1': 'edge1',
    'router1': ('edge1', 'access1'),
    'router4': ('access1', 'edge4'),
    'endpoint4': 'edge4',
    'router2': ('access1', 'access2'),
    'router3': ('access2', 'edge2', 'edge3'),
    'endpoint2': 'edge2',
    'endpoint3': 'edge3'
}

BROADCAST_SOCKET_ADDRESS = {
    'endpoint1': ('192.168.17.2', 50000),
    'router1': ('10.20.10.2', 50000),
    'router4': ('10.20.10.3', 50000),
    'endpoint4': ('10.20.30.3', 50000),
    'router2': ('10.20.10.4', 50000),
    'router3': ('10.20.20.3', 50000),
    'endpoint2': ('172.20.1.3', 50000),
    'endpoint3': ('172.20.2.3', 50000)
}

LISTENING_SOCKET_ADDRESS = {
    'endpoint1': (('192.168.17.2', 50000),),
    'router1': (('10.20.10.2', 50000), ('192.168.17.1', 50000)),
    'router4': (('10.20.10.3', 50000), ('10.20.30.2', 50000)),
    'endpoint4': (('10.20.30.3', 50000),),
    'router2': (('10.20.10.4', 50000), ('10.20.20.1', 50000)),
    'router3': (('10.20.20.3', 50000), ('172.20.1.1', 50000), ('172.20.2.1', 50000)),
    'endpoint2': (('172.20.1.3', 50000),),
    'endpoint3': (('172.20.2.3', 50000),)
}

BUFFER_SIZE = 65536
