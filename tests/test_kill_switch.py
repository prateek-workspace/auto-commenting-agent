import pytest

from app.core.config import settings
from app.core.exceptions import KillSwitchEnabled
from app.posting.service import post_approved_comment


def test_kill_switch_blocks_posting():
    settings.AUTO_POSTING_ENABLED = False

    with pytest.raises(KillSwitchEnabled):
        post_approved_comment(comment_id=1, db=None)

    settings.AUTO_POSTING_ENABLED = True
