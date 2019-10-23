from encodeproject import download
import os


def test_download():
    download("https://encode-public.s3.amazonaws.com/2012/07/01/074e1b37-2be1-4f6a-aa42-6c512fd1834b/ENCFF000XOW.bigWig")
    os.remove("ENCFF000XOW.bigWig")