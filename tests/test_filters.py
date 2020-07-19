from encodeproject import accessions, download_urls, biosample
from .utils import cached_experiment


def test_accessions():
    assert accessions(cached_experiment(
        assembly="hg19",
        cell_line="HepG2",
        target="ARID3A"
    )) == ['ENCSR000EDP']


def test_download_urls():
    download_urls(biosample(
        accession="ENCSR000EDP",
        assembly="hg19"
    ))