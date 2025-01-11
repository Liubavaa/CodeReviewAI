from pydantic import BaseModel, HttpUrl, Field

class ReviewRequest(BaseModel):
    assignment_description: str = Field(..., min_length=10, max_length=5000)
    github_repo_url: HttpUrl
    candidate_level: str = Field(..., pattern="^(Junior|Middle|Senior)$")
