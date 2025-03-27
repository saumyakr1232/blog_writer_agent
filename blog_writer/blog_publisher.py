"""Blog publisher module for the Blog Writer Agent."""

import json
import requests
from typing import Dict, Any, Optional


class BlogPublisher:
    """Publisher for blog posts."""

    def __init__(self, api_url: str):
        """Initialize the blog publisher.

        Args:
            api_url: URL of the blog API
        """
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json"
        }

    def publish_blog(self, 
                     title: str, 
                     content: str, 
                     image_data: Optional[str] = None, 
                     tags: Optional[list] = None,
                     author: str = "AI Blog Writer") -> Dict[str, Any]:
        """Publish a blog post to the dummy URL.

        Args:
            title: Blog title
            content: Blog content in HTML format
            image_data: Base64 encoded image data (optional)
            tags: List of tags (optional)
            author: Author name (optional)

        Returns:
            Response from the blog API
        """
        if tags is None:
            tags = ["AI", "Technology", "Productivity"]

        payload = {
            "title": title,
            "content": content,
            "author": author,
            "tags": tags,
            "image": image_data
        }

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to publish blog: {str(e)}"
            raise Exception(error_msg)