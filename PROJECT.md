# DBSynaptix

> Internal Engineering Document

## Project Identity

**Public Name:** DBSynaptix  
**Internal Codename:** Mission ANVIL  
**Tagline:** Giving Data a Brain.  
**Philosophy:** Understand. Retrieve. Reason. Query.

---

## Vision

DBSynaptix is an AI-powered database intelligence system designed to enable natural-language interaction with relational databases.

Instead of relying on an LLM to reason over an entire schema for every query, DBSynaptix builds semantic knowledge about the database, retrieves relevant schema context, expands that context through relationships, generates SQL, validates it, and executes it.

The long-term objective is to evolve the system from a Text-to-SQL pipeline into a broader database intelligence platform.

---

## Design Principles

### 1. Retrieval Before Generation

Avoid sending the complete database schema to the LLM when only a subset is relevant.

```text
Question
   |
   v
Hybrid Retrieval
   |
   v
Relationship Expansion
   |
   v
Prompt Construction
   |
   v
LLM
```

### 2. Ground Generation in Database Structure

SQL generation should operate on retrieved schema information, including columns, keys, relationships, and semantic knowledge.

### 3. Modular Architecture

Each subsystem should have a focused responsibility and communicate through explicit interfaces.

### 4. Measurable AI Behaviour

AI capabilities should eventually be evaluated through reproducible benchmarks rather than subjective examples.

Relevant metrics include:

- Retrieval quality
- SQL generation success
- Execution success
- Latency
- Token usage
- Hallucination behaviour

### 5. Production-Oriented Design

Prefer maintainability, observability, safety, and scalability over shortcuts that only work for demonstrations.

---

## Current Architecture

DBSynaptix contains two major flows.

### Offline Database Understanding

```text
PostgreSQL
    |
    v
Metadata Extraction
    |
    v
Schema Assembly
    |
    v
Knowledge Generation
    |
    v
Retrieval Documents
    |
    v
Embeddings
```

### Query-Time Pipeline

```text
User Question
      |
      v
Hybrid Retriever
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

---

## Backend Modules

### Database

Responsible for:

- PostgreSQL connections
- Column metadata extraction
- Primary-key discovery
- Foreign-key discovery
- Schema assembly

### Knowledge

Responsible for:

- Semantic table summaries
- Business terminology
- Column descriptions
- Example questions
- Database knowledge construction

### Indexing

Responsible for:

- Retrieval document construction
- Embedding generation

### AI

Responsible for:

- Gemini integration
- Query preprocessing
- Similarity computation
- Hybrid retrieval

### Context

Responsible for:

- Selecting retrieved schema context
- Expanding context using parent relationships
- Expanding context using reverse/child relationships

### SQL

Responsible for:

- Prompt construction
- SQL validation
- SQL execution

### Services

Responsible for:

- Coordinating the end-to-end Text-to-SQL workflow
- Connecting retrieval, context construction, generation, validation and execution

### Benchmark

Currently provides:

- Northwind benchmark questions
- Dataset configuration
- Benchmark runner foundation

The evaluation layer will be expanded as development continues.

---

## Current Development Status

### Implemented

- PostgreSQL metadata engine
- Schema assembly
- AI-generated database knowledge
- Retrieval document generation
- Gemini embeddings
- Query preprocessing
- Hybrid retrieval
- Relationship-aware context expansion
- Prompt construction
- Gemini SQL generation
- SQL validation
- SQL execution
- End-to-end Text-to-SQL orchestration
- Northwind benchmark foundation
- Component and pipeline tests

### In Development / Planned

- Professional frontend
- Persistent semantic index
- SQL self-correction
- SQL explanations
- Query history
- Expanded benchmark metrics and reporting
- Query caching
- Multi-database support
- Schema change detection

---

## Frontend Direction

The frontend is the next major development phase.

The intended experience is a modern AI database workspace centred around:

- Database connection
- Natural-language question input
- Generated SQL
- Query results
- Pipeline visibility
- Query history
- Evaluation information

Candidate technologies include:

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- Framer Motion
- Monaco Editor

These technologies represent the current frontend direction and are not part of the implemented backend.

---

## Evaluation Strategy

The Northwind dataset provides the initial benchmark foundation.

Evaluation should eventually measure:

- Retrieval relevance
- SQL generation success
- SQL execution success
- Query latency
- Prompt and completion token usage
- Failure categories
- SQL repair success after self-correction is implemented

Benchmark results should only become public project metrics when the evaluation procedure is reproducible.

---

## Development Roadmap

### Phase 1 — Core Backend

Implemented:

- Database metadata engine
- Semantic knowledge layer
- Embedding generation
- Hybrid retrieval
- Context expansion
- Text-to-SQL generation
- SQL validation
- SQL execution

### Phase 2 — Product Interface

Planned:

- Landing page
- Database connection flow
- Query workspace
- SQL viewer/editor
- Results table
- Pipeline state visualization

### Phase 3 — Reliability

Planned:

- SQL self-correction
- Persistent semantic index
- Query history
- SQL explanations
- Query caching

### Phase 4 — Evaluation

Started:

- Northwind benchmark dataset
- Benchmark runner foundation

Planned:

- Retrieval metrics
- SQL accuracy metrics
- Execution metrics
- Latency reporting
- Token usage reporting
- Failure analysis

### Phase 5 — Platform Expansion

Planned:

- pgvector integration
- Multi-database support
- Schema change detection
- Advanced retrieval optimisation

---

## Coding Standards

### Python

- `snake_case` for variables and functions
- `PascalCase` for classes
- Type hints where useful
- Small, focused functions
- Clear module boundaries

### Frontend

- Functional components
- Hooks
- `PascalCase` components
- `camelCase` variables

### General

Prefer readability and explicit behaviour over unnecessary abstraction.

---

## Commit Convention

```text
feat:     new functionality
fix:      bug fix
docs:     documentation
test:     testing changes
refactor: internal restructuring
perf:     performance improvement
style:    formatting or UI-only changes
chore:    maintenance
```

---

## Future Research Directions

Potential areas to explore after the core product is stable:

- Agentic SQL planning
- Conversational database interactions
- Streaming generation
- Query optimisation
- Automated dashboard generation
- AI-generated data insights

---

## Product Principle

DBSynaptix should not be a thin prompt wrapper.

Its core architecture should remain:

**Understand → Retrieve → Reason → Query**