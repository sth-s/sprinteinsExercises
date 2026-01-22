from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class PlayType(SQLModel, table=True):
    __tablename__ = "play_types"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    
    plays: List["Play"] = Relationship(back_populates="type")

class Play(SQLModel, table=True):
    __tablename__ = "plays"
    id: str = Field(primary_key=True)
    name: str
    type_id: int = Field(foreign_key="play_types.id")
    
    type: PlayType = Relationship(back_populates="plays")
    performances: List["Performance"] = Relationship(back_populates="play")

class Customer(SQLModel, table=True):
    __tablename__ = "customers"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    
    invoices: List["Invoice"] = Relationship(back_populates="customer")

class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id")
    
    customer: Customer = Relationship(back_populates="invoices")
    performances: List["Performance"] = Relationship(back_populates="invoice")

class Performance(SQLModel, table=True):
    __tablename__ = "performances"
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoices.id")
    play_id: str = Field(foreign_key="plays.id")
    audience: int
    
    invoice: Invoice = Relationship(back_populates="performances")
    play: Play = Relationship(back_populates="performances")
