# Grupo: 
# Comisión: 4

## PARTE 1 Diagnóstico de java-ismos

| # | Java-ismo | Inversión conceptual | Síntoma observable |
|---|-----------|----------------------|--------------------|
| 1 | **Getters preventivos sin lógica** (`Figura.getNombre()`, `Figura.getColor()`) | Java obliga a atributos privados y, por costumbre, a getters que no aportan. Python permite acceso directo y el idioma `@property`; sin lógica detrás, el getter es ceremonia y se elimina. | Atributos accesibles directamente; getters vacíos que solo agregan ruido y pueden esconder modificaciones no deseadas. |
| 2 | **Getters y setters con lógica** (`Lado.getLongitud()`, `Lado.setLongitud()`) | La validación (longitud positiva) sí merece un guardián. Python lo resuelve con `@property` y `@longitud.setter`: se conserva la lógica con sintaxis de atributo. | El acceso correcto debería ser `lado.longitud`; con getters/setters explícitos habría que cambiar todas las llamadas. |
| 3 | **Static accidental** (`catalogo = []` a nivel de clase) | En Java `static` es una decisión explícita; en Python un atributo mutable a nivel de clase se comparte entre todas las instancias casi sin querer. Se elimina la declaración desnuda y el catálogo se administra desde `__init__`. | Si se modifica el atributo de una instancia, el cambio afecta a todas las demás instancias, con resultados inesperados. |
| 4 | **`super().__init__()` olvidado** (re-asignación manual de atributos) | En Java el `super` se invoca implícito; en Python hay que escribirlo. Declaramos `super().__init__(nombre, color)` al inicio y eliminamos la re-asignación a mano. | Sin el constructor del padre, `Figura` no inicializa sus atributos y el objeto falla en tiempo de ejecución. |
| 5 | **Sobrecarga de constructores** (`Triangulo`/`Cuadrado` con `*args` + `isinstance`) | Python no tiene sobrecarga; el patrón idiomático son fábricas con nombre: `@classmethod regular()`, `desde_lados()`, `por_defecto()`. | No se sabe qué constructor se está llamando; el código es difícil de leer y propenso a errores de tipo. |
| 6 | **Argumento por defecto mutable** (`lados=[]`, `observaciones=[]`) | El default mutable se evalúa UNA sola vez al definir la función y queda compartido. Se corrige con `lados=None` y copiando con `list(...)`. | Dos polígonos creados sin argumentos comparten la misma lista: `p1.agregar_observacion("error")` aparece también en `p2`. |
| 7 | **Bucle acumulador manual** (perímetro con `total = 0`) | Python trae `sum()` y expresiones generadoras: `sum(l.longitud for l in self._lados)` resuelve iteración y acumulación de forma expresiva. | Más líneas y más riesgo de error para una operación trivial del dominio. |
| 8 | **Falta de copia defensiva** (guardar y retornar el alias de la lista) | La referencia se expone igual que en Java; la solución es copiar al entrar (`self._lados = list(lados)`) y al salir (`tuple(self._lados)`). | El cliente puede hacer `poligono.getLados().clear()` o `.pop()` desde afuera y destruir el estado interno del objeto. |

## Tabla de equivalencias Java → Python (sobre nuestro código)

