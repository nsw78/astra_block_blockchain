"""DEPRECATED — use app.services.contract_service.ContractService instead."""
from app.services.contract_service import ContractService

_svc = ContractService()

analyze_contract = _svc.analyze_contract
analyze_source_code_for_risks = _svc.analyze_source
fetch_contract_source_etherscan = _svc.fetch_source
