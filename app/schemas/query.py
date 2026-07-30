from typing import Any

from pydantic import BaseModel

from app.schemas.database import DatabaseConnectionRequest


class QueryRequest(BaseModel):
    """
    Request for a natural-language database query.
    """

    question: str
    database: DatabaseConnectionRequest

class PipelineTimings(BaseModel):
    retrieval_ms: float
    context_ms: float
    generation_ms: float
    execution_ms: float
    total_ms: float
class QueryResponse(BaseModel):
    """
    Response produced by the Text-to-SQL pipeline.
    """

    question: str
    sql: str
    results: list[dict[str, Any]]

    repair_attempted: bool
    repair_successful: bool

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    timings: PipelineTimings

