/**
 * Client for the ReviewGuard moderation API.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

/**
 * Submit a review for moderation.
 *
 * @param {string} reviewText - The raw review text to moderate.
 * @returns {Promise<{decision: string, reason: string, suggested_review: string}>}
 * @throws {Error} With a user-facing message if the request or the API call fails.
 */
export async function moderateReview(reviewText) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}/api/moderate-review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ review_text: reviewText }),
    });
  } catch (networkError) {
    throw new Error(
      "Couldn't reach the moderation server. Is the backend running?"
    );
  }

  const body = await response.json().catch(() => null);

  if (!body || body.success !== true) {
    const message = body?.message || "Moderation request failed.";
    throw new Error(message);
  }

  return body.data;
}