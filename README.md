# AI Customer Support & Billing Assistant API

AI-powered customer support and billing assistant built with FastAPI, PostgreSQL, SQLAlchemy, Docker, and Gemini function calling.

## Features

* AI-powered customer support chat
* Customer information lookup
* Invoice information lookup
* Payment status lookup
* Subscription status lookup
* Support ticket lookup
* Support ticket creation
* Gemini function calling
* Multiple tool calling
* Tool-level permissions
* Human approval workflow for write actions
* Approval rejection
* Error handling
* PostgreSQL database
* SQLAlchemy ORM
* Alembic migrations
* Docker Compose
* Interactive Swagger API documentation

## Tech Stack

* Python 3.11
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* Gemini API
* Docker
* Docker Compose
* Uvicorn

## How It Works

The application allows users to communicate with an AI assistant through a REST API.

The AI analyzes the user's request and decides whether an application tool is required.

For example:

```text
User
  ↓
POST /api/v1/chat
  ↓
Gemini AI
  ↓
Function / Tool Selection
  ↓
Application Tool
  ↓
PostgreSQL
  ↓
Tool Result
  ↓
Gemini AI
  ↓
Final Response
```

Read-only operations can be executed directly.

Write operations require human approval before the actual action is executed.

## Available AI Tools

The assistant currently supports the following tools:

### get_customer

Retrieves customer information.

### get_invoice

Retrieves invoice information.

### get_payment_status

Retrieves payment information and payment status.

### get_subscription

Retrieves subscription information.

### get_ticket

Retrieves support ticket information.

### create_support_ticket

Creates a new support ticket.

This is a write operation and requires human approval.

## Human Approval Workflow

Write actions are protected by a human approval workflow.

Example:

```text
User requests a new support ticket
        ↓
AI detects create_support_ticket
        ↓
Approval request created
        ↓
Approval status = pending
        ↓
Human reviews request
        ↓
Approve
        ↓
Support ticket is created
```

If the request is rejected:

```text
Approval request
        ↓
Reject
        ↓
Approval status = rejected
        ↓
Action is not executed
```

This prevents write operations from being executed automatically without approval.

## Project Structure

```text
ai-support-assistant/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── app/
│   ├── ai/
│   │   ├── client.py
│   │   ├── permissions.py
│   │   ├── service.py
│   │   ├── tools.py
│   │   └── tools_schema.py
│   │
│   ├── api/
│   │   ├── ai.py
│   │   ├── approval.py
│   │   ├── customer.py
│   │   ├── invoice.py
│   │   ├── payment.py
│   │   ├── subscription.py
│   │   └── ticket.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── dependencies.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── approval.py
│   │   ├── customer.py
│   │   ├── invoice.py
│   │   ├── payment.py
│   │   ├── subscription.py
│   │   └── ticket.py
│   │
│   ├── services/
│   │   ├── approval_service.py
│   │   ├── customer_service.py
│   │   ├── invoice_service.py
│   │   ├── payment_service.py
│   │   ├── subscription_service.py
│   │   └── ticket_service.py
│   │
│   └── main.py
│
├── .env
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Database

The application uses PostgreSQL as the primary database.

SQLAlchemy is used as the ORM and Alembic is used for database migrations.

### Main Tables

* customers
* invoices
* payments
* subscriptions
* support_tickets
* approvals

## API Endpoints

### Health Endpoints

```text
GET /
GET /health
GET /health/database
```

### AI Chat

```text
POST /api/v1/chat
```

Request:

```json
{
  "prompt": "What is the status of subscription 1?"
}
```

### Customers

```text
GET /api/v1/customers
```

### Invoices

```text
GET /api/v1/invoices
```

### Payments

```text
GET /api/v1/payments
```

### Subscriptions

```text
GET /api/v1/subscriptions
```

### Support Tickets

```text
POST /api/v1/tickets
```

### Approvals

```text
GET /api/v1/approvals/{approval_id}
POST /api/v1/approvals/{approval_id}/approve
POST /api/v1/approvals/{approval_id}/reject
```

## AI Chat Examples

### Customer Information

Request:

```json
{
  "prompt": "Tell me the name and email of customer 1."
}
```

The AI can call:

```text
get_customer
```

### Payment Status

Request:

```json
{
  "prompt": "What is the payment status of payment 1?"
}
```

The AI can call:

```text
get_payment_status
```

### Subscription Status

Request:

```json
{
  "prompt": "What is the status of subscription 1?"
}
```

The AI can call:

```text
get_subscription
```

### Support Ticket

Request:

```json
{
  "prompt": "Tell me the details of support ticket 2."
}
```

The AI can call:

```text
get_ticket
```

### Multiple Tools

The assistant can use multiple tools for a single request.

Example:

```json
{
  "prompt": "For customer 1, tell me the payment status of payment 1 and the subscription status of subscription 1."
}
```

The AI can call:

```text
get_payment_status
get_subscription
```

and combine the results into a single response.

## Human Approval Example

Request:

```json
{
  "prompt": "Create a high priority support ticket for customer 1. The subject is Account security and the description is The customer needs help securing the account."
}
```

The AI detects that `create_support_ticket` is a write operation.

Instead of creating the ticket immediately, the application creates an approval request.

Example response:

```json
{
  "response": "Human approval is required before this action can be executed. Approval ID: 3. The action has not been executed yet."
}
```

The approval can then be reviewed.

### Approve

```text
POST /api/v1/approvals/3/approve
```

If approved, the support ticket is created.

### Reject

```text
POST /api/v1/approvals/3/reject
```

If rejected, the support ticket is not created.

## Permissions

The application separates tools into read-only and write operations.

### Read-only Tools

```text
get_customer
get_invoice
get_payment_status
get_subscription
get_ticket
```

### Write Tools

```text
create_support_ticket
```

Write tools require human approval.

## Environment Variables

Create a `.env` file in the project root.

```env
APP_NAME=AI Customer Support & Billing Assistant API
APP_VERSION=1.0.0
DEBUG=True
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5434/ai_support_db
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Never commit your real API key to GitHub.

