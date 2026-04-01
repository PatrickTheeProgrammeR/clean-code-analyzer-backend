from pydantic import BaseModel


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
    issues: list[IssueResponse]


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