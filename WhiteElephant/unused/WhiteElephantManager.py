import random

from WhiteElephant.unused.WhiteElephantOutput import WhiteElephantOutput


class WhiteElephantManager:
    outputBoundary: WhiteElephantOutput
    active_drafts: list
    def __init__(self, outputBoundary:WhiteElephantOutput) -> None:
        self.outputBoundary = outputBoundary
        self.active_drafts = []

    def _member_in_game(self, member: str):
        for game in self.active_drafts:
            if member in game["members"]:
                return True
        return False

    def create_white_elephant(self, members:list[str]) -> None:
        for member in members:
            if self._member_in_game(member):
                self.outputBoundary.prepareFail(f"User {member} is alredy in a draft. Finish all "
                                                f"drafts before beginning a new one")
                return

        game = {"members": members, "factions": {member: [] for member in members}, "started" : False,
                "order": [], "assignments": {}, "remaining_factions": []}
        self.active_drafts.append(game)
        self.outputBoundary.prepareSuccess("New draft created")


    def nominate_faction(self,user: str, faction):
        for game in self.active_drafts:
            if user in game["members"]:
                if len(game["factions"][user]) > 1:
                    self.outputBoundary.prepareFail(f"User {user} has already selected 2 factions")
                    return
                game["factions"][user].append(faction)
                self.outputBoundary.prepareSuccess(f"{faction['id']} added successfully")
                return

        self.outputBoundary.prepareFail(f"User {user} is not in a draft.")


    def begin_draft(self, user: str) -> None:
        for game in self.active_drafts:
            if user in game["members"]:
                for member in game["members"]:
                    if len(game["factions"][member]) != 2:
                        self.outputBoundary.prepareFail(f"User {user} has not selected 2 factions")
                        return
                game["started"] = True
                order = list(range(len(game["members"])))
                random.shuffle(order)
                game["order"] = order
                order = order.copy()
                random.shuffle(order)
                game["order"].extend(order)
                print(game["order"])

                self.outputBoundary.prepareSuccess(f"Draft is now started")
                return

    def get_random_faction(self):
        raise NotImplementedError

    def steal_faction(self, faction):
        raise NotImplementedError