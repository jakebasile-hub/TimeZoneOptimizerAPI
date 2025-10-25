import os
import sqlite3
from datetime import datetime, timedelta
from typing import Optional
import hashlib


class AuthManager:
    def __init__(self, db_path: str = "api_usage.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for API usage tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                key_hash TEXT PRIMARY KEY,
                user_id TEXT,
                created_at TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_hash TEXT,
                endpoint TEXT,
                timestamp TIMESTAMP,
                cost REAL DEFAULT 0.001,
                FOREIGN KEY (key_hash) REFERENCES api_keys (key_hash)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_usage (
                key_hash TEXT,
                date TEXT,
                request_count INTEGER DEFAULT 0,
                total_cost REAL DEFAULT 0,
                PRIMARY KEY (key_hash, date),
                FOREIGN KEY (key_hash) REFERENCES api_keys (key_hash)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash API key for secure storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validate API key exists and is active"""
        if not api_key:
            return False
        
        key_hash = self.hash_api_key(api_key)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT is_active FROM api_keys WHERE key_hash = ?", 
            (key_hash,)
        )
        result = cursor.fetchone()
        conn.close()
        
        return result and result[0] == 1
    
    def log_usage(self, api_key: str, endpoint: str):
        """Log API usage for billing"""
        key_hash = self.hash_api_key(api_key)
        today = datetime.now().date().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Log the request
        cursor.execute(
            "INSERT INTO usage_logs (key_hash, endpoint, timestamp, cost) VALUES (?, ?, ?, ?)",
            (key_hash, endpoint, datetime.now(), 0.001)
        )
        
        # Update daily usage
        cursor.execute('''
            INSERT OR REPLACE INTO daily_usage (key_hash, date, request_count, total_cost)
            VALUES (
                ?,
                ?,
                COALESCE((SELECT request_count FROM daily_usage WHERE key_hash = ? AND date = ?), 0) + 1,
                COALESCE((SELECT total_cost FROM daily_usage WHERE key_hash = ? AND date = ?), 0) + 0.001
            )
        ''', (key_hash, today, key_hash, today, key_hash, today))
        
        conn.commit()
        conn.close()
    
    def check_rate_limit(self, api_key: str) -> bool:
        """Check if user has exceeded daily rate limit"""
        key_hash = self.hash_api_key(api_key)
        today = datetime.now().date().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT request_count FROM daily_usage WHERE key_hash = ? AND date = ?",
            (key_hash, today)
        )
        result = cursor.fetchone()
        conn.close()
        
        daily_requests = result[0] if result else 0
        return daily_requests < 100  # Free tier limit
    
    def create_api_key(self, user_id: str) -> str:
        """Create a new API key for a user"""
        # Generate a simple API key (in production, use a more secure method)
        api_key = f"tz_opt_{hashlib.sha256(f'{user_id}_{datetime.now()}'.encode()).hexdigest()[:16]}"
        key_hash = self.hash_api_key(api_key)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO api_keys (key_hash, user_id, created_at) VALUES (?, ?, ?)",
            (key_hash, user_id, datetime.now())
        )
        
        conn.commit()
        conn.close()
        
        return api_key


# Global auth manager instance
auth_manager = AuthManager()
