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
