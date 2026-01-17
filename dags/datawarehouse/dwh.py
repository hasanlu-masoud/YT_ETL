from datawarehouse.data_utils import get_conn_cursor, close_conn_cursor, create_schema, create_table, get_video_ids
from datawarehouse.data_loading import load_data
from datawarehouse.data_modification import insert_rows, update_rows, delete_rows
from datawarehouse.data_transformation import transform_data
import logging

# تنظیمات لاگر برای ثبت گزارش‌ها
logger = logging.getLogger(__name__)
table = "yt_api"

# ۱. متد پر کردن جدول موقت (Staging)
def staging_table():
    schema = 'staging'
    conn, cur = get_conn_cursor()
    
    try:
        YT_data = load_data() # خواندن داده‌ها از JSON
        create_schema(schema) # ساخت بخش staging در دیتابیس
        create_table(schema)  # ساخت جدول در staging
        
        table_ids = get_video_ids(cur, schema) # گرفتن آیدی‌های موجود
        
        for row in YT_data:
            if row['video_id'] in table_ids:
                update_rows(cur, conn, schema, row) # اگر بود، آپدیت کن
            else:
                insert_rows(cur, conn, schema, row) # اگر نبود، اضافه کن
                
        # حذف ویدیوهایی که دیگر در JSON نیستند
        ids_in_json = {row["video_id"] for row in YT_data}
        ids_to_delete = set(table_ids) - ids_in_json
        if ids_to_delete:
            delete_rows(cur, conn, schema, ids_to_delete)
            
    except Exception as e:
        logger.error(f"Error in staging table: {e}")
        raise e
    finally:
        close_conn_cursor(conn, cur)

# ۲. متد پر کردن جدول اصلی و تمیز (Core)
def core_table():
    schema = 'core'
    conn, cur = get_conn_cursor()
    
    try:
        create_schema(schema)
        create_table(schema)
        
        table_ids = get_video_ids(cur, schema)
        
        # خواندن داده‌ها از Staging برای انتقال به Core
        cur.execute(f"SELECT * FROM staging.{table};")
        rows = cur.fetchall()
        
        for row in rows:
            # جادوی ترنسفورم: تمیز کردن داده قبل از ورود به Core
            transformed_row = transform_data(row)
            
            if row["Video_ID"] in table_ids:
                update_rows(cur, conn, schema, transformed_row)
            else:
                insert_rows(cur, conn, schema, transformed_row)
                
    except Exception as e:
        logger.error(f"Error in core table: {e}")
        raise e
    finally:
        close_conn_cursor(conn, cur)