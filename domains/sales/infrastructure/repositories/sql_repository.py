import json
import logging
from pathlib import Path
from typing import Dict, List
from sqlmodel import select, Session
from sqlalchemy.orm import selectinload
from sqlalchemy.future import Engine

from domains.sales.infrastructure.repositories.repository_interface import RepositoryInterface
from domains.sales.infrastructure.repositories.orm_models import Invoice as DBInvoice, Play as DBPlay, Performance as DBPerformance

from domains.sales.models.invoice import Invoice as DomainInvoice, Performance as DomainPerformance
from domains.sales.models.play import Play as DomainPlay

class SQLRepository(RepositoryInterface):
    def __init__(self, engine: Engine, data_dir: Path):
        self.engine = engine
        self.data_dir = data_dir

    def get_invoices(self) -> List[DomainInvoice]:
        with Session(self.engine) as session:
            invoices_stmt = select(DBInvoice).options(
                selectinload(DBInvoice.customer),
                selectinload(DBInvoice.performances).selectinload(DBPerformance.play)
            )
            db_invoices = session.exec(invoices_stmt).all()
            
        domain_invoices = []
        for db_invoice in db_invoices:
            performances = [
                DomainPerformance(
                    play_id=perf.play_id, 
                    audience=perf.audience
                )
                for perf in db_invoice.performances
            ]
                
            domain_invoices.append(
                DomainInvoice(
                    customer=db_invoice.customer.name, 
                    performances=performances
                )
            )
            
        return domain_invoices

    def get_plays_dict(self) -> Dict[str, DomainPlay]:
        with Session(self.engine) as session:
            plays_stmt = select(DBPlay).options(selectinload(DBPlay.type))
            db_plays = session.exec(plays_stmt).all()
            
        return {
            play.id: DomainPlay(
                    play_id=play.id, 
                    name=play.name, 
                    type=play.type.name
                )
                for play in db_plays
            }

    def save_report(self, report: str, output_file: Path):
        try:
            file_path = self.data_dir / output_file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(report, encoding='utf-8')
        except Exception as e:
            logging.error(f"Error writing report: {e}")
            raise

    def add_invoice(self, customer: str, performances: List[dict]) -> int:
        from domains.sales.infrastructure.repositories.orm_models import Customer
        
        with Session(self.engine) as session:
            db_customer = session.exec(
                select(Customer).where(Customer.name == customer)
            ).first()
            
            if not db_customer:
                db_customer = Customer(name=customer)
                session.add(db_customer)
                session.flush()
            
            invoice = DBInvoice(customer_id=db_customer.id)
            session.add(invoice)
            session.flush()
            
            for perf in performances:
                db_perf = DBPerformance(
                    invoice_id=invoice.id,
                    play_id=perf["play_id"],
                    audience=perf["audience"]
                )
                session.add(db_perf)
            
            session.commit()
            return invoice.id
