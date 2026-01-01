from app.generation.prompts import build_comment_prompt


def test_prompt_contains_all_required_sections():
    prompt = build_comment_prompt(
        post_content="Test post",
        brand_context="Brand rules",
        past_comment_patterns=["Pattern A", "Pattern B"],
    )

    assert "BRAND CONTEXT" in prompt
    assert "POST CONTENT" in prompt
    assert "AVOID REPEATING THESE PAST COMMENT PATTERNS" in prompt
    assert "COMMENT 1" in prompt
    assert "COMMENT 2" in prompt
    assert "COMMENT 3" in prompt
