# 🐋 Docker Deployment Guide - 2026 Goal Tracker

## 📋 Yêu Cầu

- Docker 20.10+
- Docker Compose 2.0+

## 🚀 Hướng Dẫn Chạy

### 1. Chuẩn Bị File

Cấu trúc thư mục:
```
goal-tracker/
├── app.py
├── storage.py
├── scheduler.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .dockerignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── goals.html
│   ├── goal_detail.html
│   ├── add_goal.html
│   ├── edit_goal.html
│   ├── progress.html
│   └── reports.html
└── data/
    └── goals_data.json (sẽ tự tạo)
```

### 2. Cấu Hình Environment

Tạo file `.env` từ `.env.example`:
```bash
cp .env.example .env
```

Chỉnh sửa file `.env`:
```bash
# Flask
SECRET_KEY=your-random-secret-key-here

# MongoDB (tùy chọn)
MONGO_USER=admin
MONGO_PASSWORD=strong-password-here

# Telegram Bot
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# Schedule
WEEKLY_REMINDER_DAY=sunday
WEEKLY_REMINDER_TIME=20:00
MONTHLY_REVIEW_DAY=1
MONTHLY_REVIEW_TIME=09:00
```

### 3. Khởi Động Ứng Dụng

**Chạy toàn bộ (Web + MongoDB + Scheduler):**
```bash
docker-compose up -d
```

**Chỉ chạy Web (không MongoDB):**
```bash
docker-compose up -d web
```

**Xem logs:**
```bash
# Tất cả services
docker-compose logs -f

# Chỉ web
docker-compose logs -f web

# Chỉ scheduler
docker-compose logs -f scheduler
```

### 4. Kiểm Tra

Truy cập: http://localhost:5000

Kiểm tra health:
```bash
curl http://localhost:5000/
```

### 5. Quản Lý

**Dừng:**
```bash
docker-compose stop
```

**Khởi động lại:**
```bash
docker-compose restart
```

**Xóa toàn bộ:**
```bash
docker-compose down -v
```

**Rebuild sau khi sửa code:**
```bash
docker-compose up -d --build
```

## 📊 Kiến Trúc Services

### 1. **mongodb** (Optional)
- Image: `mongo:7`
- Port: `27017`
- Chức năng: Backup storage tự động
- Có thể tắt nếu chỉ dùng JSON

### 2. **web**
- Build từ Dockerfile
- Port: `5000`
- Chức năng: Flask web application
- Volume: `./data` cho JSON storage

### 3. **scheduler**
- Build từ Dockerfile
- Chức năng: Tự động gửi báo cáo
- Phụ thuộc: web service

## 🔧 Tùy Chỉnh

### Chỉ dùng JSON (không MongoDB)

Sửa `docker-compose.yml`:
```yaml
services:
  web:
    # ... existing config ...
    environment:
      MONGO_URI: ""  # Bỏ trống
    depends_on: []   # Xóa mongodb dependency
  
  # Xóa hoặc comment service mongodb
```

### Thay đổi Port

Trong `docker-compose.yml`:
```yaml
services:
  web:
    ports:
      - "8080:5000"  # Thay 8080 bằng port bạn muốn
```

### Chạy Production Mode

Đảm bảo trong `.env`:
```bash
FLASK_ENV=production
SECRET_KEY=very-strong-random-key
```

## 🔍 Troubleshooting

### Lỗi: Port 5000 đã được sử dụng
```bash
# Tìm process đang dùng port
lsof -i :5000

# Hoặc đổi port trong docker-compose.yml
ports:
  - "5001:5000"
```

### Lỗi: MongoDB không kết nối
```bash
# Kiểm tra MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb
```

### Lỗi: Scheduler không chạy
```bash
# Kiểm tra logs
docker-compose logs scheduler

# Kiểm tra web service đang chạy
curl http://localhost:5000/
```

### Data bị mất khi restart
```bash
# Đảm bảo volume được mount đúng
docker-compose down
# Kiểm tra file ./data/goals_data.json tồn tại
docker-compose up -d
```

## 📦 Backup & Restore

### Backup Data
```bash
# JSON file sẽ ở trong thư mục ./data
cp data/goals_data.json data/backup_$(date +%Y%m%d).json

# Hoặc tải từ web
curl http://localhost:5000/api/export-json -o backup.json
```

### Restore Data
```bash
# Copy file backup vào thư mục data
cp backup.json data/goals_data.json

# Restart container
docker-compose restart web
```

## 🔐 Security Notes

1. **Đổi SECRET_KEY** trong production
2. **Đổi MONGO_PASSWORD** nếu dùng MongoDB
3. **Không commit file .env** vào git
4. **Sử dụng reverse proxy** (nginx) cho production
5. **Enable HTTPS** với SSL certificate

## 📈 Production Deployment

Để deploy lên server:

1. **Cài đặt Docker & Docker Compose**
2. **Clone repo** và setup `.env`
3. **Chạy với production config**:
```bash
FLASK_ENV=production docker-compose up -d
```

4. **Setup nginx** (recommended):
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🆘 Support

Nếu gặp vấn đề:
1. Kiểm tra logs: `docker-compose logs -f`
2. Kiểm tra .env config
3. Restart services: `docker-compose restart`
4. Rebuild: `docker-compose up -d --build`
