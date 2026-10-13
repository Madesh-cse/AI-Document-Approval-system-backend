# AI-Powered Document Intelligence & Approval Platform — Backend

A FastAPI-based backend for intelligent document processing, automated information extraction, validation guardrails, retrieval-augmented generation (RAG), and human-supervised approval workflows.

The platform combines LLM-powered document intelligence with LangGraph workflow orchestration to streamline document review, approval, and rejection while maintaining role-based access control and workflow accountability.

## Overview

The backend powers an AI-driven document management platform that enables users to upload documents, process their contents using LLMs, retrieve relevant information, and route documents through controlled approval workflows.

LangGraph orchestrates document processing stages, including classification, extraction, validation, indexing, and human review. PostgreSQL stores application data, AWS S3 provides document storage, and ChromaDB supports vector-based retrieval for document-specific question answering.

The platform also integrates the Model Context Protocol (MCP) with Google Calendar to support approval review scheduling.

## Key Features

### 1. Authentication & Authorization

- JWT-based user authentication.
- Role-based access control (RBAC) for administrators, managers, and employees.
- Protected API endpoints based on user permissions.
- Role-aware document approval and rejection operations.

### 2. Document Management

- Document upload and metadata management.
- File type and size validation.
- Document lifecycle and processing status tracking.
- AWS S3 integration for persistent document storage.
- Document retrieval and processing through backend APIs.

### 3. AI-Powered Document Processing

- Automated document classification.
- Structured information extraction using OpenAI models.
- Validation of extracted information.
- Processing status updates and error handling.
- Guardrail checks for unsupported document types and invalid processing outcomes.

### 4. Agentic Workflows with LangGraph

- Orchestration of multi-stage document processing.
- Workflow transitions between classification, extraction, validation, and indexing.
- Routing processed documents to human review.
- Approval, rejection, and failure handling.
- State-based workflow execution and review decisions.

### 5. Guardrails & Validation

- Checks for unsupported document types.
- Validation of document processing inputs and extracted information.
- Controlled workflow progression based on validation outcomes.
- Handling of unsuccessful processing stages.
- Human review for approval decisions that require explicit authorization.

### 6. Human-in-the-Loop (HITL) Approval

- Human review of AI-processed documents.
- Manager and administrator approval or rejection.
- Required rejection reasons.
- Tracking of document review status and decisions.
- Integration of automated processing with human decision-making.

### 7. Retrieval-Augmented Generation (RAG)

- Document text chunking and indexing.
- Vector storage and similarity-based retrieval using ChromaDB.
- Context retrieval for document-specific questions.
- LLM-powered answers grounded in retrieved document content.
- Document Q&A functionality for accessing relevant information without manually searching entire documents.

**Storage consideration:** ChromaDB currently uses a local `chroma_db` directory. Its persistence depends on the runtime filesystem and deployment configuration. For environments with ephemeral filesystems, configure persistent storage or an external vector database.

### 8. MCP Integration — Google Calendar

- Model Context Protocol (MCP) integration with Google Calendar.
- Calendar tool integration for scheduling document approval reviews.
- Connection between document workflow events and external calendar actions.
- Review scheduling as part of the document processing workflow.

### 9. Audit Logging & Workflow Tracking

- Document status tracking across the approval lifecycle.
- Recording of approval and rejection actions.
- Reviewer identification where implemented.
- Audit events for workflow accountability.
- Traceability of important document management operations.

## Application Screenshots

### Dashboard & Profile

