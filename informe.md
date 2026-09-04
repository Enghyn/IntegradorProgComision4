# Grupo: 
# Comisión: 4

## 1A- Getters preventivos sin lógica | Metodos de clase Figura | 
#Inversión: en Java, creabamos los setters y getters porque no podiamos acceder a los atributos de la clase al hacerlos privados, pero en python no es necesario hacer esto, ya que podemos acceder a los atributos de la clase sin necesidad de hacer un getter o setter. Como no hay lógica en los getters y setters, no es necesario hacerlos, ya que no aportan nada a la clase.

#Sintoma observable: 

## 1B- Getter y setter con lógica | Metodos de clase Lado |
#Inversión: en este caso, si tiene sentido hacer los gettes y setters en python. Si bien se puede seguir accediendo a estos, ya que no son realmente
privados, si es necesario hacerlos para poder controlar la logica interna de los mismos. Por ello usamos @property para el setter y @nombre_atributo.setter para el getter.

#Sintoma observable:

## 2- Static accidental | Lista estatica de Poligono |
#Inversión: en Java estamos acostumbrado a declarar los atributoss de la clase al inicio de la misma, pero en python declararlas fuera del contructor genera un atributo de clase, que se comparte entre todas las instancias de la clase. Por ello, declaramos catalogo como un atributo de instancia en el constructor.

#Sintoma observable: 

## 3- Super olvidado
#Inversión: en Java, no declarar el super lo invoca de manera implicita. En Python, si no usamos la palabra clave `super()` para llamar a métodos de la clase padre, este no se invoca. Si se olvida de usarla, no se ejecutará el constructor de la clase padre, lo que puede causar problemas en la inicialización del objeto. Por ello declaramos el super en el constructor, y eliminamos la re-asignacion de atributos a mano.

#Sintoma observable:

## 4- Sobrecarga de constructores | Constructor de Cuadrado |
#Inversión: en Java, se puede hacer sobrecarga de constructores, pero en python no es posible. 

#Sintoma observable:

## 5- Java-ismo


## 6- Java-ismo


## 7- Java-ismo


## 8- Java-ismo