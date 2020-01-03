class Placeholder:
    def __init__(self, full_name, arguments):
        self.full_name = full_name
        self.arguments = arguments

    def exec(self):
        pass

    def __str__(self):
        return f"{self.full_name} {self.arguments}"


class FuncPlaceholder(Placeholder):
    def __init__(self, full_name, func):
        super().__init__(full_name, [])
        self.func = func

    def exec(self):
        return self.func()


class FuncStrPlaceholder(FuncPlaceholder):
    def __init__(self, full_name, func):
        super().__init__(full_name, func)

    def exec(self):
        return f'"{self.func()}"'
