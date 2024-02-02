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
        # 更新 weight
        try:
            update_query = f"UPDATE router_selector SET weight=0 WHERE sub_service_code='{sub_service_code}'"
            cursor.execute(update_query)
            conn.commit()
            print(f"Updated weight for sub_service_code {sub_service_code}")
        except Exception as e:
            print(f"Failed to update weight for sub_service_code {sub_service_code}: {str(e)}")
        # 检查是否存在记录
        select_query = f"SELECT * FROM router_selector WHERE sub_service_code='{sub_service_code}' AND support_channel='mockPaymentChannel' limit 1"
        cursor.execute(select_query)
        result = cursor.fetchone()

        if result:
            # 存在记录，更新 weight
            update_query = f"UPDATE router_selector SET weight=100 WHERE sub_service_code='{sub_service_code}' AND support_channel='mockPaymentChannel'"
            cursor.execute(update_query)
            conn.commit()
            print(f"Updated weight for sub_service_code {sub_service_code} and support_channel mockPaymentChannel")
        else:
            # 不存在记录，插入新记录
            insert_query = f"INSERT INTO router_selector (sub_service_code, sub_service_name, support_channel, channel_context, sub_service_value, amount_list, weight, partner_id, partner_name, delete_flag, partial_payment_flag) VALUES ('{sub_service_code}', NULL, 'mockPaymentChannel', NULL, NULL, NULL, 100, '5123456893', 'test', 0, 'false')"
            cursor.execute(insert_query)
            conn.commit()
            print(f"Inserted new record for sub_service_code {sub_service_code}")

    cursor.close()
    conn.close()
    print("Database connection closed")

except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)