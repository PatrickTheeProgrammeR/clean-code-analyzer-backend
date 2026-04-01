from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    code: str


class ReviewRequest(BaseModel):
    original_code: str
    user_fix: str


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