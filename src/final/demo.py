from bank_account import BankAccount

print("=" * 50)
print("1. СОЗДАНИЕ КОРРЕКТНОГО СЧЁТА")
print("=" * 50)

acc = BankAccount("Ivanov", "40817", 1000.0)
print(str(acc))
print(repr(acc))
print(f"Всего счетов: {BankAccount.total_accounts}\n")

print("=" * 50)
print("2. DEPOSIT И WITHDRAW (УСПЕШНО)")
print("=" * 50)

print(f"Баланс до пополнения: {acc.balance}")
acc.deposit(500)
print(f"После deposit(500): {acc.balance}")

print(f"Снятие 300: {acc.withdraw(300)}")
print(f"Баланс после: {acc.balance}\n")

print("=" * 50)
print("3. WITHDRAW БОЛЬШЕ БАЛАНСА")
print("=" * 50)

print(f"Текущий баланс: {acc.balance}")
print(f"Попытка снять 5000: {acc.withdraw(5000)}")
print(f"Баланс не изменился: {acc.balance}\n")

print("=" * 50)
print("4. DEPOSIT С НЕКОРРЕКТНЫМИ СУММАМИ (ValueError)")
print("=" * 50)

try:
    acc.deposit(0)
except ValueError as e:
    print(f"deposit(0) → ValueError: {e}")

try:
    acc.deposit(-50)
except ValueError as e:
    print(f"deposit(-50) → ValueError: {e}")

try:
    acc.deposit("abc")
except TypeError as e:
    print(f"deposit('abc') → TypeError: {e}\n")

print("=" * 50)
print("5. CLOSE + ОПЕРАЦИИ НА ЗАКРЫТОМ СЧЁТЕ")
print("=" * 50)

acc.close()
print(f"Счёт закрыт: {acc.is_open}")

try:
    acc.deposit(100)
except ValueError as e:
    print(f"deposit(100) на закрытом → ValueError: {e}")

print(f"withdraw(10) на закрытом → {acc.withdraw(10)}")
print(f"Баланс остался: {acc.balance}\n")

print("=" * 50)
print("6. СЕТТЕР OWNER (КОРРЕКТНОЕ ОБНОВЛЕНИЕ)")
print("=" * 50)

acc.owner = "Petrov"
print(f"Новый владелец: {acc.owner}")
print(str(acc), "\n")

print("=" * 50)
print("7. СЕТТЕР OWNER (НЕКОРРЕКТНЫЙ)")
print("=" * 50)

try:
    acc.owner = ""
except ValueError as e:
    print(f"owner = '' → ValueError: {e}")

try:
    acc.owner = "   "
except ValueError as e:
    print(f"owner = '   ' → ValueError: {e}")

try:
    acc.owner = 123
except TypeError as e:
    print(f"owner = 123 → TypeError: {e}\n")

print("=" * 50)
print("8. ОШИБКИ СОЗДАНИЯ (try/except)")
print("=" * 50)

print("Попытка 1: пустой owner")
try:
    acc2 = BankAccount("", "12345", 100)
except ValueError as e:
    print(f"  → {e}")

print("Попытка 2: owner из пробелов")
try:
    acc2 = BankAccount("   ", "12345", 100)
except ValueError as e:
    print(f"  → {e}")

print("Попытка 3: пустой number")
try:
    acc2 = BankAccount("Ivanov", "", 100)
except ValueError as e:
    print(f"  → {e}")

print("Попытка 4: number из пробелов")
try:
    acc2 = BankAccount("Ivanov", "   ", 100)
except ValueError as e:
    print(f"  → {e}")

print("Попытка 5: отрицательный баланс")
try:
    acc2 = BankAccount("Ivanov", "12345", -50)
except ValueError as e:
    print(f"  → {e}")

print("Попытка 6: баланс строкой")
try:
    acc2 = BankAccount("Ivanov", "12345", "сто")
except TypeError as e:
    print(f"  → {e}")

print("\nВсего счетов создано:", BankAccount.total_accounts)