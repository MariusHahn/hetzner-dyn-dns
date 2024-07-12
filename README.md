# Hetzner-dyn-dns

## Retrieve your zone file id

```bash
./find-available-zones.sh <YOUR_HETZNER_TOKEN>
```

This will return you a json containing all zones available with the given token. Pick the id of the zone you want change.

## Update Record

Update the record of your choice

```bash
./update-dns.sh <YOUR_HETZNER_TOKEN> <ZONE_FILE_ID> <RECORD_NAME>
```


## Combine it with a cronjob

Let's combine it with a cronjob that runs every 10 minutes.

```bash
crontab -e
```

Then add 

```bash
*/10 * * * * /path/to/your/update-dns.sh <YOUR_HETZNER_TOKEN> <ZONE_FILE_ID> <RECORD_NAME>
```