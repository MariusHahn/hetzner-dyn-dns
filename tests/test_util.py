from main.util import (
    get_current_dns_ip_address, 
    get_current_server_ip_address, 
    get_not_yet_existing_domain_names, 
    create_domain_records, 
    update_dyn_dns_records,
    delete_record,
    get_all_existing_dns_A_record_names,
)
from pytest import fixture
from main.model import Config

@fixture
def config():
    return Config.load_from_env_file()

def test_get_not_yet_existing_domain_names(config):
    existing_name = list(config.records)[0]
    create_domain_records(config.token, config.zone, {existing_name}, "192.168.1.1")
    not_existing_name = list(config.records)[1]
    assert get_not_yet_existing_domain_names(config.token, config.zone, config.records) == set([not_existing_name])
    delete_record(config.token, config.zone, existing_name)


def test_create_update_delete(config):
    test_dyn_dyns_names = config.records
    existing_dns_names = get_all_existing_dns_A_record_names(config.token, config.zone)
    for test_name in test_dyn_dyns_names:
        if test_name in existing_dns_names:
            delete_record(config.token, config.zone, test_name)
    
    create_domain_records(config.token, config.zone, test_dyn_dyns_names, "192.168.1.1")
    for test_name in test_dyn_dyns_names:
        assert get_current_dns_ip_address(config.token, config.zone,  test_name) == "192.168.1.1"

    update_dyn_dns_records(config.token, config.zone, test_dyn_dyns_names, "192.168.1.2")
    
    for test_name in test_dyn_dyns_names:
        assert get_current_dns_ip_address(config.token, config.zone,  test_name) == "192.168.1.2"
    
    for test_name in test_dyn_dyns_names:
        delete_record(config.token, config.zone, test_name)


def test_get_current_server_ip_address_returns_ipv4():
    import re

    ip = get_current_server_ip_address()
    assert re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip)

