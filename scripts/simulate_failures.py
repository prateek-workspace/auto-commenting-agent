"""
Simulate failure scenarios for evaluation.

This script is used to demonstrate:
- retry behavior
- idempotency protection
- kill switch handling

Usage:
    python scripts/simulate_failures.py
"""

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.config import settings
from app.posting.service import post_approved_comment
from app.core.exceptions import KillSwitchEnabled


def run():
    db: Session = SessionLocal()

    # --------------------------------
    # Simulate kill switch activation
    # --------------------------------
    print("Simulating kill switch...")

    settings.AUTO_POSTING_ENABLED = False

    try:
        post_approved_comment(
            comment_id=1,  # assumes demo data exists
            db=db,
        )
    except KillSwitchEnabled as e:
        print(f"Kill switch triggered correctly: {e}")

    # --------------------------------
    # Reset kill switch
    # --------------------------------
    settings.AUTO_POSTING_ENABLED = True
    print("Kill switch reset.")

    db.close()


if __name__ == "__main__":
    run()
