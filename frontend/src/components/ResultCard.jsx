import { useState } from "react";
import DecisionStamp from "./DecisionStamp";

/**
 * ResultCard — the right-hand manuscript sheet showing the moderation
 * outcome. Renders one of three states: idle (nothing submitted yet),
 * error, or a completed result with Decision / Reason / Suggested Review.
 *
 * @param {{ status: "idle" | "error" | "result", errorMessage?: string,
 *   result?: { decision: string, reason: string, suggested_review: string } }} props
 */
export default function ResultCard({ status, errorMessage, result }) {
  return (
    <div className="bg-paper-card border border-line rounded-sm shadow-[4px_4px_0_0_var(--color-line)] p-6 md:p-8 min-h-[320px] flex flex-col">
      <p className="font-mono text-xs uppercase tracking-widest text-ink-soft mb-3">
        Editor's desk
      </p>

      {status === "idle" && <IdleState />}
      {status === "error" && <ErrorState message={errorMessage} />}
      {status === "result" && result && <CompletedResult result={result} />}
    </div>
  );
}

function IdleState() {
  return (
    <div className="flex-1 flex items-center justify-center text-center">
      <p className="font-body text-ink-soft max-w-xs">
        Send a review over and the decision will land here, stamped and
        explained.
      </p>
    </div>
  );
}

function ErrorState({ message }) {
  return (
    <div className="flex-1 flex items-center justify-center text-center">
      <div>
        <p className="font-mono text-xs uppercase tracking-widest text-reject mb-2">
          Couldn't complete review
        </p>
        <p className="font-body text-ink-soft max-w-xs">{message}</p>
      </div>
    </div>
  );
}

function CompletedResult({ result }) {
  const { decision, reason, suggested_review: suggestedReview } = result;
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(suggestedReview);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // Clipboard access can fail (permissions/unsupported browser);
      // silently ignore since copying is a convenience, not core to the flow.
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <DecisionStamp decision={decision} />

      <div>
        <p className="font-mono text-xs uppercase tracking-widest text-ink-soft mb-1">
          Reason
        </p>
        <p className="font-body text-ink leading-relaxed">{reason}</p>
      </div>

      <div>
        <div className="flex items-center justify-between mb-1">
          <p className="font-mono text-xs uppercase tracking-widest text-ink-soft">
            {decision === "approve"
              ? "Review text (unchanged)"
              : "Suggested review"}
          </p>
          <button
            type="button"
            onClick={handleCopy}
            className="font-mono text-xs uppercase tracking-widest text-accent hover:text-ink cursor-pointer"
          >
            {copied ? "Copied" : "Copy"}
          </button>
        </div>
        <p className="font-body text-ink leading-relaxed border-l-2 border-line pl-3">
          {suggestedReview}
        </p>
      </div>
    </div>
  );
}