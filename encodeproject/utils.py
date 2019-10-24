from tqdm.auto import tqdm
import requests
import humanize
from typing import List, Dict
import pandas as pd

__all__ = ["download", "sample_to_dataframe"]


def download(url: str, path: str = None, block_size: int = 32768):
    """Download file at given url showing a loading bar.

    Parameters
    ----------------------
    url:str, The url from where to download the data.
    path:str=None, The path where to store the data, if None the end of the url is used.
    block_size:int=1024, The download block size.

    Raises
    ----------------------
    ValueError, 
        if the downloaded file size does not match the header file size.
    """
    if path is None:
        path = url.split("/")[-1]
    r = requests.get(url, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    t = tqdm(total=total_size, unit='iB',
             unit_scale=True, desc="Download in progress")
    with open(path, 'wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        raise ValueError(
            "The downloaded size does not match the header total size.")


def sample_informations(sample: Dict) -> Dict:
    """Return generic informations from the sample.
        sample:Dict, the sample from which to extract the informations.
    """
    return {
        "organism": sample["target"]["organism"]["name"],
        "cell_line": sample["biosample_ontology"]["term_name"],
        "target": sample["target"]["label"]
    }


def sample_files_informations(sample: Dict) -> List[Dict]:
    """Return list of informations for every files in the sample.
        sample:Dict, the sample from which to extract the files informations.
    """
    return [
        {
            "status": f["status"],
            "accession":f["accession"],
            "file_size":f["file_size"],
            "file_format":f["file_format"],
            "assembly":f["assembly"] if "assembly" in f else None,
            "biological_replicates":f["biological_replicates"],
            "output_type":f["output_type"],
            "url":f["cloud_metadata"]["url"]
        }.items() for f in sample["files"]
    ]


def sample_to_dataframe(sample: Dict) -> pd.DataFrame:
    """Return simple dataframe representation for given sample.
        sample:Dict, the sample to convert into a simple DataFrame.
    """
    df = pd.DataFrame(sample_files_informations(sample))
    for key, value in sample_informations(sample).items():
        df[key] = value
    return df
