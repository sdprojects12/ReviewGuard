import { useState } from "react";

/**
 * ReviewForm — where the user writes the review to be moderated.
 *
 * @param {{ onSubmit: (text: string) => void, isSubmitting: boolean }} props
 */
export default function ReviewForm({ onSubmit, isSubmitting }) {
  const [reviewText, setReviewText] = useState("");
  const [touched, setTouched] = useState(false);

  const isEmpty = reviewText.trim().length === 0;
  const showEmptyError = touched && isEmpty;

  function handleSubmit(event) {
    event.preventDefault();
    setTouched(true);
    if (isEmpty || isSubmitting) return;
    onSubmit(reviewText.trim());
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-paper-card border border-line rounded-sm shadow-[4px_4px_0_0_var(--color-line)] p-6 md:p-8"
    >
      <label
        htmlFor="review-text"
        className="block font-mono text-xs uppercase tracking-widest text-ink-soft mb-3"
      >
        Draft review
      </label>

      <textarea
        id="review-text"
        className="lined-paper w-full min-h-[220px] resize-y bg-transparent outline-none font-body text-base leading-[31px] text-ink placeholder:text-ink-soft/60"
        placeholder="Write the review to submit for moderation..."
        value={reviewText}
        onChange={(event) => setReviewText(event.target.value)}
        onBlur={() => setTouched(true)}
        disabled={isSubmitting}
      />

      <div className="mt-4 flex items-center justify-between gap-4">
        <p
          className="font-mono text-xs text-reject min-h-[1rem]"
          role="alert"
        >
          {showEmptyError ? "A review can't be empty." : ""}
        </p>

        <button
          type="submit"
          disabled={isSubmitting}
          className="shrink-0 bg-accent hover:bg-ink disabled:opacity-50 disabled:cursor-not-allowed text-paper font-mono text-sm uppercase tracking-widest px-6 py-3 rounded-sm transition-colors cursor-pointer"
        >
          {isSubmitting ? "Reviewing…" : "Send to review"}
        </button>
      </div>
    </form>
  );
}