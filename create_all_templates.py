#!/usr/bin/env python3
"""
create_all_templates.py - Tạo lại TẤT CẢ templates
Chạy: python create_all_templates.py
"""

import os

# Tạo thư mục templates
os.makedirs('templates', exist_ok=True)

templates = {}

# ============================================================
# 1. base.html - Base Layout
# ============================================================
templates['base.html'] = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}2026 Goal Tracker{% endblock %}</title>
    
    <!-- Bootstrap & Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    
    <style>
        /* ===== VARIABLES ===== */
        :root {
            --primary: #4f46e5;
            --secondary: #7c3aed;
            --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        /* ===== LAYOUT ===== */
        body {
            background: var(--gradient);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, sans-serif;
        }
        
        .main-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin: 20px auto;
            max-width: 1200px;
            overflow: hidden;
        }

        /* ===== NAVBAR ===== */
        .navbar-custom {
            background: var(--gradient);
            padding: 1rem 2rem;
        }
        
        .navbar-custom .nav-link {
            color: white !important;
            margin: 0 10px;
            transition: all 0.3s;
            border-radius: 8px;
            padding: 8px 16px;
        }
        
        .navbar-custom .nav-link:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .navbar-custom .nav-link.active {
            background: rgba(255,255,255,0.3);
            font-weight: bold;
        }

        /* ===== CONTENT ===== */
        .content-area {
            padding: 2rem;
        }

        /* ===== CARDS ===== */
        .stat-card {
            background: var(--gradient);
            color: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .goal-card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            transition: all 0.3s;
        }
        
        .goal-card:hover {
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transform: translateY(-3px);
        }

        /* ===== COMPONENTS ===== */
        .progress-bar-custom {
            background: var(--gradient);
        }
        
        .btn-primary-custom {
            background: var(--gradient);
            border: none;
            border-radius: 10px;
            padding: 10px 25px;
            transition: all 0.3s;
            color: white;
        }
        
        .btn-primary-custom:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(79, 70, 229, 0.4);
        }
        
        .alert-custom {
            border-radius: 10px;
            border: none;
        }
    </style>
</head>
<body>
    <div class="main-container">
        <!-- NAVBAR -->
        <nav class="navbar navbar-expand-lg navbar-custom">
            <div class="container-fluid">
                <a class="navbar-brand text-white fw-bold" href="/">
                    <i class="bi bi-bullseye"></i> 2026 Goal Tracker
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <a class="nav-link {% if request.endpoint == 'index' %}active{% endif %}" href="/">
                                <i class="bi bi-house"></i> Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {% if request.endpoint == 'goals' %}active{% endif %}" href="/goals">
                                <i class="bi bi-list-check"></i> Mục tiêu
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {% if request.endpoint == 'progress' %}active{% endif %}" href="/progress">
                                <i class="bi bi-graph-up"></i> Tiến độ
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link {% if request.endpoint == 'reports' %}active{% endif %}" href="/reports">
                                <i class="bi bi-bar-chart"></i> Báo cáo
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <!-- CONTENT -->
        <div class="content-area">
            <!-- Flash Messages -->
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }} alert-custom alert-dismissible fade show" role="alert">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <!-- Page Content -->
            {% block content %}{% endblock %}
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>'''

# ============================================================
# 2. index.html - Dashboard
# ============================================================
templates['index.html'] = '''{% extends "base.html" %}

{% block title %}Dashboard - 2026 Goal Tracker{% endblock %}

