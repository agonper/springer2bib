import sys

from os.path import join
from row_formatter import BibRowFormatter

SPRINGER_BIB_FILE = 'springer-{0}.bib'


class BibFileWriter(object):
    __slots__ = ('_output_folder', '_entries_per_file', '_stored_count',
                 '_row_formatter', '_current_out_file')

    def __init__(self, output_folder, entries_per_file):
        self._output_folder = output_folder
        self._entries_per_file = entries_per_file
        self._stored_count = 0
        self._row_formatter = BibRowFormatter()
        self._current_out_file = None

    def write(self, row):
        self._out_file().write(self._row_formatter.format(row))
        self._stored_count += 1

    def close(self):
        if self._current_out_file is not None:
            self._current_out_file.close()

    def _out_file(self):
        stored_count = self._stored_count
        entries_per_file = self._entries_per_file
        file_num = (0 if self._entries_per_file is None
                    else stored_count // entries_per_file) + 1

        if self._current_out_file is None:
            return self._open_next_out_file(file_num)

        if self._requires_file_change():
            self.close()
            return self._open_next_out_file(file_num)
        return self._current_out_file

    def _requires_file_change(self):
        stored_count = self._stored_count
        entries_per_file = self._entries_per_file

        if entries_per_file is None:
            return False
        return stored_count / entries_per_file == stored_count // entries_per_file

    def _open_next_out_file(self, file_num):
        self._current_out_file = open(
            join(self._output_folder, SPRINGER_BIB_FILE.format(file_num)), 'w', encoding="utf8")
        return self._current_out_file
