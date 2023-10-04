from typing import Set
from ..constants import GITIGNORE_FILENAME, CONTENT_BLOCK_START


def current() -> Set[str]:
    output: Set[str] = set()
    with open(GITIGNORE_FILENAME, mode="r", encoding="utf-8") as file:
        line = file.readline()
        while line:
            if line.startswith(CONTENT_BLOCK_START):
                return set(line.removesuffix("\n").split("/").pop().split(","))
            line = file.readline()
    return output
