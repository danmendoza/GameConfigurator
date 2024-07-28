import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QFileDialog, QMessageBox, QLabel, QSizePolicy
from tileset_generator.tiles_generator import TilesGenerator
from config_generator.json_editor import JsonEditor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Configurator")
        self.setGeometry(100, 100, 800, 600)

        self.project_location = ""

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.project_location_layout = QHBoxLayout()
        self.btn_set_project_location = QPushButton("Establecer Ubicación del Proyecto")
        self.btn_set_project_location.clicked.connect(self.set_project_location)

        # Set the size policy for the button
        self.btn_set_project_location.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.project_location_layout.addWidget(self.btn_set_project_location)

        self.lbl_project_location = QLabel("Ubicación del Proyecto: No establecida")
        # Set the size policy for the label to expand horizontally
        self.lbl_project_location.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.project_location_layout.addWidget(self.lbl_project_location)

        # Create a container widget for the project location layout
        self.project_location_widget = QWidget()
        self.project_location_widget.setLayout(self.project_location_layout)
        self.project_location_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        # Add the project location widget to the main layout
        self.main_layout.addWidget(self.project_location_widget)

        # Create a layout for the other two buttons
        self.buttons_layout = QVBoxLayout()

        self.btn_open_tileset_generator = QPushButton("Abrir Generador de Tilesets")
        self.btn_open_tileset_generator.clicked.connect(self.open_tileset_generator)
        self.buttons_layout.addWidget(self.btn_open_tileset_generator)

        self.btn_open_json_editor = QPushButton("Abrir Editor de JSON")
        self.btn_open_json_editor.clicked.connect(self.open_json_editor)
        self.buttons_layout.addWidget(self.btn_open_json_editor)

        # Add the buttons layout to the main layout
        self.main_layout.addLayout(self.buttons_layout)

        # Set margins and spacing
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def open_tileset_generator(self):
        self.tiles_generator = TilesGenerator(self.project_location)
        self.tiles_generator.show()

    def open_json_editor(self):
        self.json_editor = JsonEditor(self.project_location)
        self.json_editor.show()

    def set_project_location(self):
        options = QFileDialog.Options()
        project_location = QFileDialog.getExistingDirectory(self, "Seleccionar Ubicación del Proyecto", options=options)
        if project_location:
            self.project_location = project_location
            self.lbl_project_location.setText(f"Ubicación del Proyecto: {self.project_location}")
            QMessageBox.information(self, "Ubicación del Proyecto", f"Ubicación del proyecto establecida en: {self.project_location}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
