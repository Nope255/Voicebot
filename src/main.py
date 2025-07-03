from gui import window
from alias import (
    Application, SysArgv, SysExit
)

def main() -> None:
    application = Application(SysArgv)

    mainWindow = window.Window()
    mainWindow.InitApplication()

    SysExit(application.exec())
    
if __name__ == "__main__":
    main()