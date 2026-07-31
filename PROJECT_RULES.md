# Project Goal

Build an AI-powered review moderation system that helps users write constructive reviews.

The AI should moderate reviews, not censor opinions.

The focus is on wording, intent, and safety, not grammar.

# Core Principles

- Never judge grammar.
- Never change the user's opinion.
- Preserve the original meaning when suggesting edits.
- Criticism is allowed.
- Personal attacks are discouraged.
- Transparency is more important than strictness.
- Every decision should include an explanation.

# Approval Rules

Approve if:
- Genuine customer experience
- Respectful criticism
- Specific feedback

Needs Adjustment if:
- Personal insults
- Excessive profanity
- Overly emotional wording

Reject if:
- Hate speech
- Threats
- Spam
- Defamatory accusations presented as facts


Never consider

- Grammar
- Spelling mistakes
- Capitalization
- Emojis
- Slang
- Regional English

# AI Response Format:

{
    "decision":"",
    "reason":"",
    "suggested_review":""
}

# UI Rules

Green = Approve

Yellow = Needs Adjustment

Red = Reject

Never display raw JSON.

Always show:

Decision

Reason

Suggested Review

# Coding Standards

- Keep functions under 50 lines where practical.
- One responsibility per function.
- Add docstrings to public functions.
- Use meaningful variable names.
- Avoid duplicate code.
- Keep backend modular.

# Folder Rules
- Frontend

components/

pages/

services/

- Backend

routes/

services/

utils/

models/

# API Rules

- All API responses should follow
{
    "success": true,
    "data": {}
}
- Errors
{
    "success": false,
    "message":"..."
}

# Prompt Rules

Never ask Gemini to output markdown.
Always request JSON.
Never allow Gemini to invent new fields.
Keep prompts concise.
Avoid chain-of-thought requests.

# Future
- Accounts
- Analytics
- History
- Business Dashboard
- Multiple Languages
- CSV Upload
- API

# Before every release

Test

Positive review
Negative review
Mixed review
Profanity
Hate speech
Spam
Threats
Empty review
Long review

# A feature is complete when:

- It works.
- It has been tested.
- Errors are handled.
- UI looks clean.
- Code is commented where necessary.
- Changes are committed to Git.

# AI Ethics & Limitations

This AI assists with review moderation.
It may occasionally make incorrect judgments.
Its recommendations are suggestions, not absolute decisions.
Users should always have the final say before submitting a review.