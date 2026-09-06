# Grupo: 
# Comisión: 4

## 1A- Caso de los Getters preventivos sin lógica | Metodos de clase Figura | 
#Inversión: en Java, creabamos los setters y getters porque no podiamos acceder a los atributos de la clase al hacerlos privados, pero en python no es necesario hacer esto, ya que podemos acceder a los atributos de la clase sin necesidad de hacer un getter o setter. Como no hay lógica en los getters y setters, no es necesario hacerlos, ya que no aportan nada a la clase.

#Sintoma observable: Los atributos de la clase son accesibles directamente, lo que puede llevar a modificaciones no deseadas.

## 1B- Caso de los Getters y setters con lógica | Metodos de clase Lado |
#Inversión: en este caso, si tiene sentido hacer los gettes y setters en python. Si bien se puede seguir accediendo a estos, ya que no son realmente
privados, si es necesario hacerlos para poder controlar la logica interna de los mismos. Por ello usamos @property para el setter y @nombre_atributo.setter para el getter.

#Sintoma observable: Acceder a estos datos de manera python seria lado.longitud, y esta se mantendría con @property.
En caso de usar getters y setters explicitos, la forma de llamarlos sería distinto, y se tendría que cambiar toda llamada a estos metodos.

## 2- Static accidental | Lista estatica de Poligono |
#Inversión: en Java estamos acostumbrado a declarar los atributoss de la clase al inicio de la misma, pero en python declararlas fuera del contructor genera un atributo de clase, que se comparte entre todas las instancias de la clase. Por ello, declaramos catalogo como un atributo de instancia en el constructor.

#Sintoma observable: Si se modifica el atributo de una instancia, se modifica para todas las instancias de la clase, lo que puede llevar a resultados inesperados.

## 3- Super olvidado
#Inversión: en Java, no declarar el super lo invoca de manera implicita. En Python, si no usamos la palabra clave `super()` para llamar a métodos de la clase padre, este no se invoca. Si se olvida de usarla, no se ejecutará el constructor de la clase padre, lo que puede causar problemas en la inicialización del objeto. Por ello declaramos el super en el constructor, y eliminamos la re-asignacion de atributos a mano.

#Sintoma observable: Si no se llama al constructor de la clase padre, los atributos de la clase padre no se inicializan correctamente, lo que puede llevar a errores en tiempo de ejecución.

## 4- Sobrecarga de constructores | Constructor de Cuadrado |
#Inversión: en Java, se puede hacer sobrecarga de constructores, pero en python no es posible. Para ello, creamos los constructores con classsmethod, con un init que llama al super y instancia con los 
parametros, un classmethod que instancia con valorespor defecto y otro classmethod que instancia con los lados.

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