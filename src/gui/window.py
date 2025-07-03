from alias import (
    Application, Critical, MainWindow
)
from constants import (
    APP_NAME, APP_VERSION, APP_WIDTH, APP_HEIGHT
)

class Window(MainWindow):
    def __init__(self) -> None:
        super().__init__()

    def __centerScreen(self) -> None:
        application = Application.primaryScreen()

        if not application:
            Critical("[Class Window] Application Primary Screen is None.")
            return
        
        screen = application.availableGeometry()
        window = self.geometry()

        windowWidth = window.width()
        windowHeight = window.height()

        screenWidth = screen.width()
        screenHeight = screen.height()

        xLocation = (screenWidth - windowWidth) // 2
        yLocation = (screenHeight - windowHeight) // 2

        self.move(xLocation, yLocation)

    def InitApplication(self) -> None:
        self.setWindowTitle(f"{APP_NAME} | {APP_VERSION}")
        self.setMinimumSize(APP_WIDTH, APP_HEIGHT)
        self.__centerScreen()
        self.show()
