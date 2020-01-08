class Placeholder:
    """
        Base class for placeholders.

        :var str full_name:
        :var list arguments: Argument for placeholder

    """
    def __init__(self, full_name, arguments):
        self.full_name = full_name
        self.arguments = arguments

    def exec(self):
        """Each placeholder must have exec function"""
        pass

    def __str__(self):
        return f"{self.full_name} {self.arguments}"

# todo FIX: func placeholder should take argument and then pass it to func(...)


class FuncPlaceholder(Placeholder):
    """
        Represents placeholder which takes function to execute later.
        Returned value is fully determined by func itself.

        :var func func: Function to execute. Takes no arguments.TODO
    """
    def __init__(self, full_name, func):
        super().__init__(full_name, [])
        self.func = func

    def exec(self):
        """Executes func and return its returned value"""
        return self.func()


class FuncStrPlaceholder(FuncPlaceholder):
    """
            Represents placeholder which takes function to execute later.
            The returned value is enclosed with double quotes to denote JSON string value.

            :var func func: Function to execute. Takes no arguments.TODO
        """
    def __init__(self, full_name, func):
        super().__init__(full_name, func)

    def exec(self):
        """Executes func and return its value enclosed as string"""
        return f'"{self.func()}"'
