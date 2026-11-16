from __future__ import annotations

import argparse
import json
from pathlib import Path

from gold_derivatives.models import MarketSnapshot
from gold_derivatives.report import build_report


def main():
    parser = argparse.ArgumentParser(description="Compare gold funds, certificates and futures under explicit scenarios.")
    parser.add_argument("--input", type=Path, help="Optional JSON market snapshot.")
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    values = json.loads(args.input.read_text()) if args.input else {}
    snapshot = MarketSnapshot(**values)
    comparison, basis, arbitrage, _ = build_report(snapshot, args.output)
    print("\nInstrument comparison\n", comparison.round(4).to_string())
    print("\nFutures basis\n", json.dumps(basis, indent=2))
    print("\nCash-and-carry scenario\n", json.dumps(arbitrage, indent=2))
    print(f"\nOutputs written to {args.output.resolve()}")


if __name__ == "__main__":
    main()
