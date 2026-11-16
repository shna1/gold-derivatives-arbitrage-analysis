from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from .analytics import cash_and_carry, futures_basis, instrument_comparison
from .models import MarketSnapshot
from .scenarios import terminal_scenarios


COLORS = {"gold_fund": "#b08b2f", "bullion_certificate": "#53687e", "gold_futures": "#b85c38"}


def build_report(snapshot: MarketSnapshot, output_dir: str | Path):
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    comparison = instrument_comparison(snapshot)
    scenarios = terminal_scenarios(snapshot)
    comparison.to_csv(target / "instrument_comparison.csv")
    scenarios.to_csv(target / "terminal_scenarios.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), constrained_layout=True)
    fig.patch.set_facecolor("#f4f1ea")
    for ax in axes:
        ax.set_facecolor("#fbfaf7")
        ax.spines[["top", "right"]].set_visible(False)

    capital = comparison["capital_required"]
    axes[0].bar(capital.index, capital.values, color=[COLORS[name] for name in capital.index])
    axes[0].set_title("Capital for comparable notional exposure", loc="left", fontweight="bold")
    axes[0].set_ylabel("IRR — demonstration inputs")
    axes[0].tick_params(axis="x", rotation=15)

    for instrument, group in scenarios.groupby("instrument"):
        axes[1].plot(group["terminal_move"], group["return_on_capital"], marker="o", linewidth=2, label=instrument, color=COLORS[instrument])
    axes[1].axhline(0, color="#17202c", linewidth=.8)
    axes[1].set_title("Terminal return on committed capital", loc="left", fontweight="bold")
    axes[1].set_xlabel("Underlying terminal move")
    axes[1].set_ylabel("Return on capital")
    axes[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda value, _: f"{value:.0%}"))
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda value, _: f"{value:.0%}"))
    axes[1].legend(frameon=False)
    fig.suptitle("Gold Derivatives & Arbitrage Analysis — demonstration snapshot", x=.01, ha="left", fontsize=17, fontweight="bold")
    fig.savefig(target / "gold_scenarios.png", dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    return comparison, futures_basis(snapshot), cash_and_carry(snapshot), scenarios
