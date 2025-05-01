# TODO:
# - config dialogue (widget) that allows selecting:
#   - action to take (delete, suspend, bury)
#   - action threshold (next card due date)
#   -? switch to choose to target the note or
#     just individual cards (a specific view of a note)
# - When a deck is exited run:
#   - handler that checks due date of cards
#     in the deck we left
#   - filter for cards that have a next due
#     date which is at least the action threshold
#     number of days from the current day
#   - remove the notes or cards filtered for.
#     which action to take depends on switch configured
#     - this should be done in the background and be "un-doable"
#       in case the user made a mistake

from anki.collection import SearchNode
from aqt import mw, gui_hooks

from enum import Enum
# enum of actions
class Action(Enum):
    Delete = 1
    Suspend = 2
    Disable = 3


class ThresholdParameter(Enum):
    DueInDays = 1
    Stability = 2


def on_state_change(new_state: str, old_state: str):
    if old_state == "review":
        # Get config params
        # TODO: allow user to specify a list of deck names
        add_on_config = mw.addonManager.getConfig(__name__)
        deck_names: str = add_on_config["deck_names"]
        action: Action = Action(add_on_config["action"])
        threshold: int = add_on_config["threshold"]
        threshold_parameter: ThresholdParameter = ThresholdParameter(add_on_config["threshold_parameter"])

        # Get only the cards with a due date past the threshold
        graduated_cards = []
        for deck_name in deck_names:
            deck_id = mw.col.decks.id_for_name(deck_name)
            term: SearchNode = None
            if threshold_parameter == ThresholdParameter.DueInDays:
                due_days = SearchNode(due_in_days=threshold)
                new_card = SearchNode(card_state=0)
                not_due_days = SearchNode(negated=due_days)
                not_new_card = SearchNode(negated=new_card)
                term = mw.col.group_searches(not_due_days, not_new_card)
            elif threshold_parameter == ThresholdParameter.Stability:
                term = f"prop:s>{threshold}"

            search_string = mw.col.build_search_string(term)
            graduated_cards.extend(mw.col.find_cards(search_string))
        print(len(graduated_cards))

        # Perform action on cards
        # TODO: give user dialog to confirm
        # TODO: allow user to view list of card fronts to select which should be deleted
        # TODO: allow support for deleting from multiple decks
        testing = True
        if not testing:
            if action == Action.Delete:
                mw.col.remove_notes_by_card(graduated_cards)
            elif action == Action.Suspend:
                mw.col.sched.suspend_cards(graduated_cards)

        ## TODO: display splash notification telling the user which action was taken

gui_hooks.state_did_change.append(on_state_change)
