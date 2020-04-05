from encodeproject import biosample_to_dataframe
import json


def test_dataframe_extraction():
    biosample_to_dataframe(json.load(open("tests/test_sample.json")))
    biosample_to_dataframe(json.load(open("tests/long_sample.json")))