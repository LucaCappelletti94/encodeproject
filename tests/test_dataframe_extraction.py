from encodeproject import sample_to_dataframe
import pandas as pd
import json


def test_dataframe_extraction():
    sample_to_dataframe(json.load(open("tests/test_sample.json")))