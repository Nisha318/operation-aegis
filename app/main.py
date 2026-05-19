"""
Skyline Financial Tech - Demo API
WARNING: This application contains INTENTIONAL security vulnerabilities
for the Operation Aegis DevSecOps capstone project.
DO NOT deploy to production.
"""

import sqlite3
import subprocess
import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(
    title="Skyline Financial Tech API",
    description="Demo banking API - intentionally vulnerable for security scanning.",
    version="1.0.0",
)

# ------------------------------------------------------------------ #
# VULN-001: Hardcoded credentials (detected by Gitleaks / TruffleHog)
# ------------------------------------------------------------------ #
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"  # noqa: S105
DB_PASSWORD = "skyline_prod_password_2024!"  # noqa: S105
JWT_SECRET = "super-secret-jwt-key-do-not-share"  # noqa: S105


def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, balance REAL)"
    )
    conn.execute("INSERT INTO accounts VALUES (1, 'alice', 50000.00)")
    conn.execute("INSERT INTO accounts VALUES (2, 'bob', 12500.00)")
    conn.commit()
    return conn


# ------------------------------------------------------------------ #
# VULN-002: SQL Injection (detected by CodeQL / Semgrep)
# ------------------------------------------------------------------ #
@app.get("/account/balance")
def get_balance(username: str):
    """
    Retrieve account balance by username.
    VULNERABLE: user input concatenated directly into SQL query.
    Try: username=alice' OR '1'='1
    """
    conn = get_db()
    query = f"SELECT balance FROM accounts WHERE username = '{username}'"
    cursor = conn.execute(query)
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"username": username, "balance": row[0]}


# ------------------------------------------------------------------ #
# VULN-003: Command Injection (detected by Semgrep / CodeQL)
# ------------------------------------------------------------------ #
@app.get("/admin/ping")
def ping_host(host: str):
    """
    Admin utility - ping a host to check connectivity.
    VULNERABLE: unsanitised input passed to shell.
    Try: host=localhost; cat /etc/passwd
    """
    result = subprocess.run(
        f"ping -c 1 {host}", shell=True, capture_output=True, text=True  # noqa: S602
    )
    return {"stdout": result.stdout, "stderr": result.stderr}


# ------------------------------------------------------------------ #
# VULN-004: Broken authentication - no token validation
# ------------------------------------------------------------------ #
@app.post("/transfer")
def transfer_funds(
    from_account: str,
    to_account: str,
    amount: float,
    authorization: Optional[str] = Header(default=None),
):
    """
    Transfer funds between accounts.
    VULNERABLE: Authorization header accepted but never validated.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    return {
        "status": "transfer_complete",
        "from": from_account,
        "to": to_account,
        "amount": amount,
        "message": "Funds transferred (auth not actually verified)",
    }


# ------------------------------------------------------------------ #
# VULN-005: Sensitive data exposure in error response
# ------------------------------------------------------------------ #
@app.get("/transaction/{tx_id}")
def get_transaction(tx_id: int):
    """
    Retrieve transaction details.
    VULNERABLE: raw exception detail including internal paths exposed to client.
    """
    try:
        if tx_id < 0:
            raise ValueError(f"Invalid ID {tx_id} - internal path: {os.getcwd()}/transactions.db")
        if tx_id > 1000:
            raise FileNotFoundError(f"tx_{tx_id}.log not found in {os.getcwd()}")
        return {"tx_id": tx_id, "amount": 250.00, "status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------------ #
# Healthy endpoint (intentionally clean - for ZAP baseline)
# ------------------------------------------------------------------ #
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "skyline-financial-api"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
