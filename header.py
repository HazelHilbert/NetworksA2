import struct

HEADER_FORMATS = {
    1: 'b 4s 4s',
    2: 'b 4s 4s',
    3: 'b 4s 4s b i',
}

'''
Headers
1: Path Request
    PacketType, Sender, Destination
2: Path Response
    PacketType, Sender, Destination, Next Hop in payload
3: Forward Media
    PacketType, Sender, Destination, stream_number, frame
'''


def make_header(packet_type, sender_addr, destination_addr, stream_number=None, frame=None):
    if packet_type in {1, 2}:
        return struct.pack(HEADER_FORMATS[packet_type], packet_type, sender_addr, destination_addr)
    elif packet_type in {3}:
        return struct.pack(HEADER_FORMATS[packet_type], packet_type, sender_addr, destination_addr, stream_number,
                           frame)


def get_header_format(header):
    if isinstance(header, int):
        packet_type = header
    else:
        packet_type = header[0]
    return HEADER_FORMATS[packet_type]


def get_header_length(header):
    return struct.calcsize(get_header_format(header))


def get_producer_id(header):
    return str(get_producer_id_bytes(header).hex().upper())


def get_producer_id_bytes(header):
    return struct.unpack(get_header_format(header), header)[1]


def get_stream_number(header):
    return str(struct.unpack(get_header_format(header), header)[2])


def get_frame_number(header):
    return str(struct.unpack(get_header_format(header), header)[3])

