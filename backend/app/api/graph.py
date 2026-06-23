from fastapi import APIRouter

from app.services.graph.call_analysis_service import (
    CallAnalysisService
)

router = APIRouter(
    prefix="/graph",
    tags=["Graph"]
)


@router.get("/callees")
def get_callees(
    repository_name: str,
    method_name: str
):

    return (
        CallAnalysisService.get_callees(
            repository_name,
            method_name
        )
    )

@router.get("/callers")
def get_callers(
    repository_name: str,
    method_name: str
):

    return (
        CallAnalysisService.get_callers(
            repository_name,
            method_name
        )
    )

@router.get("/impact")
def get_impacted_methods(
    repository_name: str,
    method_name: str
):

    return (
        CallAnalysisService
        .get_impacted_methods(
            repository_name,
            method_name
        )
    )

@router.get("/call-chain")
def get_call_chain(
    repository_name: str,
    method_name: str
):

    return (
        CallAnalysisService
        .get_call_chain(
            repository_name,
            method_name
        )
    )