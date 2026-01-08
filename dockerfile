# تعریف متغیرها برای مدیریت آسان‌تر ورژن‌ها
ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.10

# انتخاب تصویر پایه (آشپزخانه اصلی)
FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

# تعیین مسیر خانه در داکر (اختیاری ولی برای نظم بهتر است)
ENV AIRFLOW_HOME=/opt/airflow

# کپی کردن لیست نیازمندی‌ها از سیستم تو به داخل داکر
COPY requirements.txt /

# نصب کتابخانه‌های پایتونی داخل محیط ایزوله‌ی داکر
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt