from dataclasses import dataclass

from busy.command.command import CollectionCommand


@dataclass
class EditorCommandBase(CollectionCommand):

    @CollectionCommand.wrap
    def execute(self):
        if not self.selection:
            self.status = "Edited nothing"
        else:
            edited = self.ui.edit_items(self.collection, self.selection)
            self.status = f"Edited {self.count(edited)}"


class EditOneItemCommand(EditorCommandBase):
    """Edit items; default to just one"""

    name = "edit"
    key = "e"


class EditManyCommand(EditorCommandBase):
    """Edit items; default to all"""

    name = 'manage'
    # key = 'm'
    default_criteria = ["1-"]
