import Link from "next/link";
import Image from "next/image";

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="border-b border-border">
        <div className="mx-auto flex h-18 max-w-[1600px] items-center justify-between px-8">
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

          <div className="flex items-center gap-7 text-sm">
            <a
              href="#architecture"
              className="text-foreground-secondary transition hover:text-foreground"
            >
              Architecture
            </a>

            <Link
              href="/benchmarks"
              className="text-foreground-secondary transition hover:text-foreground"
            >
              Benchmarks
            </Link>

            <Link
              href="/connect"
              className="rounded-lg border border-border bg-surface px-4 py-2 font-medium transition hover:bg-zinc-800"
            >
              Connect database
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="mx-auto grid min-h-[calc(100vh-72px)] max-w-[1600px] items-center gap-16 px-8 py-20 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="max-w-2xl">
          <div className="mb-6 flex items-center gap-3">
            <div className="inline-flex rounded-full border border-border bg-surface px-4 py-2 text-sm text-foreground-secondary">
              AI-powered PostgreSQL intelligence
            </div>

            <span className="text-sm font-medium text-foreground-secondary">
              Giving Data a Brain.
            </span>
          </div>

          <h1 className="text-5xl font-semibold tracking-[-0.05em] sm:text-6xl lg:text-7xl">
            Ask your database.
            <span className="block text-foreground-secondary">
              Get executable SQL.
            </span>
          </h1>

          <p className="mt-7 max-w-xl text-lg leading-8 text-foreground-secondary">
            DBSynaptix understands your schema, retrieves the relevant database
            context, generates validated SQL, and executes it against
            PostgreSQL.
          </p>

          <div className="mt-10 flex flex-wrap gap-3">
            <Link
              href="/connect"
              className="rounded-xl bg-primary px-5 py-3 text-sm font-medium text-white transition-opacity hover:opacity-90"
            >
              Connect Database
            </Link>

            <a
              href="#architecture"
              className="rounded-xl border border-border bg-surface px-5 py-3 text-sm font-medium transition hover:bg-zinc-800"
            >
              Explore Architecture
            </a>
          </div>

          <div className="mt-10 flex flex-wrap gap-x-7 gap-y-3 text-sm text-foreground-muted">
            <span>PostgreSQL</span>
            <span>Hybrid retrieval</span>
            <span>FK-aware context</span>
            <span>SQL repair</span>
          </div>
        </div>

        {/* Product demo */}
        <div className="overflow-hidden rounded-2xl border border-border bg-surface-muted shadow-2xl">
          <div className="flex items-center justify-between border-b border-border px-5 py-4">
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-error" />
              <span className="h-2.5 w-2.5 rounded-full bg-warning" />
              <span className="h-2.5 w-2.5 rounded-full bg-success" />
            </div>

            <span className="text-xs text-foreground-muted">northwind</span>
          </div>

          <div className="p-6">
            <p className="text-xs font-medium uppercase tracking-[0.18em] text-primary">
              Natural language
            </p>

            <p className="mt-3 text-lg">
              Show the top 5 customers by total revenue
            </p>

            <div className="my-6 border-t border-border" />

            <div className="flex flex-wrap gap-2">
              {["customers", "orders", "order_details"].map((table) => (
                <span
                  key={table}
                  className="rounded-lg border border-primary/30 bg-primary/10 px-3 py-1.5 font-mono text-xs text-violet-300"
                >
                  {table}
                </span>
              ))}
            </div>

            <div className="mt-6 overflow-x-auto rounded-xl border border-border bg-background p-5">
              <pre className="text-sm leading-7 text-foreground-secondary">
                <code>{`SELECT
  c.company_name,
  SUM(
    od.unit_price * od.quantity
    * (1 - od.discount)
  ) AS total_revenue
FROM customers c
JOIN orders o
  ON c.customer_id = o.customer_id
JOIN order_details od
  ON o.order_id = od.order_id
GROUP BY c.customer_id, c.company_name
ORDER BY total_revenue DESC
LIMIT 5;`}</code>
              </pre>
            </div>

            <div className="mt-5 grid grid-cols-3 gap-3">
              <div className="rounded-xl border border-border p-3">
                <p className="text-xs text-foreground-muted">Context</p>
                <p className="mt-1 text-sm font-medium">Focused schema</p>
              </div>

              <div className="rounded-xl border border-border p-3">
                <p className="text-xs text-foreground-muted">Validation</p>
                <p className="mt-1 text-sm font-medium text-success">Passed</p>
              </div>

              <div className="rounded-xl border border-border p-3">
                <p className="text-xs text-foreground-muted">Output</p>
                <p className="mt-1 text-sm font-medium">SQL + rows</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Architecture */}
      <section id="architecture" className="border-t border-border">
        <div className="mx-auto max-w-[1600px] px-8 py-28">
          <div className="max-w-3xl">
            <p className="text-sm font-medium uppercase tracking-[0.18em] text-primary">
              Architecture
            </p>

            <h2 className="mt-4 text-4xl font-semibold tracking-tight sm:text-5xl">
              Schema intelligence before SQL generation.
            </h2>

            <p className="mt-6 text-lg leading-8 text-foreground-secondary">
              DBSynaptix does not send an entire database schema to an LLM. It
              builds a persistent semantic index, retrieves relevant schema,
              expands database relationships, and generates SQL from focused
              context.
            </p>
          </div>

          {/* Indexing pipeline */}
          <div className="mt-16">
            <div className="flex items-center gap-4">
              <span className="font-mono text-xs text-primary">01</span>

              <h3 className="text-xl font-semibold">Database indexing</h3>

              <span className="text-sm text-foreground-muted">
                built once per database
              </span>
            </div>

            <div className="mt-6 grid gap-3 lg:grid-cols-5">
              {[
                {
                  title: "Schema Introspection",
                  description: "Tables, columns, primary keys and foreign keys",
                },
                {
                  title: "Knowledge Generation",
                  description:
                    "Semantic summaries, business terms and column meaning",
                },
                {
                  title: "Retrieval Documents",
                  description:
                    "Structured schema combined with generated knowledge",
                },
                {
                  title: "Embeddings",
                  description:
                    "Vector representations generated for schema documents",
                },
                {
                  title: "Persistent Index",
                  description:
                    "Reusable semantic index stored for future queries",
                },
              ].map((item, index) => (
                <div
                  key={item.title}
                  className="relative rounded-2xl border border-border bg-surface-muted p-5"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs text-primary">
                      {String(index + 1).padStart(2, "0")}
                    </span>

                    {index < 4 && (
                      <span className="hidden text-foreground-muted lg:block">
                        →
                      </span>
                    )}
                  </div>

                  <h4 className="mt-8 font-medium">{item.title}</h4>

                  <p className="mt-2 text-sm leading-6 text-foreground-muted">
                    {item.description}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Query pipeline */}
          <div className="mt-20">
            <div className="flex items-center gap-4">
              <span className="font-mono text-xs text-primary">02</span>

              <h3 className="text-xl font-semibold">Query pipeline</h3>

              <span className="text-sm text-foreground-muted">
                runs for every question
              </span>
            </div>

            <div className="mt-6 overflow-hidden rounded-2xl border border-border bg-surface-muted">
              {/* Input */}
              <div className="border-b border-border p-6">
                <p className="text-xs font-medium uppercase tracking-[0.16em] text-foreground-muted">
                  Input
                </p>

                <p className="mt-3 text-lg">
                  “Show the top 5 customers by total revenue”
                </p>
              </div>

              {/* Retrieval */}
              <div className="grid border-b border-border lg:grid-cols-[1fr_auto_1.2fr_auto_1fr] lg:items-stretch">
                <div className="p-6">
                  <span className="font-mono text-xs text-primary">01</span>

                  <h4 className="mt-5 font-medium">Query preprocessing</h4>

                  <p className="mt-2 text-sm leading-6 text-foreground-muted">
                    Extracts terms used for lexical schema matching.
                  </p>
                </div>

                <div className="hidden items-center text-foreground-muted lg:flex">
                  →
                </div>

                <div className="border-y border-border p-6 lg:border-x lg:border-y-0">
                  <span className="font-mono text-xs text-primary">02</span>

                  <h4 className="mt-5 font-medium">Hybrid retrieval</h4>

                  <p className="mt-2 text-sm leading-6 text-foreground-muted">
                    Combines deterministic schema matches with semantic
                    similarity.
                  </p>

                  <div className="mt-5 grid grid-cols-2 gap-2">
                    <div className="rounded-lg border border-border bg-background p-3">
                      <p className="text-xs text-foreground-muted">Keyword</p>
                      <p className="mt-1 font-mono text-sm">40%</p>
                    </div>

                    <div className="rounded-lg border border-border bg-background p-3">
                      <p className="text-xs text-foreground-muted">Semantic</p>
                      <p className="mt-1 font-mono text-sm">60%</p>
                    </div>
                  </div>
                </div>

                <div className="hidden items-center text-foreground-muted lg:flex">
                  →
                </div>

                <div className="p-6">
                  <span className="font-mono text-xs text-primary">03</span>

                  <h4 className="mt-5 font-medium">Relationship expansion</h4>

                  <p className="mt-2 text-sm leading-6 text-foreground-muted">
                    Expands retrieved tables through foreign-key relationships
                    required for joins.
                  </p>
                </div>
              </div>

              {/* Context */}
              <div className="border-b border-border px-6 py-5">
                <div className="flex flex-wrap items-center gap-3">
                  <span className="text-xs uppercase tracking-[0.15em] text-foreground-muted">
                    Focused context
                  </span>

                  {["customers", "orders", "order_details"].map((table) => (
                    <span
                      key={table}
                      className="rounded-lg border border-primary/30 bg-primary/10 px-3 py-1.5 font-mono text-xs text-violet-300"
                    >
                      {table}
                    </span>
                  ))}

                  <span className="ml-auto text-sm text-foreground-muted">
                    instead of all 14 tables
                  </span>
                </div>
              </div>

              {/* Generation */}
              <div className="grid border-b border-border md:grid-cols-3">
                {[
                  {
                    number: "04",
                    title: "Prompt construction",
                    description:
                      "Question + focused structured schema become the generation context.",
                  },
                  {
                    number: "05",
                    title: "SQL generation",
                    description:
                      "Gemini generates PostgreSQL using only the supplied schema context.",
                  },
                  {
                    number: "06",
                    title: "SQL validation",
                    description:
                      "Generated output is normalized and validated before execution.",
                  },
                ].map((item) => (
                  <div
                    key={item.title}
                    className="border-b border-border p-6 last:border-b-0 md:border-b-0 md:border-r md:last:border-r-0"
                  >
                    <span className="font-mono text-xs text-primary">
                      {item.number}
                    </span>

                    <h4 className="mt-5 font-medium">{item.title}</h4>

                    <p className="mt-2 text-sm leading-6 text-foreground-muted">
                      {item.description}
                    </p>
                  </div>
                ))}
              </div>

              {/* Execution + repair */}
              <div className="grid lg:grid-cols-[1fr_1.3fr]">
                <div className="border-b border-border p-6 lg:border-b-0 lg:border-r">
                  <span className="font-mono text-xs text-primary">07</span>

                  <h4 className="mt-5 font-medium">PostgreSQL execution</h4>

                  <p className="mt-2 text-sm leading-6 text-foreground-muted">
                    Validated SQL executes against the connected database and
                    returns structured rows.
                  </p>

                  <div className="mt-5 inline-flex items-center gap-2 text-sm text-success">
                    <span className="h-2 w-2 rounded-full bg-success" />
                    Success → Results
                  </div>
                </div>

                <div className="p-6">
                  <div className="flex items-start gap-5">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-warning/30 bg-warning/10 font-mono text-sm text-warning">
                      ↻
                    </div>

                    <div>
                      <p className="text-xs font-medium uppercase tracking-[0.15em] text-warning">
                        Recovery path
                      </p>

                      <h4 className="mt-2 font-medium">
                        Execution error → SQL repair → one retry
                      </h4>

                      <p className="mt-2 text-sm leading-6 text-foreground-muted">
                        If PostgreSQL rejects the generated SQL, DBSynaptix
                        sends the database error, failed query, original
                        question, and schema context back through the repair
                        pipeline before one controlled retry.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Observability */}
          <div className="mt-6 grid gap-3 sm:grid-cols-3">
            <div className="rounded-xl border border-border bg-surface-muted p-5">
              <p className="text-xs text-foreground-muted">Retrieval</p>
              <p className="mt-2 font-medium">Hybrid schema ranking</p>
            </div>

            <div className="rounded-xl border border-border bg-surface-muted p-5">
              <p className="text-xs text-foreground-muted">Observability</p>
              <p className="mt-2 font-medium">Stage latency + token usage</p>
            </div>

            <div className="rounded-xl border border-border bg-surface-muted p-5">
              <p className="text-xs text-foreground-muted">Reliability</p>
              <p className="mt-2 font-medium">Validation + repair retry</p>
            </div>
          </div>
        </div>
      </section>

      {/* Benchmark teaser */}
      <section className="border-t border-border">
        <div className="mx-auto max-w-[1600px] px-8 py-24">
          <div className="grid gap-12 lg:grid-cols-[0.8fr_1.2fr] lg:items-end">
            <div>
              <p className="text-sm font-medium uppercase tracking-[0.18em] text-primary">
                Evaluation
              </p>

              <h2 className="mt-4 text-4xl font-semibold tracking-tight">
                Measured on retrieval, not vibes.
              </h2>

              <p className="mt-5 max-w-xl leading-7 text-foreground-secondary">
                A 20-query Northwind benchmark measures whether DBSynaptix
                retrieves and supplies the schema required to answer questions
                across single-table, aggregation, multi-table, and relationship
                queries.
              </p>

              <Link
                href="/benchmarks"
                className="mt-7 inline-block text-sm font-medium text-primary hover:underline"
              >
                Explore benchmark →
              </Link>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              <div className="rounded-2xl border border-border bg-surface-muted p-6">
                <p className="text-3xl font-semibold">85.92%</p>
                <p className="mt-2 text-sm text-foreground-secondary">
                  Retrieval Recall@3
                </p>
              </div>

              <div className="rounded-2xl border border-border bg-surface-muted p-6">
                <p className="text-3xl font-semibold">97.33%</p>
                <p className="mt-2 text-sm text-foreground-secondary">
                  Context Recall
                </p>
              </div>

              <div className="rounded-2xl border border-border bg-surface-muted p-6">
                <p className="text-3xl font-semibold">46.43%</p>
                <p className="mt-2 text-sm text-foreground-secondary">
                  Schema Context Used
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
      {/* Reliability */}
      <section className="border-t border-border">
        <div className="mx-auto max-w-[1600px] px-8 py-24">
          <div className="max-w-3xl">
            <p className="text-sm font-medium uppercase tracking-[0.18em] text-primary">
              Engineering
            </p>

            <h2 className="mt-4 text-4xl font-semibold tracking-tight">
              Built for reliable Text-to-SQL.
            </h2>

            <p className="mt-5 max-w-2xl text-lg leading-8 text-foreground-secondary">
              Retrieval, relationship reasoning, controlled execution, and
              observability work together across the complete query pipeline.
            </p>
          </div>

          <div className="mt-12 grid gap-px overflow-hidden rounded-2xl border border-border bg-border md:grid-cols-2">
            <div className="bg-surface-muted p-7">
              <span className="font-mono text-xs text-primary">01</span>

              <h3 className="mt-5 text-lg font-medium">
                Semantic schema understanding
              </h3>

              <p className="mt-3 max-w-xl leading-7 text-foreground-secondary">
                Generated schema knowledge and embeddings capture meaning beyond
                literal table and column names, improving retrieval for natural
                language questions.
              </p>
            </div>

            <div className="bg-surface-muted p-7">
              <span className="font-mono text-xs text-primary">02</span>

              <h3 className="mt-5 text-lg font-medium">
                Relationship-aware reasoning
              </h3>

              <p className="mt-3 max-w-xl leading-7 text-foreground-secondary">
                Foreign-key expansion connects retrieved tables with related
                schema required for joins and multi-table SQL generation.
              </p>
            </div>

            <div className="bg-surface-muted p-7">
              <span className="font-mono text-xs text-primary">03</span>

              <h3 className="mt-5 text-lg font-medium">Controlled execution</h3>

              <p className="mt-3 max-w-xl leading-7 text-foreground-secondary">
                Generated SQL is validated before execution. Database errors can
                trigger a repair pass followed by one controlled retry.
              </p>
            </div>

            <div className="bg-surface-muted p-7">
              <span className="font-mono text-xs text-primary">04</span>

              <h3 className="mt-5 text-lg font-medium">
                Observable AI pipeline
              </h3>

              <p className="mt-3 max-w-xl leading-7 text-foreground-secondary">
                Retrieval, context construction, generation, execution latency,
                token usage, and repair behavior are surfaced as pipeline
                metadata.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="border-t border-border">
        <div className="mx-auto max-w-[1600px] px-8 py-28">
          <div className="rounded-3xl border border-border bg-surface-muted px-8 py-16 text-center sm:px-16">
            <p className="text-sm font-medium text-primary">
              Giving Data a Brain.
            </p>

            <h2 className="mx-auto mt-5 max-w-3xl text-4xl font-semibold tracking-tight sm:text-5xl">
              Turn your PostgreSQL schema into something you can ask.
            </h2>

            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-foreground-secondary">
              Connect a database, let DBSynaptix build its semantic index, and
              query your data using natural language.
            </p>

            <div className="mt-9 flex flex-wrap justify-center gap-3">
              <Link
                href="/connect"
                className="rounded-xl bg-primary px-6 py-3 text-sm font-medium text-white transition-opacity hover:opacity-90"
              >
                Connect Database
              </Link>

              <Link
                href="/benchmarks"
                className="rounded-xl border border-border bg-surface px-6 py-3 text-sm font-medium transition hover:bg-zinc-800"
              >
                View Benchmarks
              </Link>
            </div>
          </div>

          <footer className="mt-16 flex flex-col gap-4 border-t border-border pt-8 text-sm text-foreground-muted sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div>
                <span className="font-medium text-foreground">DBSynaptix</span>
                <span className="ml-3">Giving Data a Brain.</span>
              </div>

              <div className="mt-2 flex items-center gap-3">
                <span>Built by Yashasvi Tekriwal</span>

                <span className="text-border">•</span>

                <a
                  href="https://github.com/Yashasvi-14"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="transition hover:text-foreground"
                >
                  GitHub
                </a>
                <span className="text-border">•</span>

                <a
                  href="https://www.linkedin.com/in/yashasvi-tekriwal/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="transition hover:text-foreground"
                >
                  LinkedIn
                </a>
              </div>
            </div>

            <div className="flex gap-6">
              <a
                href="#architecture"
                className="transition hover:text-foreground"
              >
                Architecture
              </a>

              <Link
                href="/benchmarks"
                className="transition hover:text-foreground"
              >
                Benchmarks
              </Link>

              <Link
                href="/connect"
                className="transition hover:text-foreground"
              >
                Connect
              </Link>
            </div>
          </footer>
        </div>
      </section>
    </main>
  );
}
