from sqlalchemy.orm import Session

from app.generation.llm_client import LLMClient
from app.generation.prompts import build_comment_prompt
from app.generation.models import CommentSuggestion
from app.brand.service import get_brand_context
from app.feedback.service import get_recent_approved_comment_patterns
from app.core.enums import CommentState


def generate_comments_for_post(post_id: int, post_content: str, db: Session):
    """
    Core generation agent.

    This function demonstrates:
    - memory usage (past approved comments)
    - context engineering
    - controlled multi-output generation
    """

    brand_context = get_brand_context()

    past_patterns = get_recent_approved_comment_patterns(
        db=db,
        limit=50,
    )

    prompt = build_comment_prompt(
        post_content=post_content,
        brand_context=brand_context,
        past_comment_patterns=past_patterns,
    )

    client = LLMClient()
    raw_output = client.generate(prompt)

    comments = parse_llm_output(raw_output)

    results = []
    for text in comments:
        suggestion = CommentSuggestion(
            post_id=post_id,
            text=text,
            explanation="Generated to add unique, non-repetitive value aligned with brand voice.",
            state=CommentState.GENERATED,
        )
        db.add(suggestion)
        results.append(suggestion)

    db.commit()
    return results


def parse_llm_output(raw: str) -> list[str]:
    """
    Simple deterministic parser.
    No fancy heuristics in V1.
    """

    comments = []
    current = []

    for line in raw.splitlines():
        if line.strip().startswith("COMMENT"):
            if current:
                comments.append(" ".join(current).strip())
                current = []
        elif line.strip():
            current.append(line.strip())

    if current:
        comments.append(" ".join(current).strip())

    return comments[:3]