Make sure `.env` is included in `.gitignore`.

## Installation

Clone the repository:

```cmd
git clone https://github.com/Almas-Web/ai-support-assistant.git
```

Go to the project directory:

```cmd
cd ai-support-assistant
```

Create a virtual environment:

```cmd
python -m venv venv
```

Activate the virtual environment:

```cmd
venv\Scripts\activate
```

Install dependencies:

```cmd
pip install -r requirements.txt
```

## Database Setup

Start PostgreSQL using Docker Compose:

```cmd
docker compose up -d
```

Run Alembic migrations:

```cmd
alembic upgrade head
```

## Run the Application

Start the FastAPI application:

```cmd
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Docker

Docker Compose is used to run the PostgreSQL database.

Start the database:

```cmd
docker compose up -d
```

Check running containers:

```cmd
docker ps
```

Stop the database:

```cmd
docker compose down
```

The current Docker Compose configuration runs PostgreSQL while the FastAPI application can be run locally with Uvicorn.

## Database Migration

Create a new migration after changing database models:

```cmd
alembic revision --autogenerate -m "your migration message"
```

Apply migrations:

```cmd
alembic upgrade head
```

Check the current migration:

```cmd
alembic current
```

## Error Handling

The application handles common tool errors such as:

* Customer not found
* Invoice not found
* Payment not found
* Subscription not found
* Support ticket not found
* Approval request not found
* Already approved approval
* Already rejected approval
* Unauthorized tool execution

Example:

```json
{
  "prompt": "Tell me about customer 999."
}
```

If customer `999` does not exist, the AI returns a clear not-found response instead of failing silently.

## Testing

The application has been manually tested for:

* API health
* Database connection
* Customer lookup
* Invoice lookup
* Payment status
* Subscription status
* Support ticket lookup
* Multiple tool calls
* Missing customer handling
* Missing resource handling
* Tool permissions
* Human approval workflow
* Support ticket creation after approval
* Approval rejection
* Blocking already rejected approvals
* AI chat endpoint

## Security Considerations

This project is designed as a learning and portfolio project.

The current approval endpoints demonstrate the approval workflow but do not include production authentication and authorization.

For production use, the application should add:

* JWT authentication
* User accounts
* Role-based access control
* Permission checks for approval actions
* Audit logging
* Rate limiting
* API key protection
* Production secrets management
* HTTPS
* Stronger input validation

## Future Improvements

Possible future improvements include:

* JWT authentication
* Role-based access control
* Conversation history
* More billing tools
* More customer support tools
* Automated background tasks
* Email notifications
* SLA automation
* Redis integration
* Celery integration
* Automated pytest test suite
* Production Docker deployment
* CI/CD pipeline
* Monitoring and logging

## Learning Goals

This project was built to practice:

* FastAPI backend development
* REST API design
* PostgreSQL
* SQLAlchemy
* Alembic migrations
* Docker
* Gemini API integration
* LLM function calling
* Tool calling
* AI application architecture
* Permission handling
* Human-in-the-loop workflows
* Backend error handling

## Author

**Almas Hossen**

Python Backend Developer focused on:

* Python
* Django
* FastAPI
* PostgreSQL
* REST APIs
* Docker
* AI Integration
* Backend Automation

GitHub:

https://github.com/Almas-Web

Portfolio:

https://almas-web-portfolio.netlify.app/
