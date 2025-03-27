# Blog Writer Agent

An automated blog content generation system that leverages Azure AI with DeepSeek-V3, Notion integration, and Firebase storage to create and manage blog content. This open-source project aims to simplify and automate the blog content creation process.

## Features

- Automated blog topic generation using Azure AI
- Content creation with DeepSeek-V3 language model
- Image generation for blog posts using Azure AI
- Integration with Notion for content management
- Firebase storage for image hosting
- FastAPI-based REST API endpoints

## Prerequisites

- Python 3.x
- Azure AI account and credentials
- Notion API access
- Firebase project with storage enabled

## Environment Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env` file:
   ```env
   AZURE_ENDPOINT=your_azure_endpoint
   AZURE_CREDENTIALS=your_azure_credentials
   AZURE_MODEL_NAME=your_model_name
   AZURE_IMAGE_ENDPOINT=your_azure_image_endpoint
   AZURE_IMAGE_CREDENTIALS=your_azure_image_key
   AZURE_IMAGE_MODEL_NAME=your_azure_image_model
   NOTION_API_KEY=your_notion_api_key
   NOTION_DATABASE_ID=your_notion_database_id
   FIREBASE_CREDENTIALS_PATH=path_to_firebase_credentials.json
   FIREBASE_STORAGE_BUCKET_NAME=your_storage_bucket_name
   DUMMY_BLOG_API_URL=your_blog_api_url
   ```

## Usage

1. Start the FastAPI server:

   ```bash
   python main.py
   ```

2. Available endpoints:
   - `GET /`: Check if the service is running
   - `POST /generate-topics`: Generate blog topics
   - `POST /generate-blog`: Generate blog posts with content and images
   - `GET /health`: Health check endpoint

## Project Structure

```
├── blog_writer/
│   ├── __init__.py
│   ├── agent.py          # Main blog writer agent implementation
│   ├── blog_publisher.py # Blog publishing functionality
│   ├── image_generator.py# Azure AI image generation
│   ├── models.py         # Data models
│   └── notion_client.py  # Notion API integration
├── main.py              # FastAPI application entry point
├── requirements.txt     # Project dependencies
└── test.py             # Test suite
```

## Components

### Blog Writer Agent

Manages the blog generation process using Azure AI with DeepSeek-V3 for content creation.

### Image Generator

Generates blog post images using Azure AI and stores them in Firebase Storage.

### Notion Integration

Manages blog content through Notion's API for easy content organization and tracking.

### FastAPI Server

Provides REST API endpoints for interacting with the blog writer agent.

## Development

1. Follow Python code style guidelines (PEP 8)
2. Run tests before submitting changes
3. Keep dependencies updated
4. Use virtual environment for development

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and follow the existing code style.

## License

This project is licensed under the MIT License - see below for details:

MIT License

Copyright (c) 2024 Blog Writer Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
