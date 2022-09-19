class WebElementIsNotInput(Exception):
    def __init__(self) -> None:
        self.message = "WARNING: Passed web driver element is NOT TEXT FIELD or TEXT AREA"
        super().__init__(self.message)


class WebElementIsNotButton(Exception):
    def __init__(self) -> None:
        self.message = "WARNING: Passed web driver element is NOT BUTTON"
        super().__init__(self.message)


class WebElementIsNotDiv(Exception):
    def __init__(self) -> None:
        self.message = "WARNING: Passed web driver element is NOT DIV"
        super().__init__(self.message)