{% block content %}
<div class="container-fluid">
    <h2 class="mb-4"><i class="bi bi-speedometer2"></i> Dashboard Tổng Quan</h2>
    
    <!-- Stats Cards -->
    <div class="row">
        <div class="col-md-3">
            <div class="stat-card">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">Tổng Mục Tiêu</h6>
                        <h2 class="mb-0">{{ stats.total_goals }}</h2>
                    </div>
                    <i class="bi bi-bullseye" style="font-size: 2.5rem; opacity: 0.7;"></i>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">Đang Thực Hiện</h6>
                        <h2 class="mb-0">{{ stats.active_goals }}</h2>
                    </div>
                    <i class="bi bi-play-circle" style="font-size: 2.5rem; opacity: 0.7;"></i>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">Đã Hoàn Thành</h6>
                        <h2 class="mb-0">{{ stats.completed_goals }}</h2>
                    </div>
                    <i class="bi bi-check-circle" style="font-size: 2.5rem; opacity: 0.7;"></i>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">Hoạt Động Tuần</h6>
                        <h2 class="mb-0">{{ stats.week_subtasks }}</h2>
                    </div>
                    <i class="bi bi-calendar-week" style="font-size: 2.5rem; opacity: 0.7;"></i>
                </div>
            </div>
        </div>
    </div>

    <!-- Telegram Status -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card goal-card">
                <div class="card-body">
                    <h5><i class="bi bi-telegram"></i> Trạng Thái Telegram</h5>
                    {% if telegram_configured %}
                        <div class="alert alert-success alert-custom">
                            <i class="bi bi-check-circle-fill"></i> Đã kết nối Telegram Bot
                        </div>
                        <button class="btn btn-primary-custom" onclick="testTelegram()">
                            <i class="bi bi-send"></i> Test Gửi Thông Báo
                        </button>
                        <button class="btn btn-primary-custom ms-2" onclick="sendWeeklyReminder()">
                            <i class="bi bi-calendar-week"></i> Gửi Nhắc Nhở Tuần
                        </button>
                        <button class="btn btn-primary-custom ms-2" onclick="sendMonthlyReview()">
                            <i class="bi bi-calendar-month"></i> Gửi Báo Cáo Tháng
                        </button>
                    {% else %}
                        <div class="alert alert-warning alert-custom">
                            <i class="bi bi-exclamation-triangle-fill"></i> Chưa cấu hình Telegram. Vui lòng thiết lập trong file .env
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <!-- Goals List -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4><i class="bi bi-list-check"></i> Mục Tiêu 2026</h4>
                <a href="/goals/add" class="btn btn-primary-custom">
                    <i class="bi bi-plus-circle"></i> Thêm Mục Tiêu
                </a>
            </div>

            {% if goals %}
                {% for goal in goals %}
                <div class="goal-card card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h5 class="mb-0">
                                {% if goal.status == 'completed' %}
                                    <i class="bi bi-check-circle-fill text-success"></i>
                                {% else %}
                                    <i class="bi bi-circle text-primary"></i>
                                {% endif %}
                                {{ goal.title }}
                            </h5>
                            <span class="badge bg-primary">{{ goal.status }}</span>
                        </div>
                        
                        {% if goal.description %}
                        <p class="text-muted mb-2">{{ goal.description }}</p>
                        {% endif %}
                        
                        <div class="mb-2">
                            <small class="text-muted">
                                <i class="bi bi-calendar"></i> Hạn: {{ goal.target_date }}
                            </small>
                        </div>
                        
                        <div class="mt-3">
                            <a href="/goals/{{ goal.id }}" class="btn btn-sm btn-primary-custom">
                                <i class="bi bi-eye"></i> Chi tiết
                            </a>
                            <a href="/goals/{{ goal.id }}/edit" class="btn btn-sm btn-outline-primary">
                                <i class="bi bi-pencil"></i> Chỉnh sửa
                            </a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div class="alert alert-info alert-custom">
                    <i class="bi bi-info-circle"></i> Chưa có mục tiêu nào. 
                    <a href="/goals/add" class="alert-link">Thêm mục tiêu đầu tiên</a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function testTelegram() {
    if (!confirm('Gửi tin nhắn test đến Telegram?')) return;
    
    fetch('/api/test-telegram', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert('✅ ' + data.message);
            } else {
                alert('❌ ' + data.message);
            }
        })
        .catch(err => alert('Lỗi: ' + err));
}

function sendWeeklyReminder() {
    if (!confirm('Gửi nhắc nhở tuần đến Telegram?')) return;
    
    fetch('/api/send-weekly-reminder', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert('✅ ' + data.message);
            } else {
                alert('❌ ' + data.message);
            }
        })
        .catch(err => alert('Lỗi: ' + err));
}

