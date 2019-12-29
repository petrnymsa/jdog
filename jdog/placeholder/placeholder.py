class Placeholder:
    def __init__(self, full_name, arguments):
        self.full_name = full_name
        self.arguments = arguments

    def exec(self):
        pass

    def __str__(self):
        return f"{self.full_name} {self.arguments}"
