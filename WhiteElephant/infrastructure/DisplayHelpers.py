from WhiteElephant.infrastructure.GenericStateOutputData import GenericStateOutputData
from WhiteElephant.infrastructure.LeaderManager import LeaderManager


def generate_pre_draft_display_message(output: GenericStateOutputData, leader_manager: LeaderManager) -> str:
    message = f"Current Leader Selections:"
    for user in output.users:

        leader_ids = output.user_nominated_leaders[user]
        message += f"\n"
        for leader_id in leader_ids:
            icons = " ".join(filter(None, [leader_manager.BY_ID[leader_id].leader_emoji,
                                           leader_manager.BY_ID[leader_id].civ_emoji]))
            message += f"{icons} **{leader_manager.BY_ID[leader_id].name}** ({leader_manager.BY_ID[leader_id].civ})  "
        message += f"- nominated by {user}"
    message += f"\nDraft can start once each user has nominated 2 leaders"
    return message



def generate_draft_display_message(output: GenericStateOutputData, leader_manager: LeaderManager) -> str:
    message = f"Current Leader Assignments:"
    for user in output.users:

        leader_ids = output.current_assignments[user]
        message += f"\n{user}: "

        for i in range(2):
            leader_id = leader_ids[i]
            if leader_id is not None:
                icons = " ".join(filter(None, [leader_manager.BY_ID[leader_id].leader_emoji,
                                               leader_manager.BY_ID[leader_id].civ_emoji]))
                message += f"{icons} "
                message += f"X" * output.stolen_leaders[leader_id]
            else:
                message += "..."
            if i == 0:
                message += f" | "

        message += f" They have been stolen from {output.stolen_picks[user]} times"
        if  output.stolen_picks[user] == 2:
            message += f" and can no longer be stolen from."


    message += (
                f"\nThe remaining leaders are:")
    for leader_id in output.unselected_leaders:
        icons = " ".join(filter(None, [leader_manager.BY_ID[leader_id].leader_emoji]))
        message += f"{icons} "

    if len(output.turn_order)> 0:
        message += f"\nIt is {output.turn_order[0]}'s turn"
    else:
        message += f"\nThe draft has finished!"
    return message