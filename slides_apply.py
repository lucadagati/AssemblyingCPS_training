#!/usr/bin/env python3
"""Apply hand-authored slide tuples to a Presentation."""
from __future__ import annotations

from generate_slides import (
    add_code_slide,
    add_content_slide,
    add_demo_slide,
    add_section_slide,
    add_theory_slide,
    add_title_slide,
)


def apply_deck(prs, items, add_image=None):
    """Render slide list. Optional add_image(prs, title, rel, caption, notes, hands_on)."""
    for item in items:
        kind = item[0]
        if kind == "title":
            add_title_slide(prs, item[1], item[2], item[3] if len(item) > 3 else "",
                            item[4] if len(item) > 4 else "")
        elif kind == "section":
            add_section_slide(prs, item[1], item[2] if len(item) > 2 else "",
                              item[3] if len(item) > 3 else "")
        elif kind == "theory":
            add_theory_slide(prs, item[1], item[2], item[3] if len(item) > 3 else "",
                             item[4] if len(item) > 4 else "")
        elif kind == "demo":
            add_demo_slide(prs, item[1], item[2], item[3] if len(item) > 3 else "")
        elif kind == "content":
            add_content_slide(prs, item[1], item[2], item[3] if len(item) > 3 else "")
        elif kind == "hands_on":
            add_content_slide(prs, item[1], item[2], item[3] if len(item) > 3 else "", hands_on=True)
        elif kind == "warn":
            add_content_slide(prs, item[1], item[2], item[3] if len(item) > 3 else "", warn=True)
        elif kind == "code":
            add_code_slide(prs, item[1], item[2], item[3] if len(item) > 3 else "")
        elif kind == "image":
            if add_image is None:
                add_content_slide(prs, item[1], [f"[image: {item[2]}]"], item[4] if len(item) > 4 else "")
            else:
                add_image(prs, item[1], item[2], item[3] if len(item) > 3 else "",
                          item[4] if len(item) > 4 else "", item[5] if len(item) > 5 else False)
        else:
            raise ValueError(f"Unknown slide kind: {kind}")
