from fastapi import APIRouter
import logging
import json
from fastapi.responses import JSONResponse
from code_review_ai.models.request import ReviewRequest
from code_review_ai.services.review_service import analyze_code
from code_review_ai.services.redis_client import RedisClient

router = APIRouter(prefix="/review", tags=["Review"])
redis_client = RedisClient()  # Redis instance for caching
logger = logging.getLogger(__name__)


@router.post("")
async def review_code(request: ReviewRequest):
    """
    Perform code review for a given assignment, GitHub repository URL, and level.
    """
    try:
        cache_key = str(request)
        # Check if the result is already cached
        result = redis_client.get(cache_key)
        if result:
            logger.info(f"Cache hit for {request}")
            result = json.loads(result)

        else:
            result = await analyze_code(
                assignment_description=request.assignment_description,
                github_repo_url=str(request.github_repo_url),
                candidate_level=request.candidate_level
            )

            # Cache the result for future use
            redis_client.set(cache_key, result)

        return JSONResponse(content=result)

    except Exception as e:
        raise e
