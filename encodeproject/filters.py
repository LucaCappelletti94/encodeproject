from typing import List, Dict
from .utils import normalize_sample

__all__ = ["accessions", "download_urls"]


def accessions(experiment: Dict) -> List:
    """Return extracted accessions keys from experiment.
        experiment: Dict, the response of a experiment request.
    """
    return [
        data["accession"] for data in experiment['@graph']
    ]


def download_urls(biosample: Dict) -> List:
    """Return list of download url from given biosample files.
        biosample: Dict, the response of a biosample request.
    """
    return [
        f["cloud_metadata"]["url"]
        for f in normalize_sample(biosample)["files"]
        if "cloud_metadata" in f
    ]
