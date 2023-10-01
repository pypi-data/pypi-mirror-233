from dataclasses import dataclass

from busy.command.command import CollectionCommand
from busy.util.checklist import Checklist


@dataclass
class PrintCommand(CollectionCommand):
    """Generate a Checklist PDF"""

    full: bool = False
    default_criteria = ["1-"]
    name = "print"

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        parser.add_argument('--full', '-f', action='store_true')

    @CollectionCommand.wrap
    def execute(self):
        checklist = Checklist()
        collection = self.storage.get_collection(
            self.queue, self.collection_state)
        indices = collection.select(*self.criteria)
        if indices:
            if self.full:
                items = [collection[i].description for i in indices]
            else:
                items = [collection[i].base for i in indices]
        else:
            self.status = f"Queue '{self.queue}' has " + \
                f"no {self.collection_state} items that meet the criteria"
        queue = self.queue.capitalize()
        state = self.collection_state.capitalize()
        criteria = (": "+",".join(self.criteria)) \
            if (self.criteria != self.default_criteria) else ""
        title = f"{queue} ({state}{criteria})"
        checklist.generate(title, items)
