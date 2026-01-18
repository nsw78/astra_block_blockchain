import os
from analyzer.contract_analyzer import analyze_contract


def test_analyze_contract_no_api():
    # Without ETHERSCAN_API_KEY we expect a source_not_available message
    os.environ.pop('ETHERSCAN_API_KEY', None)
    res = analyze_contract('0x0000000000000000000000000000000000000000')
    assert isinstance(res, dict)
    assert res['address'].startswith('0x')
    assert 'analysis' in res
