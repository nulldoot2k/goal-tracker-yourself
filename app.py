#!/usr/bin/env python3
"""
app.py - Flask Web Application (Updated with Manual Backup)
- Thêm: Backup thủ công tải về máy
- Thêm: Backup thủ công gửi Telegram
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
from storage import get_storage
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# APP INITIALIZATION
# ============================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Storage Manager
MONGO_URI = os.getenv('MONGO_URI', None)
storage = get_storage(mongo_uri=MONGO_URI)

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
TELEGRAM_THREAD_ID = os.getenv('TELEGRAM_THREAD_ID', '')


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def send_telegram_message(message):
    """Gửi tin nhắn qua Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False, "Chưa cấu hình Telegram trong .env"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    if TELEGRAM_THREAD_ID:
        payload["message_thread_id"] = TELEGRAM_THREAD_ID
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True, "Đã gửi thành công!"
        else:
            return False, f"Lỗi: {response.text}"
    except Exception as e:
        return False, f"Lỗi kết nối: {str(e)}"


def send_telegram_file(file_path, caption=""):
    """Gửi file qua Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False, "Chưa cấu hình Telegram"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
            
            if TELEGRAM_THREAD_ID:
                data['message_thread_id'] = TELEGRAM_THREAD_ID
            
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                return True, "Đã gửi file thành công!"
            else:
                return False, f"Lỗi: {response.text}"
    except Exception as e:
        return False, f"Lỗi: {str(e)}"


def get_week_range(date=None):
    """Lấy ngày đầu và cuối tuần (Thứ 2 - Chủ Nhật)"""
    if date is None:
        date = datetime.now()
    
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    
    return start, end


# ============================================================
# WEB ROUTES
# ============================================================

@app.route('/')
def index():
    """Dashboard - Trang chủ"""
    data = storage.load_data()
    
    # Thống kê
    total_goals = len(data['goals'])
    active_goals = len([g for g in data['goals'] if g.get('status') == 'active'])
    completed_goals = len([g for g in data['goals'] if g.get('status') == 'completed'])
    
    # Đếm sub tasks tuần này
    week_start, week_end = get_week_range()
    week_subtasks = len([t for t in data['sub_tasks'] 
                         if week_start.date() <= datetime.strptime(t['created_at'], "%Y-%m-%d").date() <= week_end.date()])
    
    stats = {
        'total_goals': total_goals,
        'active_goals': active_goals,
        'completed_goals': completed_goals,
        'week_subtasks': week_subtasks
    }
    
    # === PHÂN TRANG CHO MỤC TIÊU TRÊN DASHBOARD ===
    page = request.args.get('page', 1, type=int)
    per_page = 2  # Bạn có thể đổi thành 5, 8, 9, 12 tùy thích
    
    all_goals = data['goals']
    total_goals_count = len(all_goals)  # để hiển thị tổng số
    
    start = (page - 1) * per_page
    end = start + per_page
    paginated_goals = all_goals[start:end]
    
    total_pages = (total_goals_count + per_page - 1) // per_page if total_goals_count > 0 else 1
    
    return render_template('index.html', 
                           goals=paginated_goals,
                           stats=stats,
                           telegram_configured=bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID),
                           page=page,
                           total_pages=total_pages,
                           total_goals=total_goals_count)


@app.route('/goals')
def goals():
    """Danh sách mục tiêu"""
    data = storage.load_data()
    
    # Đếm số hoạt động cho mỗi goal
    for goal in data['goals']:
        goal['subtask_count'] = len([t for t in data['sub_tasks'] if t['goal_id'] == goal['id']])
    
    return render_template('goals.html', goals=data['goals'])


@app.route('/goals/add', methods=['GET', 'POST'])
def add_goal():
    """Thêm mục tiêu mới"""
    if request.method == 'POST':
        data = storage.load_data()
        
        max_id = max([g['id'] for g in data['goals']], default=0)
        
        goal = {
            "id": max_id + 1,
            "title": request.form['title'],
            "description": request.form.get('description', ''),
            "target_date": request.form.get('target_date', '2026-12-31'),
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "status": "active",
            "progress": 0
        }
        
        data['goals'].append(goal)
        storage.save_data(data)
        
        flash('✅ Đã tạo mục tiêu mới thành công!', 'success')
        return redirect(url_for('goal_detail', goal_id=goal['id']))
    
    return render_template('add_goal.html')


@app.route('/goals/<int:goal_id>')
def goal_detail(goal_id):
    """Chi tiết mục tiêu - CHỈ quản lý hoạt động"""
    data = storage.load_data()
    goal = next((g for g in data['goals'] if g['id'] == goal_id), None)
    
    if not goal:
        flash('❌ Không tìm thấy mục tiêu', 'danger')
        return redirect(url_for('goals'))
    
    # Lấy danh sách hoạt động
    sub_tasks = [t for t in data['sub_tasks'] if t['goal_id'] == goal_id]
    sub_tasks.sort(key=lambda x: (x['created_at'], x['created_time']), reverse=True)
    
    return render_template('goal_detail.html', goal=goal, sub_tasks=sub_tasks)


@app.route('/goals/<int:goal_id>/edit', methods=['GET', 'POST'])
def edit_goal(goal_id):
    """Chỉnh sửa mục tiêu"""
    data = storage.load_data()
    goal = next((g for g in data['goals'] if g['id'] == goal_id), None)
    
    if not goal:
        flash('❌ Không tìm thấy mục tiêu', 'danger')
        return redirect(url_for('goals'))
    
    if request.method == 'POST':
        goal['title'] = request.form['title']
        goal['description'] = request.form.get('description', '')
        goal['target_date'] = request.form.get('target_date')
        goal['status'] = request.form.get('status', 'active')
        
        storage.save_data(data)
        flash('✅ Đã cập nhật mục tiêu thành công!', 'success')
        return redirect(url_for('goal_detail', goal_id=goal_id))
    
    return render_template('edit_goal.html', goal=goal)


@app.route('/goals/<int:goal_id>/delete', methods=['POST'])
def delete_goal(goal_id):
    """Xóa mục tiêu"""
    data = storage.load_data()
    data['goals'] = [g for g in data['goals'] if g['id'] != goal_id]
    data['sub_tasks'] = [t for t in data['sub_tasks'] if t['goal_id'] != goal_id]
    storage.save_data(data)
    
    flash('✅ Đã xóa mục tiêu thành công!', 'success')
    return redirect(url_for('goals'))


@app.route('/goals/<int:goal_id>/subtask/add', methods=['POST'])
def add_subtask(goal_id):
    """Thêm hoạt động (sub task)"""
    data = storage.load_data()
    goal = next((g for g in data['goals'] if g['id'] == goal_id), None)
    
    if not goal:
        flash('❌ Không tìm thấy mục tiêu', 'danger')
        return redirect(url_for('goals'))
    
    max_id = max([t['id'] for t in data['sub_tasks']], default=0)
    
    subtask = {
        "id": max_id + 1,
        "goal_id": goal_id,
        "goal_title": goal['title'],
        "title": request.form['title'],
        "note": request.form.get('note', ''),
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "created_time": datetime.now().strftime("%H:%M:%S")
    }
    
    data['sub_tasks'].append(subtask)
    storage.save_data(data)
    
    flash('✅ Đã thêm hoạt động mới!', 'success')
    return redirect(url_for('goal_detail', goal_id=goal_id))


@app.route('/subtask/<int:subtask_id>/delete', methods=['POST'])
def delete_subtask(subtask_id):
    """Xóa hoạt động"""
    data = storage.load_data()
    subtask = next((t for t in data['sub_tasks'] if t['id'] == subtask_id), None)
    
    if not subtask:
        flash('❌ Không tìm thấy hoạt động', 'danger')
        return redirect(url_for('index'))
    
    goal_id = subtask['goal_id']
    data['sub_tasks'] = [t for t in data['sub_tasks'] if t['id'] != subtask_id]
    storage.save_data(data)
    
    flash('✅ Đã xóa hoạt động!', 'success')
    return redirect(url_for('goal_detail', goal_id=goal_id))


@app.route('/progress')
def progress():
    """Trang Tiến Độ - READ ONLY, tự động tính"""
    data = storage.load_data()
    
    today = datetime.now()
    week_start, week_end = get_week_range()
    month_start = today.replace(day=1)
    
    # ===== TIẾN ĐỘ TUẦN =====
    week_tasks = [t for t in data['sub_tasks'] 
                  if week_start.date() <= datetime.strptime(t['created_at'], "%Y-%m-%d").date() <= week_end.date()]
    
    # Thống kê tuần
    week_goals = set([t['goal_id'] for t in week_tasks])
    week_days = set([t['created_at'] for t in week_tasks])
    
    week_stats = {
        'total_activities': len(week_tasks),
        'active_goals': len(week_goals),
        'avg_per_day': round(len(week_tasks) / 7, 1) if week_tasks else 0
    }
    
    # Nhóm theo goal
    week_by_goal = {}
    for task in week_tasks:
        goal_id = task['goal_id']
        if goal_id not in week_by_goal:
            week_by_goal[goal_id] = {
                'goal_title': task['goal_title'],
                'tasks': []
            }
        week_by_goal[goal_id]['tasks'].append(task)
    
    # ===== TIẾN ĐỘ THÁNG =====
    month_tasks = [t for t in data['sub_tasks'] 
                   if datetime.strptime(t['created_at'], "%Y-%m-%d").date() >= month_start.date()]
    
    # Thống kê tháng
    month_goals = set([t['goal_id'] for t in month_tasks])
    month_days = set([t['created_at'] for t in month_tasks])
    
    # Đếm goals hoàn thành trong tháng
    completed_in_month = 0
    for goal in data['goals']:
        if goal.get('status') == 'completed':
            # Kiểm tra nếu có hoạt động trong tháng
            has_activity = any(t['goal_id'] == goal['id'] for t in month_tasks)
            if has_activity:
                completed_in_month += 1
    
    month_stats = {
        'total_activities': len(month_tasks),
        'active_goals': len(month_goals),
        'completed_goals': completed_in_month,
        'days_active': len(month_days)
    }
    
    # Nhóm theo goal
    month_by_goal = {}
    for task in month_tasks:
        goal_id = task['goal_id']
        if goal_id not in month_by_goal:
            month_by_goal[goal_id] = {
                'goal_title': task['goal_title'],
                'tasks': []
            }
        month_by_goal[goal_id]['tasks'].append(task)
    
    return render_template('progress.html',
                         week_stats=week_stats,
                         week_by_goal=week_by_goal,
                         week_range=f"{week_start.strftime('%d/%m')} - {week_end.strftime('%d/%m/%Y')}",
                         month_stats=month_stats,
                         month_by_goal=month_by_goal,
                         month_name=f"{today.month}/{today.year}")


@app.route('/reports')
def reports():
    """Báo cáo - CHỈ hiển thị khi có đủ dữ liệu"""
    data = storage.load_data()
    
    today = datetime.now()
    week_start, week_end = get_week_range()
    month_start = today.replace(day=1)
    
    # Kiểm tra dữ liệu tuần
    week_tasks = [t for t in data['sub_tasks'] 
                  if week_start.date() <= datetime.strptime(t['created_at'], "%Y-%m-%d").date() <= week_end.date()]
    
    # Kiểm tra dữ liệu tháng
    month_tasks = [t for t in data['sub_tasks'] 
                   if datetime.strptime(t['created_at'], "%Y-%m-%d").date() >= month_start.date()]
    
    # Nếu KHÔNG có dữ liệu → 404
    if not week_tasks and not month_tasks:
        flash('⚠️ Chưa có dữ liệu để tạo báo cáo. Hãy thêm hoạt động trước!', 'warning')
        return redirect(url_for('index'))
    
    # Nhóm báo cáo tuần
    week_by_goal = {}
    for task in week_tasks:
        goal_id = task['goal_id']
        if goal_id not in week_by_goal:
            week_by_goal[goal_id] = {
                'goal_title': task['goal_title'],
                'tasks': []
            }
        week_by_goal[goal_id]['tasks'].append(task)
    
    # Nhóm báo cáo tháng
    month_by_goal = {}
    for task in month_tasks:
        goal_id = task['goal_id']
        if goal_id not in month_by_goal:
            month_by_goal[goal_id] = {
                'goal_title': task['goal_title'],
                'tasks': []
            }
        month_by_goal[goal_id]['tasks'].append(task)
    
    return render_template('reports.html', 
                         week_by_goal=week_by_goal,
                         month_by_goal=month_by_goal,
                         week_range=f"{week_start.strftime('%d/%m')} - {week_end.strftime('%d/%m/%Y')}",
                         month_name=f"Tháng {today.month}/{today.year}")


# ============================================================
# API ENDPOINTS
# ============================================================

@app.route('/api/download-backup', methods=['GET'])
def api_download_backup():
    """Backup thủ công: Tải file JSON về máy"""
    try:
        json_file = 'data/goals_data.json'
        
        if not os.path.exists(json_file):
            return jsonify({'success': False, 'message': 'File không tồn tại'}), 404
        
        # Tạo tên file với timestamp
        today = datetime.now()
        download_name = f"goals_backup_{today.strftime('%Y%m%d_%H%M%S')}.json"
        
        return send_file(
            json_file,
            as_attachment=True,
            download_name=download_name,
            mimetype='application/json'
        )
    except Exception as e:
        logger.error(f"Download backup error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/backup-to-telegram', methods=['POST'])
def api_backup_to_telegram():
    """Backup thủ công: Gửi JSON về Telegram"""
    try:
        output_path = storage.export_json()
        
        today = datetime.now()
        caption = f"💾 Backup thủ công\n🗓️ {today.strftime('%d/%m/%Y %H:%M:%S')}"
        
        success, msg = send_telegram_file(output_path, caption)
        
        # Xóa file tạm
        if os.path.exists(output_path):
            os.remove(output_path)
        
        return jsonify({'success': success, 'message': msg})
    except Exception as e:
        logger.error(f"Backup to Telegram error: {e}")
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/test-telegram', methods=['POST'])
def api_test_telegram():
    """Test Telegram bot"""
    message = "🧪 *Test message từ 2026 Goal Tracker!*\n\n✅ Kết nối thành công!"
    success, msg = send_telegram_message(message)
    return jsonify({'success': success, 'message': msg})


@app.route('/api/send-weekly-reminder', methods=['POST'])
def api_send_weekly_reminder():
    """Gửi báo cáo tuần qua Telegram"""
    data = storage.load_data()
    
    week_start, week_end = get_week_range()
    
    week_tasks = [t for t in data['sub_tasks'] 
                  if week_start.date() <= datetime.strptime(t['created_at'], "%Y-%m-%d").date() <= week_end.date()]
    
    # Không gửi nếu không có dữ liệu
    if not week_tasks:
        return jsonify({'success': False, 'message': 'Chưa có dữ liệu tuần này để gửi báo cáo'})
    
    message = f"📅 *BÁO CÁO TUẦN*\n"
    message += f"_{week_start.strftime('%d/%m')} - {week_end.strftime('%d/%m/%Y')}_\n\n"
    
    by_goal = {}
    for task in week_tasks:
        goal_id = task['goal_id']
        if goal_id not in by_goal:
            by_goal[goal_id] = {
                'title': task['goal_title'],
                'tasks': []
            }
        by_goal[goal_id]['tasks'].append(task)
    
    message += f"✅ *Tổng cộng: {len(week_tasks)} hoạt động*\n\n"
    
    for idx, (goal_id, info) in enumerate(by_goal.items(), 1):
        message += f"*{idx}. {info['title']}* ({len(info['tasks'])} hoạt động)\n"
        for task in info['tasks']:
            date_str = datetime.strptime(task['created_at'], "%Y-%m-%d").strftime("%d/%m")
            message += f"   • {task['title']} - {date_str}\n"
        message += "\n"
    
    message += "💪 Tiếp tục phấn đấu tuần tới!"
    
    success, msg = send_telegram_message(message)
    return jsonify({'success': success, 'message': msg})


@app.route('/api/send-monthly-review', methods=['POST'])
def api_send_monthly_review():
    """Gửi báo cáo tháng qua Telegram"""
    data = storage.load_data()
    today = datetime.now()
    
    month_start = today.replace(day=1)
    
    month_tasks = [t for t in data['sub_tasks'] 
                   if datetime.strptime(t['created_at'], "%Y-%m-%d").date() >= month_start.date()]
    
    # Không gửi nếu không có dữ liệu
    if not month_tasks:
        return jsonify({'success': False, 'message': 'Chưa có dữ liệu tháng này để gửi báo cáo'})
    
    message = f"📊 *BÁO CÁO THÁNG {today.month}/{today.year}*\n\n"
    
    by_goal = {}
    for task in month_tasks:
        goal_id = task['goal_id']
        if goal_id not in by_goal:
            by_goal[goal_id] = {
                'title': task['goal_title'],
                'count': 0
            }
        by_goal[goal_id]['count'] += 1
    
    message += f"✅ *Tổng số hoạt động: {len(month_tasks)}*\n\n"
    
    for idx, (goal_id, info) in enumerate(by_goal.items(), 1):
        message += f"{idx}. *{info['title']}*\n"
        message += f"   📊 Số hoạt động: {info['count']}\n\n"
    
    message += "🎯 Chúc bạn đạt được mục tiêu 2026!"
    
    success, msg = send_telegram_message(message)
    return jsonify({'success': success, 'message': msg})


@app.route('/api/send-monthly-backup', methods=['POST'])
def api_send_monthly_backup():
    """Gửi backup JSON tháng qua Telegram (tự động)"""
    try:
        output_path = storage.export_json()
        
        today = datetime.now()
        caption = f"📦 Backup tháng {today.month}/{today.year}\n🗓️ {today.strftime('%d/%m/%Y %H:%M:%S')}"
        
        success, msg = send_telegram_file(output_path, caption)
        
        if os.path.exists(output_path):
            os.remove(output_path)
        
        return jsonify({'success': success, 'message': msg})
    except Exception as e:
        logger.error(f"Monthly backup error: {e}")
        return jsonify({'success': False, 'message': str(e)})


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info("=" * 60)
    logger.info("🚀 2026 GOAL TRACKER - STARTING")
    logger.info("=" * 60)
    logger.info(f"📍 Port: {port}")
    logger.info(f"🔧 Debug: {debug}")
    logger.info(f"💾 Storage: JSON + MongoDB")
    logger.info(f"📱 Telegram: {'✅ Configured' if TELEGRAM_BOT_TOKEN else '❌ Not configured'}")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
