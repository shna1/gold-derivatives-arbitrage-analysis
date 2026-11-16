import unittest

from gold_derivatives.models import MarketSnapshot
from gold_derivatives.scenarios import terminal_scenarios


class ScenarioTests(unittest.TestCase):
    def test_futures_has_greater_return_sensitivity(self):
        frame = terminal_scenarios(MarketSnapshot(), moves=[0.10])
        fund = frame.loc[frame.instrument == "gold_fund", "return_on_capital"].iloc[0]
        futures = frame.loc[frame.instrument == "gold_futures", "return_on_capital"].iloc[0]
        self.assertGreater(futures, fund)

    def test_three_instruments_per_move(self):
        self.assertEqual(len(terminal_scenarios(MarketSnapshot(), moves=[-0.1, 0, 0.1])), 9)


if __name__ == "__main__":
    unittest.main()