| Elemento en Java | Cómo quedó en tu código Python | ¿Traducción directa o rediseño? | Por qué |
|---|---|---|---|
| `Figura.getNombre()` / `Figura.getColor()` | Acceso directo `self._nombre` / `self._color`, getters eliminados | Rediseño | No había lógica detrás: Python no necesita ceremonia para leer atributos. |
| `Lado.getLongitud()` / `Lado.setLongitud(v)` | `@property longitud` + `@longitud.setter` | Rediseño | La validación (longitud > 0) se conserva igual, pero la API pasa de "bean" a atributo con guardián: `lado.longitud = x`. |
| `PoligonoRegular(nombre, color, medida, cantidad)` como subclase | `@classmethod regular(nombre, color, longitud_lado)` dentro de cada figura | Rediseño | En Java la clase servía para meter polígonos regulares en una lista tipada común. En Python no hay compilador que lo exija y el dominio no define una figura nueva. |
| Constructor sobrecargado con `*args` + `isinstance` | Fábricas con nombre: `@classmethod desde_lados()`, `por_defecto()`, `regular()` | Rediseño | Python no tiene sobrecarga; los classmethods explicitan la intención de cada creación. |
| `Poligono(nombre, color, lados=[], observaciones=[])` con defaults mutables | `lados=None` + `self._lados = list(lados) if lados else []` | Rediseño | Evita que dos instancias compartan la misma lista en memoria. |
| `self._lados = lados` (se guarda el alias entrante) | `self._lados = list(lados)` (copia al entrar) | Rediseño | El cliente no debe poder mutar el estado interno del polígono desde afuera. |
| `getLados()` que retorna la lista interna | `lados()` que retorna `tuple(self._lados)` | Rediseño | Copia defensiva al salir: la tupla es inmutable y no se puede vaciar desde afuera. |
| `perimetro()` con bucle `for` + `total +=` | `sum(l.longitud for l in self._lados)` | Traducción directa | Misma operación (sumar longitudes), expresada con el built-in `sum()` y un generador idiomático. |

## PARTE 2 Relaciones Estructurales Taller Etiqueta y Copias Defensivas

### Implementacion de Clases y Relaciones
Etiqueta implementada como dataclass frozen igual a True asegurando inmutabilidad.
Lado incorpora el atributo opcional etiqueta de tipo Etiqueta o None igual a None representando la asociacion cero a uno.
Poligono incluye el metodo lados que retorna list(self._lados) aplicando copia defensiva para la multiplicidad asterisco de la composicion Poligono Lado.
Taller gestiona agregacion cero a muchos de poligonos mediante recibir, restaurar e inventario el cual retorna copia defensiva list(self._poligonos).

### Pregunta
Si la sintaxis de guardar la referencia es identica en los tres casos self._algo igual a algo, como se ve en el código la diferencia entre agregación y composición? Responde para las tres relaciones, señalando el contexto exacto que lo delata.

### Respuesta
1. Composicion entre Poligono y Lado:
En el origen de los objetos componentes o en las fabricas, los objetos Lado son instanciados y creados internamente por el contenedor, ligando su ciclo de vida al poligono.

2. Agregacion entre Taller y Poligono:
En el metodo recibir del taller, este recibe un objeto polígono ya construido externamente mediante append. El taller no fabrica ni destruye los polígonos, solo los agrupa.

3. Asociacion entre Lado y Etiqueta:
En el constructor de Lado se asigna un objeto independiente recibido por parametro. No existe cocreacion ni dependencia de ciclo de vida.

## Parte 3 Herencia Justificada por Dominio
Poligono se define como clase abstracta heredando de ABC, con el metodo abstracto @abstractmethod def lados_esperados(self) -> int:.
Se implementan las subclases Triangulo (3), Cuadrado (4), Pentagono (5) y Hexagono (6), implementando cada una su lados_esperados().
En el constructor de Poligono se valida que la cantidad de lados recibida coincida exactamente con self.lados_esperados(), levantando ValueError si no coincide.
La falla temprana ocurre al intentar instanciar Poligono directamente o cualquier subclase sin lados_esperados(), lanzando TypeError en tiempo de instanciacion.

### Decisión sobre PoligonoRegular
#Inversión: En Java armábamos una clase PoligonoRegular para que el compilador nos deje meter polígonos regulares en una misma lista tipada. En Python eso no hace falta porque no tenemos un compilador exigiendo tipos. Además, por sentido común, un polígono regular no representa una figura distinta en la realidad, sino que es simplemente un triángulo o un cuadrado que tiene todos sus lados iguales.

