class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError
        else:
            self.__balance -= amount

    def __repr__(self):
        return f'BankAccount(owner={self.owner!r}, balance={self.__balance})'


if __name__ == '__main__':
    bank_anna = BankAccount('Anna', 150)
    bank_boris = BankAccount('Boris', 100)

    # операции с одним счётом не влияют на другой
    bank_anna.deposit(50)
    assert bank_anna.balance == 200
    assert bank_boris.balance == 100

    bank_boris.withdraw(30)
    assert bank_boris.balance == 70
    assert bank_anna.balance == 200

    # deposit через точку и через класс — эквивалентны
    bank_boris.deposit(100)
    assert bank_boris.balance == 170

    BankAccount.deposit(bank_anna, 100)
    assert bank_anna.balance == 300

    # withdraw при недостатке средств бросает ValueError
    try:
        bank_boris.withdraw(10_000)
        assert False, 'ожидался ValueError'
    except ValueError:
        pass

    assert repr(bank_anna) == "BankAccount(owner='Anna', balance=300)"

    # __balance — приватный через name mangling, напрямую снаружи недоступен
    try:
        bank_anna.__balance
        assert False, 'ожидался AttributeError'
    except AttributeError:
        pass

    # но доступен через переименованное имя (mangling, а не защита доступа)
    assert bank_anna._BankAccount__balance == 300

    print('OK')