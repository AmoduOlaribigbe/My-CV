"""
SecureVigil Database Module
SQLite persistence for vulnerability scan results and historical tracking
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json


DB_NAME = "vulnerabilities.db"


def init_db(db_path: str = DB_NAME) -> None:
    """
    Initialize database schema
    
    Args:
        db_path: Path to SQLite database file
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Main scans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id TEXT NOT NULL,
            host TEXT NOT NULL,
            hostname TEXT,
            port INTEGER NOT NULL,
            protocol TEXT,
            service TEXT,
            product TEXT,
            version TEXT,
            risk TEXT,
            cvss_estimate REAL,
            recommendation TEXT,
            scan_date TEXT NOT NULL,
            FOREIGN KEY (scan_id) REFERENCES scan_summary(scan_id)
        )
    """)

    # Scan summary table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id TEXT UNIQUE NOT NULL,
            target TEXT NOT NULL,
            total_findings INTEGER,
            high_risk INTEGER,
            medium_risk INTEGER,
            low_risk INTEGER,
            risk_score INTEGER,
            scan_date TEXT NOT NULL,
            scan_duration REAL,
            notes TEXT
        )
    """)

    # Create indexes for better query performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_scan_id ON scans(scan_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_risk ON scans(risk)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_host ON scans(host)
    """)

    conn.commit()
    conn.close()
    print("[+] Database initialized successfully")


def save_scan(results: List[Dict], target: str, scan_id: Optional[str] = None, 
              notes: Optional[str] = None, db_path: str = DB_NAME) -> str:
    """
    Save scan results to database
    
    Args:
        results: List of scan results with risk classification
        target: Target IP/range that was scanned
        scan_id: Optional custom scan ID (auto-generated if not provided)
        notes: Optional notes about the scan
        db_path: Path to database file
    
    Returns:
        Scan ID
    """
    if not scan_id:
        scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    scan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Calculate summary statistics
    summary = {
        "total": len(results),
        "high": sum(1 for r in results if r.get("risk") == "HIGH"),
        "medium": sum(1 for r in results if r.get("risk") == "MEDIUM"),
        "low": sum(1 for r in results if r.get("risk") == "LOW"),
    }
    
    # Calculate risk score
    risk_weights = {"HIGH": 10, "MEDIUM": 5, "LOW": 1}
    risk_score = sum(risk_weights.get(r.get("risk", "LOW"), 0) for r in results)

    # Save individual findings
    for item in results:
        cursor.execute("""
            INSERT INTO scans 
            (scan_id, host, hostname, port, protocol, service, product, version, 
             risk, cvss_estimate, recommendation, scan_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scan_id,
            item.get("host", ""),
            item.get("hostname", ""),
            item.get("port", 0),
            item.get("protocol", "tcp"),
            item.get("service", ""),
            item.get("product", ""),
            item.get("version", ""),
            item.get("risk", "LOW"),
            item.get("cvss_estimate", 0.0),
            item.get("recommendation", ""),
            scan_date
        ))

    # Save scan summary
    cursor.execute("""
        INSERT INTO scan_summary 
        (scan_id, target, total_findings, high_risk, medium_risk, low_risk, 
         risk_score, scan_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        scan_id,
        target,
        summary["total"],
        summary["high"],
        summary["medium"],
        summary["low"],
        risk_score,
        scan_date,
        notes
    ))

    conn.commit()
    conn.close()
    
    print(f"[+] Scan results saved successfully (ID: {scan_id})")
    print(f"    Total findings: {summary['total']}")
    print(f"    HIGH: {summary['high']} | MEDIUM: {summary['medium']} | LOW: {summary['low']}")
    
    return scan_id


def get_scan_by_id(scan_id: str, db_path: str = DB_NAME) -> List[Dict]:
    """
    Retrieve specific scan results by ID
    
    Args:
        scan_id: Scan identifier
        db_path: Path to database file
    
    Returns:
        List of scan results
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT host, hostname, port, service, product, version, risk, 
               cvss_estimate, recommendation, scan_date
        FROM scans 
        WHERE scan_id = ?
        ORDER BY risk DESC, port ASC
    """, (scan_id,))
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    return results


def get_all_scans(limit: int = 100, db_path: str = DB_NAME) -> List[Tuple]:
    """
    Retrieve all scan results (limited)
    
    Args:
        limit: Maximum number of results to return
        db_path: Path to database file
    
    Returns:
        List of tuples containing scan data
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT host, port, service, risk, scan_date 
        FROM scans 
        ORDER BY scan_date DESC, risk DESC
        LIMIT ?
    """, (limit,))
    
    data = cursor.fetchall()
    conn.close()
    return data


def get_scan_summaries(limit: int = 10, db_path: str = DB_NAME) -> List[Dict]:
    """
    Get summary of all scans
    
    Args:
        limit: Maximum number of summaries to return
        db_path: Path to database file
    
    Returns:
        List of scan summaries
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT scan_id, target, total_findings, high_risk, medium_risk, 
               low_risk, risk_score, scan_date, notes
        FROM scan_summary 
        ORDER BY scan_date DESC 
        LIMIT ?
    """, (limit,))
    
    columns = [desc[0] for desc in cursor.description]
    summaries = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    return summaries


def get_scan_trends(days: int = 30, db_path: str = DB_NAME) -> List[Dict]:
    """
    Get historical scan trends for analytics
    
    Args:
        days: Number of days to look back
        db_path: Path to database file
    
    Returns:
        List of trend data
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            DATE(scan_date) as date,
            COUNT(*) as scan_count,
            SUM(high_risk) as total_high,
            SUM(medium_risk) as total_medium,
            SUM(low_risk) as total_low,
            AVG(risk_score) as avg_risk_score
        FROM scan_summary 
        WHERE scan_date >= date('now', '-' || ? || ' days')
        GROUP BY DATE(scan_date)
        ORDER BY date DESC
    """, (days,))
    
    columns = [desc[0] for desc in cursor.description]
    trends = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    return trends


def get_high_risk_findings(limit: int = 20, db_path: str = DB_NAME) -> List[Dict]:
    """
    Get all high-risk findings across all scans
    
    Args:
        limit: Maximum number of findings to return
        db_path: Path to database file
    
    Returns:
        List of high-risk findings
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT host, port, service, product, version, recommendation, scan_date
        FROM scans 
        WHERE risk = 'HIGH'
        ORDER BY scan_date DESC
        LIMIT ?
    """, (limit,))
    
    columns = [desc[0] for desc in cursor.description]
    findings = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    return findings


def get_host_history(host: str, db_path: str = DB_NAME) -> List[Dict]:
    """
    Get scan history for specific host
    
    Args:
        host: IP address of host
        db_path: Path to database file
    
    Returns:
        List of scans for the host
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT scan_id, port, service, risk, scan_date
        FROM scans 
        WHERE host = ?
        ORDER BY scan_date DESC
    """, (host,))
    
    columns = [desc[0] for desc in cursor.description]
    history = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    return history


def delete_old_scans(days: int = 90, db_path: str = DB_NAME) -> int:
    """
    Delete scans older than specified days (for cleanup)
    
    Args:
        days: Age threshold in days
        db_path: Path to database file
    
    Returns:
        Number of scans deleted
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get scan IDs to delete
    cursor.execute("""
        SELECT scan_id FROM scan_summary
        WHERE scan_date < date('now', '-' || ? || ' days')
    """, (days,))
    
    scan_ids = [row[0] for row in cursor.fetchall()]
    
    if not scan_ids:
        conn.close()
        return 0
    
    # Delete from both tables
    placeholders = ','.join('?' * len(scan_ids))
    
    cursor.execute(f"""
        DELETE FROM scans WHERE scan_id IN ({placeholders})
    """, scan_ids)
    
    cursor.execute(f"""
        DELETE FROM scan_summary WHERE scan_id IN ({placeholders})
    """, scan_ids)
    
    deleted_count = len(scan_ids)
    conn.commit()
    conn.close()
    
    print(f"[+] Deleted {deleted_count} old scans")
    return deleted_count


if __name__ == "__main__":
    # Example usage
    print("Initializing database...")
    init_db()
    
    print("\nDatabase ready for use!")
    print(f"Database file: {DB_NAME}")
