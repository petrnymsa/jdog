from jdog.placeholder.placeholder import Placeholder
import random


class RangePlaceholder(Placeholder):
    def __init__(self, full_name, args):
        super().__init__(full_name, args)
        self.prop = args[0]
        self.low = args[1]
        if len(args) > 2:
            self.high = args[2]
        #self.times = 0

    def exec(self):
        # if self.high:
        #     self.times = random.randint(self.low, self.high - 1)
        # else:
        #     self.times = self.low
        #
        # return f'"{self.prop}"'
        pass

