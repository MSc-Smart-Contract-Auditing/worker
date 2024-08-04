import os
from pathlib import Path


class URL:

    @staticmethod
    def __trim_slash(path: str):
        return path[:-1] if path.endswith("/") else path

    def __init__(self, base: str):
        self.base = URL.__trim_slash(base)

    def __truediv__(self, other: str):
        return URL(f"{self.base}/{URL.__trim_slash(other)}")

    def __str__(self):
        return self.base


class WorkingDirectory:
    @staticmethod
    def set(directory: Path | str):
        os.environ["WORK_DIR"] = str(directory)

    @staticmethod
    def get() -> Path:
        return Path(os.environ.get("WORK_DIR", ""))
