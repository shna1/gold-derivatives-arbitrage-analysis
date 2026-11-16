from __future__ import annotations

import numpy as np
import pandas as pd

from .models import MarketSnapshot


def terminal_scenarios(snapshot: MarketSnapshot, moves=None) -> pd.DataFrame:
    snapshot.validate()
    moves = np.asarray(moves if moves is not None else [-0.20, -0.10, 0.0, 0.10, 0.20, 0.30], dtype=float)
    futures_notional = snapshot.futures_price * snapshot.contract_multiplier
    rows = []
    for move in moves:
        fund_return = move - snapshot.round_trip_cost_rate
        certificate_return = move - snapshot.round_trip_cost_rate
        futures_pnl = futures_notional * move - futures_notional * snapshot.round_trip_cost_rate
        rows.extend([
            {"terminal_move": move, "instrument": "gold_fund", "return_on_capital": fund_return, "profit_loss": snapshot.fund_price * fund_return},
            {"terminal_move": move, "instrument": "bullion_certificate", "return_on_capital": certificate_return, "profit_loss": snapshot.certificate_price / snapshot.certificate_units_per_gram * certificate_return},
            {"terminal_move": move, "instrument": "gold_futures", "return_on_capital": futures_pnl / snapshot.initial_margin, "profit_loss": futures_pnl},
        ])
    return pd.DataFrame(rows)
