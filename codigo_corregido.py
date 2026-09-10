from abc import ABC, abstractmethod
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


class Poligono(Figura, ABC):
    def __init__(self, nombre, color, lados=None, observaciones=None):
        super().__init__(nombre, color)
        self._lados = list(lados) if lados else []
        self._observaciones = list(observaciones) if observaciones else []

        if len(self._lados) != self.lados_esperados():
            raise ValueError(f"{nombre} debe tener {self.lados_esperados()} lados")

        if not hasattr(Poligono, '_catalogo'):
            Poligono._catalogo = []
        Poligono._catalogo.append(self)

    @abstractmethod
    def lados_esperados(self) -> int:
        pass

    def perimetro(self):
        return sum(l.longitud for l in self._lados)

    def area(self):
        return "area sin calcular"

    def agregar_observacion(self, texto):
        self._observaciones.append(texto)

    def lados(self):
        return tuple(self._lados)


class Taller:
    def __init__(self):
        self._poligonos = []

    def recibir(self, poligono: Poligono):
        self._poligonos.append(poligono)

    def restaurar(self, poligono: Poligono):
        self._poligonos.remove(poligono)

    def inventario(self):
        return tuple(self._poligonos)


class Triangulo(Poligono):
    def __init__(self, nombre, color, lados):
        super().__init__(nombre, color, lados)

    @classmethod
    def desde_lados(cls, lados):
        return cls("triángulo", "negro", lados)

    @classmethod
    def por_defecto(cls):
        return cls("triángulo", "negro", [])

    @classmethod
    def regular(cls, nombre, color, longitud_lado):
        lados = [Lado(longitud_lado) for _ in range(3)]
        return cls(nombre, color, lados)

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

    @classmethod
    def regular(cls, nombre, color, longitud_lado):
        lados = [Lado(longitud_lado) for _ in range(4)]
        return cls(nombre, color, lados)

    def lados_esperados(self):
        return 4


class Pentagono(Poligono):
    def __init__(self, nombre, color, lados):
        super().__init__(nombre, color, lados)

    @classmethod
    def regular(cls, nombre, color, longitud_lado):
        lados = [Lado(longitud_lado) for _ in range(5)]
        return cls(nombre, color, lados)

    def lados_esperados(self):
        return 5


class Hexagono(Poligono):
    def __init__(self, nombre, color, lados):
        super().__init__(nombre, color, lados)

    @classmethod
    def regular(cls, nombre, color, longitud_lado):
        lados = [Lado(longitud_lado) for _ in range(6)]
        return cls(nombre, color, lados)

    def lados_esperados(self):
        return 6