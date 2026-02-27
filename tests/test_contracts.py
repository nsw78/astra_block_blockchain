"""Tests for contract analysis endpoints."""
import os


def test_analyze_contract_invalid_address(client):
    resp = client.get("/api/v1/contracts/analyze", params={"address": "not-valid"})
    assert resp.status_code == 422


def test_analyze_contract_no_api_key(client):
    os.environ.pop("ETHERSCAN_API_KEY", None)
    addr = "0x0000000000000000000000000000000000000000"
    resp = client.get("/api/v1/contracts/analyze", params={"address": addr})
    assert resp.status_code == 200
    data = resp.json()
    assert data["address"] == addr
    assert "analysis" in data


def test_analyze_contract_service_directly():
    os.environ.pop("ETHERSCAN_API_KEY", None)
    from app.services.contract_service import ContractService
    svc = ContractService()
    result = svc.analyze_contract("0x0000000000000000000000000000000000000000")
    assert result["address"].startswith("0x")
    assert "analysis" in result
