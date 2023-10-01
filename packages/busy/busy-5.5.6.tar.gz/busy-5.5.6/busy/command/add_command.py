from dataclasses import dataclass

from busy.command.command import QueueCommand
from busy.model.item import Item


@dataclass
class AddCommand(QueueCommand):

    description: str = ""
    name = 'add'
    key = 'a'

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        parser.add_argument('--description', '-d', nargs='?')

    def clean_args(self):
        super().clean_args()
        if not self.provided('description'):
            self.description = self.ui.edit_text("")
            # edited = self.ui.edit_items(self.collection, self.selection)

    @QueueCommand.wrap
    def execute(self):
        if self.description:
            item = Item(self.description)
            self.collection.insert(0, item)
            self.status = "Added: " + self.description
        else:
            self.status = "Nothing added"


    # @CollectionCommand.wrap
    # def execute(self):
    #     if not self.selection:
    #         self.status = "Edited nothing"
    #     else:
    #         edited = self.ui.edit_items(self.collection, self.selection)
    #         self.status = f"Edited {self.count(edited)}"
