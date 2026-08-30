"""Speaker notes as a continuous monologue — read aloud verbatim."""
from __future__ import annotations

import re

from decks.projection import NOTES_IDX

_META = re.compile(
    r"^(Session timing|Instructor timing|Instructor cues|\[Instructor meta\])",
    re.I | re.M,
)

_OPENING = {
    "theory": "In this slide we cover {title}.{book}",
    "demo": "In this demonstration, {title}.{book}",
    "content": "On this slide, {title}.{book}",
    "hands_on": "Now we move to the hands-on part: {title}. Open your lab VM and follow along.{book}",
    "warn": "Before we continue, an important note about {title}.{book}",
}

_TRANSITIONS = (
    "First, ",
    "Next, ",
    "By contrast, ",
    "We should also consider that ",
    "Another key point is that ",
    "Furthermore, ",
    "In addition, ",
    "Finally, ",
    "Also, ",
    "Then, ",
)

_CLOSING = {
    "theory": "I'll pause here for questions, then we'll continue.",
    "demo": "Check that your screen matches what we showed before moving on.",
    "content": "If these objectives are clear, we can proceed.",
    "hands_on": "Raise your hand if you're stuck — we'll wait until most of you are done.",
    "warn": "Keep this difference in mind for the rest of the lab.",
}


def _join(parts: list[str]) -> str:
    return "\n\n".join(p.strip() for p in parts if p and p.strip())


def _split_label_body(bullet: str) -> tuple[str, str]:
    if ":" in bullet and bullet.index(":") < 48:
        label, body = bullet.split(":", 1)
        return label.strip(), body.strip()
    return "", bullet.strip()


def _spoken_flow(text: str) -> str:
    """Turn slide notation into spoken phrasing."""
    s = text.strip()
    s = re.sub(r"\s*→\s*", ", then ", s)
    s = re.sub(r"\s*->\s*", ", then ", s)
    s = re.sub(r"\s*—\s*", " — ", s)
    s = re.sub(r"\s+", " ", s)
    if s and s[-1] not in ".!?":
        s += "."
    return s


def _lc_first(s: str) -> str:
    """Lowercase first letter unless it starts an acronym (ETL, IoT, …)."""
    if not s:
        return s
    word = s.split(None, 1)[0]
    if word.isupper() or (len(word) > 1 and word[0].isupper() and word[1].isupper()):
        return s
    return s[0].lower() + s[1:]


def _bullet_to_sentence(bullet: str, index: int) -> str:
    raw = bullet.strip()
    if raw.startswith("$ "):
        cmd = raw[2:].strip()
        return (
            f"Please run the following command on your VM: {cmd}. "
            "Wait until you see a sensible result before continuing."
        )
    if re.match(r"^\d+\.\s", raw):
        step = re.sub(r"^\d+\.\s*", "", raw)
        return _spoken_flow(step)

    label, body = _split_label_body(raw)
    trans = _TRANSITIONS[min(index, len(_TRANSITIONS) - 1)]
    body = _spoken_flow(body)

    if label:
        label_l = label.lower()
        if body:
            body_s = _spoken_flow(body)
            rest = _lc_first(body_s)
            if label_l == "centralized":
                return f"{trans}in the centralized approach, {rest}"
            if label_l == "federated":
                return f"{trans}in the federated approach, {rest}"
            if "bottleneck" in label_l and "centralized" in label_l:
                return f"{trans}a major bottleneck of centralized training is {rest}"
            if "bottleneck" in label_l and "federated" in label_l:
                return f"{trans}federated learning also has bottlenecks: {rest}"
            if "value proposition" in label_l or label_l == "s4t value proposition":
                return f"{trans}for Stack4Things, the value proposition is that {rest}"
            if label_l in {"lab demo", "demo"}:
                return f"{trans}our lab demonstration uses {rest}"
            return f"{trans}regarding {label_l}, {rest}"
    sent = _spoken_flow(raw)
    return f"{trans}{sent[0].upper()}{sent[1:]}" if sent else trans.rstrip()


def _book_clause(book_ref: str) -> str:
    if not book_ref.strip():
        return ""
    return f" This material is covered in {book_ref.strip()}."


def _prose_bullets(item: tuple, *, kind: str) -> str:
    title = item[1]
    bullets = item[2] if len(item) > 2 and isinstance(item[2], list) else []
    book_ref = ""
    if kind == "theory" and len(item) > 3 and isinstance(item[3], str):
        book_ref = item[3]

    book = _book_clause(book_ref)
    opening_tpl = _OPENING.get(kind, "This slide presents {title}.{book}")
    paragraphs: list[str] = [opening_tpl.format(title=title, book=book)]

    if bullets:
        sentences = [_bullet_to_sentence(b, i) for i, b in enumerate(bullets)]
        # Group into paragraphs of ~2 sentences for readability
        chunk: list[str] = []
        for i, sent in enumerate(sentences):
            chunk.append(sent)
            if len(chunk) >= 2 or i == len(sentences) - 1:
                paragraphs.append(" ".join(chunk))
                chunk = []

    paragraphs.append(_CLOSING.get(kind, "Let's move to the next slide."))
    return _join(paragraphs)


