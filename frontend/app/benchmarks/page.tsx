import Link from "next/link";
import Image from "next/image";

const difficultyMetrics = [
  {
    name: "Easy",
    description: "Single-table queries",
    retrieval: 100,
    context: 100,
    precision: 18.83,
    perfect: "5/5",
  },
  {
    name: "Medium",
    description: "Aggregation queries",
    retrieval: 100,
    context: 100,
    precision: 26.02,
    perfect: "5/5",
  },
  {
    name: "Hard",
    description: "Multi-table queries",
    retrieval: 73.33,
    context: 93.33,
    precision: 40.17,
    perfect: "4/5",
  },
  {
    name: "Complex",
    description: "Relationship queries",
    retrieval: 70.33,
    context: 96,
    precision: 61.5,
    perfect: "4/5",
  },
];

const headlineMetrics = [
  {
    value: "20",
    label: "Benchmark Queries",
    detail: "Across four difficulty levels",
  },
  {
    value: "85.92%",
    label: "Retrieval Recall@3",
    detail: "Relevant tables found in top-3",
  },
  {
    value: "97.33%",
    label: "Context Recall",
    detail: "Required tables available to generation",
  },
  {
    value: "36.63%",
    label: "Context Precision",
    detail: "Relevant tables within supplied context",
  },
];

function MetricBar({ value }: { value: number }) {
  return (
    <div className="h-1.5 w-full overflow-hidden rounded-full bg-white/10">
      <div
        className="h-full rounded-full bg-primary"
        style={{ width: `${Math.min(value, 100)}%` }}
      />
    </div>
  );
}

