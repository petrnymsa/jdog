import random
from jdog.placeholder.placeholder import Placeholder


class OptionPlaceholder(Placeholder):
    def __init__(self, full_name, args):
        super().__init__(full_name, args)

    def exec(self):
        pick = random.choice(self.arguments)
        try:
            return pick.exec()
        except:
            return f'"{pick}"'
