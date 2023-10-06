"""
This part is integer calculation, you can easily
calculate it using functions. For example, getting
the factor of a number, judging whether a number
is a perfect number, I wish you a happy use.

Thank you very much for using hyc library, I'll
make it even better for you!
"""


# 找一个数所有的因数
def find_factors(num: int) -> [int, int]:
    return [i for i in range(num + 1) if i % num == 0]


# 判断一个数是否为质数
def prime_num(num: int) -> bool:
    return len(find_factors(num)) == 2


# （最大）公因数
def gcd(num_list: [int, int]) -> ([int, int], int):
    cd = []
    for i in find_factors(num_list[0]):
        common = True
        for j in num_list:
            if not i in find_factors(j):
                common = False
        if common:
            cd.append(i)
    return cd, max(cd)


# 注意：本函数会返回两个值：两个数的公因数和最大公因数；请在该函数的参数内传入一个包含两个或以上数字的列表！

# （最小）公倍数
def lcm(num_list: [int, int]) -> int:
    i = 1
    common = False
    while not common:
        common = True
        now_num = num_list[0] * i
        for j in num_list:
            if not now_num % j == 0:
                common = False
        i += 1
    return now_num


# 注意：请在该函数的参数内传入一个包含两个或以上数字的列表！

# 分解质因数
def prime_factorization(num: int) -> str:
    prime_factors = []
    now_num = num
    while not prime_num(now_num):
        prime_factor = find_factors(now_num)[1]
        now_num = int(now_num / prime_factor)
        prime_factors.append(str(prime_factor))
    if prime_factors:
        text = f"{num} = {' * '.join(prime_factors)} * {now_num}"
        ' * '.join(prime_factors)
    else:
        text = f'{num} = {num}'
    return text


# 互质数
def coprime(num_list: [int, int]) -> bool:
    return len(gcd(num_list)) == 1
