def add(num1: int, num2: int) -> int:
    return num1 + num2

class BankAccount:
    def __init__(self, balance: int):
        self.balance = balance

    def deposit(self, amount: int):
        self.balance += amount

    def withdraw(self, amount: int):
        self.balance -= amount
    


    def get_balance(self):
        return self.balance