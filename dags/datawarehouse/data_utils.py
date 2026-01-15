from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor

def get_conn_cursor():
    # ساخت یک هوک برای اتصال به دیتابیس
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt", database="elt_db")
    conn = hook.get_conn() # ایجاد اتصال
    cur = conn.cursor(cursor_factory=RealDictCursor) # ساخت یک "مکان‌نما" برای اجرای دستورات
    return conn, cur

def close_conn_cursor(conn, cur):
    # بستن مکان‌نما و اتصال برای آزاد کردن منابع
    cur.close()
    conn.close()