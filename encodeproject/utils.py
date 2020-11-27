from tqdm.auto import tqdm
import requests
import humanize
import os
from typing import List, Dict
import pandas as pd

__all__ = ["download", "biosample_to_dataframe"]


def download(url: str, path: str = None, block_size: int = 32768, cache: bool = False, append: bool = False):
    """Download file at given url showing a loading bar.

    Parameters
    ----------------------
    url:str,
        The url from where to download the data.
    path:str=None,
        The path where to store the data, if None the end of the url is used.
    block_size:int=1024,
        The download block size.
    append: bool = False,
        Wethever to append to the given file or not.
    cache: bool = False,
        Wethever to skip download if local file already exists.

    Raises
    --------------------------
    ValueError,
        If the request has not a status code 200 (success).
    """
    if path is None:
        path = url.split("/")[-1]
    if cache and os.path.exists(path):
        return
    r = requests.get(url, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    t = tqdm(
        total=total_size,
        unit='iB',
        unit_scale=True,
        desc="Downloading to {path}".format(path=path),
        dynamic_ncols=True,
        leave=False
    )
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    # If the user hits ctrl-c during the download we want to remove the partial
    # downloaded file.
    try:
        modality = "ab" if append else "wb"
        with open(path, modality) as f:
            for data in r.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
    except KeyboardInterrupt as e:
        os.remove(path)
        t.close()
        raise e
    if r.status_code != 200:
        os.remove(path)
        raise ValueError(
            "Request to url {url} finished with status code {status}.".format(
                url=url,
                status=r.status_code
            )
        )


def sample_informations(sample: Dict) -> Dict:
    """Return generic informations from the sample.
        sample:Dict, the sample from which to extract the informations.
    """
    if "target" in sample:
        target = sample["target"]
        organism = target["organism"]
        label = target["label"]
        if isinstance(organism, dict):
            organism = organism["name"]
    else:
        label = organism = "Unknown"

    keys = (
        "accession",
        "status",
        "assay_title",
        "assay_term_name",
        "replication_type",
        "date_released",
    )

    return {
        "organism": organism,
        "target": label,
        "term_id": sample["biosample_ontology"]["term_id"],
        "cell_line": sample["biosample_ontology"]["term_name"],
        "institute_name": sample["lab"]["institute_name"],
        "title": sample["lab"]["title"],
        **{
            key: sample[key] if key in sample else None
            for key in keys
        }
    }


def extract_analysis_objects(analysis_objects: Dict, accession: str) -> Dict:
    if accession not in analysis_objects:
        return {
            "encode_version": None,
        }
    analysis_object = analysis_objects[accession]
    encode_versions = analysis_object["pipeline_award_rfas"]
    return {
        "encode_version": None if encode_versions is None or len(encode_versions) == 0 else int(encode_versions[0][-1]),
    }


def sample_files_informations(sample: Dict) -> List[Dict]:
    """Return list of informations for every files in the sample.
        sample:Dict, the sample from which to extract the files informations.
    """
    if len(sample["files"]) == 0:
        return [{}]
    keys = (
        "accession",
        "assay_term_name",
        "assembly",
        "file_format",
        "file_size",
        "file_type",
        "output_category",
        "output_type",
        "read_length",
        "read_length_units",
        "run_type",
        "schema_version",
        "status",
    )

    if "analysis_objects" in sample:
        remapped_analysis_objects = {
            file_code.split("/")[2]: analysis_object
            for analysis_object in sample["analysis_objects"]
            for file_code in analysis_object["files"]
        }
    else:
        remapped_analysis_objects = {}

    return [
        {
            **{
                key: f[key] if key in f else None
                for key in keys
            },
            **extract_analysis_objects(remapped_analysis_objects, f["accession"]),
            "biological_replicates": sorted(f["biological_replicates"]) if "biological_replicates" in f else None,
            "technical_replicates": sorted(f["technical_replicates"]) if "technical_replicates" in f else None,
            "url":f["cloud_metadata"]["url"] if "cloud_metadata" in f else None,
        } for f in sample["files"]
    ]


def biosample_to_dataframe(sample: Dict) -> pd.DataFrame:
    """Return simple dataframe representation for given sample.
        sample:Dict, the sample to convert into a simple DataFrame.
    """
    sample = normalize_sample(sample)
    data = sample_files_informations(sample)
    metadata = sample_informations(sample)
    df = pd.DataFrame([
        {
            **metadata,
            **d,
        }
        for d in data
    ])
    return df


def normalize_sample(sample: Dict) -> Dict:
    if "files" not in sample:
        return {
            "files": [sample.copy()],
            **sample.copy()
        }
    return sample
