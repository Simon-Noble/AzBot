"""
This class is for running a singly white elephant game


"""
import random

from WhiteElephant.infrastructure.Leader import Leader

class TooManyLeadersException(Exception):
    pass
class DuplicateLeaderException(Exception):
    pass
class DraftStartedException(Exception):
    pass
class SelectedLeaderMismatchException(Exception):
    pass
class OutOfOrderException(Exception):
    pass
class TooManyStealsException(Exception):
    pass
class NoLeaderException(Exception):
    pass

class Game:
    users: list[str]
    game_id:str

    nominated_leaders: list[Leader]
    user_nominated_leaders: dict[str, list[Leader]]

    turn_order: list[str]

    unselected_leaders: list[Leader]

    current_assignment: dict[str, list[Leader|None]]
    stolen_leaders: dict[str, int]
    stolen_picks: dict[str, list[int]]


    draft_stared: bool

    def __init__(self, users: list[str], game_id: str):
        self.users = users
        self.game_id = game_id

        self.nominated_leaders = []
        self.user_nominated_leaders = {user:[] for user in users}
        self.turn_order = []
        self.unselected_leaders = []
        self.draft_stared = False



        self.stolen_leaders = {}
        self.stolen_picks = {}
        self.current_assignment = {}



    def nominate_leader(self, user: str, leader: Leader) -> None:
        """

        :param user:
        :param game_name:
        :param leader:
        :return:
        """
        if self.draft_stared:
            raise DraftStartedException("")

        if len(self.user_nominated_leaders[user]) >= 2:
            raise TooManyLeadersException("")
        for chosen_leader in self.nominated_leaders:
            if leader.id == chosen_leader.id:
                raise DuplicateLeaderException("")



        self.user_nominated_leaders[user].append(leader)
        self.nominated_leaders.append(leader)

    def begin_draft(self):
        if self.draft_stared:
            raise DraftStartedException("")
        for user in self.users:
            if len(self.user_nominated_leaders[user]) != 2:
                raise SelectedLeaderMismatchException(f"{user} selected "
                                                      f"{len(self.user_nominated_leaders[user])} leaders")

        order = list(self.users.copy())
        random.shuffle(order)
        order2 = order.copy()
        order2.reverse()
        order.extend(order2)

        self.turn_order = order

        self.stolen_leaders = {leader.id: 0 for leader in self.nominated_leaders}
        self.stolen_picks = {user: [0, 0] for user in self.users}
        self.current_assignment = {user: [None, None] for user in self.users}

        self.unselected_leaders = self.nominated_leaders.copy()
        random.shuffle(self.unselected_leaders)


        self.draft_stared = True



    def draw_from_deck(self, user: str) -> Leader:
        if not self.draft_stared:
            raise DraftStartedException("Draft not Started")
        if user != self.turn_order[0]:
            raise OutOfOrderException(f"It is currently {self.turn_order[0]}'s turn")

        leader = self.unselected_leaders.pop(0)
        if self.current_assignment[user][0] is None:
            self.current_assignment[user][0] = leader
        elif self.current_assignment[user][1] is None:
            self.current_assignment[user][1] = leader
        else:
            raise TooManyLeadersException()

        self.turn_order.pop(0)
        return leader


    def steal_leader(self, user: str, victim: str, pick_number: int) -> Leader:

        # ensure pick is valid and being done by a valid user
        if not self.draft_stared:
            raise DraftStartedException("Draft not started")
        if user != self.turn_order[0]:
            raise OutOfOrderException(f"It is currently {self.turn_order[0]}'s turn")

        leader = self.current_assignment[victim][pick_number]
        if leader is None:
            raise NoLeaderException()

        if self.stolen_leaders[leader.id] >= 2:
            raise TooManyStealsException(f"{leader.id} has already been stolen 2 times!")
        if self.stolen_picks[leader.id][pick_number] >= 2:
            raise TooManyStealsException(f"{victim} has already had their pick {pick_number+1} stolen twice!")

        # set current players leader to the stolen leader and update theft on leader
        if self.current_assignment[user][0] is None:
            self.current_assignment[user][0] = leader
        elif self.current_assignment[user][1] is None:
            self.current_assignment[user][1] = leader
        else:
            raise TooManyLeadersException()
        self.stolen_leaders[leader.id] += 1

        # update victim and turn order

        self.current_assignment[victim][pick_number] = None
        self.stolen_picks[victim][pick_number] += 1

        self.turn_order[0] = victim


        return leader


