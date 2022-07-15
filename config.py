from pathlib import Path

class Config:
    BASE_URL = "https://www.carlogos.org"
    MAKERS_LIST_URL = BASE_URL + "/car-brands-a-z/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
    }
    MAX_THUMBNAIL_SIZE = (256, 256)
    MAX_OPTIMIZED_SIZE = (1024, 1024)
    RAW_DIRPATH = Path(__file__).parent / "raw"
    THUMBNAIL_DIRPATH = Path(__file__).parent / "thumbnails"
    OPTIMIZED_DIRPATH = Path(__file__).parent / "optimized"