export default function BenchmarksPage() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <header className="border-b border-white/10">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
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

          <nav className="flex items-center gap-6 text-sm text-foreground-muted">
            <Link
              href="/workspace"
              className="transition hover:text-foreground"
            >
              Workspace
            </Link>

            <span className="text-foreground">Benchmarks</span>

            <Link
              href="/connect"
              className="rounded-lg border border-white/10 px-4 py-2 text-foreground transition hover:bg-white/5"
            >
              Connect database
            </Link>
          </nav>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-6 py-16">
        <div className="max-w-3xl">
          <p className="mb-3 text-sm font-medium uppercase tracking-[0.2em] text-primary">
            Evaluation
          </p>

          <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
            Retrieval benchmark
          </h1>

          <p className="mt-5 text-lg leading-8 text-foreground-muted">
            Measuring how effectively DBSynaptix retrieves relevant schema and
            constructs database context before SQL generation.
          </p>
        </div>

        <div className="mt-12 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {headlineMetrics.map((metric) => (
            <div
              key={metric.label}
              className="rounded-2xl border border-white/10 bg-white/[0.03] p-6"
            >
              <p className="text-3xl font-semibold tracking-tight">
                {metric.value}
              </p>

              <p className="mt-2 font-medium">{metric.label}</p>

              <p className="mt-1 text-sm text-foreground-muted">
                {metric.detail}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
            <p className="text-sm text-foreground-muted">Perfect retrieval</p>

            <div className="mt-2 flex items-end justify-between">
              <p className="text-3xl font-semibold">13 / 20</p>
              <p className="text-sm text-foreground-muted">
                65% of benchmark queries
              </p>
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
            <p className="text-sm text-foreground-muted">Perfect context</p>

            <div className="mt-2 flex items-end justify-between">
              <p className="text-3xl font-semibold">18 / 20</p>
              <p className="text-sm text-foreground-muted">
                90% of benchmark queries
              </p>
            </div>
          </div>
        </div>

        <section className="mt-16">
          <div>
            <p className="text-sm font-medium text-primary">
              Difficulty breakdown
            </p>

            <h2 className="mt-2 text-2xl font-semibold">
              Performance as schema reasoning becomes harder
            </h2>
          </div>

          <div className="mt-8 overflow-hidden rounded-2xl border border-white/10">
            <div className="hidden grid-cols-[1.4fr_1fr_1fr_1fr_0.7fr] gap-6 border-b border-white/10 bg-white/[0.03] px-6 py-4 text-xs uppercase tracking-wider text-foreground-muted md:grid">
              <span>Difficulty</span>
              <span>Retrieval recall</span>
              <span>Context recall</span>
              <span>Context precision</span>
              <span>Perfect</span>
            </div>

            {difficultyMetrics.map((metric) => (
              <div
                key={metric.name}
                className="grid gap-5 border-b border-white/10 px-6 py-6 last:border-b-0 md:grid-cols-[1.4fr_1fr_1fr_1fr_0.7fr] md:items-center md:gap-6"
              >
                <div>
                  <p className="font-medium">{metric.name}</p>
                  <p className="mt-1 text-sm text-foreground-muted">
                    {metric.description}
                  </p>
                </div>

                <div>
                  <div className="mb-2 flex justify-between text-sm">
                    <span className="md:hidden text-foreground-muted">
                      Retrieval
                    </span>
                    <span>{metric.retrieval.toFixed(2)}%</span>
                  </div>
                  <MetricBar value={metric.retrieval} />
                </div>

                <div>
                  <div className="mb-2 flex justify-between text-sm">
                    <span className="md:hidden text-foreground-muted">
                      Context
                    </span>
                    <span>{metric.context.toFixed(2)}%</span>
                  </div>
                  <MetricBar value={metric.context} />
                </div>

                <div>
                  <div className="mb-2 flex justify-between text-sm">
                    <span className="md:hidden text-foreground-muted">
                      Precision
                    </span>
                    <span>{metric.precision.toFixed(2)}%</span>
                  </div>
                  <MetricBar value={metric.precision} />
                </div>

                <p className="text-sm">
                  <span className="md:hidden text-foreground-muted">
                    Perfect context:{" "}
                  </span>
                  {metric.perfect}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-16 grid gap-6 lg:grid-cols-[1.5fr_1fr]">
          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-7">
            <p className="text-sm font-medium text-primary">Methodology</p>

            <h2 className="mt-2 text-2xl font-semibold">
              What this benchmark measures
            </h2>

            <p className="mt-4 leading-7 text-foreground-muted">
              Twenty natural-language questions are evaluated against the
              Northwind schema. Each question defines the tables required to
              answer it. DBSynaptix performs hybrid retrieval and
              relationship-aware context expansion, then the retrieved and final
              context tables are compared with those expected tables.
            </p>

            <div className="mt-7 grid gap-3 sm:grid-cols-3">
              {[
                ["14", "Database tables"],
                ["20", "Questions"],
                ["4", "Difficulty levels"],
              ].map(([value, label]) => (
                <div
                  key={label}
                  className="rounded-xl border border-white/10 p-4"
                >
                  <p className="text-xl font-semibold">{value}</p>
                  <p className="mt-1 text-sm text-foreground-muted">{label}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-7">
            <p className="text-sm font-medium text-primary">
              Schema context used
            </p>

            <p className="mt-4 text-4xl font-semibold">46.43%</p>

            <p className="mt-2 text-sm text-foreground-muted">
              Average portion of the 14-table schema supplied to SQL generation
              while maintaining 97.33% context recall.
            </p>

            <div className="mt-6">
              <MetricBar value={46.43} />
            </div>

            <p className="mt-6 leading-7 text-foreground-muted">
              The objective is not to send the entire schema to the model.
              Retrieval narrows the schema while relationship expansion recovers
              tables needed for joins.
            </p>
          </div>
        </section>

        <div className="mt-16 border-t border-white/10 pt-8 text-sm text-foreground-muted">
          Benchmark results reflect retrieval and schema-context performance.
          They do not represent end-to-end SQL accuracy.
        </div>
      </section>
    </main>
  );
}
