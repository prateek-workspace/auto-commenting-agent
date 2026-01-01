This is an internal AI system for **industry-targeted professional engagement** that safely generates, reviews, and auto-posts brand-aligned comments on social media posts.

This system is intentionally designed as **controlled automation**, not blind AI posting.

---

## Why it Exists

Manual engagement does not scale.  
Blind automation destroys trust.

Prossima balances:
- relevance
- quality
- speed
- safety

by combining **AI generation + human approval + defensive automation**.

---

## Core Guarantees

- No posting without human approval  
- No silent failures  
- No duplicate posting  
- No off-brand or unsafe content  
- Full audit trail of decisions  

---

## High-Level Flow

```

Post Submitted
↓
Target Validation
↓
AI Generates 3 Comments
↓
Brand Validation
↓
Human Review
↓
Approved
↓
Auto-Posted (Idempotent)
↓
Feedback Stored

```

---

## Architecture Overview

Each folder under `app/` is treated as an **internal service / agent**:

```

app/
├── core/        # config, DB, locks, state machine
├── posts/       # targeting & post ingestion
├── generation/  # LLM + prompt engineering
├── brand/       # brand rules & validators
├── review/      # human approval workflow
├── posting/     # auto-posting, retries, idempotency
├── feedback/    # memory & learning loop

```

Supporting folders:
```

docs/     # architecture, safeguards, scaling
scripts/  # demo & failure simulation
tests/    # safety & correctness tests

````

---

## State Machine (Critical)

Comments move through strict states:

- `generated`
- `under_review`
- `edited`
- `approved`
- `posting`
- `posted`
- `failed`

Illegal transitions are blocked at runtime.

This prevents:
- posting without approval
- editing after posting
- double posting during retries

---

## Brand & Context Engineering

Brand rules are enforced at **two layers**:

1. Injected into every LLM prompt
2. Validated after generation

Violations are **blocked before approval**.

---

## Memory & Learning (No Black Boxes)

The system **does not retrain models**.

Instead:
- Only *approved* comments are remembered
- Recent approved comments are summarized
- These summaries are injected as **negative constraints**
- This prevents repetition across 100 → 10,000 comments

This approach is:
- explainable
- deterministic
- auditable

---

## Human-in-the-Loop Enforcement

Human approval is **mandatory**.

Even if:
- the model output looks perfect
- the system has seen similar posts before

Approval is enforced at the **service layer**, not the UI.

---

## Auto-Posting Safety

Auto-posting includes:
- idempotency keys (no duplicates)
- retry limits
- confirmation checks
- explicit FAILED states
- global kill switch

The system **cannot post twice**.

---

## Environment Setup

### Requirements
- Python 3.11+
- Supabase (PostgreSQL)
- Gemini API key

## Running the System

```bash
python -m uvicorn app.main:app --reload
```

Open:

* API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## API Entry Points (V1)

* `POST /posts/submit`
* `POST /generation/generate/{post_id}`
* `POST /review/approve/{comment_id}`
* `POST /posting/post/{comment_id}`
* `POST /feedback/record/{comment_id}`

---

## Testing Philosophy

Tests focus on **risk boundaries**, not happy paths:

* state machine enforcement
* kill switch behavior
* idempotent posting
* prompt guarantees

Run:

```bash
pytest
```

---

## Design Tradeoffs

**Chosen**

* safety over speed
* determinism over intelligence
* explainability over ML complexity

**Deferred**

* auto-approval
* scraping
* opaque ML retraining

---

## Final Note

It is designed for **high-risk automation environments**.

If something goes wrong, the system should:

* fail loudly
* fail safely
* fail visibly
