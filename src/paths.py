from pathlib import Path

BASE = Path.cwd()


class STATIC:
    PATH = BASE / "static"

    class MOCKS:
        PATH = BASE / "static" / "mocks"
        ARTISTS = BASE / "static" / "mocks" / "artists.json"
