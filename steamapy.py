import steam
from steam.api import interface

steam.api.key.set("DB2CF0896A1B5A00399BC289D8CF28F1")

schema = steam.items.schema(440)
for item in schema:
    if item.name == "Spiral Sallet":
        print(item.schema_id)
        print(item.tradable)