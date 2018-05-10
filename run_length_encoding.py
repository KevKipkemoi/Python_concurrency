'''Image compression using run length encoding.
This technique basically takes a sequence of bits and
replaces any strings of repeated bits with the number
of bits repeated.
For example, the string 000011000 might be replaced with
04 12 03, then break each row into 127 bit chunks.
'''
from PIL import Image
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
'''This function accepts a bitarray named row. It splits into
chunks that are 127 bits wide
'''
def compress_row(row):
    compressed = bytearray()
    chunks = split_bits(row, 127)
    for chunk in chunks:
        compressed.extend(compress_chunk(chunk))
    return compressed

'''Wrap these functions in a method that runs everything
in an executor, since we are noy certain whether it will
run effectively in a thread or process
'''
def compress_in_executor(executor, bits, width):
    row_compressors = []
    for row in split_bits(bits, width):
        compressor = executor.submit(compress_row, row)
        row_compressors.append(compressor)

    compressed = bytearray()
    for compressor in row_compressors:
        compressed.extend(compressor.result())

'''Function loads image using the pillow module, converts
it into bits, and compresses it
'''
def compress_image(in_filename, out_filename, executor=None):
    executor = executor if executor else ProcessPoolExecutor()
    with Image.open(in_filename) as image:
        bits = bitarray(image.convert('1').getdata())
        width, height = image.size

    compressed = compress_in_executor(executor, bits, width)

    with open(out_filename, 'wb') as file:
        in_filename, out_filename = sys.argv[1:3]
        #executor = ThreadPoolExecutor(4)
        executor = ProcessPoolExecutor()
        compress_image(in_filename, out_filename, executor)