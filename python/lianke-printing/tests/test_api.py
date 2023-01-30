from lianke_printing.api import LiankePrinting


def test_printer_enum():
    lk = LiankePrinting("123", "123", "11123")
    result = lk.printer_enum()
    assert result["code"] == 200
