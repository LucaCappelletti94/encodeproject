from encodeproject import biosample, biosamples

def test_biosample():
    biosample("ENCSR000EDP")
    biosample("ENCSR000EDP", False)

def test_biosamples():
    biosamples(["ENCFF454HMH", "ENCFF663AYS"])
    biosamples(["ENCSR000EDP"], False)