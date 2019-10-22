from encodeproject import experiment
from dict_hash import sha256
from typing import Dict
import json
import os


def cached_experiment(**kwargs: Dict):
    path = "tests/cached_experiments"
    os.makedirs(path, exist_ok=True)
    path = "{path}/{sha}.json".format(
        path=path,
        sha=sha256(kwargs)
    )
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    response = experiment(**kwargs)
    with open(path, "w") as f:
        return json.dump(response, f)
    return response
