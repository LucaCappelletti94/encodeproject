from requests import get
from typing import Dict, List


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


def experiment(cell_line: str = None, assembly: str = None, target: str = None, status: str = "released", parameters: Dict[str, str] = None) -> Dict:
    """Return JSON response for given parameters.
        cell_line: str = None, the label for the chosen cell line for instance "HepG2".
        assembly: str = None, the assembly label, for instance "hg19".
        target: str = None, the target name, for instance "ARID3A".
        status: str = "released", the release status, can be either "released", "archived" or "revoked".
        parameters: Dict[str, str], the remaining parameters that are not currently supported directly.
    """
    return encode_query({
        "type": "Experiment",
        "status": status,
        **({} if cell_line is None else {"biosample_ontology.term_name": cell_line}),
        **({} if assembly is None else {"assembly": assembly}),
        **({} if target is None else {"target.label": target}),
        **({} if parameters is None else parameters)
    })


def biosample(accession: str, file_format: str = None, output_type: str = None, assembly: str = None, biological_replicates: List = None) -> Dict:
    """Return JSON response for given biosample.
        accession:str, code corresponding to biosample.
        file_format:str=None, the format of the files, for instance bigwig.
        output_type:str = None, the output of the files, for instance fold change over control.
        assembly:str=None, the assembly of the files, for instance assembly.
        biological_replicates:List=None, the specific biological replicates, for instance [2, 1].
    """
    sample = encode_query(
        path="experiments/{accession}".format(accession=accession)
    )
    files = sample["files"]
    sample["files"] = [
        f for f in files
        if (file_format is None or f["file_format"].lower() == file_format.lower()) and
           (output_type is None or f["output_type"].lower() == output_type.lower()) and
           (assembly is None or f["assembly"].lower() == assembly.lower()) and
           (biological_replicates is None or set(
               f["biological_replicates"]) == set(biological_replicates))
    ]
    return sample
