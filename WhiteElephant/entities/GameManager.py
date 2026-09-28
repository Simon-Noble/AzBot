"""

Holds a list of games and deals with their creation and management
"""
from collections import Counter

from WhiteElephant.GameStateStore.GameStateStore import GameStateStore, NullGameStateStore
from WhiteElephant.entities.Game import Game

class GameNotFoundException(Exception):
    pass
class DuplicateGameException(Exception):
    pass
class DuplicateUserException(Exception):
    pass

class GameManager:
    games: dict[str,Game]
    store: GameStateStore
    def __init__(self, store: GameStateStore | None = None):
        self._store = store or NullGameStateStore()
        self.games = {}

        for game_id, state in self._store.load_all().items():
            game = Game.from_dict(state)
            game.on_change = self._save
            self.games[game_id] = game

    def create_game(self, users:list[str], game_id: str):

        counter = Counter(users)
        for key in counter.keys():
            if counter[key] > 1:
                raise DuplicateUserException()
        if game_id in self.games.keys():
            raise DuplicateGameException()
        game = Game(users, game_id)

        game.on_change = self._save
        self._save(game)

        self.games[game_id] = game


    def get_game(self, game_id:str) -> Game:
        if not game_id in self.games.keys():
            raise GameNotFoundException()
        return self.games[game_id]

    def delete_game(self, game_id:str):
        game = self.games[game_id]
        self._store.delete(game_id)
        del self.games[game_id]
        game.on_change = None

    def _save(self, game: Game) -> None:
        self._store.save(game.game_id, game.to_dict())
