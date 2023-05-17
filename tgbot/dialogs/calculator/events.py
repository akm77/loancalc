from aiogram.types import Message
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ManagedCounterAdapter

from . import states
from ...config import Settings
from ...utils.decimals import check_digit_value, format_decimal


async def on_amount_changed(event: ChatEvent, widget: ManagedCounterAdapter, manager: DialogManager):
    ctx = manager.current_context()
    amount = widget.get_value()
    ctx.dialog_data.update(amount=amount)


async def on_loan_period_changed(event: ChatEvent, widget: ManagedCounterAdapter, manager: DialogManager):
    ctx = manager.current_context()
    loan_period = widget.get_value()
    ctx.dialog_data.update(loan_period=loan_period)


async def on_interest_rate_changed(event: ChatEvent, widget: ManagedCounterAdapter, manager: DialogManager):
    ctx = manager.current_context()
    interest_rate = widget.get_value()
    ctx.dialog_data.update(interest_rate=interest_rate)


async def on_enter_amount(message: Message, message_input: MessageInput,
                          manager: DialogManager):
    ctx = manager.current_context()
    config: Settings = manager.middleware_data.get("config")
    try:
        amount = check_digit_value(message.text, type_factory=int,
                                   min_value=config.min_amount, max_value=config.max_amount)
        ctx.dialog_data.update(amount=amount)
    except ValueError:
        await message.answer(f"Ошибка ввода {message.text}, необходимо целое число в диапазоне  \n"
                             f"от {format_decimal(config.min_amount, delimiter=' ', pre=2)} "
                             f"до {format_decimal(config.max_amount, delimiter=' ', pre=2)}")
        return
    await manager.switch_to(states.CalculatorStates.enter_data)
