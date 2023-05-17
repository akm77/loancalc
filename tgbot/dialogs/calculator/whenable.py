from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable


def is_admin(data: Dict, widget: Whenable, manager: DialogManager):
    admins = manager.middleware_data.get("config").admins
    user = manager.middleware_data.get("event_from_user").id
    return user in admins
