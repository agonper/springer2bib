import argparse
import sys
import csv

from os import listdir
from os.path import isfile, join, basename

from csv_loader import SpringerCSVLoader
from bib_writer import BibFileWriter

INPUT = 'input'
OUTPUT = 'output'
NUM = 'num'


def main():
    args = parse_arguments()

    loader = SpringerCSVLoader(args[INPUT])
    writer = BibFileWriter(args[OUTPUT], args[NUM])

    for row in loader.load_rows():
        writer.write(row)
    writer.close()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Springer Link CSV to BibTeX formar converter')
    parser.add_argument(INPUT, metavar='in', type=str, nargs=1,
                        help='path to a folder containing one or more CSV files')
    parser.add_argument(OUTPUT, metavar='out', type=str,
                        nargs=1, help='path to a folder where resulting files will be stored')
    parser.add_argument('-n', '--number', dest=NUM, type=int,
                        nargs=1, help='number of entries for each resulting .bib file (all-in-one by default)')
    args = parser.parse_args(sys.argv[1:])

    return {
        INPUT: args.input[0],
        OUTPUT: args.output[0],
        NUM: args.num[0] if args.num is not None else None
    }


if __name__ == "__main__":
    main()
