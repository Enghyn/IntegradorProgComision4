# demo_sintomas.py
# Demostración de dos javaísmos con síntomas reproducibles, usando parte1_diagnostico.py (implementación ANTERIOR al arreglo idiomático)
from parte1_diagnostico import Poligono, Lado

print('Sintoma 1: Argumento por defecto mutable')
p1 = Poligono('p1', 'rojo')
p2 = Poligono('p2', 'azul')
p1.agregar_observacion('¡javaísmo!')
print('¿Las observaciones están compartidas?', p1._observaciones is p2._observaciones)  # True
print('Observaciones de p2:', p2._observaciones) # Tiene la observación de p1
print()

print('Sintoma 2: Falta de copia defensiva en la inicialización')
lados = [Lado(3), Lado(4), Lado(5)]
p = Poligono('p', 'verde', lados)
print('Perímetro antes de modificar la lista externa:', p.perimetro())
lados.append(Lado(6))
print('Perímetro después de modificar la lista externa:', p.perimetro())  # Cambia el perímetro
print()

print('=== Migración de Getter a @property en Lado ===')
print('Convertimos Lado.getLongitud() / setLongitud() a @property.')
print('Esto nos permite usar sintaxis pythónica sin perder las validaciones.')
print()

class LadoAntes:
    def __init__(self, longitud):
        self._longitud = longitud

    def getLongitud(self):
        return self._longitud

    def setLongitud(self, valor):
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor


class LadoDespues:
    def __init__(self, longitud):
        self._longitud = longitud

    @property
    def longitud(self):
        return self._longitud

    @longitud.setter
    def longitud(self, valor):
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor

    def getLongitud(self):
        return self.longitud

    def setLongitud(self, valor):
        self.longitud = valor


print('--- ANTES (Sintaxis estilo Java) ---')
lado_a = LadoAntes(5)
print(f'Leemos con el getter: {lado_a.getLongitud()}')
lado_a.setLongitud(10)
print(f'Cambiamos el valor a 10: {lado_a.getLongitud()}')
try:
    lado_a.setLongitud(-3)
except ValueError as e:
    print(f'Intento de asignar -3 rechazado: {e}')

print()
print('--- DESPUÉS (Uso con @property y compatibilidad) ---')
lado_d = LadoDespues(5)
print(f'Lectura directa (Python): {lado_d.longitud}')
print(f'Lectura con getter anterior: {lado_d.getLongitud()}')
lado_d.longitud = 10
print(f'Asignación directa a 10: {lado_d.longitud}')
lado_d.setLongitud(15)
print(f'Asignación con setter a 15: {lado_d.getLongitud()}')
try:
    lado_d.longitud = -3
except ValueError as e:
    print(f'Intento de asignar -3 rechazado por la property: {e}')

print()
print('✔ El código viejo con get/set sigue funcionando sin tocar una sola línea.')
print('✔ El código nuevo ya puede usar la sintaxis limpia de atributos (.longitud).')
print('✔ La regla de negocio (longitud positiva) se mantiene protegida.')