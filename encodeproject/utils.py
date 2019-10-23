from tqdm.auto import tqdm
import requests

__all__ = ["download"]


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
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(path, 'wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        raise ValueError(
            "The downloaded size does not match the header total size.")
