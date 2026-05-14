import requests
import logging
from typing import Optional, List, Set
from hcloud import Client
from hcloud.zones import Zone, ZoneRecord, ZoneRRSet, BoundZoneRRSet
from hcloud.actions import BoundAction

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_current_server_ip_address() -> str:
    return requests.get("https://api.ipify.org").text


def get_all_existing_dns_A_record_names(token: str, zone: str) -> Set[str]:
    client = Client(token=token)
    return {rr_set.name for rr_set in client.zones.get_rrset_all(zone=Zone(name=zone), type=["A"])}


def delete_record(token: str, zone: str, name: str) -> None:
    client: Client = Client(token)
    response = client.zones.delete_rrset(ZoneRRSet(zone=Zone(name=zone), name=name, type="A",))
    response.action.wait_until_finished()

def get_current_dns_ip_address(token : str, zone_name: str, record: str) -> Optional[str]: 
    client = Client(token=token)
    records = client.zones.get_rrset(zone=Zone(name=zone_name), name=record, type="A").records or []
    return records[0].value if len(records) == 1 else None


def get_not_yet_existing_domain_names(token: str, zone: str, domain_names: Set[str]) -> Set[str] :
    client = Client(token=token)
    existing_records: List[BoundZoneRRSet] = client.zones.get_rrset_all(zone=Zone(name=zone), type=["A"])
    existing_domain_names: Set[str] = {
        existing_record.name 
        for existing_record in existing_records 
        if existing_record.name in domain_names
    }
    return domain_names - existing_domain_names

def create_domain_records(token: str, zone: str, domain_names_to_create: Set[str], current_server_ip: str):
    client = Client(token=token)
    for domain_name_to_create in domain_names_to_create:
        response = client.zones.create_rrset(
            zone=Zone(name=zone),
            name=domain_name_to_create,
            type="A",
            ttl=600,
            records=[ZoneRecord(value=current_server_ip)],
        )
        response.action.wait_until_finished()
        logging.info(f"new record for {domain_name_to_create} has been create with ip address {current_server_ip}")




def update_dyn_dns_records(token: str, zone: str, dyn_dns_domain_names: Set[str], current_server_ip: str):
    client = Client(token=token)
    existing_record_sets: List[BoundZoneRRSet] = client.zones.get_rrset_all(zone=Zone(name=zone), type=["A"])
    dyn_dns_record_sets = (
        dyn_dns_record_set
        for dyn_dns_record_set in existing_record_sets
        if dyn_dns_record_set.name in dyn_dns_domain_names
    )
    for dyn_dns_record_set in dyn_dns_record_sets:
        name: str = dyn_dns_record_set.name
        records : List[ZoneRecord] = dyn_dns_record_set.records or []
        if 1 < len(records) or records[0].value != current_server_ip:
            response: BoundAction = dyn_dns_record_set.set_rrset_records([ZoneRecord(current_server_ip)])
            response.wait_until_finished()
            logging.info(f"ip address for {name} has been update to the servers new ip address {current_server_ip}")
        else:
            logging.info(f"ip address for {name} stayes unchanged. Nothing todo")

