import struct

'''
Headers
1: Path Request
    PacketType, Source (requester), Destination, last hop
2: Path Response
    PacketType, Source, Destination (requester), last hop, Next Hop
3: Forward Media
    PacketType, Sender, Destination, next hop, frame
4: Delete Forwarding Info
    PacketType, Sender
'''

HEADER_FORMATS = {
    1: 'b 4s 4s 4s',
    2: 'b 4s 4s 4s 4s',
    3: 'b 4s 4s 4s i',
    4: 'b 4s'
}

NO_NEXT_HOP = b'0000'


def make_header(packet_type, source_addr, destination_addr=None, last_hop=None, frame_or_next_hop=None):
    if packet_type in {1}:
        return struct.pack(HEADER_FORMATS[packet_type], packet_type, source_addr, destination_addr, last_hop)
    if packet_type in {2, 3}:
        return struct.pack(HEADER_FORMATS[packet_type], packet_type, source_addr, destination_addr, last_hop,
                           frame_or_next_hop)
    if packet_type in {4}:
        return struct.pack(HEADER_FORMATS[packet_type], packet_type, source_addr)


def change_last_hop(header, last_hop):
    packet_type = get_packet_type(header)
    if packet_type in {1}:
        return make_header(get_packet_type(header), get_source(header), get_destination(header), last_hop)
    elif packet_type in {2, 3}:
        return make_header(get_packet_type(header), get_source(header), get_destination(header), last_hop,
                           get_frame_or_next_hop(header))


def change_last_and_next_hop(header, last_hop, next_hop):
    packet_type = get_packet_type(header)
    if packet_type in {1}:
        return make_header(get_packet_type(header), get_source(header), get_destination(header), last_hop)
    elif packet_type in {2, 3}:
        return make_header(get_packet_type(header), get_source(header), get_destination(header), last_hop, next_hop)


def get_header_format(header):
    if isinstance(header, int):
        packet_type = header
    else:
        packet_type = get_packet_type(header)
    return HEADER_FORMATS[packet_type]


def get_header_length(header):
    return struct.calcsize(get_header_format(header))


def get_packet_type(header):
    return header[0]


def get_source(header):
    return struct.unpack(get_header_format(header), header)[1]


def get_destination(header):
    return struct.unpack(get_header_format(header), header)[2]


def get_last_hop(header):
    return struct.unpack(get_header_format(header), header)[3]


def get_frame_or_next_hop(header):
    return struct.unpack(get_header_format(header), header)[4]


def parse_datagram(datagram):
    packet_type = datagram[0][0]
    header = datagram[0][:get_header_length(packet_type)]
    payload = datagram[0][get_header_length(packet_type):]
    address = datagram[1]
    return packet_type, header, payload, address
