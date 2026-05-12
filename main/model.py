from typing import NamedTuple, List
    
class Zone(NamedTuple):
    name: str
    records: List[str]

class ConsoleProject(NamedTuple):
    token: str
    zone: Zone