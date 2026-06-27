class BankAccount:
    total_accounts = 0
    
    def __init__(self, owner, number, balance=0.0):
        self._owner = None
        self._number = None
        self._balance = None
        self._is_open = True
        
        self.owner = owner
        self.number = number
        self.balance = balance
        
        BankAccount.total_accounts += 1
    
    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value):
        if not isinstance(value, str):
            raise TypeError("Owner must be a string")
        if not value.strip():
            raise ValueError("Owner cannot be empty or whitespace")
        self._owner = value.strip()
    
    @property
    def number(self):
        return self._number
    
    @number.setter
    def number(self, value):
        if not isinstance(value, str):
            raise TypeError("Number must be a string")
        if not value.strip():
            raise ValueError("Number cannot be empty or whitespace")
        self._number = value.strip()
    
    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Balance must be a number")
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = float(value)
    
    @property
    def is_open(self):
        return self._is_open
    
    def deposit(self, amount):
        if not self._is_open:
            raise ValueError("Cannot deposit to a closed account")
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a number")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        return self._balance
    
    def withdraw(self, amount):
        if not self._is_open:
            return False
        if not isinstance(amount, (int, float)):
            return False
        if amount <= 0 or amount > self._balance:
            return False
        self._balance -= amount
        return True
    
    def close(self):
        self._is_open = False
    
    def __str__(self):
        return f"{self._owner} [#{self._number}] — баланс {self._balance:.2f}"
    
    def __repr__(self):
        return (f"BankAccount(owner='{self._owner}', "
                f"number='{self._number}', "
                f"balance={self._balance})")