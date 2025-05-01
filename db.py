from dotenv import load_dotenv
import os
from mysql.connector import pooling
import sqlite3

load_dotenv()



def init_db_pool(app):
    # 初始化資料庫連線池
    if app.config['DB_TYPE'] == "sqlite":
        sql_name = os.getenv("SQLLITE_INIT_FILE")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sql_path = os.path.join(script_dir, sql_name)

        conn = sqlite3.connect(os.getenv("SQLITE_DB_PATH"))
        cursor = conn.cursor()

        # 讀取並執行 SQL 指令
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        cursor.executescript(sql_script)  # ✅ 可以一次執行多條 SQL 指令
        conn.commit()

        # 確認是否建立成功
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for row in cursor.fetchall():
            print(row)

        cursor.close()
        
        app.db_pool = conn
        
    elif app.config['DB_TYPE'] == "mysql":
        dbconfig = {
            'host': os.getenv("MYSQL_HOST"),
            'user': os.getenv("MYSQL_USER"),
            'password': os.getenv("MYSQL_PASSWORD"),
            'database': os.getenv("MYSQL_DATABASE"),
        }
        
        pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=app.config['DB_POOLSIZE'],
            **dbconfig
        )

        # 將資料庫連線池儲存在 current_app 中
        app.db_pool = pool