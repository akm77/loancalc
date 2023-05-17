from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Jinja
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgbot.config import Settings

from tgbot.utils.decimals import value_to_decimal, format_decimal


def formatvalue(value: Decimal) -> str:
    return format_decimal(value, pre=2)


def get_message_text() -> str:
    minus_delimiter = f"<pre>{'-' * 30}</pre>\n"
    equal_delimiter = f"<pre>{'=' * 30}</pre>\n"
    return """\
    
"""


async def cost_calculation(config: Settings, db_session: async_sessionmaker,
                           data: dict, manager: DialogManager) -> Optional[str]:
    calculation_values = dict()
    return await Jinja(get_message_text()).render_text(calculation_values, manager)


def annuity_payment(amount, interest_rate, loan_period):
    return (amount * interest_rate / (12 * 100)) / (1 - pow(1 + interest_rate / (12 * 100), -loan_period))
