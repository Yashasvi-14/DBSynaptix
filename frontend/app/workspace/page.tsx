"use client";

import Link from "next/link";
import { useState, useSyncExternalStore } from "react";

type DatabaseConnection = {
  host: string;
  port: number;
  database: string;
  username: string;
  password: string;
};

type SchemaColumn = {
  name: string;
  type: string;
};

type ForeignKey = {
  column: string;
  references: {
    table: string;
    column: string;
  };
};

type TableSchema = {
  columns: SchemaColumn[];
  primary_keys: string[];
  foreign_keys: ForeignKey[];
};

type DatabaseSchema = Record<string, TableSchema>;

type QueryResponse = {
  question: string;
  sql: string;
  results: Record<string, unknown>[];
  repair_attempted: boolean;
  repair_successful: boolean;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  timings: {
    retrieval_ms: number;
    context_ms: number;
    generation_ms: number;
    execution_ms: number;
    total_ms: number;
  };
};

type QueryHistoryItem = {
  id: number;
  response: QueryResponse;
};

function subscribe() {
  return () => {};
}

function getConnectionSnapshot() {
  return sessionStorage.getItem("dbsynaptix_connection");
}

function getServerConnectionSnapshot() {
  return null;
}

function getSchemaSnapshot() {
  return sessionStorage.getItem("dbsynaptix_schema");
}

function getServerSchemaSnapshot() {
  return null;
}

function formatCellValue(value: unknown): string {
  if (value === null || value === undefined) {
    return "NULL";
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`border-b-2 px-4 py-4 text-sm transition ${
        active
          ? "border-primary text-foreground"
          : "border-transparent text-foreground-muted hover:text-foreground-secondary"
      }`}
    >
      {children}
    </button>
  );
}

function formatDuration(ms: number) {
  if (ms < 1000) {
    return `${ms.toFixed(2)} ms`;
  }

  return `${(ms / 1000).toFixed(2)} s`;
}

function PipelineStep({
  title,
  description,
  duration,
}: {
  title: string;
  description: string;
  duration: number;
}) {
  return (
    <div className="rounded-xl border border-border bg-background p-4">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-success/10 text-xs text-success">
            ✓
          </span>

          <span className="text-sm font-medium">{title}</span>
        </div>

        <span className="shrink-0 font-mono text-xs text-foreground-muted">
          {formatDuration(duration)}
        </span>
      </div>

      <p className="mt-2 pl-8 text-xs text-foreground-muted">{description}</p>
    </div>
  );
}

