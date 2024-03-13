import mysql.connector
import sys

# 数据库连接配置
config = {
    'host': '182.160.17.58',
    'user': 'root',
    'password': 'Admin172.16.22.231',
    'database': 'opay_egypt'
}

# 连接数据库
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # 给定的 sub_service_code
    # sub_service_codes = ['GovernmentBookFair']
    # sub_service_codes = sys.argv[1:]

    # 查询 sub_service_code
    select_query = "SELECT sub_service_code from opay_service_config WHERE opay_service_code in( SELECT opay_service_code from recharge_payment_service_category WHERE business_type in ('OnlineService' ))"
    cursor.execute(select_query)
    result = cursor.fetchall()
    print(result)

except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)