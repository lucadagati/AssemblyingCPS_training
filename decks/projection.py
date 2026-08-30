"""Sanitize deck tuples for classroom projection (no instructor timing on slides)."""
from __future__ import annotations

import re

# Slides omitted from projection — content moves to speaker notes only.
_SKIP_TITLE_PATTERNS = (
    re.compile(r"\d+-minute timeline", re.I),
    re.compile(r"^timeline$", re.I),
    re.compile(r"instructor checklist", re.I),
    re.compile(r"^modular timing model$", re.I),
    re.compile(r"^training paths — pick one$", re.I),
)

NOTES_IDX = {
    "section": 3,
    "theory": 4,
    "demo": 3,
    "content": 3,
    "hands_on": 3,
    "warn": 3,
    "code": 3,
    "image": 4,
}

_TIME_IN_TITLE = re.compile(r"\s*\(\d+\s*min(?:utes?)?\)", re.I)
_MODULE_TIER = re.compile(r"\s*\((CORE|EXT|ADV)[^)]*\)", re.I)
_DURATION_FRAGMENT = re.compile(r"\+\d+–\d+\s*min(?:utes?)?(?:,\s*OPTIONAL)?", re.I)
_NOW_IN_TITLE = re.compile(r"\s*\(?\s*do this NOW[^)]*\)?", re.I)
_AT_MINUTE = re.compile(r"\s*\(?\s*at minute \d+[^)]*\)?", re.I)
_STEP_NUM = re.compile(r"^Step \d+ —\s*", re.I)
_HANDS_ON_SECTION = re.compile(r"^Hands-on\s*—\s*", re.I)
_HANDS_ON_WORD = re.compile(r"^Hands-on\s+", re.I)
_INSTRUCTOR_PHRASES = re.compile(
    r"(instructor|speaker notes|presenter|do this now|bookmark while|while stack boots|"
    r"before hands-on|minute \d+|DEMO GOAL review|projects for class|classroom pacing)",
    re.I,
)
_TIMING_BULLET = re.compile(
    r"^\d+–\d+\s*min\s*—|^\d+–\d+\s*min\s+|^\d+\s*min\s*—|^\d+h\s+(CORE|STANDARD|FULL)\s*→",
    re.I,
)
_PATH_TIMING_BULLET = re.compile(r"^\d+h\s+", re.I)


def _join_notes(parts: list[str]) -> str:
    return "\n\n".join(p.strip() for p in parts if p and p.strip())


def _bullets_to_notes(bullets: list[str]) -> str:
    return "\n".join(f"• {line}" for line in bullets if line.strip())


def _explicit_notes(item: tuple) -> str:
    idx = NOTES_IDX.get(item[0], 3)
    if len(item) > idx and isinstance(item[idx], str):
        return item[idx]
    return ""


def _should_skip(title: str) -> bool:
    t = title.strip()
    return any(p.search(t) for p in _SKIP_TITLE_PATTERNS)


def _clean_title(title: str) -> str:
    t = _MODULE_TIER.sub("", title)
    t = _DURATION_FRAGMENT.sub("", t)
    t = _TIME_IN_TITLE.sub("", t)
    t = _NOW_IN_TITLE.sub("", t)
    t = _AT_MINUTE.sub("", t)
    t = _STEP_NUM.sub("", t)
    t = _HANDS_ON_SECTION.sub("Lab: ", t)
    t = _HANDS_ON_WORD.sub("Lab: ", t)
    t = re.sub(r"\s*—?\s*learning outcomes before hands-on", " — learning outcomes", t, flags=re.I)
    t = re.sub(r"\s+\(\s*OPTIONAL\s*\)", " (optional)", t, flags=re.I)
    t = re.sub(r"\s+before hands-on", "", t, flags=re.I)
    t = re.sub(r"\s*—\s*$", "", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" ·—")


