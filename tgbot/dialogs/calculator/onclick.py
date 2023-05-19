import logging

from aiogram import Bot
from aiogram.types import CallbackQuery, InputFile, FSInputFile, BufferedInputFile
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from tgbot.config import Settings
from tgbot.services.excel_library import PaymentSchedule, LoanCondition
from tgbot.utils.calculation import cost_calculation, annuity_payment
from tgbot.utils.decimals import format_decimal

logger = logging.getLogger(__name__)

PROPOSAL = """\
Сумма лизинга - <b>{amount_string}</b> {currency}
Срок лизинга (мес) - <b>{loan_period}</b>{interest_rate_repr}
Ежемесячный платеж - <b>{monthly_fee}</b> {currency}
<pre>--------------------------------</pre>
<pre>{payment_schedule}</pre>
"""


async def on_click_calculate(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.show_mode = ShowMode.SEND
    dialog_data = manager.current_context().dialog_data
    config: Settings = manager.middleware_data.get("config")
    session = manager.middleware_data.get('db_session')
    cost_calculation_text = await cost_calculation(config=config,
                                                   db_session=session,
                                                   data=dialog_data,
                                                   manager=manager)
    dialog_data.update(cost_calculation_text=cost_calculation_text)


async def on_click_exit(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.show_mode = ShowMode.SEND
    dialog_data = manager.current_context().dialog_data

    loan_period = int(dialog_data.get("loan_period"))
    interest_rate = int(dialog_data.get("interest_rate"))
    balance = int(dialog_data.get("amount"))
    dialog_data["amount_string"] = format_decimal(balance, delimiter=' ', pre=2)

    monthly_fee = annuity_payment(balance, interest_rate, loan_period)
    condition = LoanCondition(amount=balance,
                              loan_period=loan_period,
                              monthly_fee=monthly_fee,
                              interest_rate=interest_rate if dialog_data.get("interest_rate_repr") else None)
    data = []
    payment_schedule = []
    for i in range(1, loan_period + 1):
        interest = balance * interest_rate / (12 * 100)
        debt = monthly_fee - interest
        balance -= debt
        data.append([i, balance, debt, interest, monthly_fee])
        payment_schedule.append(f"{i:>2}. "
                                f"{format_decimal(balance, delimiter=' ', pre=2):>12} "
                                f"{format_decimal(debt, delimiter=' ', pre=2):>12} "
                                f"{format_decimal(interest, delimiter=' ', pre=2):>12}")
    dialog_data["payment_schedule"] = "\n".join(payment_schedule)
    xl = PaymentSchedule(condition, data).get_workbook()
    await callback.message.edit_text(PROPOSAL.format_map(dialog_data))
    await callback.message.answer_document(
        BufferedInputFile(xl,
                          f"Расчет {dialog_data['amount_string']} {dialog_data['currency']} на {loan_period} м.xlsx"))

