"""Main entry point for the Blog Writer Agent application."""

import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks

from blog_writer.agent import BlogWriterAgent
from blog_writer.image_generator import ImageGenerator
from blog_writer.notion_client import NotionClient

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Blog Writer Agent")

# Initialize Notion client
notion_client = NotionClient(
    api_key=os.getenv("NOTION_API_KEY"),
    database_id=os.getenv("NOTION_DATABASE_ID")
)

# Image generator client
image_generator_client = ImageGenerator(
    api_key=os.getenv("AZURE_IMAGE_CREDENTIALS"),
    api_endpoint=os.getenv("AZURE_IMAGE_ENDPOINT"),
    model_name=os.getenv("AZURE_IMAGE_MODEL_NAME"),
    firebase_creds_path=os.getenv("FIREBASE_CREDENTIALS_PATH"),
    storage_bucket_name=os.getenv("FIREBASE_STORAGE_BUCKET_NAME"),
)

# Initialize Blog Writer Agent
blog_agent = BlogWriterAgent(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    azure_credentials=os.getenv("AZURE_CREDENTIALS"),
    model_name=os.getenv("AZURE_MODEL_NAME"),
    notion_client=notion_client,
    image_generator=image_generator_client,
    dummy_blog_api_url=os.getenv("DUMMY_BLOG_API_URL")
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Blog Writer Agent is running"}


@app.post("/generate-topics")
async def generate_topics(background_tasks: BackgroundTasks):
    """Endpoint to generate blog topics with content and images."""
    background_tasks.add_task(blog_agent.generate_blogs)
    return {"message": "Blog topics and content generation started"}


@app.post("/generate-blog")
async def generate_blog(background_tasks: BackgroundTasks):
    """Endpoint to generate blog posts with content and images."""
    background_tasks.add_task(blog_agent.generate_blogs)
    return {"message": "Blog post generation started"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
