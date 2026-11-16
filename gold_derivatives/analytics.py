from __future__ import annotations

import pandas as pd

from .models import MarketSnapshot


def instrument_comparison(snapshot: MarketSnapshot) -> pd.DataFrame:
    snapshot.validate()
    notional = snapshot.futures_price * snapshot.contract_multiplier
    certificate_unit_price = snapshot.certificate_price / snapshot.certificate_units_per_gram
    rows = [
        {"instrument": "gold_fund", "quoted_price": snapshot.fund_price, "capital_required": snapshot.fund_price * snapshot.contract_multiplier, "reference_value": snapshot.fund_nav, "premium_discount": snapshot.fund_price / snapshot.fund_nav - 1, "leverage": 1.0},
        {"instrument": "bullion_certificate", "quoted_price": certificate_unit_price, "capital_required": notional, "reference_value": certificate_unit_price, "premium_discount": 0.0, "leverage": 1.0},
        {"instrument": "gold_futures", "quoted_price": snapshot.futures_price, "capital_required": snapshot.initial_margin, "reference_value": snapshot.fund_price, "premium_discount": snapshot.futures_price / snapshot.fund_price - 1, "leverage": notional / snapshot.initial_margin},
    ]
    return pd.DataFrame(rows).set_index("instrument")


def futures_basis(snapshot: MarketSnapshot) -> dict[str, float]:
    snapshot.validate()
    simple_basis = snapshot.futures_price / snapshot.fund_price - 1
    annualized_basis = (1 + simple_basis) ** (365 / snapshot.days_to_maturity) - 1
    return {"simple_basis": simple_basis, "annualized_basis": annualized_basis}


def cash_and_carry(snapshot: MarketSnapshot) -> dict[str, float]:
    snapshot.validate()
    spot_cost = snapshot.fund_price * snapshot.contract_multiplier
    futures_proceeds = snapshot.futures_price * snapshot.contract_multiplier
    funding_cost = spot_cost * snapshot.annual_funding_rate * snapshot.days_to_maturity / 365
    transaction_cost = (spot_cost + futures_proceeds) * snapshot.round_trip_cost_rate
    gross_spread = futures_proceeds - spot_cost
    net_spread = gross_spread - funding_cost - transaction_cost
    return {
        "spot_capital": spot_cost,
        "futures_notional": futures_proceeds,
        "gross_spread": gross_spread,
        "funding_cost": funding_cost,
        "transaction_cost": transaction_cost,
        "net_spread_before_execution_risk": net_spread,
        "net_return_on_spot_capital": net_spread / spot_cost,
    }
