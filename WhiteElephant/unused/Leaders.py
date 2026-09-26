
"""Civilization VI leader data, sourced from https://civilization.fandom.com/wiki/Leaders_(Civ6)

Icon fields are *keys*, not image URLs. Map them to files or Discord emoji in ICON_MAP / your own code.
  leader_icon : the leader portrait/icon
  civ_icons   : the civilization emblem(s) (two entries for Eleanor and Kublai Khan)
"""
from __future__ import annotations
import json
import unicodedata
from pathlib import Path


def _norm(s: str) -> str:
    """Lowercase and strip accents so 'Bà Triệu' matches 'ba trieu'."""
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()




with (Path(__file__).with_name("leaders.json")).open(encoding="utf-8") as _f:
    _DATA = json.load(_f)

_EMOJIS: dict[str, dict] = _DATA["emojis"]


def _markup(icon_key: str) -> str:
    emoji = _EMOJIS.get(icon_key)
    return f"<:{emoji['name']}:{emoji['id']}>" if emoji else ""


def _build(entry: dict) -> dict:
    entry = dict(entry)
    entry["leader_emoji"] = _markup(entry["leader_icon"])
    entry["civ_emojis"] = [m for key in entry["civ_icons"] if (m := _markup(key))]
    return entry


LEADERS: list[dict] = [_build(e) for e in _DATA["leaders"]]
PERSONAS: list[dict] = [_build(e) for e in _DATA["personas"]]
ALL_LEADERS: list[dict] = LEADERS + PERSONAS
BY_ID = {l["id"]: l for l in ALL_LEADERS}
BY_NAME = {_norm(l["name"]): l for l in ALL_LEADERS}


def find_leader(query: str) -> dict | None:
    """Exact (accent/case-insensitive) match on name, then id."""
    q = _norm(query)
    return BY_NAME.get(q) or BY_ID.get(q.replace(" ", "_"))


def search_leaders(query: str, limit: int = 25, include_personas: bool = False) -> list[dict]:
    """Substring search on leader name or civ; useful for autocomplete (Discord max 25)."""
    q = _norm(query)
    pool = ALL_LEADERS if include_personas else LEADERS
    hits = [l for l in pool if q in _norm(l["name"]) or any(q in _norm(c) for c in l["civs"])]
    return hits[:limit]


def leaders_for_civ(civ: str) -> list[dict]:
    c = _norm(civ)
    return [l for l in ALL_LEADERS if any(_norm(x) == c for x in l["civs"])]


# Fill this in once you have icons (emoji strings, file paths, or URLs), e.g.
# ICON_MAP = {"leader_gandhi": "<:gandhi:123456789012345678>", "civ_indian": "<:india:123...>"}
ICON_MAP: dict[str, str] = {}


def icons_for(leader: dict) -> tuple[str | None, list[str | None]]:
    """Return (leader_icon, [civ_icons]) resolved through ICON_MAP (None if unmapped)."""
    return (
        ICON_MAP.get(leader["leader_icon"]),
        [ICON_MAP.get(k) for k in leader["civ_icons"]],
    )

