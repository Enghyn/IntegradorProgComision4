from dataclasses import dataclass


@dataclass(frozen=True)
class Etiqueta:
    texto: str


class Figura:
    def __init__(self, nombre, color):
        self._nombre = nombre
        self._color = color
        self._construida = True

    def area(self):
        return 0.0


class Lado:
    def __init__(self, longitud, etiqueta: Etiqueta | None = None):
        self._longitud = longitud
        self._etiqueta = etiqueta

    @property
    def longitud(self):
        return self._longitud

    @longitud.setter
    def longitud(self, valor):
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor

    @property
    def etiqueta(self):
        return self._etiqueta


class Poligono(Figura):
    def __init__(self, nombre, color, lados=None, observaciones=None):
        super().__init__(nombre, color)
        self._lados = list(lados) if lados else []
        self._observaciones = list(observaciones) if observaciones else []
        if not hasattr(Poligono, '_catalogo'):
            Poligono._catalogo = []
        Poligono._catalogo.append(self)

    def lados_esperados(self):
        return 0

    def perimetro(self):
        return sum(l.longitud for l in self._lados)

    def area(self):
        return "area sin calcular"

    def agregar_observacion(self, texto):
        self._observaciones.append(texto)

    def lados(self):
        return list(self._lados)


class Taller:
    def __init__(self):
        self._poligonos = []

    def recibir(self, poligono: Poligono):
        self._poligonos.append(poligono)

    def restaurar(self, poligono: Poligono):
        self._poligonos.remove(poligono)

    def inventario(self):
        return list(self._poligonos)


class Triangulo(Poligono):
    def __init__(self, nombre, color, lados):
        super().__init__(nombre, color, lados)

    @classmethod
    def desde_lados(cls, lados):
        return cls("triángulo", "negro", lados)

    @classmethod
    def por_defecto(cls):
        return cls("triángulo", "negro", [])

    def lados_esperados(self):
        return 3


class Cuadrado(Poligono):
    def __init__(self, nombre, color, lados):
        super().__init__(nombre, color, lados)

    @classmethod
    def desde_lados(cls, lados):
        return cls("cuadrado", "negro", lados)

    @classmethod
    def por_defecto(cls):
        return cls("cuadrado", "negro", [])

    def lados_esperados(self):
        return 4
