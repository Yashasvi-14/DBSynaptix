\# DBSynaptix Project Structure



This document describes the high-level organisation of the DBSynaptix repository.



```text

dbsynaptix/

│

├── app/

│   ├── ai/

│   │   ├── preprocessing.py

│   │   ├── provider.py

│   │   ├── retrieval.py

│   │   └── similarity.py

│   │

│   ├── context/

│   │   └── context\_builder.py

│   │

│   ├── database/

│   │   ├── connection.py

│   │   └── schema\_builder.py

│   │

│   ├── indexing/

│   │   ├── document\_builder.py

│   │   └── embedding\_builder.py

│   │

│   ├── knowledge/

│   │   ├── knowledge\_builder.py

│   │   ├── knowledge\_store.py

│   │   ├── models.py

│   │   └── prompts.py

│   │

│   ├── models/

│   │   └── connection\_profile.py

│   │

│   ├── routers/

│   │   └── database.py

│   │

│   ├── schemas/

│   │   ├── database.py

│   │   └── response.py

│   │

│   ├── services/

│   │   ├── database\_service.py

│   │   └── text\_to\_sql\_service.py

│   │

│   ├── sql/

│   │   ├── prompt\_builder.py

│   │   ├── sql\_executor.py

│   │   ├── sql\_generator.py

│   │   └── sql\_validator.py

│   │

│   ├── config.py

│   └── main.py

│

├── benchmark/

│   ├── datasets/

│   │   └── northwind/

│   │       ├── questions.json

│   │       └── README.md

│   ├── config.py

│   └── runner.py

│

├── docs/

│   ├── DESIGN.md

│   └── PROJECT\_STRUCTURE.md

│

├── tests/

│   └── ...

│

├── .env.example

├── .gitignore

├── CHANGELOG.md

├── PROJECT.md

├── README.md

└── requirements.txt

```



\## Module Responsibilities



\### `app/database`



Connects to PostgreSQL and extracts structural metadata including columns, primary keys, and foreign keys.



\### `app/knowledge`



Transforms raw schema metadata into semantic database knowledge using the AI provider.



\### `app/indexing`



Builds retrieval documents and generates embeddings used by the retrieval pipeline.



\### `app/ai`



Contains AI integration, preprocessing, similarity computation, and hybrid retrieval.



\### `app/context`



Expands retrieved tables through database relationships to construct generation context.



\### `app/sql`



Handles prompt construction, SQL validation, and SQL execution.



\### `app/services`



Coordinates lower-level modules into application workflows.



\### `app/routers`



Exposes application functionality through FastAPI routes.



\### `benchmark`



Contains benchmark datasets and infrastructure used to evaluate the Text-to-SQL pipeline.



\### `tests`



Contains component, integration, retrieval, SQL, and end-to-end pipeline tests.


