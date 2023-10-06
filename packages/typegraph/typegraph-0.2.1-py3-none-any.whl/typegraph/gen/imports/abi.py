from ..types import Result
from abc import abstractmethod
from typing import List, Protocol

class Abi(Protocol):
    @abstractmethod
    def glob(self, pattern: str, exts: List[str]) -> Result[List[str], str]:
        raise NotImplementedError
    @abstractmethod
    def read_file(self, path: str) -> Result[str, str]:
        raise NotImplementedError

