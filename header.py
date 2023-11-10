import struct

'''
Headers
1: Path Request
    PacketType, Source, Destination
2: Path Response
    PacketType, Source, Destination, --> Next Hop in payload
3: Forward Media
    PacketType, Sender, Destination, stream_number, frame
'''

HEADER_FORMATS = {
    1: 'b 4s 4s',
    2: 'b 4s 4s',
    3: 'b 4s 4s b i',
}


def make_header(packet_type, source_addr, destination_addr, stream_number=None, frame=None):
    if packet_type in {1, 2}:
        return struct.pack(HEADER_FORMATS[packet_type], packet_type, source_addr, destination_addr)
    elif packet_type in {3}:
        return struct.pack(HEADER_FORMATS[packet_type], packet_type, source_addr, destination_addr, stream_number,
                           frame)


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


def get_stream_number(header):
    return struct.unpack(get_header_format(header), header)[3]


def get_frame(header):
    return struct.unpack(get_header_format(header), header)[4]


def parse_datagram(datagram):
    packet_type = datagram[0][0]
    header = datagram[0][:get_header_length(packet_type)]
    payload = datagram[0][get_header_length(packet_type):]
    address = datagram[1]
    return packet_type, header, payload, address
