import xml.etree.ElementTree as ET


class Uniprot:

    URL = '{http://uniprot.org/uniprot}'

    def __init__(self, file):
        self.tree = ET.fromstring(file)

    @property
    def accession(self) -> list:
        for item in self.tree.iter(self.URL + 'uniprot'):
            entries = item.findall(self.URL + 'entry')
            for entry in entries:
                return entry.findtext(self.URL + 'accession')

    @property
    def gene_primary_name(self) -> list:
        for item in self.tree.iter(self.URL + 'uniprot'):
            entries = item.findall(self.URL + 'entry')
            for entry in entries:
                return entry.find(self.URL + 'gene').find(self.URL + 'name[@type="primary"]').text

    @property
    def gene_synonym(self) -> list:
        for item in self.tree.iter(self.URL + 'uniprot'):
            entries = item.findall(self.URL + 'entry')
            for entry in entries:
                return entry.find(self.URL + 'gene').find(self.URL + 'name[@type="synonym"]').text

    @property
    def full_name(self) -> str:
        for item in self.tree.iter(self.URL + 'uniprot'):
            entries = item.findall(self.URL + 'entry')
            for entry in entries:
                return entry.find(self.URL + 'protein').find(self.URL + 'recommendedName').findtext(self.URL + 'fullName')

    def organism(self) -> str:
        pass

    def reference(self) -> str:
        pass

    def feature(self) -> list:
        pass

    def author(self) -> str:
        pass

