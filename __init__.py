# TODO:
# - config dialogue (widget) that allows selecting:
#   - action to take (delete, suspend, bury)
#   - action threshold (next card due date)
#   -? switch to choose to target the note or
#     just individual cards (a specific view of a note)
# - When a deck is exited run:
#   ...
#   - remove the notes or cards filtered for.
#     which action to take depends on switch configured
#     - this should be done in the background and be "un-doable"
#       in case the user made a mistake
from __future__ import annotations

from enum import Enum
# enum of actions
class Action(Enum):
    Delete = 1
    Suspend = 2
    Disable = 3


class ThresholdParameter(Enum):
    DueInDays = 1
    Stability = 2

from aqt import mw, gui_hooks
from anki.collection import SearchNode, OpChangesWithCount
from aqt.qt import QWidget
from collections.abc import Sequence
from anki.cards import CardId
from aqt.operations import CollectionOp
from anki.utils import ids2str
from anki.dbproxy import DBProxy
from aqt.operations.note import remove_notes
from aqt.operations.scheduling import suspend_cards

def remove_cards(*,
            parent: QWidget,
            card_ids: Sequence[CardId]
                 ) -> CollectionOp[OpChangesWithCount]:
    """Remove notes by card ID without blocking main thread"""
    # get note ids corresponding to card_ids
    db = DBProxy
    note_ids = db.list(
            f"select nid from cards where id in {ids2str(card_ids)}"
        )
    return remove_notes(parent=parent, note_ids=note_ids)

def on_state_change(new_state: str, old_state: str):
    if old_state == "review":
        # Get config params
        add_on_config = mw.addonManager.getConfig(__name__)
        deck_names: str = add_on_config["decks"]
        action: Action = Action(add_on_config["action"])
        threshold: int = add_on_config["threshold"]
        threshold_parameter: ThresholdParameter = ThresholdParameter(add_on_config["threshold_parameter"])

        # Get only the cards with a due date past the threshold
        graduated_cards = []
        for deck_name in deck_names:
            deck_id = mw.col.decks.id_for_name(deck_name)
            term: SearchNode | str = None
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

        # Perform action on cards
        # TODO: give user dialog to confirm
        # TODO: allow user to view list of card fronts to select which should be deleted
        testing = True
        if not testing:
            if action == Action.Delete:
                # non-blocking remove
                return remove_cards(parent=mw, card_ids=graduated_cards)
                # mw.col.remove_notes_by_card(graduated_cards)
            elif action == Action.Suspend:
                return suspend_cards(parent=mw, card_ids=graduated_cards)
        return None
    return None


gui_hooks.state_did_change.append(on_state_change)

from aqt.qt import QAction, QMenu
from .ConfigWidget import show_config_dialog

# Create a menu item for easy access
addon_top_menu = QMenu("Graduate Cards", mw)
config_action = QAction("Graduate Cards", mw)
config_action.triggered.connect(show_config_dialog)
addon_top_menu.addAction(config_action)
# Add the menu to Anki's menu bar
mw.form.menubar.addMenu(addon_top_menu)
# what happens when "config" click on from Tools -> Add-Ons
mw.addonManager.setConfigAction(__name__, show_config_dialog)

