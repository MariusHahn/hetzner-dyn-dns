# hetzner-dyn-dns

## Retrieve your zone file id

```bash
./find-available-zones.sh <YOUR_HETZNER_TOKEN>
```

This will return you a json containing all zones available with the given token. Pick the id of the zone you want change.

## Update Record

Update the record of your choice

```bash
xxxx <YOUR_HETZNER_TOKEN> <ZONE_FILE_ID> <RECORD_NAME> 
```
