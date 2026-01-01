"""
Prompt construction & context engineering.

This module explicitly answers:
- how past memory is used
- how brand context is injected
- how repetition is avoided
"""


def build_comment_prompt(
    post_content: str,
    brand_context: str,
    past_comment_patterns: list[str],
) -> str:
    """
    past_comment_patterns:
    - summaries of previously APPROVED comments
    - used strictly as NEGATIVE CONSTRAINTS
      (what phrasing / structure to avoid, not what topics to avoid)
    """

    avoided_patterns = "\n".join(
        f"- {p}" for p in past_comment_patterns
    ) if past_comment_patterns else "- None"

    return (
        "You are an internal AI system generating professional, brand-aligned comments.\n\n"

        "====================\n"
        "BRAND CONTEXT (MANDATORY)\n"
        "====================\n"
        f"{brand_context}\n\n"

        "====================\n"
        "POST CONTENT\n"
        "====================\n"
        f"{post_content}\n\n"

        "====================\n"
        "PAST COMMENT MEMORY (NEGATIVE CONSTRAINTS)\n"
        "====================\n"
        "The following patterns come from previously APPROVED comments.\n"
        "They are provided ONLY to avoid repetition in phrasing, structure, or angle.\n"
        "Do NOT avoid topics solely because they appear below.\n\n"
        f"{avoided_patterns}\n\n"

        "====================\n"
        "INSTRUCTIONS (STRICT)\n"
        "====================\n"
        "- Generate exactly THREE distinct comments.\n"
        "- Each comment must add genuine insight OR ask a thoughtful, relevant question.\n"
        "- Do NOT repeat phrasing, structure, or ideas across the three comments.\n"
        "- Maximum 2 sentences per comment.\n"
        "- Keep each comment concise and professional.\n"
        "- No emojis. No hashtags. No marketing slogans.\n"
        "- Do NOT introduce facts, statistics, or claims not present in the post.\n"
        "- Do NOT mention the brand explicitly unless it is clearly natural.\n\n"

        "====================\n"
        "OUTPUT FORMAT (NO DEVIATION)\n"
        "====================\n"
        "COMMENT 1:\n"
        "<text>\n\n"
        "COMMENT 2:\n"
        "<text>\n\n"
        "COMMENT 3:\n"
        "<text>\n"
    )
