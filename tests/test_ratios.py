
from src.finance.ratios import (
    revenue_growth,
    net_profit_margin,
    debt_to_equity,
    cash_flow_to_net_profit,
)


def test_revenue_growth():
    assert revenue_growth(120, 100) == 20


def test_net_profit_margin():
    assert net_profit_margin(15, 100) == 15


def test_debt_to_equity():
    assert debt_to_equity(200, 400) == 0.5


def test_cash_flow_to_net_profit():
    assert cash_flow_to_net_profit(120, 100) == 1.2


def test_zero_revenue():
    assert net_profit_margin(10, 0) is None

