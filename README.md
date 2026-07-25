# DBSynaptix

> **Giving Data a Brain.**

**Understand. Retrieve. Reason. Query.**

DBSynaptix is an AI-powered database intelligence system that translates natural-language questions into executable SQL.

Instead of sending an entire database schema directly to an LLM, DBSynaptix first builds semantic knowledge about the database, retrieves the most relevant schema context, expands that context through database relationships, and then generates, validates, and executes SQL.

The project focuses on building a modular and retrieval-driven Text-to-SQL architecture rather than a prompt-only SQL generator.

---

## Core Capabilities

- PostgreSQL metadata extraction
- Primary-key and foreign-key discovery
- AI-generated semantic database knowledge
- Gemini embedding generation
- Hybrid keyword and semantic schema retrieval
- Foreign-key-aware context expansion
- Context-grounded SQL generation
- SQL validation
- SQL execution against PostgreSQL
- End-to-end natural-language-to-results pipeline
- Northwind benchmark dataset and evaluation foundation

---

## Architecture

DBSynaptix separates database understanding from query-time SQL generation.

### Offline Knowledge Pipeline

```text
PostgreSQL Database
        |
        v
Metadata Extraction
        |
        v
Schema Assembly
        |
        v
Knowledge Builder
        |
        v
Document Builder
        |
        v
Embedding Generation
        |
        v
Semantic Schema Index
```

The system extracts database structure and enriches it with AI-generated semantic knowledge such as table summaries, business terminology, column descriptions, and example questions.

### Query-Time Pipeline

```text
Natural Language Question
          |
          v
    Hybrid Retrieval
          |
          v
     Context Builder
          |
          v
      Prompt Builder
          |
          v
         Gemini
          |
          v
      SQL Validator
          |
          v
       SQL Executor
          |
          v
         Results
```

Only relevant schema context is supplied to the generation pipeline. The context builder can expand retrieved tables using foreign-key relationships when additional tables are required for joins.

---

## Retrieval Strategy

The retrieval layer combines multiple signals to identify schema components relevant to a question.

```text
User Question
      |
      +---- Keyword Matching
      |
      +---- Semantic Similarity
      |
      v
 Hybrid Retrieval Ranking
      |
      v
 Relevant Tables
      |
      v
 Relationship Expansion
```

This design is intended to reduce unnecessary schema context while preserving information required for multi-table queries.

---

## Tech Stack

**Backend**

- Python
- FastAPI
- PostgreSQL
- Psycopg
- Pydantic

**AI**

- Google Gemini
- Gemini Embeddings

**Testing & Evaluation**

- Python test suite
- Northwind benchmark dataset

The frontend is currently planned as the next development phase.

---

## Project Structure

```text
dbsynaptix/
|
├── app/
│   ├── ai/             # AI provider, preprocessing and retrieval
│   ├── context/        # Relationship-aware context expansion
│   ├── database/       # PostgreSQL connection and metadata extraction
│   ├── indexing/       # Retrieval document and embedding generation
│   ├── knowledge/      # Semantic database knowledge generation
│   ├── models/         # Internal data models
│   ├── routers/        # FastAPI routes
│   ├── schemas/        # API request/response schemas
│   ├── services/       # Application orchestration
│   └── sql/            # Prompt construction, validation and execution
│
├── benchmark/
│   └── datasets/
│       └── northwind/  # Text-to-SQL benchmark questions
│
├── docs/               # Engineering and design documentation
├── tests/              # Component and pipeline tests
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd dbsynaptix
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and provide your Gemini API key.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Database connection information is supplied through the database connection request when connecting to PostgreSQL.

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

---

## Benchmarking

DBSynaptix includes a Northwind benchmark foundation for evaluating the Text-to-SQL pipeline across different query types.

The current dataset contains questions covering:

- Simple retrieval
- Filtering
- Aggregation
- Joins
- Analytical queries

The benchmark infrastructure is being developed to measure areas such as SQL generation success, execution success, latency, retrieval behaviour, and token usage.

No benchmark metric is treated as a project claim until it has been reproduced through the evaluation pipeline.

---

## Current Status

### Implemented

- Database metadata engine
- Semantic knowledge generation
- Retrieval document generation
- Gemini embeddings
- Hybrid schema retrieval
- Relationship-aware context construction
- Text-to-SQL generation pipeline
- SQL validation and execution
- Component and end-to-end tests
- Northwind benchmark dataset and runner foundation

### Next

- Frontend workspace
- Persistent semantic index
- SQL self-correction
- Query history
- SQL explanations
- Expanded benchmark evaluation and reporting
- Multi-database support

---

## Design Philosophy

A Text-to-SQL system should not require an LLM to reason over every table in a database for every question.

DBSynaptix therefore follows a retrieval-first architecture:

**Understand the database → Retrieve relevant context → Reason over relationships → Generate SQL**

The long-term goal is to evolve this architecture into a database intelligence platform capable of working with larger schemas while keeping generation grounded in relevant database context.
