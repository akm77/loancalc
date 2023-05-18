from tempfile import NamedTemporaryFile

from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

EMPTY_ROW = [""]


class PaymentSchedule:
    def __init__(self, data):
        self.data = data
        self.wb = None
        self.ws: Worksheet | None = None

    def _create_workbook(self):
        self.wb = Workbook()
        self.ws = self.wb.active

    def _fill_worksheet(self):
        _ = [self.ws.append(row) for row in self.data]

    def get_workbook(self):
        self._create_workbook()
        self._fill_worksheet()
        with NamedTemporaryFile() as tmp:
            self.wb.save(tmp.name)
            tmp.seek(0)
            stream = tmp.read()
        return stream
