#!/usr/bin/python3
"""
DNA sequence converter
Takes two arguments - file name and number L
"""

import argparse

# bases alphabet
BASES = 'ACGT'


def convert_dna(file_name: str, length: int):
    try:
        # open file
        with open(file_name, 'rb') as file:
            index = 1
            # read L bytes and write converted data
            while data := file.read(length):
                print(f'@READ_{index}')
                # write 2 most significant bits of each byte converted to bases alphabet
                print(''.join(BASES[byte >> 6] for byte in data))

                print(f'+READ_{index}')
                # write bytes without 2 most significant bits increased by 33
                print(''.join(chr((byte & 0b00111111) + 33) for byte in data))

                index += 1

    except FileNotFoundError:
        print(f'Error: File not found: {file_name}')
        exit(10)

    except PermissionError:
        print(f'Error: Permission error while opening the file: {file_name}')
        exit(11)


if __name__ == '__main__':
    # parse arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('file_name', type=str, help='path to an encoded file')
    arg_parser.add_argument('length', type=int, help='number L')
    args = arg_parser.parse_args()

    # check L is positive number
    try:
        assert args.length > 0
    except AssertionError:
        print('Error: Number L must be a positive number')
        exit(12)

    convert_dna(args.file_name, args.length)
