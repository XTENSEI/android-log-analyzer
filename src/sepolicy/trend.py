"""
Trend Analysis Module

Historical trend analysis of AVC denials using SQLite for persistence.
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime


TREND_DB_DIR = os.path.expanduser("~/.cache/sepolicy_patcher")
TREND_DB_PATH = os.path.join(TREND_DB_DIR, "trends.db")


def init_database() -> None:
    """Initialize the trend database."""
    os.makedirs(TREND_DB_DIR, exist_ok=True)
    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS denials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            source TEXT,
            target TEXT,
            tclass TEXT,
            permission TEXT,
            raw TEXT
        )
    ''')
    c.execute('''
        CREATE INDEX IF NOT EXISTS idx_source ON denials(source)
    ''')
    c.execute('''
        CREATE INDEX IF NOT EXISTS idx_target ON denials(target)
    ''')
    conn.commit()
    conn.close()


def store_denial(denial: Dict[str, Any]) -> None:
    """Store an AVC denial in the database."""
    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()
    
    for perm in denial.get('permissions', []):
        c.execute(
            "INSERT INTO denials (timestamp, source, target, tclass, permission, raw) VALUES (?,?,?,?,?,?)",
            (
                denial.get('timestamp', datetime.now().timestamp()),
                denial.get('source', ''),
                denial.get('target', ''),
                denial.get('class', ''),
                perm,
                denial.get('raw', '')
            )
        )
    
    conn.commit()
    conn.close()


def get_top_denials(limit: int = 20) -> List[Tuple[str, str, str, str, int]]:
    """Get the most frequent denials."""
    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT source, target, tclass, permission, COUNT(*) as cnt
        FROM denials
        GROUP BY source, target, tclass, permission
        ORDER BY cnt DESC
        LIMIT ?
    ''', (limit,))
    results = c.fetchall()
    conn.close()
    return results


def get_top_sources(limit: int = 10) -> List[Tuple[str, int]]:
    """Get the most active source domains."""
    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT source, COUNT(*) as cnt
        FROM denials
        GROUP BY source
        ORDER BY cnt DESC
        LIMIT ?
    ''', (limit,))
    results = c.fetchall()
    conn.close()
    return results


def get_top_targets(limit: int = 10) -> List[Tuple[str, int]]:
    """Get the most frequently targeted types."""
    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT target, COUNT(*) as cnt
        FROM denials
        GROUP BY target
        ORDER BY cnt DESC
        LIMIT ?
    ''', (limit,))
    results = c.fetchall()
    conn.close()
    return results


def get_denials_by_time_range(
    start_time: float,
    end_time: float
) -> List[Tuple[float, str, str, str, str]]:
    """Get denials within a time range."""
    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT timestamp, source, target, tclass, permission
        FROM denials
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp DESC
    ''', (start_time, end_time))
    results = c.fetchall()
    conn.close()
    return results


def clear_history() -> None:
    """Clear all trend data."""
    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM denials")
    conn.commit()
    conn.close()


def get_database_stats() -> Dict[str, Any]:
    """Get database statistics."""
    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM denials")
    total = c.fetchone()[0]
    
    c.execute("SELECT COUNT(DISTINCT source) FROM denials")
    unique_sources = c.fetchone()[0]
    
    c.execute("SELECT COUNT(DISTINCT target) FROM denials")
    unique_targets = c.fetchone()[0]
    
    c.execute("SELECT MIN(timestamp), MAX(timestamp) FROM denials")
    time_range = c.fetchone()
    
    conn.close()
    
    return {
        'total_denials': total,
        'unique_sources': unique_sources,
        'unique_targets': unique_targets,
        'oldest_entry': datetime.fromtimestamp(time_range[0]).isoformat() if time_range[0] else None,
        'newest_entry': datetime.fromtimestamp(time_range[1]).isoformat() if time_range[1] else None,
    }


def print_trend_report(limit: int = 20) -> None:
    """Print a formatted trend report."""
    print("\n=== AVC Denial Trend Report ===\n")
    
    stats = get_database_stats()
    print(f"Total denials recorded: {stats['total_denials']}")
    print(f"Unique sources: {stats['unique_sources']}")
    print(f"Unique targets: {stats['unique_targets']}")
    
    print("\n--- Top Denials by Frequency ---")
    for src, tgt, cls, perm, cnt in get_top_denials(limit):
        print(f"  {src} -> {tgt} : {cls} ({perm}) - {cnt} times")
    
    print("\n--- Top Source Domains ---")
    for src, cnt in get_top_sources(10):
        print(f"  {src} - {cnt} denials")
    
    print("\n--- Top Target Types ---")
    for tgt, cnt in get_top_targets(10):
        print(f"  {tgt} - {cnt} denials")
