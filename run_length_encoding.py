'''Image compression using run length encoding.
This technique basically takes a sequence of bits and
replaces any strings of repeated bits with the number
of bits repeated.
For example, the string 000011000 might be replaced with
04 12 03, then break each row into 127 bit chunks.
'''
from bitarray import bitarray

def compress_chunk(chunk):
    compressed = bytearray()
    count = 1
    last = chunk[0]
    for bit in chunk[1:]:
        if bit != last:
            compressed.append(count | (128 * last))
            count = 0
            last = bit
        count += 1
    compressed.append(count | (128 * last))
    return compressed