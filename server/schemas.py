from pydantic import BaseModel
from typing import List, Optional


class Stock(BaseModel):
    name: str
    symbol: str

    class Config:
        extra = "allow"


class ExecutionStep(BaseModel):
    step_number: int
    instruction: str
    target: Optional[List[str]] = None

    class Config:
        extra = "allow"


class FinancialPerformanceFigure(BaseModel):
    class Config:
        extra = "allow"


class QueryMetadata(BaseModel):
    target_years: List[int] = []
    query_scope: str
    identified_topic: str
    query_type: str

    class Config:
        extra = "allow"


class QueryExecutionData(BaseModel):
    identified_stocks: List[Stock]
    execution_steps: List[ExecutionStep]
    required_data_parameters: List[str]
    relevant_financial_performance_figures: List[FinancialPerformanceFigure]
    relevant_financial_ratios: List[str]
    query_metadata: List[QueryMetadata]

    class Config:
        extra = "allow"


class QueryParameterizationData(BaseModel):
    query: str
