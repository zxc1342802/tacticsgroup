import pandas as pd
import pymysql
import math

# 连接到MySQL数据库
connection = pymysql.connect(
    host='101.132.157.104',
    user='zkgj_platform',
    password='nNEGYy3KxK5XRch2',
    database='zkgj_platform'
)

# 读取Excel文件
df = pd.read_excel('/Users/leijm/Downloads/sssss1123123.xlsx')

# 遍历每行数据
for index, row in df.iterrows():
    key = row.iloc[0]  # 第一列作为key
    values = row.iloc[1:]  # 后面的列作为values
    for value in values:
        if pd.isna(value):
            # value是NaN
            print("Value is NaN")
            continue
        # 构建SQL语句
        sql = """
        INSERT INTO `zkgj_platform`.`cy_qalibrary` (`user_id`, `special_device`, `category`,`qa_type`, `question`, `answer`, `status`, `dept_id`, `create_time`, `updater`, 
        `update_time`, `deleted`, `tenant_id`, `creator`) 
        VALUES ( 124, '0', '0', '0', '{}', '{}', '0', 113, SYSDATE(), '124', SYSDATE(), b'0', 0, '124');
        """.format(key, value)

        # 执行SQL语句
        with connection.cursor() as cursor:
            cursor.execute(sql)

        # 提交事务
        connection.commit()

# 关闭数据库连接
connection.close()