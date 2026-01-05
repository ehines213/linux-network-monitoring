from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import sqlite3
from pathlib import Path

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


DB_PATH = Path(__file__).with_name("metrics.db")
API_KEY_ENV_NAME = "X-API-Key"  # header name

app = FastAPI(title="Linux Network Monitoring Platform")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host TEXT NOT NULL,
                ts TEXT NOT NULL,
                cpu_pct REAL NOT NULL,
                mem_pct REAL NOT NULL,
                disk_pct REAL NOT NULL,
                rx_kbps REAL NOT NULL,
                tx_kbps REAL NOT NULL,
                ping_ms REAL
            )
        """)
        conn.commit()

init_db()

class MetricPayload(BaseModel):
    host: str = Field(min_length=1, max_length=128)
    cpu_pct: float = Field(ge=0, le=100)
    mem_pct: float = Field(ge=0, le=100)
    disk_pct: float = Field(ge=0, le=100)
    rx_kbps: float = Field(ge=0)
    tx_kbps: float = Field(ge=0)
    ping_ms: float | None = Field(default=None, ge=0)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(payload: MetricPayload, x_api_key: str | None = Header(default=None)):
    # Simple auth check (replace with proper secrets mgmt later)
    expected = "dev-key-change-me"
    if x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid API key")

    ts = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO metrics (host, ts, cpu_pct, mem_pct, disk_pct, rx_kbps, tx_kbps, ping_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            payload.host, ts, payload.cpu_pct, payload.mem_pct,
            payload.disk_pct, payload.rx_kbps, payload.tx_kbps, payload.ping_ms
        ))
        conn.commit()

    return {"ingested": True, "ts": ts}

@app.get("/latest")
def latest(limit: int = 50):
    limit = max(1, min(limit, 500))
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT host, ts, cpu_pct, mem_pct, disk_pct, rx_kbps, tx_kbps, ping_ms
            FROM metrics
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return [
        {
            "host": r[0], "ts": r[1], "cpu_pct": r[2], "mem_pct": r[3],
            "disk_pct": r[4], "rx_kbps": r[5], "tx_kbps": r[6], "ping_ms": r[7]
        }
        for r in rows
    ]

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/index.html")
