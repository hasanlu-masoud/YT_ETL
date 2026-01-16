# اول از همه ابزارهای فایل اول (جعبه‌ابزار) را می‌آوریم
from datawarehouse.data_utils import table, get_conn_cursor, close_conn_cursor

# ۱. متد برای اضافه کردن اطلاعات جدید
def insert_rows(data, schema):
    conn, cur = get_conn_cursor() # درِ دیتابیس را باز کن
    
    if schema == "staging":
        # دستور برای گذاشتن داده‌های اولیه در قفسه
        insert_sql = f"""
            INSERT INTO {schema}.{table} ("Video_ID", "Video_Title", "Upload_Date", "Duration", "Video_Views", "Likes_Count", "Comments_Count")
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
    else:
        # دستور برای گذاشتن داده‌های تمیز در قفسه اصلی
        insert_sql = f"""
            INSERT INTO {schema}.{table} ("Video_ID", "Video_Title", "Upload_Date", "Duration", "Video_Type", "Video_Views", "Likes_Count", "Comments_Count")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        
    cur.execute(insert_sql, data) # مأمور برود و داده را در قفسه بگذارد
    conn.commit() # تایید نهایی برای ذخیره شدن
    close_conn_cursor(conn, cur) # بستن در

# ۲. متد برای نو کردن اطلاعات قدیمی (تعداد بازدید و لایک)
def update_rows(data, schema):
    conn, cur = get_conn_cursor()
    
    # می‌گوییم هر جا که آیدی ویدیو (Video_ID) یکی بود، بازدید و لایک را آپدیت کن
    update_sql = f"""
        UPDATE {schema}.{table}
        SET "Video_Views" = %s, "Likes_Count" = %s, "Comments_Count" = %s
        WHERE "Video_ID" = %s;
    """
    
    cur.execute(update_sql, data)
    conn.commit()
    close_conn_cursor(conn, cur)

# ۳. متد برای پاک کردن ویدیوهای اضافه
def delete_rows(ids_to_delete, schema):
    conn, cur = get_conn_cursor()
    
    # دستور برای حذف کردن ویدیو بر اساس آیدی
    delete_sql = f'DELETE FROM {schema}.{table} WHERE "Video_ID" = %s;'
    
    # اینجا برای هر آیدی که در لیست است، یک بار دستور حذف را اجرا می‌کنیم
    for video_id in ids_to_delete:
        cur.execute(delete_sql, (video_id,))
        
    conn.commit()
    close_conn_cursor(conn, cur)