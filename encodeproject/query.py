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


def experiment(cell_line: str = None, assembly: str = None, target: str = None, status: str = "released", searchTerm: str = None, parameters: Dict[str, str] = None) -> Dict:
    """Return JSON response for given parameters.
        cell_line: str = None, the label for the chosen cell line for instance "HepG2".
        assembly: str = None, the assembly label, for instance "hg19".
        target: str = None, the target name, for instance "ARID3A".
        status: str = "released", the release status, can be either "released", "archived" or "revoked".
        searchTerm: str = None, additional search terms.
        parameters: Dict[str, str], the remaining parameters that are not currently supported directly.
    """
    return encode_query({
        "type": "Experiment",
        "status": status,
        **{
            key: value for key, value in {
                "biosample_ontology.term_name": cell_line,
                "assembly": assembly,
                "target.label": target,
                "searchTerm": searchTerm
            }.items() if value is not None
        },
        ** ({} if parameters is None else parameters)
    })


def biosample(accession: str) -> Dict:
    """Return JSON response for given biosample.
        accession:str, code corresponding to biosample.
    """
    return encode_query(
        path="experiments/{accession}".format(accession=accession)
    )
