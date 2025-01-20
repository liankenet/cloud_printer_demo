import unittest
from lianke_printing.api import LiankePrinting


class LiankePrintingTestCase(unittest.TestCase):
    lk = LiankePrinting("123", "123", "11123")

    def test_printer_enum(self):
        result = self.lk.printer_enum()
        assert result["code"] == 200

    def test_printer_list(self):
        result = self.lk.printer_list()
        assert result["code"] == 200
