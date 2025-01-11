from fastapi import FastAPI
from code_review_ai.routes.review import router as review_router
from code_review_ai.utils.logger import configure_logging

# Initialize FastAPI app
app = FastAPI(title="Auto-Review Tool", version="1.0")

# Configure logging
configure_logging()

# Include routes
app.include_router(review_router)

# Add custom error handlers
# add_exception_handlers(app)

@app.get("/")
async def root():
    return {"message": "Welcome to the Auto-Review Tool API!"}
