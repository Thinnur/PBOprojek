from PySide6.QtWidgets import QApplication
from controllers.keuangan_controller import PengelolaKeuangan
import sys

def main():
    app = QApplication(sys.argv)
    pengelola = PengelolaKeuangan()
    pengelola.view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()