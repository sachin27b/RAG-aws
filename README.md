# Flask Knowledge Base App

A production-ready Flask application for PDF document processing with AWS Bedrock Knowledge Base integration and Groq LLM-powered question answering.

## Features

- **PDF Processing**: Upload any PDF with automatic chunking (configurable page size)
- **AWS S3 Integration**: Automatic S3 upload for each document chunk
- **Bedrock Knowledge Base**: Synchronous ingestion job triggering in AWS Bedrock
- **Semantic Retrieval**: Query the Knowledge Base using advanced semantic search
- **AI-Powered Answers**: Generate final answers using Groq LLM
- **User-Friendly UI**: Clear logging and real-time status updates
- **Modular Architecture**: Clean, maintainable backend structure
- **Production-Ready**: Enterprise-grade code organization and error handling

## Project Structure

```
flask-kb-app/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── app.js
│   │
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── s3_service.py
│   │   ├── ingestion_service.py
│   │   ├── retrieval_service.py
│   │   ├── llm_service.py
│   │   └── context_service.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── logger.py
│   │
│   └── utils/
│       └── tokenizer.py
│
├── uploads/
├── .env
├── run.py
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- AWS Account with Bedrock access
- Groq API key
- S3 bucket for document storage

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sachin27b/RAG-aws
cd RAG-aws
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_BUCKET_NAME=your_bucket_name
AWS_DEFAULT_REGION=us-east-1

# Groq API
GROQ_API_KEY=your_groq_api_key

```

**Note**: Never commit your `.env` file to version control.

## Usage

### Start the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

### Upload and Query Documents

1. Navigate to the web interface
2. Upload a PDF document
3. Wait for processing and ingestion to complete
4. Enter your question in the query box
5. Receive AI-generated answers based on your documents


### Code Structure

- **Services**: Business logic separated into focused service modules
- **Routes**: Clean API endpoints in `routes.py`
- **Config**: Centralized configuration management
- **Utils**: Reusable utility functions
