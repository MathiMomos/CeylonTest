# 1. Qué es Ceylon
Ceylon es un lenguaje de programación estructurado e interpretado de fácil aprendizaje y que brinda una sintaxis sencilla y familiar para cualquier programador. Ceylon ha sido creado con el propósito de que sus creadores aprendan y comprendan el quid del cómo se crean los lenguajes de programación que aprendemos y utilizamos en nuestra labor diaria. Este lenguaje, y su interprete, han sido creados tomando en cuenta las consideraciones críticas que se deben tomar en cuenta al momento de atreverse a crear un lenguaje de programación: su léxico, su sintaxis y su semántica.

El objetivo de esta documentación es el de detallar las especificaciones del lenguaje de forma rápida y resumida. Al final de esta documentación estaremos dejando la gramática completa y algunos canvas que hemos utilizado para planificar la implementación del intérprete de este lenguaje de programación. Esperamos abarcar todas, o al menos gran parte de, las características de Ceylon en este documento.

# 2. Pinceladas sobre Ceylon
Como hemos mencionado en el punto anterior, Ceylon es un lenguaje de programación interpretado que sigue el paradigma de la programación estructurada. De forma más técnica, detallamos a continuación otras características técnicas de este lenguaje:

- **Tipado dinámico y fuerte:** En Ceylon, el tipo de una variable o constante se define en tiempo de ejecución. Además, las variables pueden cambiar de tipo durante la ejecución del programa, mientras que las constantes mantienen su tipo original. Ceylon es de tipado fuerte ya que el lenguaje no admite operaciones entre entidades de diferente tipo.
- **Ámbito léxico:** El alcance de las variables en Ceylon se basa en la estructura del código. Una variable declarada dentro de un bloque solo es accesible dentro de ese bloque y en los sub bloques dentro de él. Esto ayuda a mantener el código organizado y evita efectos inesperados en otras partes del programa.

# 3. Tipos de variable
Ceylon cuenta con dos tipos de clasificación en sus variables. La primera clasificación es según su mutabilidad:

- **Variable**: Los identificadores que son definidos como variables tiene que ser inicializadas al mismo tiempo que declaradas. Las variables, una vez declaradas, no pueden convertirse en finales.

```python
variable = 10;
```

- **Final**: Los identificadores que son definidos como finales no pueden cambiar su valor en tiempo de ejecución y deben ser inicializadas obligatoriamente.

```java
final CONSTANT = 10;
```

En el siguiente apartado, definiremos la segunda categoría de variables.

# 4. Tipos de datos
La segunda forma de clasificar a las variables de Ceylon es por su tipo de datos. Ceylon cuenta con 4 tipos de datos:

- **Number**: Este tipo de dato se usa para representar números enteros y reales. Se suelen utilizar para realizar las operaciones aritméticas disponibles en el lenguaje.

```python
x = 5;
x = 5.5;
```

- **String**: Los strings representar cadenas de texto. Tienen una operación especial de concatenación con el operador `...` para unir dos o más cadenas.

```python
x = "Hola Mundo";
```

- **Boolean**: Los valores booleanos se utilizan para representar verdades o falsedades dentro de un programa de Ceylon. Se suelen utilizar para realizar operaciones booleanas disponibles en el lenguaje.

```java
x = true;
```

- **Null**: Se utiliza para indicar la ausencia de algún valor válido.

```java
x = null;
```
  
