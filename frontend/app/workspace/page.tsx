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

type QueryResponse = {
  question: string;
  sql: string;
  results: Record<string, unknown>[];
  repair_attempted: boolean;
  repair_successful: boolean;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
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

function formatCellValue(value: unknown): string {
  if (value === null || value === undefined) {
    return "NULL";
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}

export default function WorkspacePage() {
  const storedConnection = useSyncExternalStore(
    subscribe,
    getConnectionSnapshot,
    getServerConnectionSnapshot
  );

  let connection: DatabaseConnection | null = null;

  if (storedConnection) {
    try {
      connection = JSON.parse(
        storedConnection
      ) as DatabaseConnection;
    } catch {
      connection = null;
    }
  }

  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [response, setResponse] =
    useState<QueryResponse | null>(null);

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
        }
      );

      const data = await apiResponse.json();

      if (!apiResponse.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            "Failed to execute query."
        );
      }

      setResponse(data);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to execute query."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-background">
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

              <span className="text-foreground-secondary">
                Connected to
              </span>

              <span className="font-medium">
                {connection.database}
              </span>
            </div>
          )}
        </div>
      </nav>

      <section className="mx-auto max-w-[1200px] px-8 py-16">
        <div className="max-w-3xl">
          <div className="text-sm font-medium text-primary">
            QUERY WORKSPACE
          </div>

          <h1 className="mt-4 text-4xl font-semibold tracking-[-0.04em]">
            Ask your database.
          </h1>

          <p className="mt-4 text-foreground-secondary">
            Ask a question in natural language and DBSynaptix
            will retrieve the relevant schema context, generate
            SQL, validate it, and execute it.
          </p>
        </div>

        <div className="mt-10 rounded-2xl border border-border bg-surface p-6">
          <label className="text-sm text-foreground-secondary">
            Question
          </label>

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            placeholder="e.g. Show the top 5 products by unit price"
            rows={4}
            className="mt-3 w-full resize-none rounded-xl border border-border bg-background px-4 py-4 text-sm text-foreground outline-none transition focus:border-primary"
          />

          <div className="mt-4 flex justify-end">
            <button
              onClick={handleQuery}
              disabled={
                loading ||
                !connection ||
                !question.trim()
              }
              className="rounded-xl bg-primary px-5 py-3 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading
                ? "Running pipeline..."
                : "Generate SQL"}
            </button>
          </div>
        </div>

        {error && (
          <div className="mt-6 rounded-xl border border-error/30 bg-error/10 px-4 py-3 text-sm text-error">
            {error}
          </div>
        )}

        {response && (
        <div className="mt-8 rounded-2xl border border-border bg-surface p-6">
          {/* Generated SQL */}
          <div className="text-sm font-medium text-foreground-secondary">
            Generated SQL
          </div>

          <pre className="mt-4 overflow-x-auto rounded-xl border border-border bg-background p-5 font-mono text-sm leading-6">
            {response.sql}
          </pre>

          {/* Metadata */}
          <div className="mt-5 flex flex-wrap gap-4 text-xs text-foreground-muted">
            <span>
              Rows: {response.results.length}
            </span>

            <span>
              Tokens: {response.total_tokens}
            </span>

            <span>
              Repair:{" "}
              {response.repair_attempted
                ? response.repair_successful
                  ? "Successful"
                  : "Attempted"
                : "Not needed"}
            </span>
          </div>

          {/* Query Results */}
          {response.results.length > 0 && (
            <div className="mt-8 border-t border-border pt-6">
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <h2 className="text-sm font-medium text-foreground-secondary">
                    Query Results
                  </h2>

                  <p className="mt-1 text-xs text-foreground-muted">
                    {response.results.length} rows returned
                  </p>
                </div>
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
                          )
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
                                className="whitespace-nowrap px-5 py-3 text-foreground"
                              >
                                {formatCellValue(row[column])}
                              </td>
                            )
                          )}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Empty result */}
          {response.results.length === 0 && (
            <div className="mt-8 border-t border-border pt-6">
              <div className="rounded-xl border border-border bg-background px-5 py-8 text-center">
                <p className="text-sm text-foreground-secondary">
                  Query executed successfully but returned no rows.
                </p>
              </div>
            </div>
          )}
        </div>
      )}
      </section>
    </main>
  );
}