function sendMonthlyReview() {
    if (!confirm('Gửi báo cáo tháng đến Telegram?')) return;
    
    fetch('/api/send-monthly-review', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert('✅ ' + data.message);
            } else {
                alert('❌ ' + data.message);
            }
        })
        .catch(err => alert('Lỗi: ' + err));
}
</script>
{% endblock %}'''

# ============================================================
# 3. goals.html - Danh sách mục tiêu
# ============================================================
templates['goals.html'] = '''{% extends "base.html" %}

{% block title %}Quản Lý Mục Tiêu{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="bi bi-list-check"></i> Quản Lý Mục Tiêu</h2>
        <a href="/goals/add" class="btn btn-primary-custom">
            <i class="bi bi-plus-circle"></i> Thêm Mục Tiêu Mới
        </a>
    </div>

    {% if goals %}
        <div class="row">
            {% for goal in goals %}
            <div class="col-md-6">
                <div class="goal-card card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <div class="flex-grow-1">
                                <h5 class="mb-1">
                                    {% if goal.status == 'completed' %}
                                        <i class="bi bi-check-circle-fill text-success"></i>
                                    {% elif goal.status == 'paused' %}
                                        <i class="bi bi-pause-circle text-warning"></i>
                                    {% else %}
                                        <i class="bi bi-circle text-primary"></i>
                                    {% endif %}
                                    {{ goal.title }}
                                </h5>
                                <small class="text-muted">
                                    <i class="bi bi-calendar-plus"></i> Tạo: {{ goal.created_at }}
                                </small>
                            </div>
                            <div>
                                {% if goal.status == 'active' %}
                                    <span class="badge bg-primary">Đang thực hiện</span>
                                {% elif goal.status == 'completed' %}
                                    <span class="badge bg-success">Hoàn thành</span>
                                {% elif goal.status == 'paused' %}
                                    <span class="badge bg-warning">Tạm dừng</span>
                                {% endif %}
                            </div>
                        </div>

                        {% if goal.description %}
                        <p class="text-muted mb-3">{{ goal.description }}</p>
                        {% endif %}

                        <div class="mb-3">
                            <div class="d-flex justify-content-between mb-1">
                                <small><i class="bi bi-flag"></i> <strong>Hạn:</strong></small>
                                <small><strong>{{ goal.target_date }}</strong></small>
                            </div>
                            <div class="d-flex justify-content-between mb-1">
                                <small><i class="bi bi-list-task"></i> <strong>Hoạt động:</strong></small>
                                <small><strong>{{ goal.subtask_count }} tasks</strong></small>
                            </div>
                        </div>

                        <div class="d-flex gap-2">
                            <a href="/goals/{{ goal.id }}" class="btn btn-sm btn-primary-custom flex-grow-1">
                                <i class="bi bi-eye"></i> Chi tiết
                            </a>
                            <a href="/goals/{{ goal.id }}/edit" class="btn btn-sm btn-outline-primary">
                                <i class="bi bi-pencil"></i>
                            </a>
                            <form method="POST" action="/goals/{{ goal.id }}/delete"
                                  onsubmit="return confirm('Xóa mục tiêu và tất cả hoạt động?')">
                                <button type="submit" class="btn btn-sm btn-outline-danger">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-info alert-custom">
            <i class="bi bi-info-circle"></i> Chưa có mục tiêu nào. 
            <a href="/goals/add" class="alert-link">Thêm mục tiêu đầu tiên</a> để bắt đầu theo dõi tiến độ 2026!
        </div>
    {% endif %}
</div>
{% endblock %}'''

# ============================================================
# 4. goal_detail.html - Chi tiết (CHỈ hoạt động)
# ============================================================
templates['goal_detail.html'] = '''{% extends "base.html" %}

{% block title %}{{ goal.title }} - Chi Tiết{% endblock %}

{% block content %}
<div class="container-fluid">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <a href="/goals" class="btn btn-outline-secondary btn-sm mb-2">
                <i class="bi bi-arrow-left"></i> Quay lại
            </a>
            <h2>
                {% if goal.status == 'completed' %}
                    <i class="bi bi-check-circle-fill text-success"></i>
                {% elif goal.status == 'paused' %}
                    <i class="bi bi-pause-circle text-warning"></i>
                {% else %}
                    <i class="bi bi-circle text-primary"></i>
                {% endif %}
                {{ goal.title }}
            </h2>
        </div>
        <a href="/goals/{{ goal.id }}/edit" class="btn btn-outline-primary">
            <i class="bi bi-pencil"></i> Chỉnh sửa
        </a>
    </div>

    <div class="row">
        <!-- CỘT TRÁI: Thông tin -->
        <div class="col-md-4">
            <div class="card goal-card">
                <div class="card-body">
                    <h5><i class="bi bi-info-circle"></i> Thông Tin Mục Tiêu</h5>
                    
                    {% if goal.description %}
                    <div class="mb-3">
                        <strong>Mô tả:</strong>
                        <p class="text-muted mb-0">{{ goal.description }}</p>
                    </div>
                    {% endif %}
                    
                    <div class="mb-2">
                        <strong><i class="bi bi-calendar-plus"></i> Ngày tạo:</strong><br>
                        <span class="text-muted">{{ goal.created_at }}</span>
                    </div>
                    
                    <div class="mb-2">
                        <strong><i class="bi bi-calendar-check"></i> Hạn hoàn thành:</strong><br>
                        <span class="text-muted">{{ goal.target_date }}</span>
                    </div>
                    
                    <div class="mb-3">
                        <strong><i class="bi bi-flag"></i> Trạng thái:</strong><br>
                        {% if goal.status == 'active' %}
                            <span class="badge bg-primary">Đang thực hiện</span>
                        {% elif goal.status == 'completed' %}
                            <span class="badge bg-success">Hoàn thành</span>
                        {% elif goal.status == 'paused' %}
                            <span class="badge bg-warning">Tạm dừng</span>
                        {% endif %}
                    </div>
                    
                    <div class="alert alert-info alert-custom">
                        <i class="bi bi-info-circle"></i>
                        <strong>Tổng hoạt động:</strong> {{ sub_tasks|length }}
                    </div>
                    
                    <a href="/progress" class="btn btn-outline-primary w-100">
                        <i class="bi bi-graph-up"></i> Xem Tiến Độ
                    </a>
                </div>
            </div>
        </div>

        <!-- CỘT PHẢI: Hoạt động -->
        <div class="col-md-8">
            <!-- Form thêm hoạt động -->
            <div class="card goal-card mb-3">
                <div class="card-body">
                    <h5><i class="bi bi-plus-circle"></i> Thêm Hoạt Động Mới</h5>
                    
                    <form method="POST" action="/goals/{{ goal.id }}/subtask/add">
                        <div class="row">
                            <div class="col-md-8 mb-2">
                                <input type="text" class="form-control" name="title" required
                                       placeholder="Tên hoạt động... (VD: Hoàn thành module 1)">
                            </div>
                            <div class="col-md-4 mb-2">
                                <button type="submit" class="btn btn-primary-custom w-100">
                                    <i class="bi bi-check"></i> Thêm
                                </button>
                            </div>
                        </div>
                        <input type="text" class="form-control form-control-sm" name="note"
                               placeholder="Ghi chú thêm (tùy chọn)...">
                    </form>
                </div>
            </div>

            <!-- Danh sách hoạt động -->
            <div class="card goal-card">
                <div class="card-body">
                    <h5 class="mb-3">
                        <i class="bi bi-list-task"></i> Danh Sách Hoạt Động
                        <span class="badge bg-primary">{{ sub_tasks|length }}</span>
                    </h5>
                    
                    {% if sub_tasks %}
                        {% for task in sub_tasks %}
                        <div class="card mb-2" style="background: #f8f9fa; border: 1px solid #dee2e6;">
                            <div class="card-body py-2">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div class="flex-grow-1">
                                        <h6 class="mb-1">
                                            <i class="bi bi-check-circle text-success"></i> 
                                            {{ task.title }}
                                        </h6>
                                        
                                        {% if task.note %}
                                        <p class="text-muted small mb-1">{{ task.note }}</p>
                                        {% endif %}
                                        
                                        <small class="text-muted">
                                            <i class="bi bi-calendar"></i> {{ task.created_at }}
                                            <i class="bi bi-clock ms-2"></i> {{ task.created_time }}
                                        </small>
                                    </div>
                                    
                                    <form method="POST" action="/subtask/{{ task.id }}/delete" 
                                          onsubmit="return confirm('Xóa hoạt động này?')"
                                          style="display: inline;">
                                        <button type="submit" class="btn btn-sm btn-outline-danger">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </form>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    {% else %}
                        <div class="alert alert-info alert-custom">
                            <i class="bi bi-info-circle"></i> Chưa có hoạt động nào. 
                            Thêm hoạt động đầu tiên ở trên!
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

# ============================================================
# 5. add_goal.html
# ============================================================
templates['add_goal.html'] = '''{% extends "base.html" %}

{% block title %}Thêm Mục Tiêu Mới{% endblock %}

{% block content %}
<div class="container" style="max-width: 600px;">
    <h2 class="mb-4"><i class="bi bi-plus-circle"></i> Thêm Mục Tiêu Mới</h2>
    
    <div class="card goal-card">
        <div class="card-body">
            <form method="POST">
                <div class="mb-3">
                    <label for="title" class="form-label"><strong>Tên mục tiêu</strong> <span class="text-danger">*</span></label>
                    <input type="text" class="form-control" id="title" name="title" required 
                           placeholder="Ví dụ: Học Python, Tăng doanh thu 50%...">
                </div>

                <div class="mb-3">
                    <label for="description" class="form-label"><strong>Mô tả chi tiết</strong></label>
                    <textarea class="form-control" id="description" name="description" rows="4"
                              placeholder="Chi tiết về mục tiêu này, các bước thực hiện..."></textarea>
                    <small class="text-muted">Mô tả rõ mục tiêu giúp bạn tập trung hơn</small>
                </div>

                <div class="mb-4">
                    <label for="target_date" class="form-label"><strong>Hạn hoàn thành</strong></label>
                    <input type="date" class="form-control" id="target_date" name="target_date" value="2026-12-31">
                    <small class="text-muted">Ngày dự kiến hoàn thành mục tiêu</small>
                </div>

                <div class="d-flex gap-2">
                    <button type="submit" class="btn btn-primary-custom flex-grow-1">
                        <i class="bi bi-check-circle"></i> Tạo Mục Tiêu
                    </button>
                    <a href="/goals" class="btn btn-outline-secondary flex-grow-1">
                        <i class="bi bi-x-circle"></i> Hủy
                    </a>
                </div>
            </form>
        </div>
    </div>

    <div class="alert alert-info alert-custom mt-3">
        <i class="bi bi-lightbulb"></i> <strong>Mẹo:</strong> Chia mục tiêu lớn thành các mục tiêu nhỏ hơn để dễ theo dõi và đạt được!
    </div>
</div>
{% endblock %}'''

# ============================================================
# 6. edit_goal.html
# ============================================================
templates['edit_goal.html'] = '''{% extends "base.html" %}

{% block title %}Chỉnh Sửa Mục Tiêu{% endblock %}

{% block content %}
<div class="container" style="max-width: 600px;">
    <h2 class="mb-4"><i class="bi bi-pencil"></i> Chỉnh Sửa Mục Tiêu</h2>
    
    <div class="card goal-card">
        <div class="card-body">
            <form method="POST">
                <div class="mb-3">
                    <label for="title" class="form-label"><strong>Tên mục tiêu</strong> <span class="text-danger">*</span></label>
                    <input type="text" class="form-control" id="title" name="title" required 
                           value="{{ goal.title }}">
                </div>

                <div class="mb-3">
                    <label for="description" class="form-label"><strong>Mô tả chi tiết</strong></label>
                    <textarea class="form-control" id="description" name="description" rows="4">{{ goal.description }}</textarea>
                </div>

                <div class="mb-3">
                    <label for="target_date" class="form-label"><strong>Hạn hoàn thành</strong></label>
                    <input type="date" class="form-control" id="target_date" name="target_date" 
                           value="{{ goal.target_date }}">
                </div>

                <div class="mb-4">
                    <label for="status" class="form-label"><strong>Trạng thái</strong></label>
                    <select class="form-select" id="status" name="status">
                        <option value="active" {% if goal.status == 'active' %}selected{% endif %}>
                            Đang thực hiện
                        </option>
                        <option value="paused" {% if goal.status == 'paused' %}selected{% endif %}>
                            Tạm dừng
                        </option>
                        <option value="completed" {% if goal.status == 'completed' %}selected{% endif %}>
                            Hoàn thành
                        </option>
                    </select>
                </div>

                <div class="d-flex gap-2">
                    <button type="submit" class="btn btn-primary-custom flex-grow-1">
                        <i class="bi bi-save"></i> Lưu Thay Đổi
                    </button>
                    <a href="/goals/{{ goal.id }}" class="btn btn-outline-secondary flex-grow-1">
                        <i class="bi bi-x-circle"></i> Hủy
                    </a>
                </div>
            </form>
        </div>
    </div>

    <div class="mt-3">
        <form method="POST" action="/goals/{{ goal.id }}/delete" 
              onsubmit="return confirm('Bạn chắc chắn muốn xóa mục tiêu này? Hành động này không thể hoàn tác!')">
            <button type="submit" class="btn btn-outline-danger w-100">
                <i class="bi bi-trash"></i> Xóa Mục Tiêu Này
            </button>
        </form>
    </div>
</div>
{% endblock %}'''

# ============================================================
# 7. progress.html - Tiến độ READ-ONLY
# ============================================================
templates['progress.html'] = '''{% extends "base.html" %}

{% block title %}Tiến Độ{% endblock %}

{% block content %}
<div class="container-fluid">
    <h2 class="mb-4"><i class="bi bi-graph-up-arrow"></i> Tiến Độ Mục Tiêu</h2>

    <!-- TIẾN ĐỘ TUẦN -->
    <div class="card goal-card mb-4">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5><i class="bi bi-calendar-week"></i> Tiến Độ Tuần Này</h5>
                <span class="badge bg-primary">{{ week_range }}</span>
            </div>

            {% if week_stats.total_activities > 0 %}
                <!-- Tổng quan tuần -->
                <div class="row mb-4">
                    <div class="col-md-4">
                        <div class="stat-card text-center">
                            <h3 class="mb-1">{{ week_stats.total_activities }}</h3>
                            <small>Hoạt động tuần này</small>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="stat-card text-center">
                            <h3 class="mb-1">{{ week_stats.active_goals }}</h3>
                            <small>Mục tiêu đang làm</small>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="stat-card text-center">
                            <h3 class="mb-1">{{ week_stats.avg_per_day }}</h3>
                            <small>Hoạt động/ngày</small>
                        </div>
                    </div>
                </div>

                <!-- Chi tiết theo mục tiêu -->
                <h6 class="mb-3">Chi Tiết Theo Mục Tiêu</h6>
                {% for goal_id, info in week_by_goal.items() %}
                <div class="card mb-3" style="background: #f8f9fa; border: 2px solid #dee2e6;">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="mb-0">
                                <i class="bi bi-bullseye text-primary"></i> 
                                {{ info.goal_title }}
                            </h6>
                            <span class="badge bg-success">{{ info.tasks|length }} hoạt động</span>
                        </div>
                        
                        <div class="mt-2">
                            {% for task in info.tasks %}
                            <div class="d-flex justify-content-between align-items-center py-1 border-bottom">
                                <span>
                                    <i class="bi bi-check-circle-fill text-success"></i>
                                    {{ task.title }}
                                </span>
                                <small class="text-muted">{{ task.created_at }}</small>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div class="alert alert-secondary alert-custom">
                    <i class="bi bi-info-circle"></i> 
                    Chưa có hoạt động nào trong tuần này. Hãy bắt đầu làm việc!
                </div>
            {% endif %}
        </div>
    </div>

    <!-- TIẾN ĐỘ THÁNG -->
    <div class="card goal-card">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5><i class="bi bi-calendar-month"></i> Tiến Độ Tháng {{ month_name }}</h5>
            </div>

            {% if month_stats.total_activities > 0 %}
                <!-- Tổng quan tháng -->
                <div class="row mb-4">
                    <div class="col-md-3">
                        <div class="stat-card text-center">
                            <h3 class="mb-1">{{ month_stats.total_activities }}</h3>
                            <small>Tổng hoạt động</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card text-center">
                            <h3 class="mb-1">{{ month_stats.active_goals }}</h3>
                            <small>Mục tiêu đang làm</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card text-center">
                            <h3 class="mb-1">{{ month_stats.completed_goals }}</h3>
                            <small>Hoàn thành</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card text-center">
                            <h3 class="mb-1">{{ month_stats.days_active }}</h3>
                            <small>Ngày làm việc</small>
                        </div>
                    </div>
                </div>

                <!-- Biểu đồ theo mục tiêu -->
                <h6 class="mb-3">Phân Bố Theo Mục Tiêu</h6>
                <div class="row">
                    {% for goal_id, info in month_by_goal.items() %}
                    <div class="col-md-6 mb-3">
                        <div class="card" style="background: #f8f9fa; border: 2px solid #dee2e6;">
                            <div class="card-body">
                                <h6 class="mb-2">
                                    <i class="bi bi-bullseye text-primary"></i> 
                                    {{ info.goal_title }}
                                </h6>
                                
                                <div class="d-flex justify-content-between mb-2">
                                    <span><strong>Số hoạt động:</strong></span>
                                    <span class="badge bg-primary">{{ info.tasks|length }}</span>
                                </div>
                                
                                <div class="progress" style="height: 10px;">
                                    <div class="progress-bar progress-bar-custom" 
                                         style="width: {{ (info.tasks|length / month_stats.total_activities * 100)|round }}%;">
                                    </div>
                                </div>
                                
                                <small class="text-muted mt-2 d-block">
                                    <i class="bi bi-percent"></i>
                                    {{ (info.tasks|length / month_stats.total_activities * 100)|round(1) }}% tổng hoạt động
                                </small>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="alert alert-secondary alert-custom">
                    <i class="bi bi-info-circle"></i> 
                    Chưa có hoạt động nào trong tháng này.
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Ghi chú -->
    <div class="alert alert-info alert-custom mt-4">
        <i class="bi bi-lightbulb"></i> <strong>Lưu ý:</strong> 
        Tiến độ được tính tự động dựa trên số lượng hoạt động bạn đã tạo. 
        Càng nhiều hoạt động = Càng tiến bộ! 💪
    </div>
</div>
{% endblock %}'''

# ============================================================
# 8. reports.html - Báo cáo
# ============================================================
templates['reports.html'] = '''{% extends "base.html" %}

{% block title %}Báo Cáo{% endblock %}

{% block content %}
<div class="container-fluid">
    <h2 class="mb-4"><i class="bi bi-bar-chart"></i> Báo Cáo & Thống Kê</h2>

    <!-- Báo cáo tuần -->
    <div class="card goal-card mb-4">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5><i class="bi bi-calendar-week"></i> Báo Cáo Tuần ({{ week_range }})</h5>
                <button class="btn btn-primary-custom btn-sm" onclick="sendWeeklyReport()">
                    <i class="bi bi-telegram"></i> Gửi Telegram
                </button>
            </div>

            {% if week_by_goal %}
                {% for goal_id, info in week_by_goal.items() %}
                <div class="mb-4 pb-3 {% if not loop.last %}border-bottom{% endif %}">
                    <h6 class="mb-3">
                        <i class="bi bi-bullseye text-primary"></i> 
                        <strong>{{ loop.index }}. {{ info.goal_title }}</strong>
                        <span class="badge bg-primary ms-2">{{ info.tasks|length }} hoạt động</span>
                    </h6>
                    
                    <div class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th width="50">#</th>
                                    <th>Hoạt Động</th>
                                    <th width="100">Ngày</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for task in info.tasks %}
                                <tr>
                                    <td>{{ loop.index }}</td>
                                    <td>
                                        <i class="bi bi-check-circle text-success"></i> {{ task.title }}
                                        {% if task.note %}
                                        <br><small class="text-muted">{{ task.note }}</small>
                                        {% endif %}
                                    </td>
                                    <td><small>{{ task.created_at }}</small></td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                {% endfor %}
                
                <div class="alert alert-success alert-custom mt-3">
                    <i class="bi bi-trophy"></i> <strong>Tuyệt vời!</strong> 
                    Bạn đã hoàn thành 
                    {% set total_tasks = namespace(value=0) %}
                    {% for goal_id, info in week_by_goal.items() %}
                        {% set total_tasks.value = total_tasks.value + info.tasks|length %}
                    {% endfor %}
                    {{ total_tasks.value }} hoạt động trong tuần này!
                </div>
            {% else %}
                <div class="alert alert-secondary alert-custom">
                    <i class="bi bi-info-circle"></i> Chưa có hoạt động nào được ghi nhận trong tuần này.
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Báo cáo tháng -->
    <div class="card goal-card">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5><i class="bi bi-calendar-month"></i> Báo Cáo {{ month_name }}</h5>
                <button class="btn btn-primary-custom btn-sm" onclick="sendMonthlyReport()">
                    <i class="bi bi-telegram"></i> Gửi Telegram
                </button>
            </div>

            {% if month_by_goal %}
                {% set total_month_tasks = namespace(value=0) %}
                {% for goal_id, info in month_by_goal.items() %}
                    {% set total_month_tasks.value = total_month_tasks.value + info.tasks|length %}
                {% endfor %}
                
                <div class="alert alert-info alert-custom mb-3">
                    <i class="bi bi-info-circle"></i> 
                    <strong>Tổng số hoạt động tháng này: {{ total_month_tasks.value }}</strong>
                </div>

                <div class="row">
                    {% for goal_id, info in month_by_goal.items() %}
                    <div class="col-md-6 mb-3">
                        <div class="card" style="background: #f8f9fa; border: 2px solid #dee2e6;">
                            <div class="card-body">
                                <h6 class="mb-3">
                                    <i class="bi bi-bullseye text-primary"></i> {{ info.goal_title }}
                                </h6>
                                <div class="mb-2">
                                    <i class="bi bi-check-circle text-success"></i>
                                    <strong>Số hoạt động:</strong> {{ info.tasks|length }}
                                </div>
                                <small class="text-muted">
                                    <i class="bi bi-calendar-range"></i> 
                                    Từ {{ info.tasks|map(attribute='created_at')|min }} 
                                    đến {{ info.tasks|map(attribute='created_at')|max }}
                                </small>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>

                <div class="alert alert-success alert-custom mt-3">
                    <i class="bi bi-trophy"></i> <strong>Xuất sắc!</strong> 
                    Bạn đã duy trì {{ total_month_tasks.value }} hoạt động trong {{ month_name }}. 
                    Tiếp tục phấn đấu!
                </div>
            {% else %}
                <div class="alert alert-secondary alert-custom">
                    <i class="bi bi-info-circle"></i> Chưa có hoạt động nào được ghi nhận trong tháng này.
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function sendWeeklyReport() {
    if (!confirm('Gửi báo cáo tuần đến Telegram?')) return;
    
    fetch('/api/send-weekly-reminder', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert('✅ ' + data.message);
            } else {
                alert('❌ ' + data.message);
            }
        })
        .catch(err => alert('Lỗi: ' + err));
}

function sendMonthlyReport() {
    if (!confirm('Gửi báo cáo tháng đến Telegram?')) return;
    
    fetch('/api/send-monthly-review', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert('✅ ' + data.message);
            } else {
                alert('❌ ' + data.message);
            }
        })
        .catch(err => alert('Lỗi: ' + err));
}
</script>
{% endblock %}'''

# ============================================================
# WRITE ALL FILES
# ============================================================
print("="*70)
print("🚀 TẠO TẤT CẢ TEMPLATES")
print("="*70)

for filename, content in templates.items():
    filepath = os.path.join('templates', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Đã tạo {filepath}")

print("\n"+"="*70)
print("🎉 HOÀN THÀNH!")
print("="*70)
print(f"\n📁 Đã tạo {len(templates)} templates:")
for filename in templates.keys():
    print(f"   • {filename}")
print("\n💡 Bây giờ bạn có thể chạy: python app.py")
print("="*70)
