"""
IT Asset Management Dashboard
Flask-based system for tracking enterprise IT assets
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime, timedelta
import csv
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-in-production'


def init_asset_db():
    """Initialize asset tracking database"""
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_tag TEXT UNIQUE NOT NULL,
            asset_type TEXT NOT NULL,
            hostname TEXT,
            ip_address TEXT,
            location TEXT,
            department TEXT,
            status TEXT DEFAULT 'Active',
            manufacturer TEXT,
            model TEXT,
            serial_number TEXT,
            purchase_date TEXT,
            warranty_expiry TEXT,
            last_maintenance TEXT,
            next_maintenance TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            maintenance_date TEXT NOT NULL,
            maintenance_type TEXT,
            technician TEXT,
            description TEXT,
            cost REAL,
            FOREIGN KEY (asset_id) REFERENCES assets(id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            alert_type TEXT,
            alert_message TEXT,
            alert_date TEXT DEFAULT CURRENT_TIMESTAMP,
            resolved INTEGER DEFAULT 0,
            FOREIGN KEY (asset_id) REFERENCES assets(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("[+] Asset database initialized")


@app.route('/')
def index():
    """Dashboard homepage"""
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()
    
    # Get summary statistics
    cursor.execute("SELECT COUNT(*) FROM assets")
    total_assets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM assets WHERE status = 'Active'")
    active_assets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM assets WHERE status = 'Faulty'")
    faulty_assets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE resolved = 0")
    pending_alerts = cursor.fetchone()[0]
    
    # Get recent assets
    cursor.execute("""
        SELECT id, asset_tag, asset_type, hostname, location, status 
        FROM assets 
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    recent_assets = cursor.fetchall()
    
    # Get pending maintenance
    cursor.execute("""
        SELECT id, asset_tag, asset_type, next_maintenance 
        FROM assets 
        WHERE next_maintenance IS NOT NULL 
        AND date(next_maintenance) <= date('now', '+7 days')
        ORDER BY next_maintenance ASC
        LIMIT 5
    """)
    pending_maintenance = cursor.fetchall()
    
    # Get unresolved alerts
    cursor.execute("""
        SELECT a.id, a.alert_type, a.alert_message, a.alert_date, 
               ast.asset_tag, ast.hostname
        FROM alerts a
        JOIN assets ast ON a.asset_id = ast.id
        WHERE a.resolved = 0
        ORDER BY a.alert_date DESC
        LIMIT 10
    """)
    unresolved_alerts = cursor.fetchall()
    
    conn.close()
    
    stats = {
        'total': total_assets,
        'active': active_assets,
        'faulty': faulty_assets,
        'alerts': pending_alerts
    }
    
    return render_template('dashboard.html', 
                          stats=stats,
                          recent_assets=recent_assets,
                          pending_maintenance=pending_maintenance,
                          alerts=unresolved_alerts)


@app.route('/assets')
def assets():
    """View all assets"""
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()
    
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    type_filter = request.args.get('type', 'all')
    
    query = "SELECT * FROM assets WHERE 1=1"
    params = []
    
    if status_filter != 'all':
        query += " AND status = ?"
        params.append(status_filter)
    
    if type_filter != 'all':
        query += " AND asset_type = ?"
        params.append(type_filter)
    
    query += " ORDER BY asset_tag"
    
    cursor.execute(query, params)
    columns = [desc[0] for desc in cursor.description]
    assets_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    
    return render_template('assets.html', assets=assets_data)


@app.route('/asset/<int:asset_id>')
def asset_detail(asset_id):
    """View asset details"""
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
    columns = [desc[0] for desc in cursor.description]
    asset = dict(zip(columns, cursor.fetchone()))
    
    # Get maintenance history
    cursor.execute("""
        SELECT * FROM maintenance_logs 
        WHERE asset_id = ? 
        ORDER BY maintenance_date DESC
    """, (asset_id,))
    maintenance_history = cursor.fetchall()
    
    conn.close()
    
    return render_template('asset_detail.html', 
                          asset=asset, 
                          maintenance=maintenance_history)


@app.route('/asset/add', methods=['GET', 'POST'])
def add_asset():
    """Add new asset"""
    if request.method == 'POST':
        conn = sqlite3.connect('assets.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO assets 
                (asset_tag, asset_type, hostname, ip_address, location, 
                 department, status, manufacturer, model, serial_number, 
                 purchase_date, warranty_expiry, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                request.form['asset_tag'],
                request.form['asset_type'],
                request.form.get('hostname', ''),
                request.form.get('ip_address', ''),
                request.form.get('location', ''),
                request.form.get('department', ''),
                request.form.get('status', 'Active'),
                request.form.get('manufacturer', ''),
                request.form.get('model', ''),
                request.form.get('serial_number', ''),
                request.form.get('purchase_date', ''),
                request.form.get('warranty_expiry', ''),
                request.form.get('notes', '')
            ))
            
            conn.commit()
            asset_id = cursor.lastrowid
            
            # Check if maintenance alert needed
            check_and_create_alerts(cursor, asset_id)
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            return f"Error: {e}", 400
        finally:
            conn.close()
        
        return redirect(url_for('assets'))
    
    return render_template('add_asset.html')


