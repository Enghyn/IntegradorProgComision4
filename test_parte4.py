from codigo_corregido import Triangulo, Cuadrado, Lado
from libreria_externa import PlanoCAD
from protocolos import Exportable, exportar_todo


def main():
    items: list[Exportable] = [
        Triangulo.regular("t1", "rojo", 3),
        Cuadrado.regular("c1", "azul", 2),
        PlanoCAD("plano-001", "1:50"),
    ]
    for s in exportar_todo(items):
        print(s)


if __name__ == "__main__":
    main()