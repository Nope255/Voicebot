from type import(
    MainWindow, APP_NAME, APP_WIDTH, APP_HEIGHT
)

class Window(MainWindow):
    def __init__(self) -> None:
        super().__init__()

    def InitApplication(self) -> None:
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(APP_WIDTH, APP_HEIGHT)

        self.show()
