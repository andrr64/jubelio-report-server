from dataclasses import dataclass


@dataclass
class GeneratedFile:
    path: str
    filename: str
    content_type: str
