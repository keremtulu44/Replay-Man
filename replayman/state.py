"""SQLite durum, görev kuyruğu ve kaldığı yerden devam."""
from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from .catalog import Asset

SCHEMA = """
CREATE TABLE IF NOT EXISTS assets (
    id TEXT PRIMARY KEY,
    yahoo_symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    catalog_hash TEXT NOT NULL,
    last_seen REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS tasks (
    asset_id TEXT NOT NULL,
    interval TEXT NOT NULL,
    start TEXT NOT NULL,
    end TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    attempts INTEGER NOT NULL DEFAULT 0,
    next_retry_at REAL NOT NULL DEFAULT 0,
    last_error TEXT,
    error_kind TEXT,
    rows INTEGER,
    from_cache INTEGER,
    updated_at REAL NOT NULL,
    PRIMARY KEY (asset_id, interval, start, end)
);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status, next_retry_at);
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_requests_ts ON requests(ts);
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at REAL NOT NULL,
    finished_at REAL,
    status TEXT NOT NULL,
    summary_json TEXT
);
"""


@dataclass(frozen=True)
class Task:
    asset_id: str
    interval: str
    start: str
    end: str
    status: str
    attempts: int
    next_retry_at: float
    last_error: str | None
    error_kind: str | None


class State:
    def __init__(self, path: str | Path, clock: Callable[[], float] = time.time) -> None:
        self.clock = clock
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, timeout=30)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "State":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def upsert_assets(self, assets: Iterable[Asset], catalog_hash: str) -> None:
        now = self.clock()
        with self.conn:
            for asset in assets:
                self.conn.execute(
                    """INSERT INTO assets(id,yahoo_symbol,name,category,catalog_hash,last_seen)
                       VALUES(?,?,?,?,?,?)
                       ON CONFLICT(id) DO UPDATE SET
                         yahoo_symbol=excluded.yahoo_symbol,
                         name=excluded.name,
                         category=excluded.category,
                         catalog_hash=excluded.catalog_hash,
                         last_seen=excluded.last_seen""",
                    (asset.id, asset.yahoo_symbol, asset.name, asset.category, catalog_hash, now),
                )

    def plan_tasks(self, tasks: Iterable[tuple[str, str, str, str]]) -> int:
        now = self.clock()
        before = self.conn.total_changes
        with self.conn:
            self.conn.executemany(
                """INSERT OR IGNORE INTO tasks(asset_id,interval,start,end,updated_at)
                   VALUES(?,?,?,?,?)""",
                [(a, i, s, e, now) for a, i, s, e in tasks],
            )
        return self.conn.total_changes - before

    def reset_running(self) -> None:
        with self.conn:
            self.conn.execute(
                "UPDATE tasks SET status='pending', updated_at=? WHERE status='running'",
                (self.clock(),),
            )

    def reset_failed(self, include_permanent: bool = False) -> int:
        kinds = "('transient','rate_limit','unknown','failed')"
        if include_permanent:
            kinds = "('transient','rate_limit','unknown','failed','permanent','no_data','invalid_data')"
        with self.conn:
            cur = self.conn.execute(
                f"""UPDATE tasks SET status='pending', attempts=0, next_retry_at=0,
                       last_error=NULL, error_kind=NULL, updated_at=?
                    WHERE status='failed' AND (error_kind IN {kinds} OR error_kind IS NULL)""",
                (self.clock(),),
            )
        return cur.rowcount

    def due_tasks(self, now: float, max_attempts: int) -> list[Task]:
        rows = self.conn.execute(
            """SELECT * FROM tasks
               WHERE status='pending' AND attempts < ? AND next_retry_at <= ?
               ORDER BY asset_id, interval, start""",
            (max_attempts, now),
        ).fetchall()
        return [self._task(row) for row in rows]

    def next_retry_time(self, max_attempts: int) -> float | None:
        row = self.conn.execute(
            """SELECT MIN(next_retry_at) AS t FROM tasks
               WHERE status='pending' AND attempts < ?""",
            (max_attempts,),
        ).fetchone()
        return row["t"] if row and row["t"] is not None else None

    @staticmethod
    def _task(row: sqlite3.Row) -> Task:
        return Task(
            row["asset_id"], row["interval"], row["start"], row["end"],
            row["status"], row["attempts"], row["next_retry_at"],
            row["last_error"], row["error_kind"],
        )

    def mark_running(self, task: Task) -> None:
        with self.conn:
            self.conn.execute(
                """UPDATE tasks SET status='running', updated_at=?
                   WHERE asset_id=? AND interval=? AND start=? AND end=?""",
                (self.clock(), task.asset_id, task.interval, task.start, task.end),
            )

    def mark_complete(self, task: Task, rows: int, from_cache: bool) -> None:
        with self.conn:
            self.conn.execute(
                """UPDATE tasks SET status='complete', attempts=attempts+1,
                       rows=?, from_cache=?, last_error=NULL, error_kind=NULL, updated_at=?
                   WHERE asset_id=? AND interval=? AND start=? AND end=?""",
                (rows, int(from_cache), self.clock(), task.asset_id, task.interval, task.start, task.end),
            )

    def mark_retry(self, task: Task, kind: str, message: str, delay: float) -> None:
        with self.conn:
            self.conn.execute(
                """UPDATE tasks SET status='pending', attempts=attempts+1,
                       next_retry_at=?, last_error=?, error_kind=?, updated_at=?
                   WHERE asset_id=? AND interval=? AND start=? AND end=?""",
                (self.clock() + delay, message[:2000], kind, self.clock(),
                 task.asset_id, task.interval, task.start, task.end),
            )

    def mark_failed(self, task: Task, kind: str, message: str) -> None:
        with self.conn:
            self.conn.execute(
                """UPDATE tasks SET status='failed', attempts=attempts+1,
                       last_error=?, error_kind=?, updated_at=?
                   WHERE asset_id=? AND interval=? AND start=? AND end=?""",
                (message[:2000], kind, self.clock(), task.asset_id, task.interval, task.start, task.end),
            )

    def mark_pending_no_attempt(self, task: Task) -> None:
        with self.conn:
            self.conn.execute(
                """UPDATE tasks SET status='pending', updated_at=?
                   WHERE asset_id=? AND interval=? AND start=? AND end=?""",
                (self.clock(), task.asset_id, task.interval, task.start, task.end),
            )

    def record_request(self, ts: float) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO requests(ts) VALUES(?)", (ts,))
            self.conn.execute("DELETE FROM requests WHERE ts < ?", (ts - 7200,))

    def request_count_since(self, ts: float) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM requests WHERE ts >= ?", (ts,)).fetchone()[0]

    def oldest_request_since(self, ts: float) -> float | None:
        row = self.conn.execute("SELECT MIN(ts) FROM requests WHERE ts >= ?", (ts,)).fetchone()
        return row[0] if row and row[0] is not None else None

    def last_request_time(self) -> float | None:
        row = self.conn.execute("SELECT MAX(ts) FROM requests").fetchone()
        return row[0] if row and row[0] is not None else None

    def get_meta(self, key: str, default: str | None = None) -> str | None:
        row = self.conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row["value"] if row else default

    def set_meta(self, key: str, value: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO meta(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, value),
            )

    def get_float(self, key: str, default: float = 0.0) -> float:
        value = self.get_meta(key)
        return float(value) if value is not None else default

    def set_float(self, key: str, value: float) -> None:
        self.set_meta(key, str(value))

    def start_run(self) -> int:
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO runs(started_at,status) VALUES(?,?)", (self.clock(), "running")
            )
        return int(cur.lastrowid)

    def finish_run(self, run_id: int, status: str, summary: dict) -> None:
        with self.conn:
            self.conn.execute(
                "UPDATE runs SET finished_at=?, status=?, summary_json=? WHERE id=?",
                (self.clock(), status, json.dumps(summary, ensure_ascii=False), run_id),
            )

    def task_counts(self) -> dict[str, int]:
        rows = self.conn.execute("SELECT status, COUNT(*) AS n FROM tasks GROUP BY status").fetchall()
        return {row["status"]: row["n"] for row in rows}

    def all_tasks(self) -> list[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM tasks ORDER BY asset_id, interval, start").fetchall()

    def coverage(self) -> list[sqlite3.Row]:
        return self.conn.execute(
            """SELECT asset_id, interval,
                      SUM(CASE WHEN status='complete' THEN 1 ELSE 0 END) AS complete,
                      SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) AS failed,
                      SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END) AS pending,
                      SUM(COALESCE(rows,0)) AS rows
               FROM tasks GROUP BY asset_id, interval ORDER BY asset_id, interval"""
        ).fetchall()
