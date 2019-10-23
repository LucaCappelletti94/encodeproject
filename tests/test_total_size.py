from encodeproject import total_size


def test_total_size():
    assert total_size(["https://encode-public.s3.amazonaws.com/2012/07/01/074e1b37-2be1-4f6a-aa42-6c512fd1834b/ENCFF000XOW.bigWig"]) == "374.9 MB"
