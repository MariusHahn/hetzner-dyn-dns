from __future__ import annotations

from os import getenv
from typing import NamedTuple

from hcloud import Client
from hcloud.zones import Zone, ZoneRecord, ZoneRRSet

from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class RRSet(NamedTuple):
    zone_name : str
    name : str
    typ3 : str


def main():
    load_dotenv()
    token = str(getenv("TOKEN"))
    current_server_ip = get_current_server_ip_address()

    for rr_set in get_rrsets():
        if get_current_dns_ip_address(token, rr_set) != current_server_ip:
            update_ip_address(token, current_server_ip, rr_set)
        else:
            logging.info(f"Nothing to do. Public ip address unchanged: {current_server_ip}")


def get_current_server_ip_address():
    import requests
    return requests.get("https://api.ipify.org").text


def get_current_dns_ip_address(token, rr_set):
    client = Client(token=token)
    rrset = client.zones.get_rrset(zone=Zone(name=rr_set.zone_name), name=rr_set.name, type=rr_set.typ3)
    return rrset.records[0].value


def update_ip_address(token, current_server_ip, rr_set):
    client = Client(token=token)
    record_set = ZoneRRSet(zone=Zone(name=rr_set.zone_name), name=rr_set.name, type=rr_set.typ3)
    action = client.zones.set_rrset_records(
        rrset=record_set,
        records=[ZoneRecord(value=current_server_ip)],
    )
    action.wait_until_finished()
    logging.info(f"IP address has been updated to: {current_server_ip}")
    


def get_rrsets():
    import os
    import json
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    file_path = os.path.join(script_dir, 'rr_sets.json')
    with open(file_path, "r") as file:
        return [RRSet(rr_set['zoneName'], rr_set['name'], rr_set['type']) for rr_set in json.load(file)]


if __name__ == "__main__":
    main()
