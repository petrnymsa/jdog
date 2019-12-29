from jdog.placeholder.placeholder import Placeholder


class FakerPlaceholder(Placeholder):
    def __init__(self, full_name, arguments, faker):
        super().__init__(full_name, arguments)
        self.faker = faker
