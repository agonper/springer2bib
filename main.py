import argparse
import sys
import csv

from os import listdir
from os.path import isfile, join, basename

INPUT = 'input'
OUTPUT = 'output'


def main():
    args = parse_arguments()
    with open(args[OUTPUT], 'w', encoding="utf8") as out_file:
        files = lookup_csv_files(args[INPUT])
        for input_file in files:
            process_csv_file(input_file, out_file)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Springer Link CSV to BibTeX formar converter')
    parser.add_argument(INPUT, metavar='in', type=str, nargs=1,
                        help='path to a folder containing one or more CSV files')
    parser.add_argument(OUTPUT, metavar='out', type=str,
                        nargs=1, help='output file name')
    args = parser.parse_args(sys.argv[1:])

    return {
        INPUT: args.input[0],
        OUTPUT: args.output[0]
    }


def lookup_csv_files(folder):
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    return [join(folder, f) for f in files if '.csv' in f]


def process_csv_file(file_name, writer):
    with open(file_name, encoding="utf8") as input_file:
        csv_file = csv.DictReader(input_file)
        for row in csv_file:
            writer.write(row_to_bib(row))


def row_to_bib(row):
    properties = row_to_article_properties(row) \
        if row['Content Type'] == 'Article' else row_to_common_properties(row)
    return "@article{{{0},{1}}}".format(citation_name(row), properties)


def row_to_article_properties(row):
    properties = ",volume={{{0}}},number={{{1}}}"
    return row_to_common_properties(row) + properties.format(row['Journal Volume'], row['Journal Issue'])


def row_to_common_properties(row):
    properties = "title={{{0}}},url={{{1}}},DOI={{{2}}},journal={{{3}}},author={{{4}}},year={{{5}}}"
    return properties.format(row['Item Title'], row['URL'], row['Item DOI'],
                             row['Publication Title'], short_authors(row), row['Publication Year'])


def citation_name(row):
    authors = short_authors(row).split(' ')
    doc_id = '_'.join(authors) if len(row['Authors']) != 0 \
        else '_'.join(row['Item DOI'].split('/'))
    name = doc_id + '_' + row['Publication Year']
    return name.lower()


def short_authors(row):
    authors = row['Authors'].split(' ')
    return ' '.join(authors[:4])


if __name__ == "__main__":
    main()
