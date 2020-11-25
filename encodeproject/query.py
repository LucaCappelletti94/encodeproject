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
    perturbed: bool = None,
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
    perturbed: bool = None,
        Wether to filter perturbed data (True), unperturbed data (False) or 
        both of the classes (None).
    searchTerm: str = None, 
        additional search terms.
    parameters: Dict[str, str],
        the remaining parameters that are not currently supported directly.
    limit: Union[str, int] = "all",
        Number of experiments to query for. Use "all" for all experiments.
    """
    if perturbed not in (True, False, None):
        raise ValueError((
            "Given value '{}' for parameter `perturbed` is not supported.\n"
            "The valid values are `True`, `False` and `None`."
        ).format(perturbed))
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
                "perturbed": perturbed,
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
    file_format: str = "bigWig",
    replication_type: str = "isogenic",
    output_type: str = None,
    min_biological_replicates: int = 0
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
    file_format: str = "bigWig",
        Type of the format of the files.
        Use None to skip this filter.
    replication_type: str = "isogenic",
        Type of the experiment replication.
        Use None to skip this filter.
    output_type: str = None,
        Type of output to filter for.
        Use None to skip this filter.
    min_biological_replicates: int = 0,
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
        if status is not None:
            data = data[data.status == status]
        if organism is not None:
            data = data[data.organism == organism]
        if file_format is not None:
            data = data[data.file_format == file_format]
        if assembly is not None:
            data = data[data.assembly == assembly]
        if replication_type is not None:
            data = data[data.replication_type == replication_type]
        if output_type is not None:
            data = data[data.output_type == output_type]
        if min_biological_replicates > 0:
            data = data[data.biological_replicates.str.len() >=
                        min_biological_replicates]
    return data


def _biosample(kwargs) -> Dict:
    return biosample(**kwargs)


def biosamples(
    accessions: List[str],
    to_dataframe: bool = True,
    use_multiprocessing: bool = True,
    **kwargs
) -> List[Union[Dict, pd.DataFrame]]:
    """Return list of JSON responses for given accession codes.

    Parameters
    -----------------------------
    accessions: List[str],
        code corresponding to biosample.
    to_dataframe: bool = True,
        Whetever to convert the obtained data to a DataFrame.
    use_multiprocessing: bool = True,
        Wether to use multiprocessing or execute in single thread.

    Returns
    -----------------------------
    Return the list of biosamples curresponding to given accession code.
    """
    tasks = [
        {
            "accession": accession,
            "to_dataframe": to_dataframe,
            **kwargs
        }
        for accession in accessions
    ]
    if use_multiprocessing:
        with Pool(min(cpu_count(), len(accessions))) as p:
            data = list(tqdm(
                p.imap(_biosample, tasks),
                total=len(accessions),
                desc="Retrieving biosamples",
                leave=False,
                dynamic_ncols=True
            ))
            p.close()
            p.join()
    else:
        data = [
            _biosample(task)
            for task in tqdm(
                tasks,
                total=len(accessions),
                desc="Retrieving biosamples",
                leave=False,
                dynamic_ncols=True
            )
        ]

    data = [
        sample
        for sample in data
        if sample is not None
    ]

    return pd.concat(data).reset_index(drop=True) if to_dataframe else data
