from tqdm.auto import tqdm
import requests
import humanize
import os
from typing import List, Dict
import pandas as pd

__all__ = ["download", "biosample_to_dataframe"]


def download(url: str, path: str = None, block_size: int = 32768, cache: bool = False):
    """Download file at given url showing a loading bar.

    Parameters
    ----------------------
    url:str,
        The url from where to download the data.
    path:str=None,
        The path where to store the data, if None the end of the url is used.
    block_size:int=1024,
        The download block size.
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
        with open(path, 'wb') as f:
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

    return {
        "organism": organism,
        "cell_line": sample["biosample_ontology"]["term_name"],
        "target": label
    }


def sample_files_informations(sample: Dict) -> List[Dict]:
    """Return list of informations for every files in the sample.
        sample:Dict, the sample from which to extract the files informations.
    """
    return [
        {
            "status": f["status"] if "status" in f else None,
            "accession":f["accession"] if "accession" in f else None,
            "file_size":f["file_size"] if "file_size" in f else None,
            "file_format":f["file_format"] if "file_format" in f else None,
            "assembly":f["assembly"] if "assembly" in f else None,
            "biological_replicates":sorted(f["biological_replicates"]),
            "output_type":f["output_type"] if "output_type" in f else None,
            "url":f["cloud_metadata"]["url"] if "cloud_metadata" in f else None,
        } for f in sample["files"]
    ]


def biosample_to_dataframe(sample: Dict) -> pd.DataFrame:
    """Return simple dataframe representation for given sample.
        sample:Dict, the sample to convert into a simple DataFrame.
    """
    sample = normalize_sample(sample)
    df = pd.DataFrame(sample_files_informations(sample))
    for key, value in sample_informations(sample).items():
        df[key] = value
    return df


def normalize_sample(sample: Dict) -> Dict:
    if "files" not in sample:
        return {
            "files": [sample.copy()],
            **sample.copy()
        }
    return sample
