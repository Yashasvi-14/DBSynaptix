"use client";

import Link from "next/link";
import Image from "next/image";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export default function ConnectPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    host: "localhost",
    port: "5432",
    database: "",
    username: "",
    password: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [indexing, setIndexing] = useState(false);

  function updateField(field: keyof typeof form, value: string) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setSuccess(false);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/database/connect`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            host: form.host,
            port: Number(form.port),
            database: form.database,
            username: form.username,
            password: form.password,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok || data.success === false) {
        throw new Error(
          data.detail || data.message || "Failed to connect to database.",
        );
      }

      setSuccess(true);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to connect to database.",
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleIndexDatabase() {
    setIndexing(true);
    setError("");

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/database/index`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            host: form.host,
            port: Number(form.port),
            database: form.database,
            username: form.username,
            password: form.password,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok || data.success === false) {
        throw new Error(
          data.detail || data.message || "Failed to index database.",
        );
      }

      const schemaResponse = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/database/schema`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            host: form.host,
            port: Number(form.port),
            database: form.database,
            username: form.username,
            password: form.password,
          }),
        },
      );

      const schemaData = await schemaResponse.json();

      if (!schemaResponse.ok || schemaData.success === false) {
        throw new Error(
          schemaData.detail ||
            schemaData.message ||
            "Failed to retrieve database schema.",
        );
      }

      sessionStorage.setItem(
        "dbsynaptix_schema",
        JSON.stringify(schemaData.data),
      );

      sessionStorage.setItem(
        "dbsynaptix_connection",
        JSON.stringify({
          host: form.host,
          port: Number(form.port),
          database: form.database,
          username: form.username,
          password: form.password,
        }),
      );

      router.push("/workspace");
    } catch (error) {
      setError(
        error instanceof Error ? error.message : "Failed to index database.",
      );
    } finally {
      setIndexing(false);
    }
  }

  const inputClass =
    "mt-2 w-full rounded-xl border border-border bg-background px-4 py-3 text-sm text-foreground outline-none transition focus:border-primary";

  return (
    <main className="min-h-screen bg-background">
      <nav className="border-b border-border">
        <div className="mx-auto flex h-18 max-w-[1600px] items-center px-8">
          <Link href="/" className="flex items-center gap-3">
            <Image
              src="/dbsynaptix-icon.png"
              alt=""
              width={98}
              height={98}
              priority
              className="h-24 w-24 object-contain"
            />

            <span className="text-lg font-semibold tracking-tight">
              DBSynaptix
            </span>
          </Link>
        </div>
      </nav>

      <section className="mx-auto grid min-h-[calc(100vh-72px)] max-w-[1200px] items-center gap-16 px-8 py-16 lg:grid-cols-2">
        <div>
          <div className="mb-5 text-sm font-medium text-primary">
            DATABASE CONNECTION
          </div>

          <h1 className="text-5xl font-semibold tracking-[-0.04em]">
            Connect your database.
          </h1>

          <p className="mt-6 max-w-lg text-lg leading-8 text-foreground-secondary">
            Connect PostgreSQL to build a semantic representation of your schema
            and start querying your data with natural language.
          </p>

          <div className="mt-10 space-y-5 text-sm text-foreground-secondary">
            <Feature number="01" text="Extract database metadata" />
            <Feature number="02" text="Generate semantic knowledge" />
            <Feature number="03" text="Build retrieval embeddings" />
            <Feature number="04" text="Query with natural language" />
          </div>
        </div>

        <div className="rounded-2xl border border-border bg-surface p-8">
          <div>
            <h2 className="text-xl font-semibold">PostgreSQL</h2>

            <p className="mt-2 text-sm text-foreground-secondary">
              Enter the connection details for your database.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="mt-8 space-y-5">
            <div className="grid gap-5 sm:grid-cols-[1fr_140px]">
              <label className="text-sm text-foreground-secondary">
                Host
                <input
                  value={form.host}
                  onChange={(event) => updateField("host", event.target.value)}
                  className={inputClass}
                  placeholder="localhost"
                  required
                />
              </label>

              <label className="text-sm text-foreground-secondary">
                Port
                <input
                  type="number"
                  value={form.port}
                  onChange={(event) => updateField("port", event.target.value)}
                  className={inputClass}
                  placeholder="5432"
                  required
                />
              </label>
            </div>

            <label className="block text-sm text-foreground-secondary">
              Database
              <input
                value={form.database}
                onChange={(event) =>
                  updateField("database", event.target.value)
                }
                className={inputClass}
                placeholder="northwind"
                required
              />
            </label>

            <label className="block text-sm text-foreground-secondary">
              Username
              <input
                value={form.username}
                onChange={(event) =>
                  updateField("username", event.target.value)
                }
                className={inputClass}
                placeholder="postgres"
                required
              />
            </label>

            <label className="block text-sm text-foreground-secondary">
              Password
              <input
                type="password"
                value={form.password}
                onChange={(event) =>
                  updateField("password", event.target.value)
                }
                className={inputClass}
                placeholder="••••••••"
                required
              />
            </label>

            <button
              type="submit"
              disabled={loading}
              className="mt-2 w-full rounded-xl bg-primary px-5 py-3 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Connecting..." : "Connect Database"}
            </button>
            {error && (
              <div className="rounded-xl border border-error/30 bg-error/10 px-4 py-3 text-sm text-error">
                {error}
              </div>
            )}

            {success && (
              <div className="space-y-3">
                <div className="rounded-xl border border-success/30 bg-success/10 px-4 py-3 text-sm text-success">
                  Database connected successfully.
                </div>

                <button
                  type="button"
                  onClick={handleIndexDatabase}
                  disabled={indexing}
                  className="w-full rounded-xl border border-primary/40 bg-primary/10 px-5 py-3 text-sm font-medium text-primary transition hover:bg-primary/15 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {indexing ? "Building semantic index..." : "Index Database"}
                </button>
              </div>
            )}
          </form>

          <p className="mt-5 text-center text-xs text-foreground-muted">
            Credentials are used only to connect to your database.
          </p>
        </div>
      </section>
    </main>
  );
}

function Feature({ number, text }: { number: string; text: string }) {
  return (
    <div className="flex items-center gap-4">
      <span className="font-mono text-xs text-foreground-muted">{number}</span>

      <span>{text}</span>
    </div>
  );
}
