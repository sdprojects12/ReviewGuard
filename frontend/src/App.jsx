import ModerationPage from "./pages/ModerationPage";

export default function App() {
  return (
    <div className="min-h-screen px-4 py-10 md:py-16">
      <div className="max-w-4xl mx-auto">
        <header className="mb-10 md:mb-14">
          <h1 className="font-display text-3xl md:text-4xl tracking-wide">
            ReviewGuard
          </h1>
          <p className="font-mono text-xs uppercase tracking-widest text-ink-soft mt-2">
            Moderation, not censorship
          </p>
          <div className="mt-6 h-px bg-line" />
        </header>

        <ModerationPage />
      </div>
    </div>
  );
}