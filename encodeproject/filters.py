from typing import List, Dict

def accessions(response:Dict)->List:
    """Return extracted accessions keys from response."""
    return [
        data["accession"] for data in response['@graph']
    ]