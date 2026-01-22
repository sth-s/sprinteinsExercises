#!/usr/bin/env python3
import os
import json
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import SQLModel, Session
from shared.infrastructure.database import Database
from domains.sales.infrastructure.repositories.orm_models import PlayType, Play, Customer, Invoice, Performance

load_dotenv()
db_path = Path(os.getenv("DB_PATH", "data/theater.db"))
data_dir = Path(os.getenv("DATA_DIR", "data"))

if db_path.exists():
    print(f"Database already exists: {db_path}")
    exit(0)

db = Database(db_path)
SQLModel.metadata.create_all(db.get_engine())
print(f"Created: {db_path}")

plays_json = json.loads((data_dir / "plays.json").read_text())
invoices_json = json.loads((data_dir / "invoices.json").read_text())

with Session(db.get_engine()) as session:
    play_types = {}
    for play_id, info in plays_json.items():
        if info['type'] not in play_types:
            play_types[info['type']] = PlayType(name=info['type'])
            session.add(play_types[info['type']])
        session.flush()
        session.add(Play(id=play_id, name=info['name'], type_id=play_types[info['type']].id))
    
    for inv in invoices_json:
        customer = Customer(name=inv['customer'])
        session.add(customer)
        session.flush()
        
        invoice = Invoice(customer_id=customer.id)
        session.add(invoice)
        session.flush()
        
        for perf in inv['performances']:
            session.add(Performance(invoice_id=invoice.id, play_id=perf['playID'], audience=perf['audience']))
    
    session.commit()

print("Done!")
