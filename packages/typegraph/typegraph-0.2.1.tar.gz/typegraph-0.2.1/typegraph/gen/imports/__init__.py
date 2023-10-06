from .abi import Abi
from dataclasses import dataclass

@dataclass
class RootImports:
    abi: Abi
