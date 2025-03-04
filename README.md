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

- **Null**: Se utiliza para indicar la ausencia de algún valor válido

```java
x = null;
```

# 5. Casting
Ceylon proporciona dos funciones principales para realizar casting (conversiones) entre strings y números:

- **tonum()**: Esta función convierte strings a números. Si el string contiene un número válido, lo convierte; de lo contrario, genera un error.

```python
x = tonum("5.5");    // x = 5.5
x = tonum("123");    // x = 123
x = tonum("hola");   // Error: No se puede convertir
```

- **tostr()**: Esta función convierte números a strings. Es útil para mostrar valores numéricos como texto.

```python
x = tostr(5.5);      // x = "5.5"
x = tostr(123);      // x = "123"
```

Estas funciones son fundamentales para manejar conversiones entre números y strings en Ceylon.

# 6. Estructuras de control
Ceylon, al ser un lenguaje estructurado, cuenta con un número considerable de estructuras de control.

## Estructuras condicionales:

- `if/elif/else`: Con el bloque condicional `if` se pueden evaluar sentencias booleanas para ejecutar condicionalmente bloques de código. Para evitar el anidamiento excesivo, hemos implementando también `elif` que se utiliza para establecer un condición sucesiva de no haberse cumplido la anterior. Y, por último, se utiliza `else` en caso de que ninguna condición se haya validado como verdadera:

```python
x = 10;
if (x == 5) {
	print("x es 5");
} elif (x == 15) {
	print("x es 15");
} else {
	print("x no es 15 ni 5");
}
```

- `switch`: Similar al bloque `if/elif/else` pero de uso más compacto y práctico. `switch` evalúa igualdades entre la variable proporcionada y las expresiones `cases` establecidos para ejecutar un bloque de código de manera selectiva. `default` esta disponible y es el equivalente a `else` en el sentido de que ejecuta el bloque si ningún caso anterior se ha ejecutado.

```jsx
x = 10
switch (x) {
	case 5 {
		print("x es 5");
	}
	case 10 {
		print("x es 10");
	}
	default {
		print("x no es 15 ni 5");
	}
}
```

## Estructuras de bucle

- `while`: La estructura de bucle `while` ejecuta el mismo bloque de código especificado mientras una condición no sea verdadera

```python
x = 0;

while (x < 10) {
	print("hola mundo");
	x++;
}
```

- `for`: La estructura de bucle `for` ejecuta un bloque de código de forma repetitiva hasta que se cumpla una condición dada. Adicionalmente permite definir e inicializar una variable y también una operación de incremento o decremento sobre cualquier variable al finalizar una iteración

```jsx
for (x = 0; x < 10; x++) {
	print("hola mundo");
}
```

# 7. Funciones
Además, Ceylon permite la reutilización de código mediante el uso de funciones.

## Funciones:

- `fn`**:** Las funciones se definen utilizando la palabra clave `fn`, permitiendo reutilizar bloques de código. Se pueden definir con o sin parámetros y pueden devolver valores utilizando `return`.

 

Función simple sin parámetros

```python
fn saludar() {
    print("¡Hola, mundo!");
}

saludar();
```

Función con parámetros y retorno de valor:

```python
fn sumar(a, b) {
    return a + b;
}

sumar(14, 6);
```

# 8. Alcance
Ceylon define el alcance de las variables y funciones a través de ámbitos (*scopes*), lo que determina dónde pueden ser accedidas dentro del código. Existen diferentes niveles de ámbito según dónde se declaren las variables o funciones.

## Ámbito Global:

- Una variable o función declarada fuera de cualquier bloque pertenece al ámbito global y puede ser utilizada en cualquier parte del código.

```python
mensaje = "Hola desde el ámbito global";

fn saludar() {
    print(mensaje);
}
```

## Ámbito de Bloque:

- Las variables declaradas dentro de un bloque solo existen dentro de ese bloque y no pueden ser accedidas desde fuera.

```python
fn ejemplo() {
    interno = "Esta variable solo existe dentro de la función";
    print(interno);
}

print(interno);
```

(Esto daría error)

## Sombra de variables (*Shadowing*):

- Si una variable global tiene el mismo nombre que un parámetro de una función, dentro de la función se tomará el valor del parámetro en lugar del valor global.

```python
mensaje = "Hola desde el ámbito global";

fn mostrarMensaje(mensaje) {
    print(mensaje);
}

mostrarMensaje("Hola desde la función");
print(mensaje);
```

# 9. I/O
Ceylon proporciona funcionalidades para manejar entrada y salida (I/O) que permiten a los programas interactuar con el usuario y archivos. Veamos las principales operaciones de I/O disponibles.

## Salida Estándar:

- `print()`: La función `print()` muestra texto en la consola. Se permite la concatenación.

```python
print("¡Hola mundo!");

nombre = "Ana";
edad = 25;
print("Mi nombre es " ... nombre ... " y tengo " ... edad ... " años.");

print("Línea 1");
print("Línea 2");
```

## Entrada Estándar:

- `scan()`: Ceylon permite leer una cadena de texto desde la consola

```python
print("Ingrese su nombre: ");
scan(nombre);
print("Hola " ... nombre);
```
  
