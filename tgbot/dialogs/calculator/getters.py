from aiogram_dialog import DialogManager

from tgbot.config import Settings
from . import constants
from ...utils.calculation import annuity_payment
from ...utils.decimals import format_decimal


async def calculator_form(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('db_session')
    config: Settings = middleware_data.get("config")
    ctx = dialog_manager.current_context()
    start_data = ctx.start_data
    dialog_data = ctx.dialog_data
    dialog_data["currency"] = config.currency

    amount = dialog_data.get("amount") or config.default_amount
    amount = int(amount)
    amount_kbd = dialog_manager.find(constants.CalculatorForm.AMOUNT_COUNTER)
    await amount_kbd.set_value(value=amount)

    started_by = start_data.get("started_by") or "UNKNOWN"
    if not (loan_period := dialog_data.get("loan_period")):
        dialog_data["loan_period"] = loan_period = 12

    if not (interest_rate := dialog_data.get("interest_rate")):
        dialog_data["interest_rate"] = interest_rate = 50

    interest_rate = int(interest_rate)
    loan_period = int(loan_period)

    admins = config.admins
    user = dialog_manager.middleware_data.get("event_from_user").id
    interest_rate_repr = ""
    if user in admins:
        interest_rate_repr = "\nПроцентная ставка - <b>{interest_rate} %</b>"
    dialog_data["interest_rate_repr"] = interest_rate_repr

    monthly_fee = annuity_payment(amount, interest_rate, loan_period)
    dialog_data["monthly_fee"] = format_decimal(monthly_fee, delimiter=" ", pre=2)

    admins = config.admins
    user = dialog_manager.middleware_data.get("event_from_user").id

    return {"started_by": started_by,
            "amount": format_decimal(amount, delimiter=" ", pre=1),
            "currency": config.currency,
            "loan_period": loan_period,
            "interest_rate_repr": interest_rate_repr,
            "monthly_fee": dialog_data["monthly_fee"]}
