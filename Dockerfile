# استفاده از تصویر رسمی پایتون
FROM python:3.10

# تنظیم متغیرهای محیطی برای بهینه‌سازی اجرا
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# مشخص کردن دایرکتوری کاری
WORKDIR /app

# کپی کردن فایل‌های مورد نیاز برای نصب وابستگی‌ها
COPY requirements.txt .

# نصب وابستگی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن کل پروژه به داخل کانتینر
COPY . .

# باز کردن پورت ۸۰۰۰ برای دسترسی به جنگو
EXPOSE 8000

# اجرای سرور جنگو
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
