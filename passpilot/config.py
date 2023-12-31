import toml
from typing import Dict

class Config:
    def __init__(self) -> None:
        self.data: Dict = {}
    
    def load(self, path: str) -> None:
        with open(path, "r",encoding='utf-8') as f:
            self.data = toml.load(f)
