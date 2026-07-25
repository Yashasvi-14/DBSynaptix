# Changelog

All notable changes to DBSynaptix are documented in this file.

---

## [Unreleased]

### In Development

- Frontend workspace
- Persistent semantic index
- SQL self-correction
- Query history
- SQL explanations
- Expanded benchmark evaluation and reporting

---

## [v1.0-backend] - 2026-07-26

### Added

#### Database Engine

- PostgreSQL connection support
- Column metadata extraction
- Primary-key discovery
- Foreign-key discovery
- Structured schema assembly

#### Semantic Knowledge Layer

- AI-generated table summaries
- Business terminology generation
- Column descriptions
- Example question generation
- Database knowledge construction

#### Indexing

- Retrieval document construction
- Gemini embedding generation
- Schema embedding pipeline

#### Retrieval

- Query preprocessing
- Keyword-based relevance scoring
- Semantic similarity scoring
- Hybrid schema retrieval
- Foreign-key-aware context expansion

#### Text-to-SQL Pipeline

- Context-grounded prompt construction
- Gemini SQL generation
- SQL validation
- PostgreSQL query execution
- End-to-end Text-to-SQL orchestration

#### API

- Database connection endpoint
- Database schema retrieval endpoint

#### Evaluation

- Northwind benchmark dataset
- Benchmark configuration
- Benchmark runner foundation
- Query categories covering retrieval, filtering, aggregation, joins, and analytics

#### Testing

- Knowledge layer tests
- Indexing tests
- Retrieval tests
- Context builder tests
- Prompt builder tests
- SQL validator tests
- SQL executor tests
- End-to-end Text-to-SQL pipeline tests

#### Repository

- Environment-based Gemini configuration
- Example environment configuration
- Modular backend package structure
- Engineering documentation

---

## Planned

### Product Interface

- Database connection interface
- Natural-language query workspace
- Generated SQL viewer
- Results table
- Pipeline visualization

### Reliability

- SQL self-correction
- Persistent semantic index
- Query history
- SQL explanations
- Query caching

### Evaluation

- Retrieval metrics
- SQL accuracy metrics
- Execution metrics
- Latency reporting
- Token usage reporting
- Failure analysis

### Platform

- pgvector integration
- Multi-database support
- Schema change detection