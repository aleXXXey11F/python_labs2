def digital_root(n):
    while n >= 10:                # пока не одна цифра
        s = 0
        while n > 0:              # суммируем цифры
            s += n % 10
            n //= 10
        n = s
    return n