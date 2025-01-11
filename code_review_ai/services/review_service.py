from code_review_ai.services.github_client import fetch_repository_contents
from code_review_ai.services.ai_client import analyze_with_ai


async def analyze_code(assignment_description: str, github_repo_url: str, candidate_level: str):
    """
    Fetch repository contents, analyze code, and return a structured review.
    """
    # Fetch repository contents
    repo_contents = await fetch_repository_contents(github_repo_url)

    # Analyze code using the AI API
    review_result = await analyze_with_ai(
        assignment_description=assignment_description,
        repo_contents=repo_contents,
        candidate_level=candidate_level
    )

    return {
        "found_files": [file["path"] for file in repo_contents],
        "downsides/comments": review_result[0],
        "rating": review_result[1],
        "conclusion": review_result[2],
    }
