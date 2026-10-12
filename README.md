# AI-Powered Document Intelligence & Approval Platform — Backend

A FastAPI-based backend for AI-powered document processing, information extraction, validation, retrieval-augmented generation (RAG), and human-supervised approval workflows.

## Overview

The backend integrates LLM-powered processing with structured workflows to classify documents, extract relevant information, apply validation guardrails, index document content, and support document-specific question answering.

LangGraph orchestrates document processing and approval stages, while PostgreSQL manages application data and AWS S3 provides persistent document storage. Human-in-the-Loop (HITL) review connects automated processing with authorized approval decisions.

## Key Features

### 1. Authentication & Authorization
- JWT-based authentication.
- Role-based access control for administrators, managers, and employees.
- Protected API operations based on user permissions.

### 2. Document Management
- Document upload and metadata management.
- File type and size validation.
- Document lifecycle and processing status tracking.
- Persistent document storage integration with AWS S3.

### 3. AI-Powered Document Processing
- Document classification.
- Structured information extraction using OpenAI models.
- Validation of extracted information.
- Processing status and error handling.

### 4. Agentic Workflows with LangGraph
- Orchestration of document processing stages.
- Workflow transitions for classification, extraction, validation, and indexing.
- Routing to human review when required.
- Approval, rejection, and failure handling.

### 5. Guardrails & Validation
- Checks for unsupported document types.
- Validation of processing inputs and extracted information.
- Controlled workflow progression based on validation results.
- Error handling for unsuccessful processing stages.

### 6. Human-in-the-Loop Approval
- Human review of AI-processed documents.
- Manager approval or rejection.
- Tracking of review decisions and workflow status.
- Integration between automated processing and human decision-making.

### 7. Retrieval-Augmented Generation (RAG)
- Document text chunking and indexing.
- Vector storage using ChromaDB.
- Context retrieval for document-specific questions.
- LLM-powered responses based on retrieved document content.

### 8. MCP Integration
- Model Context Protocol (MCP) integration with Google Calendar.
- Scheduling document approval review events.
- Connecting document workflow activities with external tools.

### 9. Audit & Workflow Tracking
- Document status tracking.
- Approval history and reviewer information.
- Audit logging for workflow accountability, where implemented.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | Database ORM |
| JWT | Authentication |
| OpenAI | LLM-powered processing |
| LangChain | LLM and RAG integration |
| LangGraph | Workflow orchestration |
| ChromaDB | Vector storage and retrieval |
| MCP | External tool integration |
| AWS S3 | Document storage |
| Docker | Containerization |

## Architecture Overview

```text
              Frontend Application
                       |
                       v
                  FastAPI API
                       |
             Authentication & RBAC
                       |
                       v
               Document Management
                       |
                       v
              LangGraph Workflow
                       |
          +------------+------------+
          |            |            |
          v            v            v
    Classification  Extraction  Validation
          |            |            |
          +------------+------------+
                       |
                       v
                Document Indexing
                    ChromaDB
                       |
                       v
              Human-in-the-Loop
                       |
                Approval Decision

       Supporting Services
       PostgreSQL | AWS S3
       OpenAI | MCP | Google Calendar
```

## Project Structure

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   └── services/
├── mcp/
├── uploads/
├── requirements.txt
├── main.py
└── README.md
```

*This is a representative structure. Adjust it to match the actual backend repository.*

## Getting Started

### Prerequisites

- Python
- PostgreSQL
- OpenAI API key
- AWS account and S3 bucket
- Google Calendar credentials for calendar integration

### 1. Clone the Repository

```bash
git clone https://github.com/Madesh-cse/AI-Document-Approval-system-backend
cd backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file with the configuration required by your implementation.

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/DATABASE_NAME

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

OPENAI_API_KEY=your-openai-api-key

AWS_REGION=ap-south-1
AWS_S3_BUCKET=your-s3-bucket-name
```

Configure any additional AWS credentials, Google Calendar credentials, and vector database settings required by the application.

**Security:** Never commit populated `.env` files, API keys, or service credentials to version control. Use IAM roles or another secure credential mechanism for AWS where possible.

### 5. Start the Backend

Run the application using the correct import path for your FastAPI entry point. For example:

```bash
uvicorn main:app --reload
```

If the application entry point is inside a package, update the command accordingly.

### 6. Access API Documentation

Once the backend is running, open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Modules

The API is organized around the following functional areas, subject to the routes implemented in the repository:

- Authentication and user management
- Document upload and retrieval
- Document processing
- Document approval and review
- Document-specific question answering
- Workflow status and audit information

## Security Considerations

- Enforce authentication and authorization on protected endpoints.
- Validate uploaded files and enforce file size restrictions.
- Restrict document access according to user permissions.
- Secure AWS S3 objects and credentials.
- Validate AI-generated structured data before using it in business workflows.
- Keep human approval decisions separate from automated AI outputs where required.

## Future Enhancements

- Expand supported document types and extraction strategies.
- Improve automated evaluation of extraction and RAG quality.
- Add comprehensive unit and integration tests.
- Improve logging, monitoring, and workflow observability.
- Expand audit reporting and approval analytics.
- Strengthen production deployment and access controls.

## Learning Outcomes

This project demonstrates practical implementation of:

- REST API development with FastAPI.
- PostgreSQL database integration using SQLAlchemy.
- LLM-powered document processing.
- LangGraph agentic workflow orchestration.
- RAG implementation with ChromaDB.
- Validation guardrails and Human-in-the-Loop approval.
- JWT authentication and RBAC.
- AWS S3 and MCP-based integrations.

## Project Links

- Frontend Demo: https://drive.google.com/file/d/1QCYanANUBEmQn6LIpcwOEvcEy43g9GKv/view?usp=drive_link
- Frontend Repository: https://github.com/Madesh-cse/AI-Document-Approval-system-frontend
- Backend Repository: https://github.com/Madesh-cse/AI-Document-Approval-system-backend

