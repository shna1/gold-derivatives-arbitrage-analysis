import unittest

from gold_derivatives.analytics import cash_and_carry, futures_basis, instrument_comparison
from gold_derivatives.models import MarketSnapshot


class AnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = MarketSnapshot()

    def test_simple_basis(self):
        expected = self.snapshot.futures_price / self.snapshot.fund_price - 1
        self.assertAlmostEqual(futures_basis(self.snapshot)["simple_basis"], expected)

    def test_futures_leverage_uses_margin(self):
        table = instrument_comparison(self.snapshot)
        expected = self.snapshot.futures_price * self.snapshot.contract_multiplier / self.snapshot.initial_margin
        self.assertAlmostEqual(table.loc["gold_futures", "leverage"], expected)

    def test_costs_reduce_cash_and_carry_spread(self):
        result = cash_and_carry(self.snapshot)
        self.assertLess(result["net_spread_before_execution_risk"], result["gross_spread"])

    def test_invalid_maturity_fails(self):
        with self.assertRaisesRegex(ValueError, "days_to_maturity"):
            MarketSnapshot(days_to_maturity=0).validate()


if __name__ == "__main__":
    unittest.main()
