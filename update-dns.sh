#!/bin/bash


base_url='https://dns.hetzner.com/api/v1'
auth_string="Auth-API-Token: $1" 
zone_id=$2 
record_name='wg'

echo  "Zone id: $zone_id"

record_id=$(curl -s "$base_url/records?zone_id={$zone_id}" -H "$auth_string" \
     | jq '.records[] | select(.name == "'"$record_name"'")' \
     | jq -r '.id')

echo "Record id: $record_id"

dns_ip=$(curl -s "$base_url/records/$record_id" -H "$auth_string" \
     | jq -r '.record.value')

echo "dns service ip: $dns_ip"

current_ip=$(curl -s ifconfig.me)

echo "current ip: $current_ip"

if [ "$current_ip" == "$dns_ip" ]; 
then
     echo "Nothing to do. Ip unchanged: $current_ip"
else
     echo "old ip was $dns_ip, change it to current ip: $current_ip"
     update_response_code=$(curl -s -o /dev/null -w "%{http_code}" \
          -X "PUT" "$base_url/records/$record_id" \
          -H 'Content-Type: application/json' \
          -H  "$auth_string" \
          -d '{
               "value": "'"$current_ip"'",
               "ttl": 0,
               "type": "A",
               "name": "'"$record_name"'",
               "zone_id": "'"$zone_id"'"
               }')
     if [ "$update_response_code" -eq 200 ]; then
          echo "DNS record updated successfully"
     else
          echo "Failed to update DNS record"
     fi
fi
