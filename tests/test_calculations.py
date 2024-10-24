import pytest
from app.calculations import add, BankAccount

@pytest.mark.parametrize("num1, num2, expected", [(1, 2, 3), (0, 0, 0)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected



def test_bank_account():
    account = BankAccount(100)
    assert account.get_balance() == 100