export default function WorkspacePage() {
  const storedConnection = useSyncExternalStore(
    subscribe,
    getConnectionSnapshot,
    getServerConnectionSnapshot,
  );

  let connection: DatabaseConnection | null = null;

  if (storedConnection) {
    try {
      connection = JSON.parse(storedConnection) as DatabaseConnection;
    } catch {
      connection = null;
    }
  }

  const storedSchema = useSyncExternalStore(
    subscribe,
    getSchemaSnapshot,
    getServerSchemaSnapshot,
  );

  let schema: DatabaseSchema | null = null;

  if (storedSchema) {
    try {
      schema = JSON.parse(storedSchema) as DatabaseSchema;
    } catch {
      schema = null;
    }
  }

  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [response, setResponse] = useState<QueryResponse | null>(null);

  const [expandedTables, setExpandedTables] = useState<Set<string>>(new Set());

  const [activeTab, setActiveTab] = useState<"results" | "sql" | "pipeline">(
    "results",
  );

  const [queryHistory, setQueryHistory] = useState<QueryHistoryItem[]>([]);

  function toggleTable(tableName: string) {
    setExpandedTables((current) => {
      const next = new Set(current);

      if (next.has(tableName)) {
        next.delete(tableName);
      } else {
        next.add(tableName);
      }

      return next;
    });
  }

  async function handleQuery() {
    if (!connection || !question.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const apiResponse = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/query`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question.trim(),
            database: connection,
          }),
        },
      );

      const data = await apiResponse.json();

      if (!apiResponse.ok) {
        throw new Error(
          data.detail || data.message || "Failed to execute query.",
        );
      }

      setResponse(data);
      setQueryHistory((current) => [
        {
          id: Date.now(),
          response: data,
        },
        ...current,
      ]);
    } catch (error) {
      setError(
        error instanceof Error ? error.message : "Failed to execute query.",
      );
    } finally {
      setLoading(false);
    }
  }
  function handleHistorySelect(item: QueryHistoryItem) {
    setQuestion(item.response.question);
    setResponse(item.response);
    setActiveTab("results");
    setError("");
  }

  return (
    <main className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="border-b border-border">
        <div className="mx-auto flex h-18 max-w-[1600px] items-center justify-between px-8">
          <Link href="/" className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary font-semibold text-white">
              D
            </div>

            <span className="text-lg font-semibold tracking-tight">
              DBSynaptix
            </span>
          </Link>

          {connection && (
            <div className="flex items-center gap-3 text-sm">
              <span className="h-2 w-2 rounded-full bg-success" />

              <span className="text-foreground-secondary">Connected to</span>

              <span className="font-medium">{connection.database}</span>
            </div>
          )}
        </div>
      </nav>
      <div className="mx-auto flex max-w-[1600px]">
        {/* Schema Sidebar */}
        <aside className="sticky top-[72px] h-[calc(100vh-72px)] w-72 shrink-0 overflow-y-auto border-r border-border p-5">
          <div className="text-xs font-medium uppercase tracking-wider text-foreground-muted">
            Database
          </div>

          <div className="mt-3 flex items-center gap-3 rounded-lg bg-surface px-3 py-2.5">
            <span className="h-2 w-2 shrink-0 rounded-full bg-success" />

            <span className="truncate text-sm font-medium">
              {connection?.database ?? "No database"}
            </span>
          </div>

          <div className="mt-8 flex items-center justify-between">
            <div className="text-xs font-medium uppercase tracking-wider text-foreground-muted">
              Schema
            </div>

            {schema && (
              <span className="text-xs text-foreground-muted">
                {Object.keys(schema).length} tables
              </span>
            )}
          </div>

          {/* Tables */}
          <div className="mt-3 space-y-1">
            {schema &&
              Object.entries(schema).map(([tableName, table]) => {
                const expanded = expandedTables.has(tableName);

                return (
                  <div key={tableName}>
                    <button
                      type="button"
                      onClick={() => toggleTable(tableName)}
                      className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-sm transition hover:bg-surface"
                    >
                      <span className="w-4 shrink-0 text-xs text-foreground-muted">
                        {expanded ? "▾" : "▸"}
                      </span>

                      <span className="truncate">{tableName}</span>
                    </button>

                    {expanded && (
                      <div className="ml-5 border-l border-border py-1 pl-3">
                        {table.columns.map((column) => {
                          const isPrimary = table.primary_keys.includes(
                            column.name,
                          );

                          const foreignKey = table.foreign_keys.find(
                            (key) => key.column === column.name,
                          );

                          return (
                            <div key={column.name} className="py-1.5">
                              <div className="flex min-w-0 items-center gap-2">
                                <span className="w-5 shrink-0 text-[10px] font-medium text-foreground-muted">
                                  {isPrimary ? "PK" : foreignKey ? "FK" : ""}
                                </span>

                                <span className="truncate text-xs text-foreground-secondary">
                                  {column.name}
                                </span>
                              </div>

                              <div className="ml-7 truncate text-[10px] text-foreground-muted">
                                {column.type}
                              </div>

                              {foreignKey && (
                                <div className="ml-7 truncate text-[10px] text-primary">
                                  → {foreignKey.references.table}.
                                  {foreignKey.references.column}
                                </div>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
          </div>
        </aside>

        {/* Query Workspace */}
        <section className="min-w-0 flex-1 px-10 py-16">
          {/* KEEP ALL YOUR EXISTING WORKSPACE CONTENT HERE */}
          {/* Header */}
          <div className="max-w-3xl">
            <div className="text-sm font-medium text-primary">
              QUERY WORKSPACE
            </div>

            <h1 className="mt-4 text-4xl font-semibold tracking-[-0.04em]">
              Ask your database.
            </h1>

            <p className="mt-4 text-foreground-secondary">
              Ask a question in natural language and DBSynaptix will retrieve
              the relevant schema context, generate SQL, validate it, and
              execute it.
            </p>
          </div>

          {/* Question */}
          <div className="mt-10 rounded-2xl border border-border bg-surface p-6">
            <label className="text-sm text-foreground-secondary">
              Question
            </label>

            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="e.g. Show the top 5 products by unit price"
              rows={4}
              className="mt-3 w-full resize-none rounded-xl border border-border bg-background px-4 py-4 text-sm text-foreground outline-none transition focus:border-primary"
            />

            <div className="mt-4 flex justify-end">
              <button
                onClick={handleQuery}
                disabled={loading || !connection || !question.trim()}
                className="rounded-xl bg-primary px-5 py-3 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Running pipeline..." : "Generate SQL"}
              </button>
            </div>
          </div>

          {queryHistory.length > 0 && (
            <div className="mt-6 rounded-2xl border border-border bg-surface">
              <div className="flex items-center justify-between border-b border-border px-6 py-4">
                <div>
                  <h2 className="text-sm font-medium">Query History</h2>

                  <p className="mt-1 text-xs text-foreground-muted">
                    Queries from this session
                  </p>
                </div>

                <button
                  onClick={() => setQueryHistory([])}
                  className="text-xs text-foreground-muted transition hover:text-foreground"
                >
                  Clear
                </button>
              </div>

              <div className="divide-y divide-border">
                {queryHistory.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => handleHistorySelect(item)}
                    className="w-full px-6 py-4 text-left transition hover:bg-background"
                  >
                    <div className="flex items-start justify-between gap-6">
                      <div className="min-w-0">
                        <p className="truncate text-sm font-medium">
                          {item.response.question}
                        </p>

                        <p className="mt-2 truncate font-mono text-xs text-foreground-muted">
                          {item.response.sql}
                        </p>
                      </div>

                      <span className="shrink-0 font-mono text-xs text-foreground-muted">
                        {formatDuration(item.response.timings.total_ms)}
                      </span>
                    </div>

                    <div className="mt-3 flex flex-wrap gap-4 text-xs text-foreground-muted">
                      <span>{item.response.results.length} rows</span>

                      <span>{item.response.total_tokens} tokens</span>

                      {item.response.repair_attempted && (
                        <span>SQL repaired</span>
                      )}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Query Error */}
          {error && (
            <div className="mt-6 rounded-xl border border-error/30 bg-error/10 px-4 py-3 text-sm text-error">
              {error}
            </div>
          )}

          {/* Response */}
          {response && (
            <div className="mt-8 overflow-hidden rounded-2xl border border-border bg-surface">
              {/* Tabs */}
              <div className="flex items-center border-b border-border px-6">
                <TabButton
                  active={activeTab === "results"}
                  onClick={() => setActiveTab("results")}
                >
                  Results
                </TabButton>

                <TabButton
                  active={activeTab === "sql"}
                  onClick={() => setActiveTab("sql")}
                >
                  SQL
                </TabButton>

                <TabButton
                  active={activeTab === "pipeline"}
                  onClick={() => setActiveTab("pipeline")}
                >
                  Pipeline
                </TabButton>
              </div>

              {/* Results */}
              {activeTab === "results" && (
                <div className="p-6">
                  {response.results.length > 0 ? (
                    <>
                      <div className="mb-4 text-xs text-foreground-muted">
                        {response.results.length} rows returned
                      </div>

                      <div className="overflow-hidden rounded-xl border border-border">
                        <div className="overflow-x-auto">
                          <table className="w-full text-left text-sm">
                            <thead className="border-b border-border bg-background">
                              <tr>
                                {Object.keys(response.results[0]).map(
                                  (column) => (
                                    <th
                                      key={column}
                                      className="whitespace-nowrap px-5 py-3 font-medium text-foreground-secondary"
                                    >
                                      {column}
                                    </th>
                                  ),
                                )}
                              </tr>
                            </thead>

                            <tbody>
                              {response.results.map((row, rowIndex) => (
                                <tr
                                  key={rowIndex}
                                  className="border-b border-border last:border-b-0"
                                >
                                  {Object.keys(response.results[0]).map(
                                    (column) => (
                                      <td
                                        key={column}
                                        className="whitespace-nowrap px-5 py-3"
                                      >
                                        {formatCellValue(row[column])}
                                      </td>
                                    ),
                                  )}
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </>
                  ) : (
                    <div className="py-10 text-center text-sm text-foreground-secondary">
                      Query executed successfully but returned no rows.
                    </div>
                  )}
                </div>
              )}

              {/* SQL */}
              {activeTab === "sql" && (
                <div className="p-6">
                  <div className="mb-3 text-xs font-medium uppercase tracking-wider text-foreground-muted">
                    Generated SQL
                  </div>

                  <pre className="whitespace-pre-wrap break-words rounded-xl border border-border bg-background p-5 font-mono text-sm leading-7">
                    {response.sql}
                  </pre>
                </div>
              )}

              {/* Pipeline */}
              {activeTab === "pipeline" && (
                <div className="p-6">
                  <div className="grid gap-3 sm:grid-cols-2">
                    <PipelineStep
                      title="Schema Retrieval"
                      description="Relevant schema context retrieved"
                      duration={response.timings.retrieval_ms}
                    />

                    <PipelineStep
                      title="Context Expansion"
                      description="Schema relationships expanded"
                      duration={response.timings.context_ms}
                    />

                    <PipelineStep
                      title="SQL Generation"
                      description="Natural language converted to SQL"
                      duration={response.timings.generation_ms}
                    />

                    <PipelineStep
                      title="Execution"
                      description="Query executed against PostgreSQL"
                      duration={response.timings.execution_ms}
                    />
                  </div>

                  <div className="mt-4 flex items-center justify-between rounded-xl border border-border bg-background px-4 py-3">
                    <span className="text-sm text-foreground-secondary">
                      Total pipeline latency
                    </span>

                    <span className="font-mono text-sm font-medium">
                      {formatDuration(response.timings.total_ms)}
                    </span>
                  </div>
                </div>
              )}

              {/* Metadata Footer */}
              <div className="flex flex-wrap gap-5 border-t border-border px-6 py-4 text-xs text-foreground-muted">
                <span>Rows: {response.results.length}</span>

                <span>Prompt: {response.prompt_tokens}</span>

                <span>Completion: {response.completion_tokens}</span>

                <span>Total tokens: {response.total_tokens}</span>

                <span>
                  Repair:{" "}
                  {response.repair_attempted
                    ? response.repair_successful
                      ? "Successful"
                      : "Attempted"
                    : "Not needed"}
                </span>
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
