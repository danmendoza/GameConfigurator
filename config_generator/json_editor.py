import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTextEdit, QMessageBox, QInputDialog, QComboBox

class JsonEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor de JSON")
        self.setGeometry(100, 100, 800, 600)

        self.main_layout = QHBoxLayout()  # Layout principal horizontal

        self.button_layout = QVBoxLayout()  # Layout vertical para los botones
        self.json_layout = QVBoxLayout()  # Layout vertical para el contenido JSON

        self.btn_open = QPushButton("Abrir JSON")
        self.btn_open.clicked.connect(self.open_json_file)
        self.button_layout.addWidget(self.btn_open)

        self.btn_new = QPushButton("Nuevo JSON")
        self.btn_new.clicked.connect(self.new_json_file)
        self.button_layout.addWidget(self.btn_new)

        self.btn_add_parent_key = QPushButton("Crear clave Padre")
        self.btn_add_parent_key.clicked.connect(self.add_parent_key)
        self.button_layout.addWidget(self.btn_add_parent_key)

        self.btn_add_child_key = QPushButton("Crear clave Hijo")
        self.btn_add_child_key.clicked.connect(self.add_child_key)
        self.button_layout.addWidget(self.btn_add_child_key)
        
        self.btn_delete_key = QPushButton("Borrar clave")  # Nuevo botón
        self.btn_delete_key.clicked.connect(self.delete_key)
        self.button_layout.addWidget(self.btn_delete_key)

        self.json_text = QTextEdit(self)
        self.json_text.setReadOnly(True)
        self.json_layout.addWidget(self.json_text)

        self.btn_save = QPushButton("Guardar JSON")
        self.btn_save.clicked.connect(self.save_json_file)
        self.json_layout.addWidget(self.btn_save)

        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addLayout(self.json_layout)
        
        self.setLayout(self.main_layout)

        self.json_data = {}  # Diccionario para almacenar los datos JSON
        self.current_file = None  # Variable para rastrear el archivo actual

    def open_json_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo JSON", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    self.json_data = json.load(file)
                    self.json_text.setPlainText(json.dumps(self.json_data, indent=4))
                    self.current_file = file_name
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo: {e}")

    def new_json_file(self):
        self.json_data = {}
        self.json_text.clear()
        self.current_file = None

    def add_parent_key(self):
        key, ok = QInputDialog.getText(self, "Crear clave Padre", "Introduce el nombre de la clave:")
        if ok and key:
            value, ok = QInputDialog.getText(self, "Crear clave Padre", "Introduce el valor de la clave:")
            if ok:
                try:
                    self.json_data[key] = json.loads(value)
                except json.JSONDecodeError:
                    self.json_data[key] = value
                self.json_text.setPlainText(json.dumps(self.json_data, indent=4))

    def add_child_key(self):
        if not self.json_data:
            QMessageBox.warning(self, "Advertencia", "Primero crea una clave padre.")
            return

        parent_key, ok = self.select_parent_key()
        if ok and parent_key:
            child_key, ok = QInputDialog.getText(self, "Crear clave Hijo", "Introduce el nombre de la clave hija:")
            if ok and child_key:
                value_type, ok = QInputDialog.getItem(self, "Tipo de Valor", "Selecciona el tipo de valor:", ["String", "File Path"], 0, False)
                if ok and value_type:
                    if value_type == "String":
                        value, ok = QInputDialog.getText(self, "Crear clave Hijo", "Introduce el valor de la clave hija:")
                        if ok:
                            if isinstance(self.json_data[parent_key], dict):
                                self.json_data[parent_key][child_key] = value
                            else:
                                QMessageBox.warning(self, "Advertencia", "La clave padre no es un objeto JSON válido.")
                    elif value_type == "File Path":
                        options = QFileDialog.Options()
                        file_name, _ = QFileDialog.getOpenFileNames(self, "Selecciona la ruta del archivo", "", "All Files (*)", options=options)
                        if file_name:
                            if isinstance(self.json_data[parent_key], dict):
                                self.json_data[parent_key][child_key] = file_name
                            else:
                                QMessageBox.warning(self, "Advertencia", "La clave padre no es un objeto JSON válido.")
                    self.json_text.setPlainText(json.dumps(self.json_data, indent=4))

    def delete_key(self):
        if not self.json_data:
            QMessageBox.warning(self, "Advertencia", "No hay claves para borrar.")
            return

        key, ok = self.select_parent_key()
        if ok and key:
            del self.json_data[key]
            self.json_text.setPlainText(json.dumps(self.json_data, indent=4))
            QMessageBox.information(self, "Éxito", f"Clave '{key}' borrada correctamente.")
        else:
            QMessageBox.warning(self, "Advertencia", "Clave no encontrada o no válida.")

    def select_parent_key(self):
        keys = list(self.json_data.keys())
        if not keys:
            return None, False

        key, ok = QInputDialog.getItem(self, "Seleccionar clave Padre", "Selecciona una clave padre:", keys, 0, False)
        return key, ok

    def save_json_file(self):
        if not self.current_file:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo JSON", "", "JSON Files (*.json);;All Files (*)", options=options)
            if not file_name:
                return
            self.current_file = file_name

        try:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                json.dump(self.json_data, file, indent=4)
            QMessageBox.information(self, "Éxito", "Archivo guardado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo: {e}")
