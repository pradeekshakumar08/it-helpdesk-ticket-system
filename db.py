import sqlite3
import random
from datetime import datetime, timedelta

import pandas as pd

DB = "tickets.db"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

CATEGORIES = ["Network", "Software", "Hardware", "Email", "Access/Password"]
PRIORITIES = ["Low", "Medium", "High"]
STATUSES = ["Open", "In Progress", "Resolved"]

SAMPLE_TITLES = {
    "Network": ["Wi-Fi keeps disconnecting", "Cannot connect to VPN", "Slow internet in office"],
    "Software": ["Excel crashes on opening", "Cannot install update", "Application freezes"],
    "Hardware": ["Laptop will not turn on", "Printer not responding", "Keyboard not working"],
    "Email": ["Cannot send emails", "Mailbox is full", "Not receiving attachments"],
    "Access/Password": ["Forgot password", "Account locked", "Need access to shared folder"],
}


def get_conn():
    return sqlite3.connect(DB)


def init_db():
    conn = get_conn()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Open',
            created_at TEXT,
            resolved_at TEXT
        )"""
    )
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    if count == 0:
        add_sample_data(conn)
    conn.close()


def add_sample_data(conn):
    random.seed(1)
    now = datetime.now()
    for _ in range(40):
        category = random.choice(CATEGORIES)
        title = random.choice(SAMPLE_TITLES[category])
        priority = random.choice(PRIORITIES)
        status = random.choice(["Open", "In Progress", "Resolved", "Resolved", "Resolved"])
        created = now - timedelta(days=random.randint(1, 60), hours=random.randint(0, 23))
        resolved = None
        if status == "Resolved":
            resolved = (created + timedelta(hours=random.randint(1, 72))).strftime(TIME_FORMAT)
        conn.execute(
            "INSERT INTO tickets (title, description, category, priority, status, created_at, resolved_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (title, "Sample ticket", category, priority, status, created.strftime(TIME_FORMAT), resolved),
        )
    conn.commit()


def add_ticket(title, description, category, priority):
    conn = get_conn()
    conn.execute(
        "INSERT INTO tickets (title, description, category, priority, status, created_at) "
        "VALUES (?, ?, ?, ?, 'Open', ?)",
        (title, description, category, priority, datetime.now().strftime(TIME_FORMAT)),
    )
    conn.commit()
    conn.close()


def get_tickets():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM tickets ORDER BY id DESC", conn)
    conn.close()
    return df


def update_status(ticket_id, new_status):
    resolved_at = datetime.now().strftime(TIME_FORMAT) if new_status == "Resolved" else None
    conn = get_conn()
    conn.execute(
        "UPDATE tickets SET status = ?, resolved_at = ? WHERE id = ?",
        (new_status, resolved_at, ticket_id),
    )
    conn.commit()
    conn.close()
