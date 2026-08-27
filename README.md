# Text-to-SQL GenAI Platform

> Convert natural-language business questions into executable PostgreSQL queries using Gemini, schema-aware prompting, SQL validation, and automatic self-correction.

## Overview

The **Text-to-SQL GenAI Platform** is an LLM-powered system that allows users to query a relational business database using natural language.

Instead of requiring users to write SQL manually, the system:

1. Understands the user's question
2. Decomposes the question into a structured representation
3. Generates PostgreSQL SQL using Gemini
4. Validates the generated query for basic SQL safety
5. Executes the query against PostgreSQL
6. Detects execution failures
7. Uses an LLM-based correction step to repair failed SQL
8. Returns the final query results
9. Logs pipeline executions for evaluation and debugging

### Pipeline

```text
Natural Language Question
          │
          ▼
┌──────────────────────┐
│ Question Decomposition│
│      Gemini LLM       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   SQL Generation     │
│      Gemini LLM       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   SQL Safety Check   │
│   Rule-Based Layer   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ PostgreSQL Execution │
└──────────┬───────────┘
           │
      ┌────┴────┐
      │ Success │
      └────┬────┘
           │
           ▼
        Results

If execution fails:

Generated SQL
     │
     ▼
PostgreSQL Error
     │
     ▼
LLM Self-Correction
     │
     ▼
Re-validation
     │
     ▼
PostgreSQL Retry

