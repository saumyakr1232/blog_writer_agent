"""Image generator module for the Blog Writer Agent."""

import os
from typing import Dict, Any, Optional
import requests
from PIL import Image
import io
import json
from openai import AzureOpenAI
import firebase_admin
from firebase_admin import credentials, initialize_app, storage
import uuid

class ImageGenerator:
    """Generator for blog post images using Azure AI."""

    def __init__(self, api_key: str, api_endpoint: str, model_name: str, firebase_creds_path: str, storage_bucket_name: str):
        """Initialize the image generator.
        Args:
            api_key: Azure AI API key
            api_endpoint: Azure AI API endpoint
            model_name: Azure AI model name
            firebase_creds_path: Path to Firebase credentials JSON file
            storage_bucket_name: Firebase Storage bucket name
        """
       
        self.client = AzureOpenAI(
            api_version="2024-02-01",
            api_key=api_key,
            azure_endpoint=api_endpoint
        )
        self.model_name = model_name
        
        # Initialize Firebase
        cred = credentials.Certificate(firebase_creds_path)
        if not firebase_admin._apps:
            initialize_app(cred)
        self.bucket = storage.bucket(name=storage_bucket_name)

    def generate_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard", style: str = "vivid") -> Optional[str]:
        """Generate an image based on the prompt.

        Args:
            prompt: Text prompt for image generation
            size: Image size ("1024x1024", "1792x1024", or "1024x1792")
            quality: Image quality ("standard" or "hd")
            style: Image style ("vivid" or "natural")

        Returns:
            Base64 encoded image data or None if generation fails
        """
        try:
            result = self.client.images.generate(
                model=self.model_name,
                prompt=prompt,
                n=1,
                size=size,
                quality=quality,
                style=style
            )

            response_data = json.loads(result.model_dump_json())
            image_url = response_data["data"][0]["url"]
            image_response = requests.get(image_url)
            image_response.raise_for_status()

            # Save image to Firebase Storage
            image = Image.open(io.BytesIO(image_response.content))
            image_buffer = io.BytesIO()
            image.save(image_buffer, format="PNG")
            image_buffer.seek(0)
            
            # Generate unique filename
            filename = f"website/blog/{uuid.uuid4()}.png"
            blob = self.bucket.blob(filename)
            
            # Upload and get public URL
            blob.upload_from_file(image_buffer, content_type="image/png")
            blob.make_public()
            print(f"Image saved to Firebase Storage at: {blob.public_url}")
            return blob.public_url

        except Exception as e:
            print(f"Failed to generate image: {str(e)}")
            return None


if __name__ == "__main__":
    # Example usage
    import dotenv
    dotenv.load_dotenv()
    print("AZURE_IMGE_ENDPOINT:", os.getenv("AZURE_IMAGE_ENDPOINT"))
    image_generator = ImageGenerator(
        api_key=os.getenv("AZURE_IMAGE_CREDENTIALS"),
        api_endpoint=os.getenv("AZURE_IMAGE_ENDPOINT"),
        model_name=os.getenv("AZURE_IMAGE_MODEL_NAME")  # Optional, if you have a specific model nam
    )
    # Generate the image
    image_url = image_generator.generate_image("A cat sitting on a couch")

    print(image_url)