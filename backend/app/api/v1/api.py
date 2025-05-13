from fastapi import APIRouter

# from app.api.v1.endpoints import (
#     auth,
#     users,
#     controls,
#     evidence,
#     reports,
#     aws,
#     llm,
# )

from app.api.v1.endpoints import evidence, reports, llm

api_router = APIRouter()

# api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(controls.router, prefix="/controls", tags=["controls"])
api_router.include_router(evidence.router, prefix="/evidence", tags=["evidence"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
# api_router.include_router(aws.router, prefix="/aws", tags=["aws"])
api_router.include_router(llm.router, prefix="/llm", tags=["llm"]) 