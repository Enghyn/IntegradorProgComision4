# Grupo: 
# Comisión: 4

## PARTE 1 Diagnostico de java-ismos

## 1A- Caso de los Getters preventivos sin lógica | Metodos de clase Figura | 
#Inversión: en Java, creabamos los setters y getters porque no podiamos acceder a los atributos de la clase al hacerlos privados, pero en python no es necesario hacer esto, ya que podemos acceder a los atributos de la clase sin necesidad de hacer un getter o setter. Como no hay lógica en los getters y setters, no es necesario hacerlos, ya que no aportan nada a la clase.

#Sintoma observable: Los atributos de la clase son accesibles directamente, lo que puede llevar a modificaciones no deseadas.

## 1B- Caso de los Getters y setters con lógica | Metodos de clase Lado |
#Inversión: en este caso, si tiene sentido hacer los getters y setters en python. Si bien se puede seguir accediendo a estos, ya que no son realmente
privados, si es necesario hacerlos para poder controlar la lógica interna de los mismos. Por ello usamos @property para el getter y @nombre_atributo.setter para el setter.

#Sintoma observable: Acceder a estos datos de manera python seria lado.longitud, y esta se mantendría con @property.
En caso de usar getters y setters explicitos, la forma de llamarlos sería distinto, y se tendría que cambiar toda llamada a estos metodos.

## 2- Static accidental | Lista estatica de Poligono |
#Inversión: en Java estamos acostumbrado a declarar los atributoss de la clase al inicio de la misma, pero en python declararlas fuera del contructor genera un atributo de clase, que se comparte entre todas las instancias de la clase. Por ello, declaramos catalogo como un atributo de instancia en el constructor.

#Sintoma observable: Si se modifica el atributo de una instancia, se modifica para todas las instancias de la clase, lo que puede llevar a resultados inesperados.

## 3- Super olvidado
#Inversión: en Java, no declarar el super lo invoca de manera implicita. En Python, si no usamos la palabra clave `super()` para llamar a métodos de la clase padre, este no se invoca. Si se olvida de usarla, no se ejecutará el constructor de la clase padre, lo que puede causar problemas en la inicialización del objeto. Por ello declaramos el super en el constructor, y eliminamos la re-asignacion de atributos a mano.

#Sintoma observable: Si no se llama al constructor de la clase padre, los atributos de la clase padre no se inicializan correctamente, lo que puede llevar a errores en tiempo de ejecución.

## 4- Sobrecarga de constructores | Constructor de Cuadrado |
#Inversión: en Java, la sobrecarga de constructores permite múltiples constructores con diferentes firmas. En Python no existe la sobrecarga; el patrón idiomático es usar classmethods como fábricas con nombres descriptivos (ej: @classmethod desde_lados(cls, lados)), o usar *args/**kwargs con lógica interna, pero preferiblemente con nombres explícitos para mayor claridad.

#Sintoma observable: Si se intenta crear un objeto con diferentes conjuntos de parámetros, se puede obtener un error de tipo o un comportamiento inesperado.
Además, es muy dificil de leer y mantener el código, ya que no se sabe que constructor se esta llamando.

## 5- Argumento por defecto mutable | Parámetros lados=[] y observaciones=[] en Poligono.__init__ |
#Inversión: en Java no se evaluan los valores por defecto en la declaracion de la firma. Pero en python, las listas por defecto en los parametros se crean una sola vez, cuando se leen los archivos. Al poner lados=[] y observaciones=[], todas las instancias creadas sin argumentos comparten exactamente la misma lista en memoria.

#Sintoma observable: Si se crean dos polígonos sin pasarles observaciones y se agrega un texto a uno, por ejemplo:p1.agregar_observacion("error"), la observación aparece automáticamente en el segundo polígono p2, contaminando el estado entre los dos objetos en memoria.


## 6- Falta de copia defensiva en la inicialización | Asignación de self._lados en Poligono.__init__ |
#Inversión: en Java se suele asignar directamente la referencia recibida. En Python, asignar la lista recibida por parámetro crea una referencia al mismo objeto en memoria. Si el código que se encuentra fuera del objeto modifica esa lista después de construir el polígono, alterará el estado interno de la clase sin que esta pueda controlarlo.

#Sintoma observable: El cliente podria modificar o vaciar la lista desde fuera del objeto utilizando algun metodo, y alterar instantáneamente el resultado de métodos internos como p.perimetro(), rompiendo la integridad del objeto.


## 7- Bucle acumulador manual | Método perimetro en Poligono |
#Inversión: en Java es normal usar bucles acumuladores manuales, es decir, bucles for con total = 0. En Python esto es innecesario, ya que este lenguaje nos da funciones built-in y expresiones nativas capaces de generarlo que resuelven la iteración y acumulación de forma expresiva, limpia y optimizada.

#Sintoma observable: El problema con hacer bucles manuales en python es que se aumenta el riesgo de generar errores y lineas de codigo innecesarias que no aportan valor al dominio


## 8- Falta copia defensiva al retornar listas | Método getLados en Poligono |
#Inversión: en Java, al retornar una coleccion, se expone la referencia a ella. En Python, al hacer return self._lados, se le entrega al cliente la lista original de la estructura de datos interna lo que rompe el encapsulamiento. Para evitar esto, siempre se debe devolver una copia list(self._lados) o una tupla inmutable.

#Sintoma observable: El cliente puede hacer poligono.getLados().clear() o usar .pop() desde afuera del objeto y borrar los lados del polígono, destruyendo la coherencia del estado interno del objeto.

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