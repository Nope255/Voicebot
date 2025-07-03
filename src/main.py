from gui import window
from type import (
    Appliation, SysArgv, SysExit
)

def main() -> None:
    application = Appliation(SysArgv)

    mainWindow = window.Window()
    mainWindow.InitApplication()
    
    SysExit(application.exec())
    
if __name__ == "__main__":
    main()