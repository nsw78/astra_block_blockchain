import os
import re
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
RPC_URL = os.getenv('RPC_URL')

# Heuristics-based contract analysis (minimal, educational)

SUSPICIOUS_PATTERNS = [
    r"owner",  # can be owner-based control
    r"mint\(|mintTo\(|mintFrom\(|mintBatch",
    r"burn\(|burnFrom",
    r"renounceOwnership",
    r"transferOwnership",
    r"_transfer",
    r"setFees|setFee",
    r"unlimited",
]


def fetch_contract_source_etherscan(address: str) -> Dict[str, Any]:
    """Fetch source code and ABI from Etherscan. Returns dict or empty dict."""
    if not ETHERSCAN_API_KEY:
        return {}
    url = (
        "https://api.etherscan.io/api"
        f"?module=contract&action=getsourcecode&address={address}&apikey={ETHERSCAN_API_KEY}"
    )
    resp = requests.get(url, timeout=15)
    if resp.status_code != 200:
        return {}
    data = resp.json()
    if data.get('status') != '1':
        return {}
    return data.get('result', [{}])[0]


def analyze_source_code_for_risks(source: str) -> Dict[str, Any]:
    """Simple regex heuristics to detect risky constructs."""
    findings = []
    lower_src = source.lower()
    for pat in SUSPICIOUS_PATTERNS:
        if re.search(pat, lower_src):
            findings.append({'pattern': pat, 'snippet': _grab_snippet(lower_src, pat)})
    # additional heuristic: check for large mint loops or arbitrary assignment to balances
    if 'mint' in lower_src and ('onlyowner' in lower_src or 'owner' in lower_src):
        findings.append({'pattern': 'owner-mint', 'snippet': 'found owner-only mint functions'})
    score = min(100, 10 * len(findings))
    return {'score': score, 'findings': findings}


def _grab_snippet(src: str, pattern: str, width: int = 120) -> str:
    m = re.search(pattern, src)
    if not m:
        return ''
    start = max(0, m.start() - 30)
    end = min(len(src), m.end() + 90)
    return src[start:end].strip().replace('\n', ' ')[:width]


def analyze_contract(address: str) -> Dict[str, Any]:
    """Public function: fetch code (Etherscan) and run simple heuristics."""
    result = {'address': address, 'source_available': False, 'analysis': {}}
    try:
        src_meta = fetch_contract_source_etherscan(address)
        source = src_meta.get('SourceCode') or ''
        if source:
            result['source_available'] = True
            analysis = analyze_source_code_for_risks(source)
            result['analysis'] = analysis
        else:
            result['analysis'] = {'error': 'source not available via Etherscan or API key missing'}
    except Exception as e:
        result['analysis'] = {'error': str(e)}
    return result