![Dashboard profile](https://github.com/Madesh-cse/AI-Document-Approval-system-backend/blob/3b775f2eba014ff2d827e8a716fecd55e53b1473/dashboard_profile-image.png)

### Document Management

![Document list](https://github.com/Madesh-cse/AI-Document-Approval-system-backend/blob/d30d48801489089eb1ec8a8f3160873feb08faa3/documentlist-4.png)

![Document management view](https://github.com/Madesh-cse/AI-Document-Approval-system-backend/blob/06eb9c3d8df96b197238caa131be7a25ee38e2b5/documentlist-6.png)

![Document processing view](https://github.com/Madesh-cse/AI-Document-Approval-system-backend/blob/4d4e55ecd6d5a94e0dc06976005873446008da39/documentlist-2.png)

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | Database ORM |
| JWT | Authentication |
| OpenAI | LLM-powered document processing |
| LangChain | LLM and RAG integration |
| LangGraph | Document workflow orchestration |
| ChromaDB | Vector storage and retrieval |
| MCP | External tool integration |
| Google Calendar | Approval review scheduling |
| AWS S3 | Document file storage |
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
                +--------+--------+
                |                 |
                v                 v
           PostgreSQL          AWS S3
          Application Data   Document Files
                |
                v
          LangGraph Workflow
                |
        +-------+--------+
        |       |        |
        v       v        v
   Classify  Extract  Validate
        |       |        |
        +-------+--------+
                |
                v
         Document Chunking
                |
                v
             ChromaDB
        Vector Index & Retrieval
                |
                v
       Human-in-the-Loop Review
                |
          +-----+-----+
          |           |
          v           v
       Approved    Rejected

       Supporting Integrations
       OpenAI | MCP | Google Calendar
```

## Project Structure

The following is a representative structure. Refer to the repository for the current implementation.

```text
AI-Document-Approval-system-backend/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   └── documents.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── mcp/
│   └── calendar_server.py
├── uploads/
├── chroma_db/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites

- Python compatible with the project's dependencies.
- PostgreSQL database.
- OpenAI API key.
- AWS account with an S3 bucket and appropriate permissions.
- Google Calendar credentials for calendar integration.
- Docker and Docker Compose for containerized execution.

### 1. Clone the Repository

```bash
git clone https://github.com/Madesh-cse/AI-Document-Approval-system-backend.git
cd AI-Document-Approval-system-backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend project root. Use the variable names expected by `app/core/config.py`.

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/DATABASE_NAME

SECRET_KEY=replace-with-a-secure-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

OPENAI_API_KEY=your-openai-api-key

AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=ap-south-1
AWS_S3_BUCKET_NAME=your-s3-bucket-name
```

Replace the placeholder values with your own configuration.

Depending on the enabled integrations, additional Google Calendar credentials or settings may be required. Check the configuration and calendar integration code for the exact variable names.

**Security recommendations:**

- Never commit `.env` files or service credentials to GitHub.
- Keep AWS credentials private and restrict their permissions to the required S3 operations.
- Use IAM roles or another secure credential mechanism when supported by the deployment environment.
- Ensure the S3 bucket and its objects are not publicly accessible unless explicitly required.
- Configure production secrets through the hosting provider's environment settings.

### 5. Configure the Database

Set `DATABASE_URL` to point to your PostgreSQL instance.

If the project uses Alembic migrations, apply the existing migrations before starting the application:

```bash
alembic upgrade head
```

Run this command from the directory containing the project's Alembic configuration. Follow the repository's existing database setup if migrations are configured differently.

### 6. Start the Backend

From the backend project root, run:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 7. Access API Documentation

FastAPI provides interactive API documentation for exploring and testing implemented endpoints.

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

Use Swagger UI to test authentication, document upload, processing, question answering, and approval operations supported by the running application.

## Docker

Docker is used to containerize the backend and support a consistent development environment.

If the repository includes the corresponding Docker configuration, build and start the services using:

```bash
docker compose up --build
```

To view running containers:

```bash
docker compose ps
```

To inspect backend logs:

```bash
docker compose logs -f
```

Ensure the required environment variables, database connection, S3 credentials, and any other dependent services are configured before starting the application.

## API Modules

The backend API is organized around the following functional areas, depending on the routes implemented in the repository:

- **Authentication:** Registration, login, and authenticated access.
- **Document management:** Uploading, listing, and retrieving documents.
- **Document processing:** AI-powered classification, extraction, and validation.
- **Approval workflow:** Document review, approval, and rejection.
- **Document Q&A:** Retrieval-based question answering.
- **Audit and tracking:** Document status and workflow activity.

For exact endpoint paths and request schemas, refer to the application's Swagger documentation.

## Security Considerations

- Enforce authentication and role-based authorization on protected endpoints.
- Validate uploaded file types and enforce file size limits.
- Restrict document operations according to user permissions.
- Secure S3 access and avoid exposing storage credentials.
- Validate AI-generated structured information before using it in business workflows.
- Treat retrieved document content as untrusted input when constructing LLM prompts.
- Keep human approval decisions distinct from automated AI outputs.
- Validate rejection reasons and other user-provided inputs.
- Configure CORS to allow only the intended frontend origins.
- Avoid logging credentials, access tokens, or sensitive document contents.

## Current Scope & Limitations

- Document classification and extraction depend on the configured LLM and supported document types.
- RAG quality depends on document parsing, chunking, embedding generation, retrieval, and the available context.
- Local ChromaDB persistence requires additional configuration for deployment environments with ephemeral filesystems.
- Google Calendar integration requires valid credentials and the appropriate API permissions.
- Docker containerization supports packaging and execution but does not itself mean the application is deployed to a cloud hosting platform.

## Future Enhancements

- Expand supported document types and extraction strategies.
- Add automated evaluation for extraction accuracy and RAG quality.
- Improve unit, integration, and end-to-end test coverage.
- Strengthen logging, monitoring, and workflow observability.
- Expand approval analytics and audit reporting.
- Improve document-level access controls and production security.
- Evaluate external vector storage for persistent, scalable retrieval.
- Optimize model and embedding workloads for resource-constrained deployments.

## Learning Outcomes

This project demonstrates practical experience with:

- REST API development using FastAPI.
- Relational database integration using PostgreSQL and SQLAlchemy.
- JWT authentication and role-based access control.
- LLM-powered document classification and information extraction.
- Agentic workflow orchestration using LangGraph.
- Retrieval-augmented generation with LangChain and ChromaDB.
- Guardrails and validation in AI workflows.
- Human-in-the-Loop approval and rejection.
- Document storage integration with AWS S3.
- MCP-based external tool integration with Google Calendar.
- Docker-based application containerization.

## Project Links

- **Frontend Demo:** [View Project Demo](https://drive.google.com/file/d/1QCYanANUBEmQn6LIpcwOEvcEy43g9GKv/view?usp=drive_link)
- **Frontend Repository:** [AI Document Approval System — Frontend](https://github.com/Madesh-cse/AI-Document-Approval-system-frontend)
- **Backend Repository:** [AI Document Approval System — Backend](https://github.com/Madesh-cse/AI-Document-Approval-system-backend)

---

**Project:** AI-Powered Document Intelligence & Approval Platform

**Focus:** AI document processing, agentic workflows, RAG, guardrails, human-supervised approvals, secure document storage, and external tool integration.


