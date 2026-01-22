#!/usr/bin/env python3
import os
import random
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import Session, select
from shared.infrastructure.database import Database
from domains.sales.infrastructure.repositories.orm_models import PlayType, Play, Customer, Invoice, Performance

PLAYS = [
    ("macbeth", "Macbeth", "tragedy"),
    ("romeo-juliet", "Romeo and Juliet", "tragedy"),
    ("midsummer", "A Midsummer Night's Dream", "comedy"),
    ("twelfth-night", "Twelfth Night", "comedy"),
    ("merchant", "The Merchant of Venice", "comedy"),
    ("king-lear", "King Lear", "tragedy"),
]

CUSTOMERS = ["SmallCorp", "TechGiant Inc", "Arts Foundation", "City Theater Group", "University Drama Club"]

load_dotenv()
db = Database(Path(os.getenv("DB_PATH", "data/theater.db")))

with Session(db.get_engine()) as session:
    play_types = {pt.name: pt for pt in session.exec(select(PlayType)).all()}
    
    for play_id, name, type_name in PLAYS:
        if not session.exec(select(Play).where(Play.id == play_id)).first():
            session.add(Play(id=play_id, name=name, type_id=play_types[type_name].id))
            print(f"Added play: {name}")
    
    all_plays = session.exec(select(Play)).all()
    
    for customer_name in CUSTOMERS:
        if session.exec(select(Customer).where(Customer.name == customer_name)).first():
            continue
        
        customer = Customer(name=customer_name)
        session.add(customer)
        session.flush()
        
        invoice = Invoice(customer_id=customer.id)
        session.add(invoice)
        session.flush()
        
        for play in random.sample(all_plays, random.randint(2, 4)):
            session.add(Performance(invoice_id=invoice.id, play_id=play.id, audience=random.randint(20, 80)))
        
        print(f"Added customer: {customer_name}")
    
    session.commit()

print("Done!")
