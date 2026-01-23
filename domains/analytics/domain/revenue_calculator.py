import polars as pl
from domains.analytics.domain.calculators.factory import CalculatorFactory


class RevenueCalculator:    
    def calculate(self, df: pl.DataFrame, all_plays: pl.DataFrame) -> pl.DataFrame:
        if df.is_empty():
            return df
        
        df_calculated = self._apply_calculators(df)
        pivoted = self._pivot_by_plays(df_calculated, all_plays)
        return self._add_totals(pivoted)
    
    def _apply_calculators(self, df: pl.DataFrame) -> pl.DataFrame:
        calculators = CalculatorFactory.get_all()
        
        first = True
        amount_chain = None
        credits_chain = None
        
        for play_type, calc in calculators.items():
            audience = pl.col("audience")
            condition = pl.col("play_type") == play_type
            
            if first:
                amount_chain = pl.when(condition).then(calc.calculate_amount(audience))
                credits_chain = pl.when(condition).then(calc.calculate_credits(audience))
                first = False
            else:
                amount_chain = amount_chain.when(condition).then(calc.calculate_amount(audience))
                credits_chain = credits_chain.when(condition).then(calc.calculate_credits(audience))
        
        if amount_chain is None:
            return df
        
        return df.with_columns([
            amount_chain.otherwise(0).alias("amount"),
            credits_chain.otherwise(0).alias("credits")
        ])
    
    def _pivot_by_plays(self, df: pl.DataFrame, all_plays: pl.DataFrame) -> pl.DataFrame:
        pivoted = df.pivot(
            on="play_name",
            index="customer",
            values=["amount", "audience", "credits"],
            aggregate_function="sum"
        )
        
        for play in all_plays["play_name"]:
            for metric in ["amount", "audience", "credits"]:
                col_name = f"{metric}_{play}"
                if col_name not in pivoted.columns:
                    pivoted = pivoted.with_columns(pl.lit(0).alias(col_name))
        
        return pivoted.fill_null(0)
    
    def _add_totals(self, df: pl.DataFrame) -> pl.DataFrame:
        amount_cols = [c for c in df.columns if c.startswith("amount_")]
        credits_cols = [c for c in df.columns if c.startswith("credits_")]
        audience_cols = [c for c in df.columns if c.startswith("audience_")]
        
        df = df.with_columns([
            pl.sum_horizontal(amount_cols).alias("total_amount"),
            pl.sum_horizontal(credits_cols).alias("total_credits"),
            pl.sum_horizontal(audience_cols).alias("total_audience"),
        ])
        
        play_cols = sorted([c for c in df.columns if c not in ["customer", "total_amount", "total_credits", "total_audience"]])
        return df.select(["customer", "total_amount", "total_credits", "total_audience"] + play_cols)
