from __future__ import annotations

import logging
from schedule import every, repeat, run_pending, idle_seconds
import time
from util import (
    get_current_server_ip_address, 
    get_not_yet_existing_domain_names, 
    create_domain_records, 
    update_dyn_dns_records,
)
from model import Config
from typing import Set

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@repeat(every(10).minutes)
def main() -> None:
    config = Config.load()
    current_server_ip = get_current_server_ip_address()
    new_dyn_dns_names: Set[str] = get_not_yet_existing_domain_names(config.token, config.zone, config.records)
    create_domain_records(config.token, config.zone, new_dyn_dns_names, current_server_ip)
    update_dyn_dns_records(config.token, config.zone, config.records, current_server_ip)


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

