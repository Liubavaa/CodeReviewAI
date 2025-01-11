import os
from httpx import AsyncClient
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def fetch_repository_contents(repo_url: str):
    """
    Fetch the contents of a GitHub repository using the GitHub API.
    """
    token = os.getenv("GITHUB_API_TOKEN")
    headers = {"Authorization": f"token {token}"}

    repo_owner, repo_name = repo_url.rstrip('/').split('/')[-2:]
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"

    logger.info(f"Fetching repository contents for {repo_url}")

    async def get_url_content(file_url: str):
        """
        Fetch file content from a URL.
        """
        async with AsyncClient() as client:
            response = await client.get(file_url, headers=headers)
            status_code = response.status_code

            # Check for GitHub rate limits
            if status_code == 403 and "X-RateLimit-Reset" in response.headers:
                raise HTTPException(status_code=429, detail="GitHub API rate limit exceeded. Try again later.")
            if status_code == 404:
                raise HTTPException(status_code=status_code, detail="Repository not found")
            if status_code != 200:
                raise HTTPException(status_code=status_code,
                                    detail=f"Failed to fetch repository: {response.text}")
            logger.info(f"Successfully fetched contents for {file_url}")

            response.raise_for_status()
            return response.json()

    async def fetch_directory_contents(directory_url: str):
        """
        Recursively fetch the contents of a directory.
        """
        directory_contents = await get_url_content(directory_url)
        all_files = []
        for item in directory_contents:
            if item["type"] == "file":
                logger.info(f"Fetching content for file: {item['path']}")
                content = await get_url_content(item["url"])
                all_files.append({
                    "path": item["path"],
                    "content": content,
                })
            elif item["type"] == "dir":
                logger.info(f"Fetching contents of directory: {item['path']}")
                nested_files = await fetch_directory_contents(item["url"])
                all_files.extend(nested_files)

        return all_files

    return await fetch_directory_contents(base_url)
