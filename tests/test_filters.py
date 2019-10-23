from encodeproject import accessions, download_urls
from .utils import cached_experiment, cached_biosample


def test_accessions():
    assert accessions(cached_experiment(
        assembly="hg19",
        cell_line="HepG2",
        target="ARID3A"
    )) == ['ENCSR000EDP']


def test_download_urls():
    assert set(download_urls(cached_biosample(
        accession="ENCSR000EDP",
        file_format="bigwig",
        assembly="hg19"
    ))) == set([
        'https://encode-public.s3.amazonaws.com/2012/07/01/074e1b37-2be1-4f6a-aa42-6c512fd1834b/ENCFF000XOW.bigWig',
        'https://encode-public.s3.amazonaws.com/2017/12/09/a5a4579f-820c-4378-9a13-20b65b6f7ed5/ENCFF339LAP.bigWig',
        'https://encode-public.s3.amazonaws.com/2017/12/09/48fb8f35-65b2-4485-b9bb-5d614c0e7b1e/ENCFF371TXR.bigWig',
        'https://encode-public.s3.amazonaws.com/2017/12/09/69c16bcf-7306-41c8-9e37-f80deca86106/ENCFF460WFF.bigWig',
        'https://encode-public.s3.amazonaws.com/2017/12/09/22e2e506-f598-4ecf-b5f0-f9baaa2fac99/ENCFF156ULZ.bigWig',
        'https://encode-public.s3.amazonaws.com/2017/12/09/453abba4-0958-4646-a0a6-bc6baaa36a46/ENCFF459PHJ.bigWig',
        'https://encode-public.s3.amazonaws.com/2017/12/09/ee5bb131-498b-4ddd-a1bc-0db4940d4f93/ENCFF086LFN.bigWig'
    ])