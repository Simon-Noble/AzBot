"""
This class is for running a singly white elephant game


"""
import copy
import functools
import random
from typing import Callable


class TooManyGiftsException(Exception):
    pass
class DuplicateGiftException(Exception):
    pass
class DraftStartedException(Exception):
    pass
class SelectedGiftMismatchException(Exception):
    pass
class OutOfOrderException(Exception):
    pass
class TooManyStealsException(Exception):
    pass
class NoLeaderException(Exception):
    pass


def logs_state(method):
    """
    Decorator for Game methods that change the game.

    After the method finishes *successfully*, the new state is reported through game.on_change.
    If the method raises, nothing is reported - so a mutating method should finish all of its
    validation before it changes anything, otherwise memory and the log can disagree.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        if self.on_change is not None:
            self.on_change(self)
        return result

    return wrapper



class Game:
    users: list[str]
    game_id:str

    nominated_gifts: list[str]
    user_nominated_gifts: dict[str, list[str]]

    turn_order: list[str]

    unselected_gifts: list[str]

    current_assignment: dict[str, list[str|None]]
    gift_times_stolen: dict[str, int]
    user_times_stolen: dict[str, int]
    current_chain:list[str]


    draft_stared: bool
    on_change: Callable[["Game"], None] | None

    def __init__(self, users: list[str], game_id: str):
        self.users = users
        self.game_id = game_id

        self.nominated_gifts = []
        self.user_nominated_gifts = {user:[] for user in users}
        self.turn_order = []
        self.unselected_gifts = []
        self.draft_stared = False



        self.gift_times_stolen = {}
        self.user_times_stolen = {}
        self.current_assignment = {}
        self.current_chain = []

        self.on_change = None

    def to_dict(self) -> dict:
        """Everything needed to rebuild this game, as plain JSON-friendly data (deep-copied)."""
        return copy.deepcopy({
            "users": self.users,
            "game_id": self.game_id,
            "nominated_gifts": self.nominated_gifts,
            "user_nominated_gifts": self.user_nominated_gifts,
            "turn_order": self.turn_order,
            "unselected_gifts": self.unselected_gifts,
            "current_assignment": self.current_assignment,
            "gift_times_stolen": self.gift_times_stolen,
            "user_times_stolen": self.user_times_stolen,
            "current_chain": self.current_chain,
            "draft_stared": self.draft_stared,
        })

    @classmethod
    def from_dict(cls, data: dict) -> "Game":
        """Inverse of to_dict. The returned game has no on_change hook until someone sets one."""
        game = cls(data["users"], data["game_id"])
        game.nominated_gifts = data["nominated_gifts"]
        game.user_nominated_gifts = data["user_nominated_gifts"]
        game.turn_order = data["turn_order"]
        game.unselected_gifts = data["unselected_gifts"]
        game.current_assignment = data["current_assignment"]
        game.gift_times_stolen = data["gift_times_stolen"]
        game.user_times_stolen = data["user_times_stolen"]
        game.current_chain = data["current_chain"]
        game.draft_stared = data["draft_stared"]
        return game

    @logs_state
    def add_gift_to_pool(self, user: str, gift: str) -> None:
        """

        :param user:
        :param gift:
        :return:
        """
        if self.draft_stared:
            raise DraftStartedException("")

        if len(self.user_nominated_gifts[user]) >= 2:
            raise TooManyGiftsException("")
        for chosen_gift in self.nominated_gifts:
            if gift == chosen_gift:
                raise DuplicateGiftException("")



        self.user_nominated_gifts[user].append(gift)
        self.nominated_gifts.append(gift)

    @logs_state
    def begin_draft(self):
        if self.draft_stared:
            raise DraftStartedException("")
        for user in self.users:
            if len(self.user_nominated_gifts[user]) != 2:
                raise SelectedGiftMismatchException(f"{user} selected "
                                                      f"{len(self.user_nominated_gifts[user])} leaders")

        order = list(self.users.copy())
        random.shuffle(order)
        order2 = order.copy()
        order2.reverse()
        order.extend(order2)

        self.turn_order = order

        self.gift_times_stolen = {leader: 0 for leader in self.nominated_gifts}
        self.user_times_stolen = {user: 0 for user in self.users}
        self.current_assignment = {user: [None, None] for user in self.users}

        self.unselected_gifts = self.nominated_gifts.copy()



        self.draft_stared = True


    @logs_state
    def draw_from_pool(self, user: str) -> str:
        if not self.draft_stared:
            raise DraftStartedException("Draft not Started")
        if user != self.turn_order[0]:
            raise OutOfOrderException(f"It is currently {self.turn_order[0]}'s turn")

        index = random.randint(0,len(self.unselected_gifts)-1)

        gift = self.unselected_gifts.pop(index)
        if self.current_assignment[user][0] is None:
            self.current_assignment[user][0] = gift
        elif self.current_assignment[user][1] is None:
            self.current_assignment[user][1] = gift
        else:
            raise TooManyGiftsException()

        self.turn_order.pop(0)
        self.current_chain = []
        return gift

    @logs_state
    def steal_gift(self, thief: str, gift: str) -> str:
        """
        Precondition: gift is currently held by some other user
        :param thief:
        :param gift:
        :return:
        """

        # find victim and pick number
        victim, pick_number = self.find_victim(gift)

        # ensure pick is valid and being done by a valid user
        if not self.draft_stared:
            raise DraftStartedException("Draft not started")
        if thief != self.turn_order[0]:
            raise OutOfOrderException(f"It is currently {self.turn_order[0]}'s turn")



        if self.gift_times_stolen[gift] >= 2:
            raise TooManyStealsException(f"{gift} has already been stolen 2 times!")
        if self.user_times_stolen[thief] >= 2:
            raise TooManyStealsException(f"{victim} has already had their pick {pick_number+1} stolen twice!")
        if gift in self.current_chain:
            raise TooManyStealsException(f"{gift} has already been stolen during this chain!")

        # set current players leader to the stolen leader and update theft on leader
        if self.current_assignment[thief][0] is None:
            self.current_assignment[thief][0] = gift
        elif self.current_assignment[thief][1] is None:
            self.current_assignment[thief][1] = gift
        else:
            raise TooManyGiftsException()
        self.gift_times_stolen[gift] += 1

        # update victim and turn order

        self.current_assignment[victim][pick_number] = None
        self.user_times_stolen[victim] += 1

        self.turn_order[0] = victim

        # update the current chain
        self.current_chain.append(gift)


        return gift

    def find_victim(self, gift: str) -> tuple[str, int] | None:
        for potential_victim in self.users:
            for i in range(2):
                if self.current_assignment[potential_victim][i] == gift:
                    victim = potential_victim
                    pick_number = i
                    return victim, pick_number
        return None



