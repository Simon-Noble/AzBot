"""
Game state store backed by an append-only JSON Lines file (one JSON object per line).

    {"game_id": "g1", "state": {...full snapshot...}}     <- written after every Game method
    {"game_id": "g1", "deleted": true}                    <- written when a game is deleted

Loading replays the file top to bottom; later lines overwrite earlier ones, so what is left is the
most recent snapshot of every live game. Every line is a complete snapshot, so a line that was
half-written when the bot crashed only costs you that one state - it is skipped on load.
"""
import json
import logging
import os
from pathlib import Path

from WhiteElephant.GameStateStore.GameStateStore import GameStateStore

log = logging.getLogger(__name__)


class JsonLinesGameStateStore(GameStateStore):
    def __init__(self, path: Path):
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.touch(exist_ok=True)
        self._end_torn_line()

    def save(self, game_id: str, state: dict) -> None:
        self._append({"game_id": game_id, "state": state})

    def delete(self, game_id: str) -> None:
        self._append({"game_id": game_id, "deleted": True})

    def load_all(self) -> dict[str, dict]:
        latest: dict[str, dict] = {}
        with self._path.open(encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    log.warning("Skipping unreadable line %d of %s", line_number, self._path)
                    continue
                if record.get("deleted"):
                    latest.pop(record["game_id"], None)
                else:
                    latest[record["game_id"]] = record["state"]
        return latest

    def _end_torn_line(self) -> None:
        """
        If the last run died mid-write, the file ends without a newline. Without this fix the next
        record would be glued onto that broken line and be lost with it - which for a delete record
        would bring a deleted game back to life.
        """
        with self._path.open("rb+") as f:
            f.seek(0, os.SEEK_END)
            if f.tell() == 0:
                return
            f.seek(-1, os.SEEK_END)
            if f.read(1) != b"\n":
                f.seek(0, os.SEEK_END)
                f.write(b"\n")

    def _append(self, record: dict) -> None:
        with self._path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")