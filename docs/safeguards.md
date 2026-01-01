# Auto-Posting Risks & Safeguards

## What Can Go Wrong

1. LLM produces unsafe or off-brand content
2. Duplicate posting due to retries
3. Posting succeeds but confirmation is lost
4. External APIs fail or timeout
5. Human reviewers make conflicting actions
6. System posts during an incident

---

## Preventive Safeguards

### Content Safety
- Brand context injected into every prompt
- Hard validators block unsafe output
- Human approval is mandatory

### Posting Safety
- Idempotency keys prevent duplicates
- Confirmation required before marking POSTED
- Retries are bounded

### Workflow Safety
- Strict state machine
- Row-level locks on review actions
- No edits allowed after approval

### Operational Safety
- Global kill switch
- Per-day posting limits (configurable)
- Manual override mechanisms

---

## Failure Handling

- All failures transition to FAILED state
- Failures are logged and surfaced
- No silent loss of actions

---

## Kill Switch

The system includes a global kill switch that:
- immediately disables auto-posting
- does not affect review or generation
- can be toggled without redeploy

---

## Design Philosophy

The system is designed assuming:
- failures are inevitable
- automation is dangerous without control
- trust is harder to regain than to lose
