"""Blog Writer Agent module for generating and managing blog content."""

from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser, PydanticOutputParser
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langgraph.graph import Graph, StateGraph
from langchain_core.globals import set_debug

from .blog_publisher import BlogPublisher
from .notion_client import NotionClient
from .image_generator import ImageGenerator

from pydantic import BaseModel, Field
from .models import BlogContent
from asyncio import gather


set_debug(True)


class BlogWriterAgent:
    """Agent for generating and managing blog content."""

    def __init__(
        self,
        azure_endpoint,
        azure_credentials,
        model_name,
        notion_client: NotionClient,
        image_generator: ImageGenerator,
        dummy_blog_api_url: str
    ):
        """Initialize the Blog Writer Agent"""
        self.notion_client = notion_client
        self.blog_publisher = BlogPublisher(dummy_blog_api_url)
        self.image_generator = image_generator

        # Initialize Azure OpenAI with DeepSeek-V3
        self.llm = AzureAIChatCompletionsModel(
            endpoint=azure_endpoint,
            credential=azure_credentials,
            model_name=model_name,
            temperature= 0.7,
            top_p= 0.95,
            frequency_penalty= 0,
            presence_penalty=0,
        )

        # Initialize output parsers
        self.topics_parser = CommaSeparatedListOutputParser()
        self.content_parser = PydanticOutputParser(pydantic_object=BlogContent)

        # Update prompts with format instructions
        self.topic_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a blog topic generator. Generate engaging and relevant topics for a AI blog."),
            ("system", f"Format instructions: {self.topics_parser.get_format_instructions()}"),
            ("user", "Generate 5 AI blog topics")
        ])

        self.content_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a blog content writer. Write engaging and informative blog posts."),
            ("system", "Format instructions: {format_instructions}"),
            ("user", "Write a blog post about: {title}")
        ])


    async def generate_blogs(self) -> List[Dict[str, Any]]:
        """Generate blog topics, create pages in Notion, and automatically generate content.
    
        Returns:
            List of created and populated Notion pages
        """
        # Generate topics using LLM with parser
        topics_chain = self.topic_prompt | self.llm | self.topics_parser
        topics = await topics_chain.ainvoke({})
        
        print("Topics:", topics, sep="\n")
        
        # Create pages and collect content generation tasks
        content_tasks = []
        created_pages = []
        
        for topic in topics:
            if topic.strip():
                # Create page
                page = self.notion_client.create_page(title=topic.strip())
                created_pages.append(page)
                # Add content generation task
                content_tasks.append(self.generate_blog_content(page["id"], topic.strip()))
        
        # Generate content concurrently
        if content_tasks:
            await gather(*content_tasks)
        
        return created_pages

    async def generate_blog_content(self, page_id: str = "1c27c2a0ddf581828766d320a9a74652", title: str ="The Future of AI: How Machine Learning is Transforming Industries") -> Dict[str, Any]:
        """Generate blog content for a given page.

        Args:
            page_id: Notion page ID

        Returns:
            Updated Notion page
        """
        # Get page details
        # page = self.notion_client.get_page(page_id)
        # title = page["properties"]["Name"]["title"][0]["text"]["content"]

        # Generate content with structured output
        content_chain = self.content_prompt | self.llm | self.content_parser
        parsed_content: BlogContent = await content_chain.ainvoke({
            "title": title,
            "format_instructions": self.content_parser.get_format_instructions() })
        
        # # Generate image prompt
        # image_chain = self.image_prompt | self.llm
        # image_prompt_response = await image_chain.ainvoke({"input": f"Create an image prompt for: {title}"})
        # image_prompt = image_prompt_response.content
        
        # Generate image
        image_url = self.image_generator.generate_image(parsed_content.image_prompt)


        # Update page with structured content and image using blocks
        self.notion_client.add_blocks(
            page_id=page_id,
            content=parsed_content.content,
            summary=parsed_content.summary,
            image_prompt=parsed_content.image_prompt,
            image_url=image_url
        )
        
        # Update page status
        self.notion_client.update_page(
            page_id,
            properties={
                "Status": {"status": {"name": "Draft"}}
            }
        )

        return self.notion_client.get_page(page_id)

    async def publish_blog(self, page_id: str) -> Dict[str, Any]:
        """Publish a blog post.

        Args:
            page_id: Notion page ID

        Returns:
            Published blog post response
        """
        # Get page details
        page = self.notion_client.get_page(page_id)
        title = page["properties"]["Name"]["title"][0]["text"]["content"]
        content = page["properties"]["Content"]["rich_text"][0]["text"]["content"]
        image_data = page["properties"]["ImageData"]["rich_text"][0]["text"]["content"]

        # Publish blog
        response = self.blog_publisher.publish_blog(
            title=title,
            content=content,
            image_data=image_data if image_data else None
        )

        # Update page status
        self.notion_client.update_page(
            page_id,
            properties={"Status": {"select": {"name": "published"}}}
        )

        return response