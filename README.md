# Analizador Y Evaluador De Diseño Modular De Aplicaciones 

# Grupo Viborita

## main.py

### Descripción
Se trata del módulo principal, en el se ejecuta el menu de interaccion que será utilizado por el usuario para acceder a la informacion que desee de la aplicación que se esta 
analizando.

### Funciones
#### main() 

*Autor: Andrés Kübler*

Es la funcion principal del modulo, llama a la funcion *crear_csv_finales("programas.txt")* que crea los archivos fuente_unico.csv y comentarios.csv, luego llama a la funcion 
*obtener_datos_csv(fuente, comentarios)*. Una vez que ya se tienen los datos, se llama a la funcion *menu_interaccion()* que valga la redundancia, ejecuta el menu de interacción.

#### obtener_datos_csv(*fuente, comentarios*)

*Autor: Ivan Litteri*

Abre los archivos fuente_unico.csv y comentarios.csv (nombres que le llegan por parámetro, en este caso el parámetro ```fuente``` corresponde a fuente_unico.csv y el parametro 
```comentarios``` corresponde a comentarios.csv), luego con los datos obtiene dos diccionarios, uno ordenado por funciones y otro ordenado por autores.
(se explicaran mas adelante) y los devuelve.

#### mostrar_menu_interaccion()

*Autor: Ivan Litteri*

Muestra en pantalla el título de la aplicacion y las opciones que tiene para elegir el usuario.

#### mostrar_ayuda_menu(*opcion*)

*Autor: Ivan Litteri*

Muestra en pantalla una breve descripcion de lo que se trata cada opción del menú.

#### menu_interaccion(*datos_por_funciones, datos_por_autores*)

*Autor: Andrés Kübler*

Muestra en pantalla el menu llamando a la funcion *mostrar_menu_interaccion()*, luego se queda en espera al ingreso del usuario, en donde éste tiene entre 6 opciones para elegir
entre ellas se encuentran:

1. Panel General de Funciones
2. Consultar Funciones
3. Analizar Reutilizacion de Codigo
4. Arbol de Invocaciones
5. Informacion de Desarrollador
6. Ayuda

Las primeras 5 se tratan de la obtención de la información correspondiente a cada punto del trabajo práctico, y la sexta opción es la que muestra en pantalla las instrucciones
de uso del menú. Internamente llama a la función *mostrar_ayuda_menu()*.

El usuario debe ingresar por teclado una de las opciones en pantalla, en caso de que ingrese una opción no disponible, se le informa y pregunta denuevo. Cada opción llama a su
función correspondiente.

```datos_por_funcion``` y ```datos_por_autor``` corresponden a los datos obtenidos anteriormente con la funcion *obtener_datos_csv(fuente, comentarios)*

Para salir del menú de opciones se debe presionar ENTER.


## m_crear_csv_finales.py

### Descripción
Obtiene informacion del archivo "programas.txt" que usa para crear un archivo csv individual para cada una de las ubicaciones, hace un merge de esos archivos y luego los borra.

### Funciones

#### crear_csv_finales(*nombre_archivo*)

*Autor: Ivan Litteri*

Ejecuta en orden funciones para crear los archivos csv finales. Primero consigue la información de las ubicaciones de los códigos que se encuentran en el archivo de programas.txt
llamando a la funcion *informacion_ubicaciones(nombre_archivos)* del módulo *m_obtener.py* a la que le pasa el parámetro ```nombre_archivo``` que en este caso se trata de
el archivo "programas.txt".

La información de las ubicaciones se la pasa a otra función que llama, *crear_csv_individuales(info_ubicaciones)* del módulo *m_csv_individuales.py* que ademas de crear los
archivos fuente y comentarios csv para cada una de las ubicaciones halladas devuelve una lista con los nombres de esos archivos csv creados que los usa luego cuando llama a la
función *merge(nombre_archivo_final, archivos_individuales, lineas_fuera_funcion)*.

Luego de hacer el merge para cada uno de los archivos csv finales borra los archivos csv individuales provisorios antes creados con la funcion 
*borrar_csv_individuales(nombres_archivos_csv_individuales)*.

#### borrar_csv_individuales(*nombres_archivos_csv_individuales*)

*Autor: Ivan Litteri*

Borra los archivos fuente y comentarios csv individuales (que se encuentran en el repositorio actual) cuyas ubicaciones se obtienen de una lista que devuelve la funcion 
*ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales)* a la que le llega por parametro ```nombres_archivos_csv_individuales``` que corresponde a una lista
con los nombres de los archivos csv individuales (tanto fuente como comentarios).

#### merge(*nombre_archivo_final, archivos_individuales, lineas_fuera_funcion*)

*Autor: Luciano Federico Aguilera*

```nombre_archivo_final``` es el nombre del archivo csv final que se quiere crear, ```archivos_individuales``` es una lista con los nombres de los archivos individuales a
abrir, ```lineas_fuera_funcion``` es una lista con las lineas que estan afuera de funciones.

Abre los archivos "n" individuales y el archivo final, graba en forma ordenada las lineas de los individuales en el archivo final y cierra todos los archivos abiertos

#### abrir_csv_individuales(*archivos*)

*Autor: Ivan Litteri*

```archivos``` es una lista con los archivos que se tienen que abrir

Se guardan los datos a leer de los archivos individuales en un diccionario ya que la unica forma que encontramos de guardar variables dinámicas fue de esta forma, entonces 
se pueden tener abiertos "n" archivos. Y devuelve un diccionario con el contenido de cada módulo como value de la key (que seria el módulo). Ya que el open devuelve un
objeto de un tipo especial al que luego se le pueden aplicar métodos como *readline()*, etc., guardamos esos objetos como values en un diccionario.

Devuelve ```diccionario_archivos_abiertos``` que es un diccionario que contiene el contenido de todos los archivos csv individuales involucrados.

#### grabar_csv_final_ordenado(*archivo_final, archivos_individuales, lineas_fuera_funcion*)

*Autor: Luciano Federico Aguilera*

```archivo_final``` es el nombre del archivo csv final que se quiere grabar, ```archivos_individuales``` es el diccionario que tiene el contenido de todos los archivos csv
individuales, ```lineas_fuera_funcion``` es la lista que contiene las lineas de codigo que estan fuera de funciones.

Lee las lineas de los archivos individuales, las compara, y graba de forma ordenada alfabeticamente por funcion el archivo final.

Primero obtiene una lista de lineas de todos los archivos individuales de la función *leer_csv_individuales(archivos_individuales)*, se obtiene la menor de ellas, luego
se recorre la lista y se encuentra la menor, cuando ocurre esto se graba esa linea en el ```archivo_final``` y se elimina de la lista esa linea, y asi sucesivamente
con cada linea hasta que ya no hay mas en la lista.

#### leer_csv_individuales(*datos*)

*Autor: Luciano Federico Aguilera*

```datos``` es el diccionario que tiene el contenido de los archivos individuales.

Lee secuencialmente cada archivo y almacena las lineas leidas en una lista. Recorriendo key por key el diccionario y leyendo linea por linea
hasta que no hay mas lineas por leer en cada archivo.

Devuelve ```lineas``` que es la lista de todas las lineas de todos los archivos csv individuales.

#### cerrar_csv_individuales(*datos*)

*Autor: Ivan Litteri*

```datos``` es el diccionario que tiene el contenido de los archivos individuales.

Cierra cada uno de los archivos individuales.


## Grafo de llamada de funciones
<img src="./grafo.svg">
