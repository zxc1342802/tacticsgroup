import json

# 提供的数据
data = '[{"Id":"51","Price":"5","Val":"5.2"},{"Id":"53","Price":"10","Val":"10.2"},{"Id":"53","Price":"13.5","Val":"13.52"},{"Id":"54","Price":"15","Val":"15.2"},{"Id":"55","Price":"25","Val":"25.2"},{"Id":"55","Price":"30","Val":"30.2"},{"Id":"55","Price":"50","Val":"50.2"}]'

parsed_data = json.loads(data)
max_num = float('-inf')  # 初始化最大值为负无穷小

for item in parsed_data:
    num = int(item['Id'])
    max_num = max(max_num, num)

print("当前最大值是:", max_num)