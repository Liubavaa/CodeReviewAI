# Coding Assignment Auto-Review Tool

The **Coding Assignment Auto-Review Tool** is a backend service built with FastAPI to automate the review of coding assignments. It integrates Google Gemini API for AI-powered code analysis and the GitHub API for fetching repository contents.

---

## Features
- Analyze coding assignments based on repository contents, assignment descriptions, and candidate levels.
- Integration with Google Gemini API for intelligent feedback and grading.
- Caching with Redis for optimized performance.
- Handles GitHub API rate limits and large repositories through pagination.

---

## Requirements
- **Python 3.12+**
- **Redis** (used for caching)
- **Docker** and **Docker Compose** (for Redis setup)
- **Poetry** for dependency management.

---

## Installation and Setup

### Clone the Repository
```bash
git clone https://github.com/your-username/CodeReviewAI.git
cd CodeReviewAI
```

### Set Up the Environment
1. Install dependencies:
   ```bash
   pip install poetry
   poetry install
   ```
2. Set up environment variables by creating a `.env` file (or with `export`):
   ```
   GOOGLE_API_KEY=your_google_api_key
   GITHUB_ACCESS_TOKEN=your_github_access_token
   ```

### Redis Setup
1. If Docker is available, start Redis using Docker Compose:
   ```bash
   docker-compose up -d
   ```
   This runs Redis on `localhost:6379`.
   
2. Alternatively, install Redis manually and start the service.

---

## Running the Application

### Local Development Server
1. Start the FastAPI server:
   ```bash
   poetry run uvicorn code_review_ai.main:app --reload
   ```
2. Access the API documentation in your browser at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## API Endpoints

### **POST** `/review`
#### Request Body
```json
{
  "assignment_description": "Create Text Summarizer",
  "github_repo_url": "https://github.com/Liubavaa/TextSummarizer",
  "candidate_level": "Junior"
}
```

#### Response Format
```json
{
  "found_files": ["README.md", "main.py"],
  "downsides/comments": "List of downsides or issues found in the repository.",
  "rating": "Rating out of 5 stars.",
  "conclusion": "Overall feedback for the assignment."
}
```

---

## Testing

1. Ensure you have Redis running during testing:
   ```bash
   docker-compose up -d
   ```
2. Run tests with `pytest`:
   ```bash
   poetry run pytest
   ```
3. Run tests coverage with `pytest`:
   ```bash
    poetry run pytest --cov=code_review_ai --cov-report=term-missing
   ```
---

## Scaling for Large Repositories and Volume

I would implement a microservices architecture with separate services (possibly with several duplicates) for handling GitHub/AI API interactions and
user requests. A message queue like Kafka would handle high traffic by queueing requests
for asynchronous processing, ensuring resilience under load. 

For repositories with 100+ files, I’d fetch files in paginated batches and process them incrementally, storing 
intermediate results in a distributed database like PostgreSQL. Redis caching would be leveraged to 
store only repository metadata and partially analyzed results.

To manage API rate limits, I’d implement, for example, request throttling. For cost control, I’d add fallback modes 
with cheaper llms for rate-limited responses.

---
