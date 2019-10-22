from encodeproject import experiment


def test_experiment():
    experiment()
    experiment(cell_line="HepG2")
    experiment(assembly="hg19")
    experiment(target="ARID3A")
    experiment(parameters={
        "target":"ARID3A"
    })