def _clean_subtitle(subtitle: str) -> str:
    if not subtitle:
        return subtitle
    if _INSTRUCTOR_PHRASES.search(subtitle):
        return ""
    lines = []
    for line in subtitle.split("\n"):
        ln = line
        ln = re.sub(r"3h core → 6h standard → 9h full\s*·?\s*", "", ln, flags=re.I)
        ln = re.sub(r"·\s*\d+\s*min\b", "", ln, flags=re.I)
        ln = _DURATION_FRAGMENT.sub("", ln)
        ln = re.sub(r"\bExtension\s*·\s*·", "Extension · ", ln)
        ln = re.sub(r"\s{2,}", " ", ln).strip(" ·")
        if ln:
            lines.append(ln)
    return "\n".join(lines)


def _clean_bullet(line: str) -> str | None:
    raw = line.strip()
    if not raw:
        return None
    if _TIMING_BULLET.match(raw) or _PATH_TIMING_BULLET.match(raw):
        return None
    if _INSTRUCTOR_PHRASES.search(raw) and not raw.startswith("$"):
        return None
    raw = _DURATION_FRAGMENT.sub("", raw)
    raw = re.sub(r"\s*\(\d+\s*min(?:utes?)?\)", "", raw, flags=re.I)
    raw = re.sub(r"\bat minute \d+[^.]*\.?", "", raw, flags=re.I).strip()
    raw = re.sub(r"\s{2,}", " ", raw).strip(" ·—")
    return raw if raw else None


def _partition_bullets(bullets: list[str]) -> tuple[list[str], list[str]]:
    kept: list[str] = []
    removed: list[str] = []
    for line in bullets:
        cl = _clean_bullet(line)
        if cl is not None:
            kept.append(cl)
        else:
            removed.append(line.strip())
    return kept, removed


def sanitize_item(item: tuple) -> tuple | None:
    prepared, _ = _prepare_item(item, deferred_notes=[])
    return prepared


def _prepare_item(item: tuple, deferred_notes: list[str]) -> tuple[tuple | None, list[str]]:
    kind = item[0]
    title = item[1] if len(item) > 1 else ""

    if kind == "title":
        row = list(item)
        if len(row) > 2:
            row[2] = _clean_subtitle(str(row[2]))
        return tuple(row), deferred_notes

    if _should_skip(title):
        removed: list[str] = []
        if len(item) > 2 and isinstance(item[2], list):
            removed = [str(x) for x in item[2]]
        note = _join_notes([f"Session timing — {title}:", _bullets_to_notes(removed)])
        if note:
            deferred_notes = deferred_notes + [note]
        return None, deferred_notes

    row = list(item)
    cleaned_title = _clean_title(title)
    row[1] = cleaned_title
    removed_bullets: list[str] = []
    notes_parts = list(deferred_notes)
    deferred_notes = []

    if cleaned_title != title.strip():
        notes_parts.append(f"Instructor timing (title): {title.strip()}")

    if kind == "section" and len(row) > 2:
        row[2] = _clean_subtitle(str(row[2]))

    bullet_kinds = {"theory", "demo", "content", "hands_on", "warn"}
    if kind in bullet_kinds and len(row) > 2 and isinstance(row[2], list):
        kept, removed_bullets = _partition_bullets(row[2])
        if not kept and kind in ("content", "hands_on"):
            note = _join_notes([f"{title}:", _bullets_to_notes(removed_bullets)])
            if note:
                deferred_notes = deferred_notes + [note]
            return None, deferred_notes
        row[2] = kept

    if kind == "image" and len(row) > 3:
        row[3] = _clean_title(str(row[3])) if row[3] else row[3]

    explicit = _explicit_notes(item)
    if explicit:
        notes_parts.append(explicit)
    if removed_bullets:
        notes_parts.append("Instructor cues:\n" + _bullets_to_notes(removed_bullets))
    merged_notes = _join_notes(notes_parts)

    if merged_notes:
        idx = NOTES_IDX.get(kind, 3)
        while len(row) <= idx:
            row.append("")
        if row[idx]:
            merged_notes = _join_notes([merged_notes, str(row[idx])])
        row[idx] = merged_notes

    return tuple(row), deferred_notes


def prepare_deck(items: list) -> list:
    """Sanitize slides for projection and attach instructor-only text to speaker notes."""
    out: list = []
    deferred: list[str] = []
    for item in items:
        prepared, deferred = _prepare_item(item, deferred)
        if prepared is not None:
            out.append(prepared)
    return out


def sanitize_deck(items: list) -> list:
    return prepare_deck(items)
