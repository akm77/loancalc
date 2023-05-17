from dataclasses import dataclass


@dataclass
class Element:
    code: str
    name: str


PERIODS = {"12": Element(code="12", name="12 месяцев"),
           "24": Element(code="24", name="24 месяца")}

MARKETS = {"local_market": Element(code="local_market", name="Местный рынок"),
           "foreign_market": Element(code="foreign_market", name="Импорт")}


def get_periods():
    return PERIODS.values()


def get_period(period: str):
    return PERIODS.get(period)


def get_markets():
    return MARKETS.values()


def get_market(market: str):
    return MARKETS.get(market)
