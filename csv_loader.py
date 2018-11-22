import csv

from os import listdir
from os.path import isfile, join, basename

ITEM_TITLE = 'Item Title'
PUBLICATION_TITLE = 'Publication Title'
BOOK_SERIES_TITLE = 'Book Series Title'
JOURNAL_VOLUME = 'Journal Volume'
JOURNAL_ISSUE = 'Journal Issue'
ITEM_DOI = 'Item DOI'
AUTHORS = 'Authors'
PUBLICATION_YEAR = 'Publication Year'
URL = 'URL'
CONTENT_TYPE = 'Content Type'


class SpringerCSVLoader(object):
    __slots__ = ('_input_folder', '_seen')

    def __init__(self, input_folder):
        self._input_folder = input_folder
        self._seen = set()

    def load_rows(self):
        files = self._lookup_csv_files()
        for input_file in files:
            yield from self._process_csv_file(input_file)

    def _lookup_csv_files(self):
        folder = self._input_folder
        files = [f for f in listdir(folder) if isfile(join(folder, f))]
        return [join(folder, f) for f in files if '.csv' in f]

    def _process_csv_file(self, file_name):
        with open(file_name, encoding="utf8") as input_file:
            csv_file = csv.DictReader(input_file)
            for row in csv_file:
                if not self._has_been_seen(row):
                    yield CSVRow(row)

    def _has_been_seen(self, row):
        title = row[ITEM_TITLE]
        if title in self._seen:
            return True
        self._seen.add(title)
        return False


class CSVRow(object):
    __slots__ = '_row'

    def __init__(self, row):
        self._row = row

    def is_article(self):
        return self.content_type() == 'Article'

    def short_authors(self):
        authors = self.authors().split(' ')
        return ' '.join(authors[:4])

    def item_title(self):
        return self._row[ITEM_TITLE]

    def publication_title(self):
        return self._row[PUBLICATION_TITLE]

    def book_series_title(self):
        return self._row[BOOK_SERIES_TITLE]

    def journal_volume(self):
        return self._row[JOURNAL_VOLUME]

    def journal_issue(self):
        return self._row[JOURNAL_ISSUE]

    def item_doi(self):
        return self._row[ITEM_DOI]

    def authors(self):
        return self._row[AUTHORS]

    def publication_year(self):
        return self._row[PUBLICATION_YEAR]

    def url(self):
        return self._row[URL]

    def content_type(self):
        return self._row[CONTENT_TYPE]
