from requests import get
from typing import Dict, List, Union, Tuple
from multiprocessing import cpu_count, Pool
from tqdm.auto import tqdm
from .utils import biosample_to_dataframe
import pandas as pd
from cache_decorator import Cache


@Cache(cache_path="encodeproject_cache/{_hash}.json.gz")
def query(url: str, parameters: Dict[str, str]) -> Dict:
    """Return JSON response at given url and parameters."""
    return get(url, params=parameters, headers={"Accept": "application/json"}).json()


def encode_query(parameters: Dict[str, str] = None, path: str = "search") -> Dict:
    """Return JSON response for given parameters on encode.
        parameters: Dict[str, str], the parameters for the query.
        path:str="search", the path where to run the query.
    """
    return query(
        url="https://encodeproject.org/{path}/".format(path=path),
        parameters=({} if parameters is None else parameters)
    )


def experiment(
    cell_line: str = None,
    assembly: str = None,
    target: str = None,
    status: str = "released",
    organism: str = "Homo sapiens",
    file_type: str = "bigWig",
    replicated: bool = True,
    searchTerm: str = None,
    parameters: Dict[str, str] = None,
    limit: Union[str, int] = "all",
    drop_errors: Union[Tuple[str], str] = (
        "extremely low read depth",
        "missing control alignments",
        "control extremely low read depth",
        "extremely low spot score",
        "extremely low coverage",
        "extremely low read length",
        "inconsistent control",
        "inconsistent read count"
    )
) -> Dict:
    """Return JSON response for given parameters.

    Parameters
    ------------------------------
    cell_line: str = None,
        the label for the chosen cell line for instance "HepG2".
    assembly: str = None,
        the assembly label, for instance "hg19".
    target: str = None,
        the target name, for instance "ARID3A".
    status: str = "released",
        the release status, can be either "released", "archived" or "revoked".
    organism: str = "Homo sapiens",
        The organism to query for.
    file_type: str = "bigWig",
        The type of the required files. By default bigWig.
    replicated: bool = True,
        Whetever to enforce for only replicated results.
    searchTerm: str = None, 
        additional search terms.
    parameters: Dict[str, str],
        the remaining parameters that are not currently supported directly.
    limit: Union[str, int] = "all",
        Number of experiments to query for. Use "all" for all experiments.
    """
    return encode_query({
        "type": "Experiment",
        "status": status,
        "limit": limit,
        **({
            "replication_type!": "unreplicated",
        } if replicated else {}),
        **({
            "audit.ERROR.category!": drop_errors
        } if drop_errors else {}),
        ** {
            key: value for key, value in {
                "biosample_ontology.term_name": cell_line,
                "assembly": assembly,
                "target.label": target,
                "searchTerm": searchTerm,
                "replicates.library.biosample.donor.organism.scientific_name": organism,
                "files.file_type": file_type
            }.items() if value is not None
        },
        ** ({} if parameters is None else parameters)
    })


def biosample(
    accession: str,
    to_dataframe: bool = True,
    status: str = "released",
    organism: str = "human",
    assembly: str = "hg19",
    output_type: str = "fold change over control",
    min_biological_replicates: int = 2
) -> Dict:
    """Return JSON response for given biosample.

    Parameters
    -----------------------------
    accessions: List[str],
        code corresponding to biosample.
    to_dataframe: bool = True,
        Whetever to convert the obtained data to a DataFrame.
        Filters are applied only to dataframes.
    status: str = "released",
        Status of data to consider.
    organism: str = "human",
        The organism to filter for.
    assembly: str = "hg19",
        The genomic assembly to use.
    min_biological_replicates: int = 2,
        The minimal amount of biologial replicas to use.

    Returns
    -----------------------------
    Return the list of biosample curresponding to given accession codes.
    """
    data = encode_query(
        path="experiments/{accession}".format(accession=accession)
    )
    data = biosample_to_dataframe(data) if to_dataframe else data
    if to_dataframe:
        data = data[
            (data.status == status) &
            (data.organism == organism) &
            (data.assembly == assembly) &
            (data.output_type == output_type) &
            (data.biological_replicates.str.len() >= min_biological_replicates)
        ]
    return data


def _biosample(kwargs) -> Dict:
    return biosample(**kwargs)


def biosamples(accessions: List[str], to_dataframe: bool = True, **kwargs) -> List[Union[Dict, pd.DataFrame]]:
    """Return list of JSON responses for given accession codes.

    Parameters
    -----------------------------
    accessions: List[str],
        code corresponding to biosample.
    to_dataframe: bool = True,
        Whetever to convert the obtained data to a DataFrame.

    Returns
    -----------------------------
    Return the list of biosamples curresponding to given accession code.
    """
    with Pool(min(cpu_count(), len(accessions))) as p:
        data = list(tqdm(
            p.imap(_biosample, (
                {
                    "accession": accession,
                    "to_dataframe": to_dataframe,
                    **kwargs
                }
                for accession in accessions)),
            total=len(accessions),
            desc="Retrieving biosamples",
            leave=False,
            dynamic_ncols=True
        ))
        p.close()
        p.join()
    return pd.concat(data).reset_index(drop=True) if to_dataframe else data
