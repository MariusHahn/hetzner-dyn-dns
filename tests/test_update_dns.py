import logging


from main.update_dns import get_current_dns_ip_address, get_current_server_ip_address
from main.model import Record

def test_get_current_dns_ip_address_500_logs_error(caplog):
    caplog.set_level(logging.INFO)

    token = "bliblablub"
    get_current_dns_ip_address(
        token,
        "hahn.wtf",
        Record("@", "A"),
    )

    assert caplog.records
    assert f"the token you have provided is invalid. {token}" in caplog.text


def test_get_current_server_ip_address_returns_ipv4():
    import re

    ip = get_current_server_ip_address()
    assert re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip)

