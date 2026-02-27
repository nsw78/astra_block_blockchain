"""
Contract analysis service — isolates business logic from HTTP layer.
"""
import re
from typing import Any, Dict, List

import requests

from app.core.config import get_settings
from app.core.exceptions import ExternalServiceError, ValidationError
from app.core.logging import get_logger

logger = get_logger("service.contract")

SUSPICIOUS_PATTERNS: List[str] = [
    r"owner",
    r"mint\(|mintTo\(|mintFrom\(|mintBatch",
    r"burn\(|burnFrom",
    r"renounceOwnership",
    r"transferOwnership",
    r"_transfer",
    r"setFees|setFee",
    r"unlimited",
]


def _grab_snippet(src: str, pattern: str, width: int = 120) -> str:
    m = re.search(pattern, src)
    if not m:
        return ""
    start = max(0, m.start() - 30)
    end = min(len(src), m.end() + 90)
    return src[start:end].strip().replace("\n", " ")[:width]


class ContractService:
    def __init__(self) -> None:
        self._settings = get_settings()

    def fetch_source(self, address: str) -> Dict[str, Any]:
        api_key = self._settings.ETHERSCAN_API_KEY
        if not api_key:
            return {}
        url = (
            "https://api.etherscan.io/api"
            f"?module=contract&action=getsourcecode&address={address}&apikey={api_key}"
        )
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as exc:
            raise ExternalServiceError("Etherscan", str(exc))
        data = resp.json()
        if data.get("status") != "1":
            return {}
        return data.get("result", [{}])[0]

    def analyze_source(self, source: str) -> Dict[str, Any]:
        findings = []
        lower = source.lower()
        for pat in SUSPICIOUS_PATTERNS:
            if re.search(pat, lower):
                findings.append({"pattern": pat, "snippet": _grab_snippet(lower, pat)})
        if "mint" in lower and ("onlyowner" in lower or "owner" in lower):
            findings.append({"pattern": "owner-mint", "snippet": "owner-only mint functions detected"})
        score = min(100, 10 * len(findings))
        return {"score": score, "findings": findings}

    def analyze_contract(self, address: str) -> Dict[str, Any]:
        if not address.startswith("0x") or len(address) != 42:
            raise ValidationError("address must be a valid 42-char hex string starting with 0x")
        result: Dict[str, Any] = {
            "address": address,
            "source_available": False,
            "analysis": {},
        }
        try:
            src_meta = self.fetch_source(address)
            source = src_meta.get("SourceCode") or ""
            if source:
                result["source_available"] = True
                result["analysis"] = self.analyze_source(source)
            else:
                result["analysis"] = {"error": "Source not available via Etherscan or API key missing"}
        except ExternalServiceError:
            raise
        except Exception as exc:
            logger.exception("Unexpected error during contract analysis")
            result["analysis"] = {"error": str(exc)}
        return result
