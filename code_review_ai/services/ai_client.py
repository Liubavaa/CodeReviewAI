import os
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

async def analyze_with_ai(assignment_description: str, repo_contents: list, candidate_level: str):
    """
    Analyze code using OpenAI or Gemini API.
    """
    token = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=token)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Craft prompt
    prompt = (
        f"Assignment: {assignment_description}\n"
        f"Candidate Level: {candidate_level}\n\n"
        f"Files with solution:\n {repo_contents}\n"
        "Review files with solution, and based on assignment and candidate level provide only:\n"
        "- Downsides/Comments\n"
        "- Rating (1 to 5 stars)\n"
        "- Conclusion."
    )

    async def gen_response(model, prompt) -> str:
        response = await model.generate_content_async(prompt)
        return response.text

    try:
        logger.info(f"Sending prompt to Gemini API.")
        result = await gen_response(model, prompt)
    except Exception as e:
        raise e

    logger.info("Successfully analyzed code using Gemini API.")
    downsides, rest = result.split("## Rating:")
    rating, conclusion = rest.split("## Conclusion:")
    return [downsides, "## Rating:" + rating, "## Conclusion:" + conclusion]
