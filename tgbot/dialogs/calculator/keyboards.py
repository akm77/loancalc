import operator

from aiogram import F
from aiogram_dialog.widgets.kbd import Row, Radio, Group, Button, SwitchTo, Cancel, Counter
from aiogram_dialog.widgets.text import Format, Const

from . import constants, events, states, onclick, whenable


def enter_price(**defaults):
    return Group(
        SwitchTo(Const("✍️ Сумма"),
                 id=constants.CalculatorForm.ENTER_AMOUNT,
                 state=states.CalculatorStates.enter_amount),
        Counter(
            id=constants.CalculatorForm.AMOUNT_COUNTER,
            text=Format("{value:d}"),
            min_value=defaults.get("min_amount"),
            max_value=defaults.get("max_amount"),
            increment=defaults.get("amount_step"),
            default=defaults.get("default_amount"),
            cycle=True,
            on_value_changed=events.on_amount_changed
        ),
        Counter(
            id=constants.CalculatorForm.LOAN_MONTH_COUNTER,
            text=Format("{value:g} м"),
            min_value=12,
            max_value=60,
            increment=12,
            default=12,
            cycle=True,
            on_value_changed=events.on_loan_period_changed,
        ),
        Counter(
            id=constants.CalculatorForm.INTEREST_RATE_COUNTER,
            text=Format("{value:g} %"),
            min_value=0,
            max_value=100,
            increment=1,
            default=50,
            cycle=True,
            on_value_changed=events.on_interest_rate_changed,
            when=whenable.is_admin
        ),
        Cancel(Const("<<"),
               on_click=onclick.on_click_exit)
    )

