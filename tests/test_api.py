"""
Skyline Financial Tech - basic API smoke tests.
Run with: pytest tests/
"""

from fastapi.testclient import TestClient
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_balance_valid_user():
    response = client.get("/account/balance?username=alice")
    assert response.status_code == 200
    assert "balance" in response.json()


def test_balance_unknown_user():
    response = client.get("/account/balance?username=nobody")
    assert response.status_code == 404


def test_transfer_no_auth():
    response = client.post(
        "/transfer?from_account=alice&to_account=bob&amount=100"
    )
    assert response.status_code == 401


def test_transfer_with_auth():
    response = client.post(
        "/transfer?from_account=alice&to_account=bob&amount=100",
        headers={"Authorization": "Bearer anything"},
    )
    assert response.status_code == 200


def test_transaction_valid():
    response = client.get("/transaction/42")
    assert response.status_code == 200


def test_transaction_negative_id_leaks_info():
    """
    Demonstrates VULN-005: error detail should NOT reach the client.
    This test documents the current (broken) behaviour - it should
    be fixed as part of the remediation write-up.
    """
    response = client.get("/transaction/-1")
    assert response.status_code == 500
    assert "detail" in response.json()
