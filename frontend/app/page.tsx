import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <nav className="border-b border-border">
        <div className="mx-auto flex h-18 max-w-[1600px] items-center justify-between px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary font-semibold text-white">
              D
            </div>

            <span className="text-lg font-semibold tracking-tight">
              DBSynaptix
            </span>
          </div>

          <span className="text-sm text-foreground-secondary">
            Giving Data a Brain.
          </span>
        </div>
      </nav>

      <section className="mx-auto flex min-h-[calc(100vh-72px)] max-w-[1600px] items-center px-8">
        <div className="max-w-3xl">
          <div className="mb-6 inline-flex rounded-full border border-border bg-surface px-4 py-2 text-sm text-foreground-secondary">
            AI Database Intelligence
          </div>

          <h1 className="text-6xl font-semibold tracking-[-0.05em]">
            Understand your database.
            <span className="block text-foreground-secondary">
              Ask it anything.
            </span>
          </h1>

          <p className="mt-7 max-w-2xl text-lg leading-8 text-foreground-secondary">
            Connect PostgreSQL and turn natural language into context-aware,
            validated SQL using semantic retrieval and AI reasoning.
          </p>

          <div className="mt-10 flex gap-3">
            <Link
              href="/connect"
              className="rounded-xl bg-primary px-5 py-3 text-sm font-medium text-white transition-opacity hover:opacity-90"
            >
              Connect Database
            </Link>

            <button className="rounded-xl border border-border bg-surface px-5 py-3 text-sm font-medium text-foreground transition-colors hover:bg-zinc-800">
              Explore Architecture
            </button>
          </div>
        </div>
      </section>
    </main>
  );
}
