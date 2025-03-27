"""Notion client module for the Blog Writer Agent."""

from typing import Dict, Any, List, Optional
from notion_client import Client
from .models import ContentBlock


class NotionClient:
    """Client for interacting with Notion API."""

    def __init__(self, api_key: str, database_id: str):
        """Initialize the Notion client.

        Args:
            api_key: Notion API key
            database_id: ID of the Notion database for blog posts
        """
        self.client = Client(auth=api_key)
        self.database_id = database_id

    def create_page(self, title: str, status: str = "Backlog") -> Dict[str, Any]:
        """Create a new page in the Notion database.

        Args:
            title: Title of the blog post
            status: Initial status of the blog post

        Returns:
            Created page object
        """
        properties = {
            "Name": {"title": [{"text": {"content": title}}]},
            "Status": {"status": {"name": status}},
            "Area": {"multi_select": [{"name": "Brand"}]},
            "Platform": {"multi_select": [{"name": "Blog"}]},
            "Visuals needed": {"checkbox": True},
        }

        page = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )
        return page

    def update_page(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Update a page in the Notion database.

        Args:
            page_id: ID of the page to update
            properties: Properties to update

        Returns:
            Updated page object
        """
        page = self.client.pages.update(page_id=page_id, properties=properties)
        return page

    def get_page(self, page_id: str) -> Dict[str, Any]:
        """Get a page from the Notion database.

        Args:
            page_id: ID of the page to retrieve

        Returns:
            Page object
        """
        page = self.client.pages.retrieve(page_id=page_id)
        return page

    def query_database(
        self,
        filter_property: Optional[str] = None,
        filter_value: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Query the Notion database with optional filters.

        Args:
            filter_property: Property to filter by
            filter_value: Value to filter for

        Returns:
            List of page objects
        """
        filter_params = {}
        if filter_property and filter_value:
            filter_params = {
                "filter": {
                    "property": filter_property,
                    "select": {
                        "equals": filter_value
                    }
                }
            }

        response = self.client.databases.query(
            database_id=self.database_id,
            **filter_params
        )
        return response["results"]

    def add_blocks(self, page_id: str, content: List[ContentBlock], summary: str, image_prompt: str, image_url: str = None) -> Dict[str, Any]:
        """Add content and image blocks to a page.

        Args:
            page_id: ID of the page to update
            summary: Summary of the blog post
            image_prompt: Image prompt for the blog post
            content: List of ContentBlock objects to add
            image_data: Optional base64 encoded image data

        Returns:
            Updated page object
        """
        blocks = []

        # Add summary block
        blocks.append({
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Summary"}
                }]
            }
        })
        
        # Split summary into chunks and add as paragraphs
        summary_chunks = []
        current_chunk = ""
        sentences = summary.split(". ")
        
        for sentence in sentences:
            # Add period back to sentence if it's not the last one
            if sentence != sentences[-1]:
                sentence += ". "
                
            # If adding this sentence would exceed 2000 chars, start a new chunk
            if len(current_chunk + sentence) > 2000:
                summary_chunks.append(current_chunk)
                current_chunk = sentence
            else:
                current_chunk += sentence
        
        # Add the last chunk if it's not empty
        if current_chunk:
            summary_chunks.append(current_chunk)

        # Create paragraph blocks for each summary chunk
        for chunk in summary_chunks:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": chunk}
                    }]
                }
            })

        # Add image prompt block
        blocks.append({
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Image prompt"}
                }]
            }
        })
        # Split image prompt into chunks and add as paragraphs
        prompt_chunks = []
        current_chunk = ""
        sentences = image_prompt.split(". ")
        
        for sentence in sentences:
            # Add period back to sentence if it's not the last one
            if sentence != sentences[-1]:
                sentence += ". "
                
            # If adding this sentence would exceed 2000 chars, start a new chunk
            if len(current_chunk + sentence) > 2000:
                prompt_chunks.append(current_chunk)
                current_chunk = sentence
            else:
                current_chunk += sentence
        
        # Add the last chunk if it's not empty
        if current_chunk:
            prompt_chunks.append(current_chunk)

        # Create paragraph blocks for each prompt chunk
        for chunk in prompt_chunks:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": chunk}
                    }]
                }
            })

        for content_block in content:
            # Handle different content types
            if content_block.content_type == "heading":
                # Map heading types to Notion heading levels
                heading_type = content_block.heading_type or "h1"
                block_type = f"heading_{heading_type[-1]}"
                
                blocks.append({
                    "object": "block",
                    "type": block_type,
                    block_type: {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": content_block.text}
                        }]
                    }
                })
            else:  # paragraph type
                # Split paragraph content into chunks of 2000 characters
                text = content_block.text
                chunks = []
                current_chunk = ""
                sentences = text.split(". ")
                
                for sentence in sentences:
                    # Add period back to sentence if it's not the last one
                    if sentence != sentences[-1]:
                        sentence += ". "
                        
                    # If adding this sentence would exceed 2000 chars, start a new chunk
                    if len(current_chunk + sentence) > 2000:
                        chunks.append(current_chunk)
                        current_chunk = sentence
                    else:
                        current_chunk += sentence
                
                # Add the last chunk if it's not empty
                if current_chunk:
                    chunks.append(current_chunk)

                # Create paragraph blocks for each chunk
                for chunk in chunks:
                    blocks.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": chunk}
                            }]
                        }
                    })

        

        # Add image block if image data is provided
        if image_url:
            # Use the Firebase URL directly for the image block
            blocks.append({
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": image_url
                    }
                }
            })

        self.client.blocks.children.append(
            block_id=page_id,
            children=blocks
        )
        return self.get_page(page_id)