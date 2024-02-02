principal = 100000
interest_rate = 0.1
target_amount = 100000000
months = 0

while principal < target_amount:
    principal *= (1 + interest_rate)
    months += 1

years = months // 12
remaining_months = months % 12

print(f"本金从10万增长到1个亿需要 {years} 年 {remaining_months} 个月")