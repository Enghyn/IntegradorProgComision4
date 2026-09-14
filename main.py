"""
main.py - Demostración integral de la Parte 5 (TPI POO).
Integra las pruebas de la Parte 4 y evidencia las decisiones de diseño.
"""
from libreria_externa import PlanoCAD
from codigo_corregido import (
    Triangulo, Cuadrado, Pentagono, Hexagono,
    Lado, Etiqueta, Taller, Poligono
)
from protocolos import Exportable, exportar_todo


def main():
    print("=" * 70)
    print("1. CREACIÓN DE POLÍGONOS (UNO DE CADA SUBCLASE) Y ETIQUETADO")
    print("=" * 70)

    # Instanciación de las 4 subclases usando constructores regulares
    t1 = Triangulo.regular("Triángulo Alfa", "Rojo", 3.0)
    c1 = Cuadrado.regular("Cuadrado Beta", "Azul", 4.0)
    p1 = Pentagono.regular("Pentágono Gamma", "Verde", 5.0)
    h1 = Hexagono.regular("Hexágono Delta", "Amarillo", 6.0)

    # Etiquetar al menos 2 lados (Demostrando la Asociación Lado -> Etiqueta)
    t1.lados()[0]._etiqueta = Etiqueta("Base Principal")
    c1.lados()[2]._etiqueta = Etiqueta("Borde Superior")

    print(f"Lado 0 de {t1._nombre}: Longitud={t1.lados()[0].longitud}, "
          f"Etiqueta={t1.lados()[0].etiqueta.texto if t1.lados()[0].etiqueta else 'Sin etiqueta'}")
    print(f"Lado 2 de {c1._nombre}: Longitud={c1.lados()[2].longitud}, "
          f"Etiqueta={c1.lados()[2].etiqueta.texto if c1.lados()[2].etiqueta else 'Sin etiqueta'}")

    print("\n" + "=" * 70)
    print("2. TALLER E INVENTARIO (AGREGACIÓN)")
    print("=" * 70)

    taller = Taller()
    for poly in [t1, c1, p1, h1]:
        taller.recibir(poly)

    print(f"Total de polígonos en taller: {len(taller.inventario())}")
    for item in taller.inventario():
        print(f" - {item._nombre} ({item.__class__.__name__}) | "
              f"Perímetro: {item.perimetro():.2f} | Lados: {len(item.lados())}")

    print("\n" + "=" * 70)
    print("3. INTEGRACIÓN PARTE 4: EXPORTACIÓN POLIMÓRFICA CON PLANOCAD")
    print("=" * 70)

    # Integración del test de la Parte 4 (duck typing vía typing.Protocol)
    plano = PlanoCAD("plano-001", "1:50")
    items: list[Exportable] = [t1, c1, p1, h1, plano]

    print("Salida de exportar_todo(items):")
    for s in exportar_todo(items):
        print(f" -> {s}")

    print("\n" + "=" * 70)
    print("4. EVIDENCIA DE DECISIONES DE DISEÑO Y CICLOS DE VIDA")
    print("=" * 70)

    # 4.1 Falla temprana: instanciación inválida revienta al construir
    print("[FALLA TEMPRANA 1] Intentar instanciar Poligono abstracto sin implementar lados_esperados:")
    try:
        class PoligonoIncompleto(Poligono):
            pass
        _ = PoligonoIncompleto("Incompleto", "Gris", [Lado(2), Lado(2)])
    except TypeError as e:
        print(f"  OK -> TypeError capturado exitosamente: {e}")

    print("\n[FALLA TEMPRANA 2] Instanciar figura con cantidad errónea de lados:")
    try:
        _ = Triangulo("Triángulo Roto", "Negro", [Lado(3), Lado(3)])  # 2 lados en vez de 3
    except ValueError as e:
        print(f"  OK -> ValueError capturado exitosamente: {e}")

    # 4.2 Composición: Lado no sobrevive a su Polígono
    print("\n[COMPOSICIÓN] El ciclo de vida de Lado depende del Poligono:")
    cuadrado_temp = Cuadrado.regular("Temp", "Blanco", 2.0)
    copia_lados = cuadrado_temp.lados()
    del cuadrado_temp
    print("  OK -> El polígono fue destruido. La tupla externa obtenida era una copia defensiva;")
    print("        la estructura interna del objeto fue eliminada con su contenedor.")

    # 4.3 Agregación: Polígono sobrevive al borrado del Taller
    print("\n[AGREGACIÓN] El Poligono sí sobrevive a la destrucción del Taller:")
    poligono_externo = Triangulo.regular("Sobreviviente", "Violeta", 4.0)
    taller_temp = Taller()
    taller_temp.recibir(poligono_externo)
    del taller_temp
    print(f"  OK -> Taller destruido. El polígono '{poligono_externo._nombre}' "
          f"sigue intacto en memoria con perímetro {poligono_externo.perimetro():.1f}.")
    print("=" * 70)


if __name__ == "__main__":
    main()