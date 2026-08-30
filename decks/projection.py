"""Sanitize deck tuples for classroom projection (no instructor timing on slides)."""
from __future__ import annotations

import re

# Slides omitted from projection — timing lives in speaker notes / INSTRUCTOR_PLAYBOOK only.
_SKIP_TITLE_PATTERNS = (
    re.compile(r"\d+-minute timeline", re.I),
    re.compile(r"instructor checklist", re.I),
)

_TIME_IN_TITLE = re.compile(r"\s*\(\d+\s*min(?:utes?)?\)", re.I)
_NOW_IN_TITLE = re.compile(r"\s*\(?\s*do this NOW[^)]*\)?", re.I)
_AT_MINUTE = re.compile(r"\s*\(?\s*at minute \d+[^)]*\)?", re.I)
_STEP_NUM = re.compile(r"^Step \d+ —\s*", re.I)
_HANDS_ON_SECTION = re.compile(r"^Hands-on\s*—\s*", re.I)
_HANDS_ON_WORD = re.compile(r"^Hands-on\s+", re.I)
_INSTRUCTOR_PHRASES = re.compile(
    r"(instructor|speaker notes|presenter|do this now|bookmark while|while stack boots|"
    r"before hands-on|minute \d+|DEMO GOAL review|projects for class)",
    re.I,
)
_TIMING_BULLET = re.compile(r"^\d+–\d+\s*min\s*—|^\d+–\d+\s*min\s+|^\d+\s*min\s*—", re.I)


def _clean_title(title: str) -> str:
    t = _TIME_IN_TITLE.sub("", title)
    t = _NOW_IN_TITLE.sub("", t)
    t = _AT_MINUTE.sub("", t)
    t = _STEP_NUM.sub("", t)
    t = _HANDS_ON_SECTION.sub("Lab: ", t)
    t = _HANDS_ON_WORD.sub("Lab: ", t)
    t = re.sub(r"\s*—?\s*learning outcomes before hands-on", " — learning outcomes", t, flags=re.I)
    t = re.sub(r"\s+before hands-on", "", t, flags=re.I)
    t = re.sub(r"\s*—\s*$", "", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip()


def _clean_subtitle(subtitle: str) -> str:
    if not subtitle:
        return subtitle
    if _INSTRUCTOR_PHRASES.search(subtitle):
        return ""
    return subtitle


def _clean_bullet(line: str) -> str | None:
    raw = line.strip()
    if not raw:
        return None
    if _TIMING_BULLET.match(raw):
        return None
    if _INSTRUCTOR_PHRASES.search(raw) and not raw.startswith("$"):
        return None
    raw = re.sub(r"\s*\(\d+\s*min(?:utes?)?\)", "", raw, flags=re.I)
    raw = re.sub(r"\bat minute \d+[^.]*\.?", "", raw, flags=re.I).strip()
    raw = re.sub(r"\s{2,}", " ", raw)
    return raw if raw else None


def _should_skip(title: str) -> bool:
    return any(p.search(title) for p in _SKIP_TITLE_PATTERNS)


def sanitize_item(item: tuple) -> tuple | None:
    kind = item[0]
    if kind == "title":
        return item

    title = item[1]
    if _should_skip(title):
        return None

    row = list(item)
    row[1] = _clean_title(title)

    if kind == "section" and len(row) > 2:
        row[2] = _clean_subtitle(str(row[2]))

    bullet_kinds = {"theory", "demo", "content", "hands_on", "warn"}
    if kind in bullet_kinds and len(row) > 2 and isinstance(row[2], list):
        cleaned = []
        for line in row[2]:
            cl = _clean_bullet(line)
            if cl is not None:
                cleaned.append(cl)
        if not cleaned and kind in ("content", "hands_on"):
            return None
        row[2] = cleaned

    if kind == "image" and len(row) > 3:
        row[3] = _clean_title(str(row[3])) if row[3] else row[3]

    return tuple(row)


def sanitize_deck(items: list) -> list:
    out = []
    for item in items:
        sanitized = sanitize_item(item)
        if sanitized is not None:
            out.append(sanitized)
    return out
