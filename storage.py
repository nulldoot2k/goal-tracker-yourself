#!/usr/bin/env python3
"""
storage.py - Dual Storage Manager (JSON + MongoDB)
Tự động sync giữa JSON và MongoDB
"""

import json
import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StorageManager:
    """Quản lý lưu trữ với JSON (primary) và MongoDB (backup)"""
    
    def __init__(self, json_file='data/goals_data.json', mongo_uri=None):
        self.json_file = json_file
        self.mongo_uri = mongo_uri
        self.mongo_enabled = False
        self.db = None
        self.collection = None
        
        # Đảm bảo thư mục data tồn tại
        os.makedirs('data', exist_ok=True)
        
        # Kết nối MongoDB nếu có
        if mongo_uri:
            self._connect_mongodb()
    
    def _connect_mongodb(self):
        """Kết nối MongoDB (không bắt buộc)"""
        try:
            client = MongoClient(
                self.mongo_uri,
                serverSelectionTimeoutMS=3000,  # Timeout 3s
                connectTimeoutMS=3000
            )
            # Test connection
            client.admin.command('ping')
            
            self.db = client['goal_tracker_2026']
            self.collection = self.db['goals_data']
            self.mongo_enabled = True
            
            logger.info("✅ MongoDB connected successfully")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.warning(f"⚠️  MongoDB not available: {e}")
            logger.info("📁 Using JSON file storage only")
            self.mongo_enabled = False
        except Exception as e:
            logger.error(f"❌ MongoDB connection error: {e}")
            self.mongo_enabled = False
    
    def load_data(self):
        """Tải dữ liệu từ JSON (primary source)"""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"📖 Loaded data from {self.json_file}")
                return self._ensure_structure(data)
            except Exception as e:
                logger.error(f"❌ Error loading JSON: {e}")
                return self._empty_structure()
        else:
            logger.info("📝 Creating new data file")
            return self._empty_structure()
    
    def save_data(self, data):
        """
        Lưu dữ liệu vào cả JSON và MongoDB
        JSON là primary, MongoDB là backup tự động
        """
        # 1. Lưu vào JSON (primary)
        try:
            data = self._ensure_structure(data)
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"💾 Saved to JSON: {self.json_file}")
        except Exception as e:
            logger.error(f"❌ Error saving JSON: {e}")
            raise
        
        # 2. Backup vào MongoDB (nếu có)
        if self.mongo_enabled:
            try:
                # Thêm timestamp
                backup_data = data.copy()
                backup_data['_backup_timestamp'] = datetime.now().isoformat()
                backup_data['_backup_source'] = 'auto_sync'
                
                # Upsert (insert hoặc update)
                self.collection.replace_one(
                    {'_id': 'current_data'},
                    {**backup_data, '_id': 'current_data'},
                    upsert=True
                )
                logger.info("🔄 Synced to MongoDB backup")
            except Exception as e:
                logger.warning(f"⚠️  MongoDB backup failed: {e}")
                # Không raise error vì MongoDB chỉ là backup
    
    def restore_from_mongodb(self):
        """Khôi phục dữ liệu từ MongoDB"""
        if not self.mongo_enabled:
            logger.error("❌ MongoDB not available")
            return None
        
        try:
            data = self.collection.find_one({'_id': 'current_data'})
            if data:
                # Xóa các field internal của MongoDB
                data.pop('_id', None)
                data.pop('_backup_timestamp', None)
                data.pop('_backup_source', None)
                
                logger.info("✅ Restored from MongoDB")
                return self._ensure_structure(data)
            else:
                logger.warning("⚠️  No backup found in MongoDB")
                return None
        except Exception as e:
            logger.error(f"❌ Error restoring from MongoDB: {e}")
            return None
    
    def export_json(self, output_path=None):
        """Export dữ liệu ra file JSON"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"data/backup_export_{timestamp}.json"
        
        try:
            data = self.load_data()
            # Thêm metadata
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'export_version': '1.0',
                'data': data
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"📦 Exported to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"❌ Export failed: {e}")
            raise
    
    def import_json(self, import_path):
        """Import dữ liệu từ file JSON"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Kiểm tra format
            if 'data' in import_data:
                data = import_data['data']
            else:
                data = import_data
            
            # Lưu vào hệ thống
            self.save_data(data)
            logger.info(f"📥 Imported from {import_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Import failed: {e}")
            return False
    
    def get_backup_info(self):
        """Lấy thông tin backup"""
        info = {
            'json_exists': os.path.exists(self.json_file),
            'json_size': 0,
            'mongodb_enabled': self.mongo_enabled,
            'mongodb_last_backup': None
        }
        
        # JSON info
        if info['json_exists']:
            info['json_size'] = os.path.getsize(self.json_file)
        
        # MongoDB info
        if self.mongo_enabled:
            try:
                backup = self.collection.find_one({'_id': 'current_data'})
                if backup:
                    info['mongodb_last_backup'] = backup.get('_backup_timestamp')
            except:
                pass
        
        return info
    
    def _ensure_structure(self, data):
        """Đảm bảo data có đủ structure cần thiết"""
        if 'goals' not in data:
            data['goals'] = []
        if 'sub_tasks' not in data:
            data['sub_tasks'] = []
        if 'progress_logs' not in data:
            data['progress_logs'] = []
        return data
    
    def _empty_structure(self):
        """Trả về structure rỗng"""
        return {
            "goals": [],
            "sub_tasks": [],
            "progress_logs": []
        }


# Singleton instance
_storage_instance = None

def get_storage(mongo_uri=None):
    """Lấy storage instance (singleton)"""
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = StorageManager(mongo_uri=mongo_uri)
    return _storage_instance
