from dataclasses import dataclass
from math import ceil


@dataclass
class Packet(object):
    version: int
    id: int
    raw: str
    mode: int = None
    val: int = None
    sub_packets: list = None


def hex2bin(packet):
    bin_rep = bin(int(packet, 16))[2:]
    return bin_rep.zfill(ceil(len(bin_rep) / 4) * 4)


def read_bits(packet, length):
    val = int(packet[:length], 2)
    return val, packet[length:]


def parse_literal(packet):
    out = ''
    group = 0
    while True:
        chunk = packet[group * 5: (group + 1) * 5]
        out += chunk[1:]
        if chunk[0] == '0':
            break
        group += 1

    return int(out, 2), packet[(group + 1) * 5:]


def parse_packet(packet):
    version, packet = read_bits(packet, 3)
    id, packet = read_bits(packet, 3)

    p = Packet(version, id, packet)

    if id == 4:
        p.val, packet = parse_literal(packet)
        return p, packet
    else:
        p.mode, packet = read_bits(packet, 1)
        sub_packets = []
        if p.mode == 0:
            # Next 15 bits rep bits per packet
            p_len, packet = read_bits(packet, 15)
            orig_len = len(packet)

            while orig_len - len(packet) < p_len:
                sub, packet = parse_packet(packet)
                sub_packets.append(sub)

        else:
            # Next 11 bits rep packet count
            sub_count, packet = read_bits(packet, 11)
            for i in range(sub_count):
                sub, packet = parse_packet(packet)
                sub_packets.append(sub)

        p.sub_packets = sub_packets
        return p, packet


def sum_versions(packet):
    if not packet.sub_packets:
        return packet.version
    else:
        return packet.version + sum(sum_versions(s) for s in packet.sub_packets)


def evaluate(packet):
    if packet.id == 0:
        return sum([evaluate(s) for s in packet.sub_packets])
    elif packet.id == 1:
        res = 1
        for s in packet.sub_packets:
            res *= evaluate(s)
        return res
    elif packet.id == 2:
        return min([evaluate(s) for s in packet.sub_packets])
    elif packet.id == 3:
        return max([evaluate(s) for s in packet.sub_packets])
    elif packet.id == 4:
        return packet.val
    elif packet.id == 5:
        return int(evaluate(packet.sub_packets[0]) > evaluate(packet.sub_packets[1]))
    elif packet.id == 6:
        return int(evaluate(packet.sub_packets[0]) < evaluate(packet.sub_packets[1]))
    elif packet.id == 7:
        return int(evaluate(packet.sub_packets[0]) == evaluate(packet.sub_packets[1]))


# packet, remaining = parse_packet(hex2bin('D2FE28'))
# packet, remaining = parse_packet(hex2bin('38006F45291200'))
# packet, remaining = parse_packet(hex2bin('EE00D40C823060'))
# packet, remaining = parse_packet(hex2bin('9C005AC2F8F0'))

with open('input.txt') as f:
    packet, remaining = parse_packet(hex2bin(f.readline().strip()))


print(sum_versions(packet))
print(evaluate(packet))
