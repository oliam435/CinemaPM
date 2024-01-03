from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget

class ResumenCompra(QWidget):
    def __init__(self, compras_realizadas):
        super().__init__()
        self.layout_resumen = QVBoxLayout()
        self.texto_resumen = QTextEdit()

        self.compras_realizadas = compras_realizadas

        self.layout_resumen.addWidget(self.texto_resumen)
        self.setLayout(self.layout_resumen)

    def mostrar_resumen(self):
        self.texto_resumen.clear()
        self.texto_resumen.append('Resumen de la compra:')
        
        for compra in self.compras_realizadas:
            resumen = f'Sala: {compra["Sala"]}, Horario: {compra["Horario"]}, Asientos: {", ".join(compra["Asientos"])}'
            self.texto_resumen.append(resumen)
    