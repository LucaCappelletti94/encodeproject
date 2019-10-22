from encodeproject import accessions
from .utils import cached_experiment

def test_accessions():
    assert accessions(cached_experiment(
        assembly="hg19",
        cell_line="HepG2",
        target="ARID3A"
    )) == ['ENCSR000EDP']