@app.route('/maintenance/log/<int:asset_id>', methods=['POST'])
def log_maintenance(asset_id):
    """Log maintenance activity"""
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO maintenance_logs 
            (asset_id, maintenance_date, maintenance_type, technician, description, cost)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            asset_id,
            request.form['maintenance_date'],
            request.form['maintenance_type'],
            request.form['technician'],
            request.form['description'],
            float(request.form.get('cost', 0))
        ))
        
        # Update asset last maintenance date
        cursor.execute("""
            UPDATE assets 
            SET last_maintenance = ?, 
                next_maintenance = date(?, '+3 months')
            WHERE id = ?
        """, (
            request.form['maintenance_date'],
            request.form['maintenance_date'],
            asset_id
        ))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        return f"Error: {e}", 400
    finally:
        conn.close()
    
    return redirect(url_for('asset_detail', asset_id=asset_id))


@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()
    
    # Asset status breakdown
    cursor.execute("""
        SELECT status, COUNT(*) as count 
        FROM assets 
        GROUP BY status
    """)
    status_breakdown = dict(cursor.fetchall())
    
    # Asset type breakdown
    cursor.execute("""
        SELECT asset_type, COUNT(*) as count 
        FROM assets 
        GROUP BY asset_type
    """)
    type_breakdown = dict(cursor.fetchall())
    
    # Department breakdown
    cursor.execute("""
        SELECT department, COUNT(*) as count 
        FROM assets 
        GROUP BY department
    """)
    dept_breakdown = dict(cursor.fetchall())
    
    conn.close()
    
    return jsonify({
        'status': status_breakdown,
        'types': type_breakdown,
        'departments': dept_breakdown
    })


@app.route('/export/csv')
def export_csv():
    """Export assets to CSV"""
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM assets")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    
    conn.close()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    writer.writerows(rows)
    
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': f'attachment; filename=assets_{datetime.now().strftime("%Y%m%d")}.csv'
    }


def check_and_create_alerts(cursor, asset_id):
    """Check asset and create alerts if needed"""
    cursor.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
    asset = cursor.fetchone()
    
    # Check warranty expiry
    if asset[12]:  # warranty_expiry column
        try:
            warranty_date = datetime.strptime(asset[12], '%Y-%m-%d')
            if warranty_date <= datetime.now() + timedelta(days=30):
                cursor.execute("""
                    INSERT INTO alerts (asset_id, alert_type, alert_message)
                    VALUES (?, ?, ?)
                """, (asset_id, 'Warranty', 'Warranty expiring within 30 days'))
        except:
            pass
    
    # Check maintenance due
    if asset[14]:  # next_maintenance column
        try:
            maint_date = datetime.strptime(asset[14], '%Y-%m-%d')
            if maint_date <= datetime.now() + timedelta(days=7):
                cursor.execute("""
                    INSERT INTO alerts (asset_id, alert_type, alert_message)
                    VALUES (?, ?, ?)
                """, (asset_id, 'Maintenance', 'Maintenance due within 7 days'))
        except:
            pass


def populate_sample_data():
    """Populate database with sample data for demonstration"""
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()
    
    sample_assets = [
        ('CBT-001', 'Desktop', 'CBT-PC-001', '192.168.1.10', 'Lab A', 'IT', 'Active', 
         'Dell', 'OptiPlex 7090', 'SN123456', '2023-01-15', '2026-01-15', None, None, 'Main CBT system'),
        ('CBT-002', 'Desktop', 'CBT-PC-002', '192.168.1.11', 'Lab A', 'IT', 'Active', 
         'Dell', 'OptiPlex 7090', 'SN123457', '2023-01-15', '2026-01-15', '2024-06-01', '2024-09-01', 'Backup system'),
        ('NET-001', 'Switch', 'CORE-SW-01', '192.168.1.1', 'Server Room', 'IT', 'Active', 
         'Cisco', 'Catalyst 2960', 'SN789012', '2022-05-10', '2025-05-10', '2024-01-10', '2024-04-10', 'Core switch'),
        ('SRV-001', 'Server', 'FILE-SRV-01', '192.168.1.100', 'Server Room', 'IT', 'Active', 
         'HP', 'ProLiant DL380', 'SN345678', '2022-03-20', '2025-03-20', None, None, 'File server'),
        ('CBT-050', 'Desktop', 'CBT-PC-050', '192.168.1.60', 'Lab B', 'IT', 'Faulty', 
         'Dell', 'OptiPlex 5090', 'SN999999', '2023-06-01', '2026-06-01', None, None, 'Needs RAM replacement'),
    ]
    
    for asset in sample_assets:
        try:
            cursor.execute("""
                INSERT INTO assets 
                (asset_tag, asset_type, hostname, ip_address, location, department, status, 
                 manufacturer, model, serial_number, purchase_date, warranty_expiry, 
                 last_maintenance, next_maintenance, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, asset)
        except:
            pass  # Skip if already exists
    
    conn.commit()
    conn.close()
    print("[+] Sample data populated")


if __name__ == '__main__':
    init_asset_db()
    
    # Uncomment to populate sample data
    # populate_sample_data()
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║          IT Asset Management Dashboard                    ║
║                                                           ║
║              Developed by Olaribigbe Amodu                ║
╚═══════════════════════════════════════════════════════════╝

Dashboard running at: http://localhost:5000
    """)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
