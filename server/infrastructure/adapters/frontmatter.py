from typing import Any

import frontmatter


def decode(content: str) -> tuple[str, dict[str, Any]]:
    post = frontmatter.loads(content)
    return post.content, dict(post)
