import os
import polars as pl

class TextRender:
    def text_report_as_statements_render(self, df: pl.DataFrame) -> str:
        lines = []
        play_cols = [c for c in df.columns if c.startswith("amount_")]
        plays = [c.replace("amount_", "") for c in play_cols]

        for row in df.iter_rows(named=True):
            lines.append(f"Statement for {row['customer']}")
            
            for play in plays:
                amount = row[f"amount_{play}"]
                audience = row[f"audience_{play}"]
                if audience > 0:
                    lines.append(f"  {play}: {self._format_currency(amount)} ({audience} seats)")
            
            lines.append(f"Amount owed is {self._format_currency(row['total_amount'])}")
            lines.append(f"You earned {row['total_credits']} credits")
            lines.append("")
        
        return os.linesep.join(lines)

    def _format_currency(self, amount: int) -> str:
        return "${:,.2f}".format(amount / 100)