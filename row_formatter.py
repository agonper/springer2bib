class BibRowFormatter(object):

    def format(self, row):
        properties = self._row_to_article_properties(row) \
            if row.is_article() else self._row_to_common_properties(row)
        return "@article{{{0},{1}}}".format(self._citation_name(row), properties)

    def _row_to_article_properties(self, row):
        properties = ",volume={{{0}}},number={{{1}}}"
        return self._row_to_common_properties(row) + properties.format(row.journal_volume(), row.journal_issue())

    def _row_to_common_properties(self, row):
        properties = "title={{{0}}},url={{{1}}},DOI={{{2}}},journal={{{3}}},author={{{4}}},year={{{5}}}"
        return properties.format(row.item_title(), row.url(), row.item_doi(),
                                 row.publication_title(), row.short_authors(), row.publication_year())

    def _citation_name(self, row):
        authors = row.short_authors().split(' ')
        doc_id = '_'.join(authors) if len(row.authors()) != 0 \
            else '_'.join(row.item_doi().split('/'))
        name = doc_id + '_' + row.publication_year()
        return name.lower()
