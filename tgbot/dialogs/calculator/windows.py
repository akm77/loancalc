from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format

from . import states, getters, keyboards

CALC_FORM = """\
Расчет для: {started_by}
<pre>------------------------------------</pre>

Сумма лизинга - <b>{amount}</b> AED
Срок лизинга (мес) - <b>{loan_period}</b>
Процентная ставка - <b>{interest_rate} %</b>
Ежемесячный платеж - <b>{monthly_fee}</b> AED
<pre>------------------------------------</pre>
"""


def calculator_window(**defaults):
    return Window(Format(CALC_FORM),
                  keyboards.enter_price(**defaults),
                  state=states.CalculatorStates.enter_data,
                  getter=getters.calculator_form)


def calculator_input_window(text: str, handler=None, state=None, getter=None, **defaults):
    return Window(
        Format(text),
        MessageInput(handler,
                     content_types=[ContentType.TEXT]),
        state=state,
        getter=getter
    )
