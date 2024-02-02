import mysql.connector
import tkinter as tk
from tkinter import messagebox
import sys

# 数据库连接配置
config = {
    'host': '182.160.17.58',
    'user': 'root',
    'password': 'Admin172.16.22.231',
    'database': 'opay_egypt'
}

# 创建窗口
window = tk.Tk()

# 设置窗口标题
window.title("输入sub_service_codes")

# 创建标签和输入框
label = tk.Label(window, text="请输入sub_service_codes（用空格分隔）:")
label.pack()

entry = tk.Entry(window)
entry.pack()


# 定义按钮点击事件
def update_database():
    sub_service_codes = entry.get().split()

    # 禁用按钮和输入框
    button.config(state=tk.DISABLED)
    entry.config(state=tk.DISABLED)

    # 连接数据库和操作...
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 执行数据库操作
        for sub_service_code in sub_service_codes:
            # 更新 weight
            update_query = f"UPDATE router_selector SET weight=0 WHERE sub_service_code='{sub_service_code}'"
            cursor.execute(update_query)
            conn.commit()
            print(f"Updated weight for sub_service_code {sub_service_code}")

            # 检查是否存在记录
            select_query = f"SELECT * FROM router_selector WHERE sub_service_code='{sub_service_code}' AND support_channel='mockPaymentChannel'"
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

        messagebox.showinfo("操作完成", "数据库已更新")

    except mysql.connector.Error as err:
        messagebox.showerror("操作失败", str(err))

    finally:
        # 启用按钮和输入框
        button.config(state=tk.NORMAL)
        entry.config(state=tk.NORMAL)

        if cursor:
            cursor.close()
        if conn:
            conn.close()


# 创建按钮
button = tk.Button(window, text="更新数据库", command=update_database)
button.pack()

# 运行窗口主循环
window.mainloop()