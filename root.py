def digital_root(n):
    while n >= 10:                # пока не одна цифра
        s = 0
        while n > 0:              # суммируем цифры
            s += n % 10
            n //= 10
        n = s
    return n

print(digital_root(942))
print(digital_root(38))
print(digital_root(5))
print(digital_root(0))