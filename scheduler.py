#!/usr/bin/env python3
"""
scheduler.py - Auto Scheduler tối ưu (hợp nhất 2 phiên bản)
- Gửi báo cáo tuần tự động
- Gửi báo cáo tháng + backup JSON
"""

import schedule
import time
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

API_URL = os.getenv('API_URL', 'http://localhost:5000')


def send_weekly_report():
    """Gửi báo cáo tuần"""
    try:
        logger.info("📅 Đang gửi báo cáo tuần...")
        response = requests.post(f"{API_URL}/api/send-weekly-reminder", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            logger.info("✅ Báo cáo tuần: " + result.get('message', 'OK'))
        else:
            logger.error(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")


def send_monthly_report_with_backup():
    """Gửi báo cáo tháng + backup JSON"""
    try:
        logger.info("📊 Đang gửi báo cáo tháng...")
        
        # 1. Báo cáo tháng
        response = requests.post(f"{API_URL}/api/send-monthly-review", timeout=30)
        if response.status_code == 200:
            result = response.json()
            logger.info("✅ Báo cáo tháng: " + result.get('message', 'OK'))
        
        # 2. Backup JSON
        logger.info("💾 Đang gửi backup JSON...")
        backup_response = requests.post(f"{API_URL}/api/send-monthly-backup", timeout=30)
        if backup_response.status_code == 200:
            backup_result = backup_response.json()
            logger.info("✅ Backup: " + backup_result.get('message', 'OK'))
        
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")


def check_monthly_schedule():
    """Kiểm tra và chạy báo cáo tháng nếu đúng ngày"""
    monthly_day = int(os.getenv('MONTHLY_REVIEW_DAY', '1'))
    if datetime.now().day == monthly_day:
        send_monthly_report_with_backup()


def main():
    """Chạy scheduler"""
    logger.info("=" * 70)
    logger.info("⏰ 2026 GOAL TRACKER - SCHEDULER")
    logger.info("=" * 70)
    
    # Cấu hình từ .env
    weekly_day = os.getenv('WEEKLY_REMINDER_DAY', 'sunday').lower()
    weekly_time = os.getenv('WEEKLY_REMINDER_TIME', '20:00')
    monthly_day = int(os.getenv('MONTHLY_REVIEW_DAY', '1'))
    monthly_time = os.getenv('MONTHLY_REVIEW_TIME', '09:00')
    
    logger.info(f"\n📅 Cấu hình:")
    logger.info(f"   • Báo cáo tuần: Mỗi {weekly_day.title()} lúc {weekly_time}")
    logger.info(f"   • Báo cáo + backup tháng: Ngày {monthly_day} lúc {monthly_time}")
    logger.info(f"   • API: {API_URL}\n")
    
    # Schedule
    getattr(schedule.every(), weekly_day).at(weekly_time).do(send_weekly_report)
    schedule.every().day.at(monthly_time).do(check_monthly_schedule)
    
    logger.info("🚀 Scheduler đã khởi động! (Nhấn Ctrl+C để dừng)\n")
    
    # Test ngay nếu được yêu cầu
    if os.getenv('TEST_ON_START', 'false').lower() == 'true':
        logger.info("🧪 Chạy test...")
        send_weekly_report()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("\n\n👋 Đã dừng scheduler!")


if __name__ == "__main__":
    main()
