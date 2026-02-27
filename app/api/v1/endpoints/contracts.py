"""
Contract analysis endpoints.
"""
from fastapi import APIRouter, Depends, Query

from app.core.security import verify_api_key
from app.models.schemas import ContractAnalyzeResponse, ContractRiskAnalysis
from app.services.contract_service import ContractService

router = APIRouter(prefix="/contracts", tags=["contracts"])

_service = ContractService()


@router.get(
    "/analyze",
    response_model=ContractAnalyzeResponse,
    summary="Analyze a smart contract",
    description="Fetches source code from Etherscan and runs heuristic risk analysis.",
)
async def analyze_contract(
    address: str = Query(
        ...,
        min_length=42,
        max_length=42,
        description="Ethereum contract address (0x...)",
        examples=["0xdAC17F958D2ee523a2206206994597C13D831ec7"],
    ),
):
    raw = _service.analyze_contract(address)
    analysis = raw.get("analysis", {})
    return ContractAnalyzeResponse(
        address=raw["address"],
        source_available=raw["source_available"],
        analysis=ContractRiskAnalysis(
            score=analysis.get("score", 0),
            findings=analysis.get("findings", []),
            error=analysis.get("error"),
        ),
    )
