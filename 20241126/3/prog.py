import struct
from sys import stdin

data = stdin.buffer.read()


def check(data):
    if len(data) < 44 or data[:4] != b'RIFF':
        return "NO"

    size = struct.unpack('<I', data[4:8])[0]

    if data[8:12] != b'WAVE' or data[12:16] != b'fmt ':
        return "NO"
    type, channels_number, sample_rate = struct.unpack('<HHI', data[20:28])[:3]

    bits_per_sample = struct.unpack('<H', data[34:36])[0]

    if data[36:40] != b'data':
        return "NO"

    file_size = struct.unpack('<I', data[40:44])[0]

    return size, type, channels_number, sample_rate, bits_per_sample, file_size


result = check(data)
if result == "NO":
    print(result)
else:
    print("Size={}, Type={}, Channels={}, Rate={}, Bits={}, Data size={}".format(*result))

