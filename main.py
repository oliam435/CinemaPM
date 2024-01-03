import sys
from PyQt6.QtWidgets import QApplication

from ventana_principal import VentanaPrincipal
from resumen_compra import ResumenCompra

def main():
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    resumen_compra = ResumenCompra(ventana_principal.compras_realizadas)

    ventana_principal.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()