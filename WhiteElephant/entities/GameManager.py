"""

Holds a list of games and deals with their creation and management
"""
from WhiteElephant.entities.Game import Game

class GameNotFoundException(Exception):
    pass

class GameManager:
    games: dict[str,Game]
    def __init__(self):
        self.games = {}

    def create_game(self, users:list[str], game_id: str):
        game = Game(users, game_id)
        self.games[game_id] = game


    def get_game(self, game_id:str) -> Game:
        if not game_id in self.games.keys():
            raise GameNotFoundException()
        return self.games[game_id]

    def delete_game(self, game_id:str):
        del self.games[game_id]