def _script_title(item: tuple) -> str:
    title = item[1]
    subtitle = str(item[2]).strip() if len(item) > 2 else ""
    footer = str(item[3]).strip() if len(item) > 3 else ""
    parts = [
        f"Welcome. In this module we will work through {title}.",
    ]
    if subtitle:
        parts.append(subtitle.replace("\n", " "))
    parts.append(
        "The session alternates theory from the book with live exercises on the Stack4Things lab VM. "
        "Replace the placeholder IP with the address of the machine you are using."
    )
    if footer:
        parts.append(footer + ".")
    parts.append("When you're ready, advance to the first section.")
    return _join(parts)


def _script_section(item: tuple) -> str:
    title = item[1]
    subtitle = str(item[2]).strip() if len(item) > 2 else ""
    text = f"We now begin a new section: {title}."
    if subtitle:
        text += f" {subtitle}."
    text += (
        " In the next slides, listen for whether we are in theory mode or hands-on mode, "
        "and open your terminal when the slides turn to lab work."
    )
    return text


def _script_code(item: tuple) -> str:
    title = item[1]
    code = item[2] if len(item) > 2 else ""
    parts = [
        f"On this slide we walk through the code for {title}.",
        "Scroll slowly through the listing on screen while I explain each part.",
    ]
    if "class Worker" in code or "Plugin.Plugin" in code:
        parts.append(
            "This is the standard Stack4Things plugin skeleton. The Worker class extends the "
            "Plugin base type. The run method is what IoTronic invokes when you call the plugin "
            "from Horizon. Parameters arrive as a dictionary from the Plugin Call JSON. "
            "Results go back through the queue, and oslo_log records what happened on the board."
        )
    elif "operation" in code and "container" in code:
        parts.append(
            "This JSON is what you paste into the Plugin Call panel. Each field is part of the "
            "contract between Horizon and the Docker lifecycle plugin: the operation to perform, "
            "the image to run, the container name, and the command to execute inside the container."
        )
    else:
        parts.append(
            "Point out the imports, the class definition, and the run method. "
            "Students will adapt this template in the lab rather than writing from scratch."
        )
    parts.append("After reviewing the code, we'll apply it in the practical exercise.")
    return _join(parts)


def _script_image(item: tuple) -> str:
    title = item[1]
    image_rel = str(item[2]) if len(item) > 2 else ""
    caption = str(item[3]).strip() if len(item) > 3 else ""
    if "seq-" in image_rel:
        kind = "sequence diagram"
        guide = (
            "Trace the diagram from left to right. Name each actor, the protocol used, "
            "and the message that crosses the cloud–edge boundary."
        )
    elif image_rel.startswith("chapter"):
        kind = "screenshot"
        guide = (
            "Walk the class through what they see in the interface. "
            "Connect each panel and button to a component we already deployed in the stack."
        )
    else:
        kind = "diagram"
        guide = (
            "Describe the main boxes and arrows. "
            "Relate each element to a Docker service or API you have already seen."
        )
    text = f"Please look at the {kind} on screen: {title}. {guide}"
    if caption:
        text += f" In particular, note the following: {caption}."
    text += " Take a few seconds to orient before we continue."
    return text


def _polish_prose(text: str) -> str:
    fixes = (
        (r"\bioTronic\b", "IoTronic"),
        (r"in the centralized approach, ETL pipeline", "in the centralized approach, an ETL pipeline"),
        (r", then single GPU cluster", ", then a single GPU cluster"),
        (r", then server aggregates", ", then the server aggregates"),
        (r", then global model improves", ", then the global model improves"),
        (r"federated learning also has bottlenecks:", "federated learning has bottlenecks:"),
        (r"trains monolithic model", "trains a monolithic model"),
        (r"operational layer for FL\.", "the operational layer for federated learning."),
    )
    for pat, repl in fixes:
        text = re.sub(pat, repl, text)
    return text


def build_script(item: tuple) -> str:
    kind = item[0]
    if kind == "title":
        body = _script_title(item)
    elif kind == "section":
        body = _script_section(item)
    elif kind in {"theory", "demo", "content", "hands_on", "warn"}:
        body = _prose_bullets(item, kind=kind)
    elif kind == "code":
        body = _script_code(item)
    elif kind == "image":
        body = _script_image(item)
    else:
        body = f"This slide covers {item[1] if len(item) > 1 else 'the next topic'}. Let's continue."
    return _polish_prose(body)


def enrich_item(item: tuple) -> tuple:
    kind = item[0]
    notes_idx = 4 if kind == "title" else NOTES_IDX.get(kind, 3)
    existing = item[notes_idx] if len(item) > notes_idx else ""
    timing_blocks: list[str] = []
    if existing:
        for block in re.split(r"\n{2,}", existing.strip()):
            b = block.strip()
            if b.startswith("Session timing") or b.startswith("Instructor timing") or b.startswith("Instructor cues"):
                timing_blocks.append(b)
    body = build_script(item)
    merged = _join([body, _join(timing_blocks)]) if timing_blocks else body
    row = list(item)
    while len(row) <= notes_idx:
        row.append("")
    row[notes_idx] = merged
    return tuple(row)


def enrich_deck(items: list) -> list:
    return [enrich_item(item) for item in items]
