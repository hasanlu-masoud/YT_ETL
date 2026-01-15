from airflow import DAG
import pendulum
from datetime import datetime, timedelta
# وارد کردن توابع از فایل video_stats که در پوشه api قرار دارد
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_to_json

# تعریف منطقه زمانی (همان‌طور که مدرس در خط ۶ و ۷ نوشته است)
local_tz = pendulum.timezone("Europe/Malta")

# ۱. تنظیمات پیش‌فرض (دقیقاً مطابق عکس مدرس)
default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": ["data@engineers.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 1, 1, tzinfo=local_tz), # تاریخ شروع که مدرس تعیین کرده
}

# ۲. تعریف DAG
with DAG(
    dag_id="produce_json",
    default_args=default_args,
    description="DAG to produce JSON file with raw data",
    schedule="0 14 * * *",
    catchup=False,
) as dag:

    # ۳. تعریف مراحل کار (Tasks)
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extract_data)

    # ۴. تعیین ترتیب اجرا
    playlist_id >> video_ids >> extract_data >> save_to_json_task