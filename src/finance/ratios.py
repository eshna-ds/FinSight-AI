
def revenue_growth(current, previous):
    if current is None or previous is None:
        return None

    if previous <= 0:
        return None

    return ((current - previous) / previous) * 100


def net_profit_margin(net_profit, revenue):
    if net_profit is None or revenue is None or revenue == 0:
        return None

    return (net_profit / revenue) * 100


def debt_to_equity(total_debt, total_equity):
    if total_debt is None or total_equity is None:
        return None

    if total_equity <= 0:
        return None

    return total_debt / total_equity


def cash_flow_to_net_profit(operating_cash_flow, net_profit):
    if operating_cash_flow is None or net_profit is None:
        return None

    if net_profit == 0:
        return None

    return operating_cash_flow / net_profit

