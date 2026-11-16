from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class MarketSnapshot:
    fund_price: float = 185_000
    fund_nav: float = 181_500
    certificate_price: float = 73_500_000
    certificate_units_per_gram: float = 1000
    futures_price: float = 196_000
    contract_multiplier: int = 1000
    initial_margin: float = 48_000_000
    days_to_maturity: int = 76
    round_trip_cost_rate: float = 0.003
    annual_funding_rate: float = 0.30

    def validate(self) -> None:
        positive = ("fund_price", "fund_nav", "certificate_price", "certificate_units_per_gram", "futures_price", "contract_multiplier", "initial_margin", "days_to_maturity")
        for field in positive:
            if getattr(self, field) <= 0:
                raise ValueError(f"{field} must be positive.")
        for field in ("round_trip_cost_rate", "annual_funding_rate"):
            if not 0 <= getattr(self, field) < 2:
                raise ValueError(f"{field} must be a decimal rate between 0 and 2.")

    def to_dict(self):
        return asdict(self)
