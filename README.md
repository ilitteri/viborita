# Analizador Y Evaluador De Diseño Modular De Aplicaciones 

# Grupo Viborita

## Índice de Módulos
|  |  |  |
| --- | --- | --- |
| [main.py](#main)  | [m_panel_general_funciones.py](#Panel-General-de-Funciones)  | [m_consulta_funciones.py](#Consulta-de-Funciones)  |
| [m_analizador_reutilizacion_codigo.py](#Analizador-de-Reutilización-de-Código)  | [m_arbol_invocaciones.py](#Árbol-de-Invocaciones)  | [m_informacion_desarrollador.py](#Información-por-Desarrollador)  |
| [m_organizar_datos.py](#Organizar-Datos)  | [m_obtener.py](#Obtener)  | [m_grafo.py](#Grafo)  |
| [m_csv_finales.py](#Crear-CSV-Finales)  | [m_csv_individuales.py](#Crear-CSV-Individuales)  | [m_analizar_linea.py](#Analizar-Línea)  |

## [main](./main.py)

[*Indice*](#Índice-de-Módulos)

### Descripción
Se trata del módulo principal, en el se ejecuta el menu de interaccion que será utilizado por el usuario para acceder a la informacion que desee de la aplicación que se esta 
analizando.

### Funciones

#### main() 

*Autor: Andrés Kübler*

Es la funcion principal del modulo, llama a la funcion *crear_csv_finales(nombre_archivo)*  del módulo [*m_crear_csv_finales.py*](#Crear-CSV-Finales) que crea los archivos 
fuente_unico.csv y comentarios.csv, luego llama a la funcion 
*obtener_datos_csv(fuente, comentarios)*. Una vez que ya se tienen los datos, se llama a la funcion *menu_interaccion()* que valga la redundancia, ejecuta el menu de 
interacción.

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

1. [Panel General de Funciones](#Panel-General-de-Funciones)
2. [Consulta de Funciones](#Consulta-de-Funciones)
3. [Analizar Reutilizacion de Código](#Analizador-de-Reutilización-de-Código)
4. [Árbol de Invocaciones](#Árbol-de-Invocaciones)
5. [Información por Desarrollador](#Información-por-Desarrollador)
6. Ayuda

Las primeras 5 se tratan de la obtención de la información correspondiente a cada punto del trabajo práctico, y la sexta opción es la que muestra en pantalla las instrucciones
de uso del menú. Internamente llama a la función *mostrar_ayuda_menu()*.

El usuario debe ingresar por teclado una de las opciones en pantalla, en caso de que ingrese una opción no disponible, se le informa y pregunta denuevo. Cada opción llama a su
función correspondiente.

```datos_por_funcion``` y ```datos_por_autor``` corresponden a los datos obtenidos anteriormente con la funcion *obtener_datos_csv(fuente, comentarios)*

Para salir del menú de opciones se debe presionar ENTER.


## [Crear CSV Finales](./m_csv_finales.py)

[*Indice*](#Índice-de-Módulos)

### Descripción
Obtiene informacion del archivo "programas.txt" que usa para crear un archivo csv individual para cada una de las ubicaciones, hace un merge de esos archivos y luego los borra.

### Funciones

#### crear_csv_finales(*nombre_archivo*)

*Autor: Ivan Litteri*

Ejecuta en orden funciones para crear los archivos csv finales. Primero consigue la información de las ubicaciones de los códigos que se encuentran en el archivo de 
programas.txt llamando a la funcion *informacion_ubicaciones(nombre_archivos)* del módulo [*m_obtener.py*](#Obtener) a la que le pasa el parámetro ```nombre_archivo``` que en 
este caso se trata de el archivo "programas.txt".

La información de las ubicaciones se la pasa a otra función que llama, *crear_csv_individuales(info_ubicaciones)* del módulo [*m_csv_individuales.py*](#Crear-CSV-Individuales) 
que ademas de crear los archivos fuente y comentarios csv para cada una de las ubicaciones halladas devuelve una lista con los nombres de esos archivos csv creados que los usa 
luego cuando llama a la función *merge(nombre_archivo_final, archivos_individuales, lineas_fuera_funcion)*.

Luego de hacer el merge para cada uno de los archivos csv finales borra los archivos csv individuales provisorios antes creados con la funcion 
*borrar_csv_individuales(nombres_archivos_csv_individuales)*.

#### borrar_csv_individuales(*nombres_archivos_csv_individuales*)

*Autor: Ivan Litteri*

Borra los archivos fuente y comentarios csv individuales (que se encuentran en el repositorio actual) cuyas ubicaciones se obtienen de una lista que devuelve la funcion 
*ubicaciones_archivos_csv_individuales(nombres_archivos_csv_individuales)* del módulo [*m_obtener.py*](#Obtener) a la que le llega por parametro 
```nombres_archivos_csv_individuales``` que corresponde a una lista con los nombres de los archivos csv individuales (tanto fuente como comentarios).

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

## [Organizar Datos](./m_organizar_datos.py)

[*Indice*](#Índice-de-Módulos)

### Descripción

Lee los archivos fuente_unico.csv y comentarios.csv secuencialmente, los procesa y con los datos extraidos de cada una de las lineas lo guarda en un diccionario.

### Funciones

#### leer_archivos_csv(*archivo_fuente, archivo_comentarios*)

*Autor: Ivan Litteri*

```archivo_fuente``` es el contenido del archivo fuente_unico.csv a leer

```archivo_comentarios``` es el contenido del archivo comentarios.csv a leer

Recibe los contenidos de los archivos csv finales, y devuelve dos diccionarios, uno ordenado por funciones y otro ordenado por autores. Primero carga la primera linea de ambos 
archivos, y mientras haya lineas para leer de los archivos, formatea la linea, y envia los datos extraidos a dos funciones distintas, una 
*actualizar_diccionario_funciones(datos_por_funciones, nombre_funcion, parametros_funcion, modulo_funcion, lineas_funcion, autor_funcion, ayuda_funcion, otros_c, indice_copia)* 
y *actualizar_diccionario_autores(datos_por_autores, nombre_funcion, lineas_funcion, autor_funcion, indice_copia)* que va actualizando los diccionarios linea a linea. Luego una 
vez que termina el recorrido, llama a la funcion *cantidad_invocaciones(datos_por_funciones, archivo_fuente)* del módulo [*m_obtener.py*](#Obtener) que le agrega las 
invocaciones. La información de la linea podia ser extraida en cada una de las funciones que actualiza el diciconario pero, para no hacer el doble de recorridos sacrificamos 
tener pocos parametros para hacer la mitad de recorridos.

#### actualizar_diccionario_funciones(*datos_por_funciones, nombre_funcion, parametros_funcion, modulo_funcion, lineas_funcion, autor_funcion, ayuda_funcion, otros_c, indice_copia*)

*Autor: Ivan Litteri*

```datos_por_funciones``` es el diccionario por funciones a actualizar, 

```nombre_funcion``` es el primer campo de la linea leida en el csv, 

```parametros_funcion``` es el segundo campo de la linea leida en el csv, 

```lineas_funcion``` es la lista de lineas que corresponde a todos los campos de la linea desde el cuarto hasta el ultimo en caso de que haya, 

```autor_funcion``` es el segundo campo de la linea de comentarios.csv y corresponde al autor de la función, 

```otros_c``` es una lista con los comentarios que no corresponden a ayuda de función y autor  de función, 

```indice_copia``` es un indice que se incrementa si existen funciones con nomrbes repetidos, entonces se agrega "_indice_" a esa función repetida.

Actualiza y da formato al diccionario ordenado por funciones, cada key del diccionario es una funcion, el value de cada key es otro diccionario con todos los datos relativos a 
esa funcion, entre ellos, "_parametros_" cuyo value es un string; "_modulo_" al que pertenece, cuyo value es un string; "_lineas_" de esa funcion, cuya value es una lista de 
lineas; "_invocaciones_", cuyo value es una lista con las invocaciones que realiza esa funcion; "_cantidad de lineas_" cuyo value es un entero, "_cantidad de invocaciones_", 
cuyo value es un entero y corresponde a la cantidad de veces que es invocada esa función; "_comentarios_" que su value es otro diccionario que contiene 3 keys: "_ayuda_" que 
contiene la ayuda de la función en caso de tenerla, sino contiene None; "_autor_" que contiene al autor de la función en caso de haberlo, sino contiene None; y "_otros_" que 
contiene una lista de comentarios extra en caso de haberlos; y "_cantidad declaraciones_" es la ultima key del diccionario que contiene cada función cuyo value corresponde a 
otro diccionario que contiene las cantidades de declaraciones de esa funcion (que corresponden al punto 1), las cuales son obtenidas por la función 
*cantidad_declaraciones(datos_por_funciones, lineas_funcion, nombre_funcion)* del módulo [*m_obtener.py*](#Obtener).

```
diccionario = {"funcion_1": {"parametros": (str),
                             "modulo": (str),
                             "lineas": (lista),
                             "invocaciones": (lista),
                             "cantidad_lineas": (int),
                             "cantidad_invocaciones": (int),
                             "comentarios": {"ayuda": (str),
                                             "autor": (str),
                                             "otros": (str)
					     }
                             "cantidad_decalraciones": {"returns": (int)
                                                        "if/elif": (int)
                                                        "for": (int)
                                                        "while": (int)
                                                        "break": (int)
                                                        "exit": (int)
                                                        "coment": (int),
							},
                                                       
             "funcion_2": {...},
             "funcion_n": {...}
	      }
```

#### actualizar_diccionario_autores(*datos_por_autores, nombre_funcion, lineas_funcion, autor_funcion, indice_copia*)

*Autor: Ivan Litteri*

```datos_por_autores``` es el diccionario por autores a actualizar, 

```nombre_funcion``` es el primer campo de la linea leida en el csv,

```lineas_funcion``` es la lista de lineas que corresponde a todos los campos de la linea desde el cuarto hasta el ultimo en caso de que haya, 

```autor_funcion``` es el segundo campo de la linea de comentarios.csv y corresponde al autor de la función,

```indice_copia``` es un indice que se incrementa si existen funciones con nomrbes repetidos, entonces se agrega "_indice_" a esa función repetida.

Actualiza y da formato al diccionario ordenado por autores, cada key del diccionario es un autor, y el value de esa key es un diccionario que contiene dos keys, "_funcion_" y 
"_lineas totales_", en donde el primero corresponde a la cantidad de lineas que tiene esa funcion, y el segundo incrementa en cada pasada las lineas de todas las funciones. 
Entonces el diccionario queda con la forma:

```
diccionario = {"autor_1": {"funciones": {"funcion_1": (int),
                                         "funcion_2": (int),
                                         "funcion_n": (int),
                                        },
                            "lineas_totales": (int)
                                                
             "autor_2": {...},
             "autor_n": {...}
	      }
```

## [Panel General de Funciones](./m_panel_general_funciones.py)

[*Indice*](#Índice-de-Módulos)

### Descripción 

...

### Funciones

#### mostrar_panel_general(lista_de_listas, longitud)

*Autor: Santiago Vaccarelli*

```lista_de_listas```  es una lista de listas creada a partir del diccionario con los datos de las funciones con un formato conveniente para realizar el punto.

```longitud``` es una lista con los valores de las longitudes maximas de cada columna de la tabla.

#### grabar_panel_control_csv(archivo, lineas)

*Autor: Santiago Vaccarelli*

```archivo``` es el archivo csv que se va a grabar.

```lineas``` es una lista de lineas a ser grabadas en el archivo csv.

#### crear_panel_general_csv(lista_de_listas)

*Autor: Santiago Vaccarelli*

```lista_de_listas```  es una lista de listas creada a partir del diccionario con los datos de las funciones con un formato conveniente para realizar el punto.

#### generar_tabla_panel_general(diccionario)

*Autor: Santiago Vaccarelli*

```diccionario``` es un diccionario con los datos necesarios de las funciones.


#### obtener_panel_general(datos_archivos_csv)

*Autor: Santiago Vaccarelli*

```datos_archivos_csv``` 

## [Consulta de Funciones](./m_consulta_funciones.py)

[*Indice*](#Índice-de-Módulos)

### Descripción

Lee el diccionario de datos por funcion, ordena las funciones por orden alfabético, imprime la tabla con las funciones de la aplicación, y se queda esperando a que el usuario 
interactue, y muestra o imprime la informacion solicitada por éste.

### Funciones

#### consultar_funciones(datos_csv)

*Autor: Joel Glauber*

```datos_csv``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

Guarda en la variable "_lista de funciones_" la lista ordenada alfabéticamente de los nombres de las funciones de la aplicación, para enviarla por parámetro a la funcion 
*tabla_funciones* del módulo [*m_obtener.py*](#Obtener) que devuelve dos cadenas, una que corresponde a la tabla a mostrar y otra que corresponde a la cantidad de guiones, 
cadenas que se envían como parámetro a la función *mostrar_tabla_funciones(tabla, cantidad_guiones)*, luego llama a la función *mostrar_instrucciones_uso()* y la función 
*analizar_ingreso_usuario(datos_csv)*

#### mostrar_instrucciones_uso()

*Autor: Ivan Litteri*

Imprime las instrucciones de uso del módulo

#### mostrar_tabla_funciones(*tabla, cantidad_guiones*)

*Autor: Joel Glauber*

```tabla``` es un string que contiene la tabla formateada

```cantidad_guiones``` es un string que contiene guiones.

Muestra en pantalla la tabla de funciones que conforman a la aplicación.

#### solicitar_ingreso_usuario(*datos_csv*)

*Autor: Joel Glauber*

```datos_csv``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

Solicita el ingreso de una cadena, que tiene que ver con las opciones que se le mostraron previamente en pantalla, opción que luego es analizada por al función 
*analizar_opcion(datos_csv, opcion)*.

#### analizar_opcion(*datos_csv, opcion*)

*Autor: Joel Glauber*

```datos_csv``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

```opcion``` es la cadena que corresponde a la opcion ingresada por el usuario.

Analiza la opción con distintas interrogaciones, si el primer caracter de la opcion corresponde a un "_#_" y ademas no es el único caracter que compone a la cadena, entonces se 
deriva a la función *opcion_numeral(datos_csv, opcion)*; si el primer caracter de la opción corresponde a un "_?_" y además no es el único caracter que compone la cadena, 
entonces se deriva a la función *opcion_pregunta(datos_csv, opcion)*; si la opción es igual a "_imprimir ?todo_" se deriva a la función *crear_ayuda_txt(datos_csv, opcion)* 
donde continúa su análisis; si la opción es igual a "_imprimir #todo_" se deriva a la función *crear_ayuda_txt(datos_csv, opcion)* donde continúa su análisis; y si la función 
pasa estas interrogaciones entonces le informa al usuario que la opción que ingreso es incorrecta y le pregunta denuevo.

#### opcion_numeral(*datos_csv, opcion*)

*Autor: Joel Glauber*

```datos_csv``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

```opcion``` es la cadena que corresponde a la opcion ingresada por el usuario.

Analiza la opción con distintas interrogaciones, si la opción es igual a "_#todo_" entonces deriva a la función *mostrar_datos_funcion(datos_csv, funcion, opcion)* y le pasa con 
un iterador todas las funciones que se encuentran en la tabla; si el contenido de la opcion desde el numeral hasta que termina (matematicamente (#; +oo) seria el numeral sin 
incluir) corresponde a una de las funciones existentes en la tabla, entonces deriva a la función *mostrar_datos_funcion(datos_csv, funcion, opcion)*; si pasa estas 
interrogaciones entonces le informa al usuario que la opción que ingreso es incorrecta y le pregunta denuevo.

#### opcion_pregunta(*datos_csv, opcion*)

*Autor: Joel Glauber*

```datos_csv``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

```opcion``` es la cadena que corresponde a la opcion ingresada por el usuario.

Analiza la opción con distintas interrogaciones, si la opción es igual a "_?todo_" entonces deriva a la función *mostrar_datos_funcion(datos_csv, funcion, opcion)* y le pasa con 
un iterador todas las funciones que se encuentran en la tabla; si el contenido de la opcion desde el numeral hasta que termina (matematicamente (?; +oo) seria el signo de 
pregunta sin incluir) corresponde a una de las funciones existentes en la tabla, entonces deriva a la función *mostrar_datos_funcion(datos_csv, funcion, opcion)*; si pasa estas 
interrogaciones entonces le informa al usuario que la opción que ingreso es incorrecta y le pregunta denuevo.

#### mostrar_datos_funcion(*datos_csv, funcion, opcion*)

*Autor: Joel Glauber*

```datos_csv``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

```funcion``` es la función que está en la tabla de funciones.

```opcion``` es la cadena que corresponde a la opción ingresada por el usuario.

Analiza si la opción contiene un "_#_" o un "_?_" (a esta instancia llega una opción valida), para el primer caso invoca a la función *formatear_datos_numeral(datos_csv, 
funcion)* y se muestra en pantalla lo obtenido (que corresponde a los datos solicitados ya formateados); para el segundo caso también invoca a la función 
*formatear_datos_pregunta(datos_csv, funcion)* y se muestra en pantalla lo obtenido (que corresponde a los datos solicitados ya formateados).

#### crear_ayuda_txt(*datos_csv, opcion*)

*Autor: Joel Glauber*

```datos_csv``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

```opcion``` es la cadena que corresponde a la opcion ingresada por el usuario.

Crea y graba archivo_ayuda.txt invocando a la función *grabar_ayuda_txt(archivo_ayuda, datos_csv, funcion, opcion)* a la que le pasa todas las funciones ya que si se llego a 
esta función es porque se ingreso una de las dos opciones que solicitan la creación de este archivo de ayuda y se pide grabar sobre todas las funciones.

#### grabar_ayuda_txt(*archivo_ayuda, datos_csv, funcion, opcion*)

*Autor: Joel Glauber*

```archivo_ayuda``` es el contenido del archivo de ayuda creado, se necesita para grabar.

```datos_csv``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

```funcion``` es la función que está en la tabla de funciones.

```opcion``` es la cadena que corresponde a la opcion ingresada por el usuario.

Analiza si la opción contiene un "_#_" o un "_?_" (a esta instancia llega una opción valida), para el primer caso invoca a la función *formatear_datos_numeral(datos_csv, 
funcion)* y se graba en el archivo_ayuda lo obtenido (que corresponde a los datos solicitados ya formateados); para el segundo caso también invoca a la función 
*formatear_datos_pregunta(datos_csv, funcion)* y se graba en el archivo_ayuda lo obtenido (que corresponde a los datos solicitados ya formateados).

#### formatear_datos_pregunta(*datos_csv, funcion*)

*Autor: Joel Glauber*

```datos_csv``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

```funcion``` es la función que está en la tabla de funciones.

Devuelve una cadena formateada con la información que se pide de la funcion que se solicita.

#### formatear_datos_numeral(*datos_csv, funcion*)

*Autor: Joel Glauber*

```datos_csv``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

```funcion``` es la función que está en la tabla de funciones.

Devuelve una cadena formateada con la información que se pide de la funcion que se solicita.

## [Analizador de Reutilización de Código](./m_analizador_reutilizacion_codigo.py)

[*Indice*](#Índice-de-Módulos)

### Descripción

Este modulo grafica la reutilizacion de  los modulos de una aplicacion y crea un archivo de tipo .txt ```analizador.txt```,
en el puede observarse la cantidad de invocaciones que tienen las distintas funciones y si son invocadas se ve una "X" que representa esto
al final del archivo se observa los totales de invocaciones para todas las funciones.

Recive un diccionario ```datos_por_funciones``` creado en el modulo [m_organizar_datos.py](#Organizar-datos)

Devuelve un archivo llamado ```analizador.txt``` que contiene a la tabla de reutilizacion e imprime por ```consola``` la misma tabla
                                                 
### Funciones

#### buscar_invocaciones(*datos_por_funciones*)

*Autor : Luciano Federico Aguilera*

Esta funcion crea una tupla a partir de las ```funcion_n (str) ```y las ```invocaciones (list)``` del diccionario ```datos_por_funcion(dict)``` de [m_organizar_datos.py]
(#Organizar-datos)  , crea un diccionario donde organizar los datos para la tabla de reutilizacion y le agrega como ```keys``` del mismo en un contador que funcionara 
posteriormente como indices de la tabla y le asigna a cada funcion en ```tupla_funciones``` un indice , en el diccionario tambien se agregan tres ```keys``` mas 
```"total"```(que contiene un diccionario con los indices como keys y sus totales) ,```"indices"```(que contiene un diccionario que tiene como keys las funciones contenidas en 
la tupla y contienen a su respectivo indice) y ```"nombres"```(que contiene los indices como keys que contienen a sus respectivas funciones  ) estas ultimas dos keys tienen la 
finalidad de ahorrar lineas y hacer mas entendible el codigo, tambien guarda la funcion que tenga mayor cantidad de caracteres para utilizarlo en ```creacion_formato_tabla```
retorna ( *diccionario_invocaciones , tupla_funciones , largo_maximo* )

#### contar_interacciones(*diccionario_invocaciones , tupla_funciones , datos_por_funciones*)

*Autor : Luciano Federico Aguilera*

Esta funcion cuenta las veces que fue utilizada una funcion dentro de cada funcion listada en la tupla y agrega los totales de cada indice a la key totales del diccionario para 
esto utiliza ```datos_por_funciones``` y ```tupla_funciones```  creados en ```buscar_invocaciones``` .
retorna ( *diccionario_invocaciones , tupla_funciones , largo_maximo* )

#### creacion_formato_tabla(*diccionerio_invocaciones, largo_maximo*)

*Autor : Luciano Federico Aguilera*

Esta funcion crea una lista que contendra las cadenas de texto correspondientes a cada linea del *analizador.txt* o bien que seran impresas por pantalla y agrega los indices 
junto con sus correspondientes funciones a cada linea la funcion toma en cuenta la funcion con mayor cantidad de caracteres para evitar errores de superposicion en la tabla.
retorna (```diccionario_invocaciones```)

#### asignacion_valores_tabla(*filas_txt, diccionario_invocaciones*)

*Autor : Luciano Federico Aguilera*

Esta funcion concatena a su correspondiente linea segun corresponda un numero(si la funcion en la columna es invocada por la funcion de la fila) ,una "X"(si la funcion de la 
fila es invocada por la funcion en la columna) o un espacio vacio (si la funcione en la fila y la columna no interactuan) 
retorna ( filas_txt )

#### creacion_archivo_txt(*filas_txt*)

*Autor : Luciano Federico Aguilera*

Esta funcion crea el ```analizador.txt``` y graba en el linea por linea los elementos de ```filas_txt``` generada en ```buscar_invocaciones```
a la vez que imprime por ```consola``` las mismas lineas.

#### analizar_reutilizacion(*datos_por_funcion*)

*Autor : Luciano Federico Aguilera*

Esta funciones es la principal y llama a todas las sub_funciones anteriores , esta funcion es la que sera llamada en *main.py* 

## [Árbol de Invocaciones](./m_arbol_invocacion.py)

[*Indice*](#Índice-de-Módulos)

### Descripción

Es el punto número 4 del Trabajo Práctico, consta en la imresión por pantalla de un árbol de invocaciones de las funciones y su respectiva cantidad de lineas.

### Funciones

#### grafica_arbol_invocaciones(*diccionario_infrmacion, funcion = None, string = ""*)

```diccionario_informacion``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

```funcion``` es la función que se debe analizar, la primera vez de la recursión es None

```string``` es la separación que se le da en la impresión (se va acumulando por recursión)

Esta función arma el árbol de invocaciones de forma recursiva, lo cual significa que se llama a ella misma a medida que se va recorriendo la información del diccionario pasada 
por parámetro. Como parametro recibe un diccionario con la información de las funciones del programa; una funcion (que de no existir vale Noone); y un string que puede estar 
compuesto por información de otras funciones o ser simplemente una separación de espacios. Primero arma un string con el nombre y cantidad de lineas de la función pasada por 
parametro, de no existir tal función llama a encontrar_main_archivo() para encontrar la función principal del programa y así comenzar el arbol. Luego comprueba si la  función 
analizada tiene invocaciones. De no tener imprime el string armado previamente, sino recorre las invocaciones y las analiza:

1) Si la invocación es la misma que la función analizada, simplemente imprime su respectivo string, para que la función no entre en un loop infinito
2) Si la invocación es la primera de todas las invocaciones, la función se llama a si misma pasando como parámetro: (diccionario_infrmacion,invocación,string)
3) Si la invocación no es la primera, la función se llama a si misma pasando como parámetro: (diccionario,invocación,un string de espacios de la longitud del string)

#### encontrar_main_archivo(*diccionario_infrmacion, funcion_main_dicc = None*)

Esta función busca la funcion principal del programa en el diccionario pasado por parámetro. Su busqueda
es a traves de un ciclo con condición de corte. Finalmente devuelve la función principal como string

## [Información por Desarrollador](./m_informacion_desarrollador.py)

[*Indice*](#Índice-de-Módulos)

### Descripción

Lee los datos extraidos de los csv finales, que se encuentran en un diccionario organizado por autores, los formatea, y muestra en pantalla la información de cada autor respecto 
al código en tablas, esa misma información la graba en un archivo de texto llamado participacion.txt.

### Funciones

#### obtener_informacion_desarrollador(*datos_csv*)

*Autor: Ivan Litteri*

```datos_csv``` es el diccionario organizado por autores con los datos de los archivos csv finales.

Ordena los datos del diccionario con la función *ordenar_diccionario_autores(datos_archivos_csv)*, datos que deriva a la función *formatear_participacion(datos_formateados)* que 
formatea los datos para mostrarlos con la función *mostrar_participacion(datos_formateados)*. Por último, crea el archivo de participacion.txt con la función 
*crear_participacion_txt(nombre_archivo, datos_formateados)*

#### crear_participacion_txt(*nombre_archivo, datos_formateados*)

*Autor: Ivan Litteri*

```nombre_archivo``` es el nombre del archivo de texto a crear.

```datos_formateados``` es el string con los datos ya formateados a grabar

Crea y graba el archivo de participacion.txt con los datos formateados.

#### mostrar_participacion(*datos_formateados*)

*Autor: Ivan Litteri*

```datos_formateados``` es el string con los datos ya formateados a mostrar

Muestra en pantalla los datos formateados.

#### formatear_participacion(*datos_ordenados*)

*Autor: Ivan Litteri*

```datos_ordenados``` es la lista con los datos de los autores ordenados por cantidad de lineas de código totales.

Formatea los datos que le llegan por parametro para mostrarlos más adelante. Obtiene las lineas de código totales de la aplicación. Declara el contador de funciones en 0. 
Inicializa la devolución en vacío para ir concatenando. Concatena la primera línea. Recorre los datos ordenados que me llegan por parámetro. Guarda los datos por columnas, 
separación, y otras nomenclaturas utilizadas para que su lectura sea más comprensible. Concatena la linea correspondiende al autor y la fila que corresponde al título de la 
tabla del autor. Concatena la linea de iguales. Recorre los datos de las funciones del auto. Establece la separacion que quiero tener entre el nombre de la funcion y la cantidad 
de lineas de esa funcion. Concatena la linea: "Funcion" ---------- "Cantidad Lineas de Funcion". Guarda el porcentaje de lineas de codigo que escribio el autor respecto del 
total del codigo. Incrementa el contador de funciones. Establece la columna y la separación. Concatena la linea que contiene la cantidad de funciones que escribio el autor y el 
porcentaje respecto a todo el codigo. Asi en cada iteración.

Devuelve la cadena formateada lista para imprimir.

#### ordenar_diccionario_autores(*datos_csv*)

*Autor: Ivan Litteri*

```datos_csv``` es el diccionario organizado por autores con los datos de los archivos csv finales.

Reordena los datos del diccionario que llega del main en otro de forma descendiente respecto de la cantidad de lineas de codigo que escribio cada autor.

Devuelve una lista con esos datos ordenados

## [Obtener](./m_obtener.py)

[*Indice*](#Índice-de-Módulos)

### Descripción

(----)

### Funciones

(----)

## [Crear CSV Individuales ](./m_csv_individuales.py)

[*Indice*](#Índice-de-Módulos)

### Descripción

(----)

### Funciones

(----)

## [Analizar Línea](./m_analizar_linea.py)

[*Indice*](#Índice-de-Módulos)

### Descripción

(----)

### Funciones

(----)

# Extra

## [Grafo](./m_grafo.py)

[*Indice*](#Índice-de-Módulos)

Hicimos un modulo extra llamado *m_grafo.py* que básicamente crea dos archivos llamados grafo.svg y grafo.png que corresponden a el árbol de invocaciones.

### Grafo de llamada de funciones
<img src="./grafo.svg">

### crear_grafo_invocaciones(*datos_csv*)

*Autor: Ivan Litteri*

```datos_csv``` es el diccionario organizado por funciones con los datos de los archivos csv finales.

Se utiliza la librería *pygraphviz*, se declara un objeto del tipo AGraph con los parámetros necesarios, se repasa función por función el diccionario, se agrega a cada función como un nodo del grafo (atributo del objeto), luego por cada función se repasan sus invocaciones y se indica hacia donde apunta cada nodo.
