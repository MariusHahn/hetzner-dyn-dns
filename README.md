# Hetzner-dyn-dns

This is my way to update the pulic ip address of raspberry pi

## install on Server

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## configure it

1. add a `.env` file with your hetzner token
```bash
TOKEN=<your-token>
```

2. add a `rr_set.json` with your 
```json
[
    {
        "zoneName": "example.com",
        "name": "x1",
        "type": "A"
    },
    {
        "zoneName": "example.com",
        "name": "x2",
        "type": "A"
    },
    …
]
```
## add to crobtab

1. open crontab with `crontab -e`
2. Add a chronjob that updates the ip addresse of your choice every 10 minutes
```bash
*/10 * * * * /<clone_path>/hetzner-dyn-dns/.venv/bin/python /<clone_path>/hetzner-dyn-dns/update-dns.py >> /<clone_path>/hetzner-dyn-dns/update-dns.log 2>&1
```