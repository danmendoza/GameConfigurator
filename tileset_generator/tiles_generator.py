import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QWidget, QInputDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QMouseEvent
from PyQt5.QtCore import Qt, QRect
from PIL import Image

class TilesGenerator(QWidget):
    def __init__(self, project_location=""):
        super().__init__()

        self.project_location = project_location

        self.setWindowTitle("Editor de Imágenes")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal horizontal
        self.main_layout = QHBoxLayout()

        # Layout vertical para los botones en el margen izquierdo
        self.button_layout = QVBoxLayout()

        # Botón para seleccionar imagen
        self.btn_open = QPushButton("Seleccionar Imagen")
        self.btn_open.clicked.connect(self.open_image)
        self.button_layout.addWidget(self.btn_open)

        # Botón para generar cuadrícula
        self.btn_grid = QPushButton("Generar Cuadrícula")
        self.btn_grid.clicked.connect(self.generate_grid)
        self.btn_grid.setEnabled(False)  # Desactivar hasta que se cargue una imagen
        self.button_layout.addWidget(self.btn_grid)

        # Botón para exportar cuadrícula
        self.btn_export = QPushButton("Exportar Cuadrícula")
        self.btn_export.clicked.connect(self.export_grid)
        self.btn_export.setEnabled(False)  # Desactivar hasta que se generen las celdas
        self.button_layout.addWidget(self.btn_export)

        # Añadir layout de botones al layout principal
        self.main_layout.addLayout(self.button_layout)

        # Etiqueta para mostrar la imagen
        self.label_image = QLabel("Aquí se mostrará la imagen")
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.mousePressEvent = self.start_selection
        self.label_image.mouseMoveEvent = self.update_selection
        self.label_image.mouseReleaseEvent = self.end_selection
        self.main_layout.addWidget(self.label_image)

        self.setLayout(self.main_layout)

        self.image = None
        self.pixmap = None
        self.cell_size = 0
        self.selected_cells = set()
        self.selecting = False

    def open_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", self.project_location, "", "Archivos de Imagen (*.png *.jpg *.jpeg)", options=options)
        if fileName:
            self.show_image(fileName)

    def show_image(self, file_path):
        # Abrir la imagen usando PIL
        self.image = Image.open(file_path)
        # Convertir la imagen a formato que Qt pueda manejar
        self.image = self.image.convert("RGBA")
        data = self.image.tobytes("raw", "RGBA")
        qim = QImage(data, self.image.width, self.image.height, QImage.Format_RGBA8888)

        # Mostrar la imagen en la etiqueta
        self.pixmap = QPixmap.fromImage(qim)
        self.label_image.setPixmap(self.pixmap.scaled(self.label_image.size(), Qt.KeepAspectRatio))
        self.btn_grid.setEnabled(True)  # Activar el botón para generar cuadrícula

    def generate_grid(self, cell_size=None):
        if self.image is None:
            return

        # Pedir el tamaño de la celda
        if(not cell_size):
            self.cell_size, ok = QInputDialog.getInt(self, "Tamaño de la celda", "Introduce el tamaño de la celda (en píxeles):", 50, 1, 1000, 1)
            if not ok:
                return
        else:
            self.cell_size = cell_size

        

        # Crear un nuevo QPixmap para dibujar la cuadrícula
        grid_pixmap = self.pixmap.copy()
        painter = QPainter(grid_pixmap)
        pen = QPen(QColor(255, 0, 0), 1, Qt.SolidLine)
        painter.setPen(pen)

        # Dibujar las líneas de la cuadrícula
        for x in range(0, grid_pixmap.width(), self.cell_size):
            painter.drawLine(x, 0, x, grid_pixmap.height())
        for y in range(0, grid_pixmap.height(), self.cell_size):
            painter.drawLine(0, y, grid_pixmap.width(), y)

        painter.end()

        # Mostrar la imagen con la cuadrícula
        self.label_image.setPixmap(grid_pixmap.scaled(self.label_image.size(), Qt.KeepAspectRatio))
        self.btn_export.setEnabled(True)  # Activar el botón para exportar cuadrícula

    def get_cell_from_position(self, event: QMouseEvent):
        if self.cell_size == 0 or self.pixmap is None:
            return None

        # Calcular la celda seleccionada basándonos en la posición real de la imagen en el QLabel
        label_width = self.label_image.width()
        label_height = self.label_image.height()
        pixmap_width = self.pixmap.width()
        pixmap_height = self.pixmap.height()

        scaled_pixmap = self.label_image.pixmap().scaled(label_width, label_height, Qt.KeepAspectRatio)
        x_offset = (label_width - scaled_pixmap.width()) // 2
        y_offset = (label_height - scaled_pixmap.height()) // 2

        x = event.pos().x() - x_offset
        y = event.pos().y() - y_offset

        if x < 0 or y < 0 or x >= scaled_pixmap.width() or y >= scaled_pixmap.height():
            return None

        col = x // (scaled_pixmap.width() / (pixmap_width / self.cell_size))
        row = y // (scaled_pixmap.height() / (pixmap_height / self.cell_size))
        return (int(col), int(row))

    def start_selection(self, event: QMouseEvent):
        self.selecting = True
        self.select_cell(event=event)

    def update_selection(self, event: QMouseEvent):
        if self.selecting:
            self.select_cell(no_remove=True, event=event)

    def end_selection(self, event: QMouseEvent):
        self.selecting = False

    def select_cell(self, event: QMouseEvent, no_remove=False):
        cell = self.get_cell_from_position(event)
        if cell is None:
            return
        if no_remove and cell in self.selected_cells:
            return

        if cell in self.selected_cells:
            self.selected_cells.remove(cell)
        else:
            self.selected_cells.add(cell)

        # Crear un nuevo QPixmap para dibujar la selección
        selection_pixmap = self.pixmap.copy()
        painter = QPainter(selection_pixmap)
        pen = QPen(QColor(0, 255, 0, 128), 1, Qt.SolidLine)
        painter.setPen(pen)
        brush = QColor(0, 255, 0, 128)
        painter.setBrush(brush)

        for cell in self.selected_cells:
            rect = QRect(cell[0] * self.cell_size, cell[1] * self.cell_size, self.cell_size, self.cell_size)
            painter.drawRect(rect)

        painter.end()

        # Mostrar la imagen con la selección
        self.label_image.setPixmap(selection_pixmap.scaled(self.label_image.size(), Qt.KeepAspectRatio))

    def export_grid(self):
        if not self.selected_cells:
            QMessageBox.warning(self, "Advertencia", "No hay celdas seleccionadas para exportar.")
            return

        if not self.are_cells_contiguous():
            QMessageBox.warning(self, "Advertencia", "Las celdas seleccionadas no son contiguas.")
            return

        # Crear una imagen nueva con las celdas seleccionadas
        selected_image = Image.new("RGBA", (self.cell_size * len(set(x for x, _ in self.selected_cells)),
                                            self.cell_size * len(set(y for _, y in self.selected_cells))))
        for cell in self.selected_cells:
            x, y = cell
            box = (x * self.cell_size, y * self.cell_size, (x + 1) * self.cell_size, (y + 1) * self.cell_size)
            cell_image = self.image.crop(box)
            selected_image.paste(cell_image, ((x - min(c[0] for c in self.selected_cells)) * self.cell_size,
                                              (y - min(c[1] for c in self.selected_cells)) * self.cell_size))

        # Guardar la imagen resultante
        filePath, _ = QFileDialog.getSaveFileName(self, "Guardar Imagen", self.project_location, "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if filePath:
            selected_image.save(filePath)

        # Reiniciar la selección de celdas
        self.reset_selection()

    def reset_selection(self):
        self.selected_cells.clear()
        # Volver a mostrar la imagen original con la cuadrícula
        self.generate_grid(cell_size=self.cell_size)

    def are_cells_contiguous(self):
        # Verificar si las celdas seleccionadas son contiguas
        def get_neighbors(cell):
            x, y = cell
            neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            return [neighbor for neighbor in neighbors if neighbor in self.selected_cells]

        if not self.selected_cells:
            return True

        cells_to_visit = [next(iter(self.selected_cells))]
        visited_cells = set()

        while cells_to_visit:
            cell = cells_to_visit.pop()
            if cell in visited_cells:
                continue
            visited_cells.add(cell)
            neighbors = get_neighbors(cell)
            cells_to_visit.extend(neighbors)

        return len(visited_cells) == len(self.selected_cells)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec_())
