# todo_python
Aplicación simple para gestionar tareas hecha con Python utilizando tkinter y una base de datos local para almacenar las tareas añadidas y si están completas o no.

Funcionamiento muy sencillo:
Se añade una nueva tarea, las no realizadas aparecerán escritas en azul, una vez se marque la casilla de que esa tarea ha terminado, no se eliminará por si el usuario quiere tener un seguimiento de las tareas completas si no que se pondrá en un color verde muy destacable, de esa forma se distinguirá del resto.
La aplicación también incluye una opción para eliminar estas tareas en caso de error o en caso de no querer seguir teniendo alguna tarea en la lista tras completarla.
Todas estas tareas se almacenan en una base de datos sql, lo que permite que no se eliminen al dejar de funcionar la aplicación, se mantendrán hasta que el usuario decida borrarlas.

Añadida también la opción de tener varios usuarios, registrar y hacer login, cada usuario tiene su lista independiente de tareas y las contraseñas se almacenan encriptadas.

Para poder ejecutar el codigo se necesita instalar las dependencias indicadas en el archivo requirements.
