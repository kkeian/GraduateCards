import os
import json
from aqt.qt import (QDialog, QComboBox, QWidget, QMessageBox,
                    QVBoxLayout, QFormLayout, QSpinBox, QListWidget,
                    QAbstractItemView, QHBoxLayout, QPushButton)
from aqt import mw

class ConfigDialog(QDialog):
    DEFAULT_THRESHOLD_DAYS = 90
    """Configuration dialog for Anki add-on."""
    def __init__(self):
        super().__init__()

        # load configuration from file if not overridden in code
        self.config = self.load_config()

        # Initialize UI
        self.setWindowTitle("Graduate Cards Configuration")
        self.setMinimumWidth(200)
        self.setup_ui()

    def load_config(self):
        """Load add-on configuration from file."""
        return mw.addonManager.getConfig(__name__)

    def save_config(self):
        """Write configuration."""
        mw.addonManager.writeConfig(__name__, self.config)

    def refresh_ui(self):
        """Refreshes UI based on saved configuration."""
        # select decks
        for i in range(self.decks.count()):
            item = self.decks.item(i)
            if item.text() in self.config.get("decks", []):
                item.setSelected(True)
        # select action
        if "action" in self.config:
            index = self.action.findText(self.config["action"])
            if index >= 0:
                self.action.setCurrentIndex(index)
        # select threshold_parameter
        if "threshold_parameter" in self.config:
            index = self.threshold_parameter.findText(self.config["threshold_parameter"])
            if index >= 0:
                self.threshold_parameter.setCurrentIndex(index)
        # fill threshold
        self.threshold.setValue(self.config.get("threshold", ConfigDialog.DEFAULT_THRESHOLD_DAYS))

    def setup_ui(self):
        """Set up the user interface of the configuration dialog widget."""
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # decks selection widget
        self.decks = QListWidget()
        self.decks.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        # get the list of decks in the current collection
        items = [deck_name_id.name for deck_name_id in mw.col.decks.all_names_and_ids()]
        self.decks.addItems(items)

        # select decks based on saved configuration
        # for i in range(self.decks.count()):
        #     item = self.decks.item(i)
        #     if item.text() in self.config.get("decks", []):
        #         item.setSelected(True)

        form_layout.addRow("Decks:", self.decks)

        # action ComboBox
        self.action = QComboBox()
        self.action.addItems(["Delete", "Suspend"])
        # if "action" in self.config:
        #     index = self.action.findText(self.config["action"])
        #     if index >= 0:
        #         self.action.setCurrentIndex(index)
        form_layout.addRow("Action:", self.action)

        # threshold parameter ComboBox
        self.threshold_parameter = QComboBox()
        self.threshold_parameter.addItems(["Due in Days", "Stability"])
        # if "threshold_parameter" in self.config:
        #     index = self.threshold_parameter.findText(self.config["threshold_parameter"])
        #     if index >= 0:
        #         self.threshold_parameter.setCurrentIndex(index)
        form_layout.addRow("Threshold Parameter:", self.threshold_parameter)

        # threshold days selection (1-365)
        self.threshold = QSpinBox()
        self.threshold.setRange(1, 365)
        # self.threshold.setValue(self.config.get("threshold", ConfigDialog.DEFAULT_THRESHOLD_DAYS))
        form_layout.addRow("Threshold days:", self.threshold)

        # fill widget initial values with config values
        self.refresh_ui()

        # add all widgets to form
        layout.addLayout(form_layout)

        # submit/cancel buttons side-by-side
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        button_layout.addStretch(1)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def update_config_from_ui(self):
        """Update configuration dictionary from UI widgets"""
        self.config["action"] = self.action.currentText()
        self.config["threshold_parameter"] = self.threshold_parameter.currentText()
        self.config["threshold"] = self.threshold.value()

        # Get all selected items
        selected_items = []
        for i in range(self.decks.count()):
            item = self.decks.item(i)
            if item.isSelected():
                selected_items.append(item.text())
        self.config["decks"] = selected_items

    def showEvent(self, event):
        """When this displays fill it with latest configuration data."""
        self.config = self.load_config()
        self.refresh_ui()
        super().showEvent(event)

    def accept(self):
        """Called when the user clicks Save"""
        self.update_config_from_ui()
        self.save_config()
        super().accept()


def show_config_dialog(parent=None):
    """Show the configuration dialog

    Args:
        parent: Parent window

    Returns:
        True if configuration was updated, False otherwise
    """
    # Create and show the dialog
    dialog = ConfigDialog()
    dialog.exec()
    return True