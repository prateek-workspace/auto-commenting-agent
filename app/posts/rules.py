"""
Rule-based targeting & filtering logic is here

This module answers:
- how targets are defined
- how false positives are reduced
- how refined ones will evolve later
"""


def is_relevant_post(
    industry: str | None,
    role: str | None,
    topics: list[str] | None,
) -> bool:
    """
    Basic V1 rule-based filter.
    """

    if industry and industry.lower() not in {
        "saas",
        "fintech",
        "ai",
        "developer tools",
    }:
        return False

    if role and role.lower() in {
        "student",
        "intern",
    }:
        return False

    if topics:
        banned_topics = {"politics", "religion"}
        if any(t.lower() in banned_topics for t in topics):
            return False

    return True
