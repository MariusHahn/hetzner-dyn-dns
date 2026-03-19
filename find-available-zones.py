from __future__ import annotations
from dotenv import load_dotenv
from os import getenv
from hcloud import Client

load_dotenv()
token = str(getenv('TOKEN'))
client = Client(token=token)

for zone in client.zones.get_all():
    print(f'zone id: {zone.id}')
    print(f'zone name: {zone.name}')
    print("-------------------------------")
