from PyQt6.QtWidgets import QApplication, QCheckBox, QLabel, QMessageBox, QPushButton, QTextEdit, QVBoxLayout, QWidget, QGridLayout, QLayout
from PyQt6.QtCore import Qt
cont = 0
from resumen_compra import ResumenCompra
class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.ventas_por_sala = {'Sala 1': 0, 'Sala 2': 0, 'Sala 3': 0}
        self.venta_general = 0
        self.total_compra = 0 
        self.iniciar_interfaz()
    def iniciar_interfaz(self):
        self.layout_principal = QVBoxLayout()
        titulo = QLabel('CinemaPM')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet('font-size: 24px; font-weight: bold; margin-top: 20px; margin-bottom: 20px;')
        self.layout_principal.addWidget(titulo)

        descripcion = QLabel('''Bienvenido a CinemaPM. Aprete el boton de Comprar Entradas y Seleccione una sala y una hora para comenzar tu compra de entradas. 
                            la pelicula que se transmitira hoy es Five Nights At Freddys.''')
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descripcion.setStyleSheet('margin-bottom: 20px; color: #333;')
        self.layout_principal.addWidget(descripcion)

        self.boton_comprar = QPushButton('Comprar Entradas')
        self.boton_resumen = QPushButton('Ver Resumen')
        self.boton_salir = QPushButton('Salir')

        self.boton_comprar.clicked.connect(self.al_hacer_click_comprar)
        self.boton_resumen.clicked.connect(self.al_hacer_click_resumen)
        self.boton_salir.clicked.connect(self.confirmar_salir)

        self.layout_principal.addWidget(self.boton_comprar)
        self.layout_principal.addWidget(self.boton_resumen)
        self.layout_principal.addWidget(self.boton_salir)

        self.layout_sala = None
        self.layout_horario = None
        self.layout_asientos = None
        self.layout_resumen = None

        self.sala_seleccionada = None
        self.horario_seleccionado = None
        self.asientos_seleccionados = []
        self.compras_realizadas = []

        self.texto_resumen = QTextEdit()
        self.texto_resumen.setReadOnly(True)

        self.setLayout(self.layout_principal)
        self.setWindowTitle('Sistema de Compra de Entradas')
        self.setGeometry(550, 150, 500, 500)
        self.show()
    def confirmar_salir(self):
        respuesta = QMessageBox.question(self, 'Salir', '¿Estás seguro de que quieres salir?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if respuesta == QMessageBox.StandardButton.Yes:
            self.close()
        else:
            pass
    def al_hacer_click_comprar(self):
        self.limpiar_layout()
        self.layout_sala = QVBoxLayout()
        label_sala = QLabel('Selecciona una sala:')
        self.layout_sala.addWidget(label_sala)

        boton_sala1 = QPushButton('Sala 1')
        boton_sala2 = QPushButton('Sala 2')
        boton_sala3 = QPushButton('Sala 3')

        boton_sala1.clicked.connect(lambda: self.al_hacer_click_sala('Sala 1'))
        boton_sala2.clicked.connect(lambda: self.al_hacer_click_sala('Sala 2'))
        boton_sala3.clicked.connect(lambda: self.al_hacer_click_sala('Sala 3'))

        self.layout_sala.addWidget(boton_sala1)
        self.layout_sala.addWidget(boton_sala2)
        self.layout_sala.addWidget(boton_sala3)

        self.layout_principal.addLayout(self.layout_sala)

        
    def al_hacer_click_sala(self, sala_seleccionada):
        self.sala_seleccionada = sala_seleccionada
        self.limpiar_layout(self.layout_sala)
        self.layout_horario = QVBoxLayout()
        label_horario = QLabel('Selecciona la hora de la función:')

        self.layout_horario.addWidget(label_horario)
        boton_horario1 = QPushButton('3pm')
        boton_horario2 = QPushButton('6pm')
        boton_horario3 = QPushButton('9pm')

        boton_horario1.clicked.connect(lambda: self.al_hacer_click_horario('3pm'))
        boton_horario2.clicked.connect(lambda: self.al_hacer_click_horario('6pm'))
        boton_horario3.clicked.connect(lambda: self.al_hacer_click_horario('9pm'))

        self.layout_horario.addWidget(boton_horario1)
        self.layout_horario.addWidget(boton_horario2)
        self.layout_horario.addWidget(boton_horario3)

        self.layout_principal.addLayout(self.layout_horario)
    def al_hacer_click_horario(self, horario_seleccionado):
        self.horario_seleccionado = horario_seleccionado
        self.limpiar_layout(self.layout_horario)
        self.layout_asientos = QVBoxLayout()
        self.grid_layout = QGridLayout()
        label_asientos = QLabel('Selecciona los asientos:')
        self.layout_asientos.addWidget(label_asientos)
        grid_layout = QGridLayout()
        asientos = ['A1', 'A2', 'A3', 'A4', 'A5',
                    'B1', 'B2', 'B3', 'B4', 'B5',
                    'C1', 'C2', 'C3', 'C4', 'C5',
                    'D1', 'D2', 'D3', 'D4', 'D3',
                    'F1', 'F2', 'F3', 'F4', 'F5']      
        fila = 0
        columna = 0
        for asiento in asientos:
            checkbox = QCheckBox(asiento)
            checkbox.stateChanged.connect(self.al_cambiar_checkbox)
            self.grid_layout.addWidget(checkbox, fila, columna)
            columna += 1
            if columna == 5:
                columna = 0
                fila += 1
        self.layout_asientos.addLayout(self.grid_layout)
        boton_aceptar = QPushButton('Aceptar')
        boton_aceptar.clicked.connect(self.al_hacer_click_aceptar)
        self.layout_asientos.addWidget(boton_aceptar)

        self.layout_principal.addLayout(self.layout_asientos)

    def verificar_disponibilidad(self, sala, horario, asientos_solicitados):
        for asiento in asientos_solicitados:
            fila, columna = self.obtener_fila_columna(asiento)
            if self.asientos_disponibles[sala][horario][fila][columna] == 1:
                return False 
        return True 
    def obtener_fila_columna(self, asiento):
        fila = ord(asiento[0]) - ord('A')
        columna = int(asiento[1]) - 1
        return fila, columna
    def al_cambiar_checkbox(self, estado):
        checkbox = self.sender()
        asiento = checkbox.text()
        cont= 0
        if estado == 2:
            self.asientos_seleccionados.append(asiento)
            cont = cont + 1
        elif estado == 0:
            self.asientos_seleccionados.remove(asiento)
            cont = cont - 1
    def al_hacer_click_aceptar(self, cont):
        cont = 1
        self.total_compra = cont * 3000
        compra = {
            'Sala': self.sala_seleccionada,
            'Horario': self.horario_seleccionado,
            'Asientos': self.asientos_seleccionados,
            'Total': self.total_compra
        }
        self.compras_realizadas.append(compra)
        self.limpiar_layout(self.grid_layout)
        self.limpiar_layout(self.layout_principal)
        self.mostrar_pantalla_principal()
    def al_hacer_click_resumen(self):
        ResumenCompra()

    def mostrar_pantalla_principal(self):
        self.texto_resumen.clear()
        self.texto_resumen.append('Resumen de la compra:')
        if self.compras_realizadas:
            ultima_compra = self.compras_realizadas[-1]
            resumen = f'Sala: {ultima_compra["Sala"]}, Horario: {ultima_compra["Horario"]}, Asientos: {", ".join(ultima_compra["Asientos"])}, Total: ${ultima_compra["Total"]}'
            self.texto_resumen.append(resumen)
            self.texto_resumen.setReadOnly(True)
        self.layout_resumen = QVBoxLayout()
        self.layout_resumen.addWidget(self.texto_resumen)
        self.layout_principal.addLayout(self.layout_resumen)


    def limpiar_layout(self, layout_or_textedit=None):
        if layout_or_textedit is None:
            layout_or_textedit = self.layout_principal

        if isinstance(layout_or_textedit, QLayout):
            for i in reversed(range(layout_or_textedit.count())):
                widget = layout_or_textedit.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
        elif isinstance(layout_or_textedit, QTextEdit):
            layout_or_textedit.clear()
        else:
            raise ValueError("Tipo de layout incopatible")

