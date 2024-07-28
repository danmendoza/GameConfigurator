import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from tileset_generator.simple_tilegen import ImageEditor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ventana Principal")
        self.setGeometry(100, 100, 400, 300)

        self.main_layout = QVBoxLayout()

        self.btn_open_editor = QPushButton("Abrir Generador de Tiles")
        self.btn_open_editor.clicked.connect(self.open_image_editor)
        self.main_layout.addWidget(self.btn_open_editor)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def open_image_editor(self):
        self.image_editor = ImageEditor()
        self.image_editor.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
