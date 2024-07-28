import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from tileset_generator.tiles_generator import TilesGenerator  # Actualiza la importación
from config_generator.json_editor import JsonEditor  # Actualiza la importación

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ventana Principal")
        self.setGeometry(100, 100, 400, 300)

        self.main_layout = QVBoxLayout()

        self.btn_open_image_editor = QPushButton("Abrir Editor de Imágenes")
        self.btn_open_image_editor.clicked.connect(self.open_image_editor)
        self.main_layout.addWidget(self.btn_open_image_editor)

        self.btn_open_json_editor = QPushButton("Abrir Editor de JSON")  # Nuevo botón
        self.btn_open_json_editor.clicked.connect(self.open_json_editor)
        self.main_layout.addWidget(self.btn_open_json_editor)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def open_image_editor(self):
        self.image_editor = TilesGenerator()
        self.image_editor.show()

    def open_json_editor(self):  # Nueva función para abrir JsonEditor
        self.json_editor = JsonEditor()
        self.json_editor.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
