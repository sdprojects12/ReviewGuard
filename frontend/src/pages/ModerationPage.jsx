import { useState } from "react";
import ReviewForm from "../components/ReviewForm";
import ResultCard from "../components/ResultCard";
import { moderateReview } from "../services/moderationApi";

/**
 * ModerationPage — the single-screen workflow: write a review, send it
 * for moderation, see the stamped decision.
 */
export default function ModerationPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState("idle"); // "idle" | "error" | "result"
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleSubmit(reviewText) {
    setIsSubmitting(true);
    setStatus("idle");

    try {
      const data = await moderateReview(reviewText);
      setResult(data);
      setStatus("result");
    } catch (error) {
      setErrorMessage(error.message);
      setStatus("error");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="grid md:grid-cols-2 gap-6 md:gap-8 items-start">
      <ReviewForm onSubmit={handleSubmit} isSubmitting={isSubmitting} />
      <ResultCard status={status} errorMessage={errorMessage} result={result} />
    </div>
  );
}