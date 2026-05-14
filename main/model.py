from typing import NamedTuple, Set, Dict
import os
from dotenv import load_dotenv

class Config(NamedTuple):
    token: str
    zone: str
    records: Set[str]

    @classmethod
    def load(cls) -> "Config":
        prefix = "HETZNER_DYNDNS"
        envs: Dict[str, str] = {name: value for name, value in os.environ.items() if name.startswith(prefix)}
        assert "HETZNER_DYNDNS_TOKEN" in envs, "You have to define a Hetzner api token"
        assert "HETZNER_DYNDNS_ZONE" in envs, "You have to define the Hetzner dns zone"
        records = {value for name, value in envs.items() if name.startswith("HETZNER_DYNDNS_RECORD")}
        assert len(records) >= 1, "you must at least define one record to update"
        return cls(envs["HETZNER_DYNDNS_TOKEN"], envs["HETZNER_DYNDNS_ZONE"], records)

    @classmethod
    def load_from_env_file(cls) -> "Config":
        load_dotenv(".env", override=False)
        return cls.load()