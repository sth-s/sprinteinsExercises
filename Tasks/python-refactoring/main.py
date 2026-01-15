import json
from statement import statement

with open("plays.json") as f:
    plays = json.load(f)

with open("invoices.json") as f:
    invoices = json.load(f)

print(statement(invoices[0], plays))
