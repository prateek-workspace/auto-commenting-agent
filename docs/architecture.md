# System Architecture

## Overview

This system is an internal AI-driven engagement platform designed to:
- identify relevant industry posts
- generate brand-aligned comments
- require human approval
- automatically post after approval
- prevent unsafe or uncontrolled behavior

The system is intentionally modular and defensive.

---

## High-Level Flow

1. Post is ingested and stored
2. Comment generation agent produces 3 suggestions
3. Suggestions are validated against brand rules
4. Human reviewer approves or requests edits
5. Approved comment is auto-posted
6. Feedback signals are recorded

At no point can the system post without explicit approval.

---

## Architectural Principles

- Separation of concerns
- Deterministic state transitions
- Defensive programming
- Human-in-the-loop enforcement
- Replaceable external dependencies

---

## App-Level Boundaries

Each folder under `app/` acts as an internal service:

- `posts` → targeting + ingestion
- `generation` → LLM interaction
- `brand` → policy + validation
- `review` → human control
- `posting` → execution + idempotency
- `feedback` → learning & memory
- `core` → shared infrastructure

---

## External Dependencies

- LLM: Gemini (replaceable)
- Database: Supabase (Postgres)
- Posting client: abstracted, platform-agnostic

All external systems are assumed to fail.

---

## Replaceability

Every external integration is wrapped behind a service layer.
This allows future migration to:
- different LLMs
- multiple brands
- additional platforms