#Rediseño código: Sacamos PoligonoRegular de la herencia y en su lugar usamos @classmethod regular(...) adentro de cada figura (Triangulo, Cuadrado, etc.). Así, en vez de obligar al usuario a pasar una lista con todos los lados repetidos a mano, la propia clase se encarga de crear los lados iguales con la cantidad exacta que necesita, sin inventar clases intermedias al vicio.

## Parte 4: ABC vs. Protocol

### 1. Implementación del contrato Exportable
Para poder trabajar al mismo tiempo con las clases de nuestro código y con
librerías externas, creamos el contrato `Exportable` usando `Protocol` con
el método `exportar() -> str`. 

Nuestra clase `Poligono`usa este método de forma directa. Por otro
lado, la clase `PlanoCAD` (que viene de la librería externa y no la podemos
tocar) ya tenía su propio método `exportar()`, así que cumple con el contrato
automáticamente sin tener que modificarla. Gracias a esto, la función 
`exportar_todo()` puede recibir una lista mezclada con polígonos y planos CAD
y hacerlos funcionar a todos juntos en tiempo de ejecución.

### 2. ¿Por qué no hubiéramos podido usar una ABC con PlanoCAD?
Las clases abstractas (`ABC`) nos exigen usar herencia explícita en el código.
Para que `PlanoCAD` funcionara con una ABC, tendríamos que haber entrado a su
archivo y escribir `class PlanoCAD(Exportable)`. 

Como la consigna nos prohibía modificar la librería externa, usar una ABC era
imposible. En cambio, con `Protocol` no importa de dónde viene la clase ni de
quién hereda: a Python solo le importa que el objeto tenga el método `exportar()`
listo para usarse (duck typing).

### 3. Elección entre ABC y Protocol: ¿Lo decide el lenguaje o el dominio?
**Lo decide el dominio, no el lenguaje.**

Python simplemente nos da las dos herramientas y nos deja elegir, pero la
decisión depende de la lógica de lo que estamos modelando:
- Usamos una **ABC** cuando existe una relación directa de "qué es" la clase.
  Por ejemplo, un Triángulo **es un** Polígono, comparten comportamiento base
  y queremos asegurarnos de que no se pueda crear uno incompleto.
- Usamos un **Protocol** cuando hablamos de una "habilidad" o acción secundaria.
  Exportar datos no define lo que es un objeto, sino algo que **sabe hacer**.
  Por eso lo comparten clases que no tienen nada que ver entre sí, como un
  Polígono de nuestro programa y un Plano CAD de una librería ajena.

## Cierre

**Cambió la forma, no la estructura.** Al pasar de Java a Python se reescribió
la sintaxis de acceso y de creación, pero el modelo de dominio quedó intacto.

Cambió:
- Los getters/setters estilo bean desaparecieron o se transformaron en `@property`
  (la API de acceso es ahora de atributo, no de método).
- `PoligonoRegular` salió de la jerarquía y se reemplazó por fábricas
  `@classmethod regular(...)` dentro de cada figura.
- La sobrecarga de constructores se convirtió en classmethods con nombre.
- Las colecciones dejaron de pasarse y devolverse por alias: copia defensiva al
  entrar (`list(...)`) y tuplas inmutables al salir.

Se mantuvo idéntico:
- La jerarquía de dominio `Figura → Poligono → Triangulo/Cuadrado/Pentagono/Hexagono`,
  con `Poligono` abstracta validando `lados_esperados()`.
- Las tres relaciones estructurales: composición `Poligono` ⊃ `Lado`,
  agregación `Taller` ⊃ `Poligono` y asociación `Lado → Etiqueta`.
- Las reglas de negocio: validación de cantidad de lados y de longitud positiva.
- El contrato `Exportable`: lo que en Java era una interfaz/clase abstracta, en
  Python es un `Protocol`; el "qué" (exponer `exportar()`) no cambió, cambió
  cómo se exige.

Esa separación confirma que lo que se portó fue el **diseño** (entidades,
relaciones y validaciones), mientras que lo que se reescribió fue la
**sintaxis** (properties, fábricas, `sum()` y comprensiones).