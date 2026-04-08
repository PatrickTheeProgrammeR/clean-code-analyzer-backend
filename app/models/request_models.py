from pydantic import BaseModel, Field
from typing import Literal


class AnalyzeRequest(BaseModel):
    code: str
    api_key: str
    analysis_standard: Literal["clean_code", "pep8", "clean_code_pep8"] = "clean_code_pep8"


class ReviewRequest(BaseModel):
    original_code: str
    user_fix: str
    api_key: str


class IssueResponse(BaseModel):
    line: int
    problem: str
    suggestion: str


class AnalyzeResponse(BaseModel):
    score: int
    summary: str = ""
    issues: list[IssueResponse] = Field(default_factory=list)


class ReviewResponse(BaseModel):
    score: int
    feedback: str
    comparison: str
    best_solution: str
    best_solution_explanation: str


class GitHubFetchRequest(BaseModel):
    url: str


class GitHubFetchResponse(BaseModel):
    code: str
    filename: str | None = None