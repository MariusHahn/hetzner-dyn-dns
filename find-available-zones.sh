#!/bin/bash

base_url='https://dns.hetzner.com/api/v1'
auth_string="Auth-API-Token: $1"

curl -s "$base_url/zones" -H "$auth_string"
