from typing import List, Dict


def accessions(response: Dict) -> List:
    """Return extracted accessions keys from response."""
    return [
        data["accession"] for data in response['@graph']
    ]


def download_urls(samples:Dict)->List:
    return [
        f["cloud_metadata"]["url"] for f in samples["files"]
    ]