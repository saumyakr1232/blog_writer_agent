from pydantic import BaseModel, Field

class ContentBlock(BaseModel):
    """Schema for a content block in the blog post."""
    content_type: str = Field(description="Type of content block (heading or paragraph)")
    heading_type: str = Field(description="Type of heading (h1, h2, h3) if content_type is heading", default=None)
    text: str = Field(description="The actual content text")

class BlogContent(BaseModel):
    """Schema for blog content output."""
    title: str = Field(description="The title of the blog post")
    content: list[ContentBlock] = Field(description="List of content blocks (headings and paragraphs)")
    summary: str = Field(description="A brief summary of the blog post")
    image_prompt: str = Field(description="Image generation prompt for the blog post")
