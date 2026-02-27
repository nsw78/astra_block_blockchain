"""Tests for the contract analysis service."""
import os
from app.services.contract_service import ContractService


def test_analyze_contract_no_api():
    os.environ.pop("ETHERSCAN_API_KEY", None)
    svc = ContractService()
    res = svc.analyze_contract("0x0000000000000000000000000000000000000000")
    assert isinstance(res, dict)
    assert res["address"].startswith("0x")
    assert "analysis" in res


def test_analyze_source_code():
    svc = ContractService()
    source = """
    contract Token {
        function mint(address to, uint256 amount) public onlyOwner {
            balanceOf[to] += amount;
        }
        function setFee(uint256 fee) public onlyOwner {
            _fee = fee;
        }
    }
    """
    result = svc.analyze_source(source)
    assert result["score"] > 0
    assert len(result["findings"]) > 0
