from __future__ import annotations

from hcloud import Client
from hcloud.zones import Zone as HcloudZone, ZoneRecord, ZoneRRSet

from dotenv import load_dotenv
import logging
from schedule import every, repeat, run_pending, idle_seconds
import time
from main.model import ConsoleProject, Zone
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@repeat(every(10).minutes)
def main() -> None:
    load_dotenv()
    current_server_ip = get_current_server_ip_address()
    console_project: ConsoleProject = get_console_project()
    zone = console_project.zone

    for record in zone.records:
        current_dns_ip = get_current_dns_ip_address(console_project.token, zone.name, record)
        if not current_dns_ip:
            logging.error("Could not retrieve dns ip. Something went wrong") 
        elif current_dns_ip != current_server_ip:
            update_ip_address(console_project.token, current_server_ip, record)
        else:
            logging.info(f"Nothing to do. Public ip address unchanged: {current_server_ip}")

def get_current_server_ip_address() -> str:
    import requests
    return requests.get("https://api.ipify.org").text


def get_current_dns_ip_address(token : str, zone_name: str, record: str) -> Optional[str]: 
    from hcloud._exceptions import APIException
    client = Client(token=token)
    records: List[ZoneRecord] = []
    try: 
        records = client.zones.get_rrset(zone=HcloudZone(name=zone_name), name=record, type="A").records or []
    except APIException as e:
        if "404" in e.message:
            logging.error(f"There is no existing record with name={record} yet. You have to add it first")
        else:
            logging.error(f"{e.message}. {token}")
    return records[0].value if len(records) == 1 else None 


def update_ip_address(token, current_server_ip, rr_set):
    client = Client(token=token)
    record_set = ZoneRRSet(zone=HcloudZone(name=rr_set.zone_name), name=rr_set.name, type=rr_set.typ3)
    action = client.zones.set_rrset_records(
        rrset=record_set,
        records=[ZoneRecord(value=current_server_ip)],
    )
    action.wait_until_finished()
    logging.info(f"IP address has been updated to: {current_server_ip}")
    
def get_console_project() -> ConsoleProject:
    import os
    import json
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    file_path = os.path.join(script_dir, 'config.json')
    with open(file_path, "r") as file:
        c = json.load(file)
        return ConsoleProject(
            c["token"], 
            Zone(
                c["zone"]["name"], 
                c["zone"]["records"]
            )
        )


if __name__ == "__main__":
    main()
    while True:
        n = idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            time.sleep(n)
        run_pending()

