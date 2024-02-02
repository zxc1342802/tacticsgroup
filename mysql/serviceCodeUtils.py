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
    #
    # # 提取 sub_service_code 并转为列表
    sub_service_codes = [row[0] for row in result]
    for sub_service_code in sub_service_codes:
        # 查询 weight
        select_query = f"SELECT id  FROM checkout_record WHERE opay_service_code = '{sub_service_code}' and step='success' ORDER BY id DESC LIMIT 1"
        cursor.execute(select_query)
        result = cursor.fetchone()
        print(f"Updated weight for sub_service_code {sub_service_code}")
       
        if result:
            # 存在记录，更新 weight
            update_query = f"UPDATE checkout_record SET support_channel='mockPaymentChannel' WHERE id='{result}'"
            cursor.execute(update_query)
            conn.commit()
            print(f"Updated weight for sub_service_code {sub_service_code} and support_channel mockPaymentChannel")

    cursor.close()
    conn.close()
    print("Database connection closed")

except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)