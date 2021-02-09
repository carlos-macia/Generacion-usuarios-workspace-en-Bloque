Autor: José Carlos Maciá Mora
Email: cmacia@iesisidormacabich.es 
Página del proyecto en hithub
https://github.com/carlos-macia/Generacion-usuarios-workspace-en-Bloque

Vídeos Youtube
Parte 1: https://youtu.be/nqX2AFXemEY
Parte 2: https://youtu.be/lc36BMvwxxg
Parte 3: https://youtu.be/71mh8NUC01c
Parte 4: https://youtu.be/ds1Yfh29lhQ
Parte 5: https://youtu.be/b66BfKD_Ras
Parte 6:: https://youtu.be/hA0kT1XnayY

1. Introducción.

Este script genera, a partir de un fichero de alumnos del gestib, usuarios en 
bloque para subir a la consola de Workspace. El script compara los datos con 
otro archivo que contiene los usuarios actuales de nuestro Workspace, para 
decidir si debe añadir o actualizar el usuario. Entre otros, se crean ficheros
de usuarios, miembros de grupos y contactos. Estos ficheros se suben posteriormente
a la consola de Workspace.

2. Requisitos.
Interprete de Python 3. La versión 2 de Python podría dar problemas con los acentos
dependiendo de la configuracióndel sistema.

3. Funcionamiento.
El script necesita dos ficheros de entrada: el fichero de datos del gestib, y el
fichero con los usuarios que hay actualmente en Workspace (users.csv).

El fichero del gestib, se tiene que transformar de xls a formato csv. Los campos
que debe tener este fichero son los siguientes:

   <número de registro, apellidos, nombre, estudios, curso, grupo, expediente>

El archivo de usuarios de Workspace lo bajaremos directamente de la consola de
Google (usuarios bloque). Se debe guardar con el nombre users.csv en la
misma ruta que se encuentre el script.
 
Los dos ficheros de entrada deben estar los más actualizados posible. Es 
recomendable bajar estos ficheros justo antes de la ejecución del script.

4. Opciones:
Básicamente hay dos opciones de ejecución: actualizar usuarios y generar grupos.

Actualizar usuarios (-a):
El script hace un recorrido por todos los alumnos del fichero del gestib. Se 
pueden dar las siguientes situaciones:
   - El alumno no se encuentra entre los usuarios del fichero de Workspace:
     Se crea una entrada de nuevo usuario en el fichero usuarios_bloque.csv
     y otra en el fichero grupos_bloque.csv.
    
   - El alumno se encuentra entre los usuarios de Workspace y los datos de la
     unidad organizativa no han variado (no se ha cambiado de curso o de 
     modalidad de estudios): no es necesario crear ninguna entrada en los
     ficheros.

   - El alumno se encuentra entre los usuarios del dominio, pero ha cambiado
     su unidad organizativa: Esta situación pasa tanto si se cambia de curso
     como de modalidad de estudios. El script genera una entrada en el fichero
     de usuarios_bloques.csv para actualizar la información de Workspace.
     ATENCION! Esta opción no genera entrada en el fichero grupos_bloques.csv.
     por lo que el alumno puede quedará en un grupo erroneo (Ver opción Generar
     grupos) 

5. Generar grupos (-g):
     Como vimos anteriormente, cuando un alumno cambia de curso o modalidad
     de estudios se le cambia de unidad organizativa automáticamente. Pero no
     se actualizaban los grupos porque el script no puede borrar los miembros
     de un grupo, esta acción se debe realizar manualmente.
     Cuando se cambia de curso académico deberemos borrar todos miembros de los
     grupos en Workspace manualmente. Después se ejecuta la opción  de generar 
     grupos, obteniendo un fichero con todos los grupos que se subiran en bloque.

6. Ejecución:
     Se necesitan cuatro ficheros para ejecutar el script:
      - genera.py   (bajar de github la versión más reciente)
      - config.ini  (bajar de github y configurar vuestro dominio)
      - Fichero del gestib en formato csv
      - El fichero de usuarios actuales en Workspace (users.csv)  

    Ejemplo:

       $python genera.py -a dades_destib.csv
       $python genera.py -g dades_destib.csv
     
7. Preparación del entorno Workspace.
     Antes de subir los ficheros de bloque generados por el script, es necesario
     crear, de forma manual desde la consola de Workspace, todas las unidades
     organizativas y grupos. Para ayudar, el script genera los ficheros
     listado_uorg.txt y listado_grupos.txt, los cuales contienen una lista
     de las unidades organizativas y grupos necesarios para que se puedan
     subir los ficheros de bloque. 

8. Subida de archivos a Workspace.
     Una vez realizados el punto 6 y 7, se puede proceder a subir los
     archivos a la consola de Workspace para crear o actualizar la información
     en bloque.
     