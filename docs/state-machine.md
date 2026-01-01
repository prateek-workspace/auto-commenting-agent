# Comment State Machine

## Purpose

The state machine enforces correctness, safety, and auditability.
It prevents illegal actions such as:
- posting without approval
- editing after posting
- duplicate posting

---

## States

- GENERATED
- REVIEWED
- EDITED
- APPROVED
- POSTED
- FAILED

---

## Allowed Transitions

GENERATED → REVIEWED  
REVIEWED → APPROVED  
REVIEWED → EDITED  
EDITED → REVIEWED  
APPROVED → POSTED  
APPROVED → FAILED  

All other transitions are forbidden.

---

## Enforcement

- Transitions are validated centrally
- Database row locking prevents concurrency issues
- Invalid transitions raise hard errors

---

## Why This Matters

This design ensures:
- human approval is mandatory
- retries cannot cause duplicate posts
- failures are visible and recoverable

The system cannot "silently succeed".
