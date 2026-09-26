import json
from pathlib import Path

import unicodedata

from WhiteElephant.infrastructure.Leader import Leader


def _norm(s: str) -> str:
    """Lowercase and strip accents so 'Bà Triệu' matches 'ba trieu'."""
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()




class LeaderManager:
    _leaders: list[Leader]


    def __init__(self):
        """
        >>> manager = LeaderManager()
        >>> len(manager.get_all_leaders())
        78
        """
        _DATA_PATH = Path(__file__).parent / "leaders.json"
        data = json.loads(_DATA_PATH.read_text(encoding="utf-8"))
        emojis = data["emojis"]
        def markup(key):
            e = emojis.get(key)
            return f"<:{e['name']}:{e['id']}>" if e else ""
        self._leaders = [
            Leader(e["id"], e["name"], e["civs"][0], markup(e["leader_icon"]),
                   [m for k in e["civ_icons"] if (m := markup(k))][0])
            for e in data["leaders"]
        ]
        self.BY_ID = {l.id: l for l in self._leaders}
        self.BY_NAME = {_norm(l.name): l for l in self._leaders}

    def find(self, query: str) -> Leader | None:
        q = _norm(query)
        return self.BY_NAME.get(q) or self.BY_ID.get(q.replace(" ", "_"))

    def search(self, query: str, limit: int) -> list[Leader]:
        q = _norm(query)

        hits = [l for l in self._leaders if q in _norm(l.name) or any(q in _norm(c) for c in l.civ)]
        return hits[:limit]

    def get_all_leaders(self):
        return self._leaders