from httpx import AsyncClient, ASGITransport
from code_review_ai.main import app
import pytest


@pytest.fixture
def mock_env(monkeypatch):
    """Set mock environment variables."""
    monkeypatch.setenv("GOOGLE_API_KEY", "xxx")
    monkeypatch.setenv("GITHUB_API_TOKEN", "xxx")


@pytest.mark.asyncio
async def test_success(mock_env):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/review", json={
            "assignment_description": "Create Text Summarizer",
            "github_repo_url": "https://github.com/Liubavaa/TextSummarizer",
            "candidate_level": "Junior"
        })
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_cached_success(mock_env):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/review", json={
            "assignment_description": "Create Text Summarizer",
            "github_repo_url": "https://github.com/Liubavaa/TextSummarizer",
            "candidate_level": "Junior"
        })
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_repo_not_found(mock_env):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/review", json={
            "assignment_description": "Create Text Summarizer",
            "github_repo_url": "https://github.com/Liubavaa/hgvhgfghfjghfhjg",
            "candidate_level": "Junior"
        })
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_wrong_http(mock_env):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/review", json={
            "assignment_description": "Create Text Summarizer",
            "github_repo_url": "something",
            "candidate_level": "Junior"
        })
        assert response.status_code != 200


@pytest.mark.asyncio
async def test_without_tokens():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/review", json={
            "assignment_description": "Create Text Summarizer",
            "github_repo_url": "https://github.com/Liubavaa/TextSummarizer",
            "candidate_level": "Middle"
        })
        assert response.status_code == 401
