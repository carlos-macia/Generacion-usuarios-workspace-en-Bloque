# Archivo: genera.py
# Autor: J.Carlos Maciá Mora
# Noviembre de 2020 
# Descripción: generador de usuarios en bloque. 
# A partir de los datos del gestib genera ficheros 
# de usuarios, grupos y contactos en bloque para
# subir a la consola de Workspace de Google

import sys
import string
import random
import configparser
from os import remove
from os import path
from os import mkdir
from shutil import rmtree
from random import randint

#####################################################
#             class User
#____________________________________________________
#
# Clase para guardar los datos de usuario que se 
# encuentran en el fichero que descargamos de la
# consola de Workspace
#
#####################################################
class User:
    def __init__(self, nombre,apellidos, email, uorg,
                 validado, expediente):
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.uorg = uorg
        self.validado = validado
        self.expediente = expediente

#####################################################
#             class ListaUsers
#____________________________________________________
#
# Clase para manejar una lista de usuarios(Class User) 
# 
#
#####################################################
class ListaUsers:
    def __init__(self):
        self._lista = []
        
    def insertar(self,user):
        self._lista.append(user)
    
    def obtenerIndice(self,indice):
        return (self._lista[indice])
    
    
    def buscarEmail(self,email):
        ret = -1
        for indice in range(len(self._lista)):
            if self._lista[indice].email == email:
                ret = indice
        return ret
    
    def buscarNombre(self, nombre, apellidos):
    
        nombre = eliminaEspacios(eliminaSimbolos(eliminaAcentos(nombre.lower())))
        apellidos = eliminaEspacios(eliminaSimbolos(eliminaAcentos(apellidos.lower())))
        ret = -1
        cont = 0
        for indice in range(len(self._lista)):
            n = eliminaEspacios(eliminaSimbolos(eliminaAcentos(self._lista[indice].nombre.lower())))
            a = eliminaEspacios(eliminaSimbolos(eliminaAcentos(self._lista[indice].apellidos.lower())))
            if n == nombre and a == apellidos:
                ret = indice
                cont += 1
        if cont > 1:
            #print ("Alerta! Nombre repetido: ", nombre, apellidos)
            ret = -2
        return ret
    
    def buscarExpediente(self,expediente):
        ret = -1
        for indice in range(len(self._lista)):
            if self._lista[indice].expediente == expediente:
                ret = indice
        return ret
    
    def getUser(self,expediente):
        indice=self.buscarExpediente(expediente)
        if indice != -1:
            return (self._lista[indice])
        else:
            return (0)
            
    def validar(self, indice):
        self._lista[indice].validado = 1
    
    def imprimir(self):
        for u in self._lista:
            print (u.nombre)

#####################################################
#             class ClassAlumno
#____________________________________________________
#
# Clase para guardar los datos del alumno que se 
# encuentran en el Gestib
#
#####################################################
class ClassAlumno:
    def __init__(self, num,apellidos, nombre, estudios, curso, grupo, expediente):
        self.num = num
        nombre = nombre.lstrip(' ').rstrip(' ') #quita el espacio del principio y final
        self.nombre = nombre.title()
        apellidos = apellidos.lstrip(' ').rstrip(' ')
        self.apellidos = apellidos.title()
        self.email = generaEmail(self.nombre,apellidos)
        self.password = "****"
        self.estudios = estudios
        self.curso = curso
        self.grupo = grupo
        self.expediente = eliminaEspacios(expediente) #puede tener el \n al final, \r o espacio
        self.uorg = generaUnidadOrganizativa(estudios, curso, grupo)

#####################################################
#             class ListaAlumnos
#____________________________________________________
#
# Clase para construir una lista de alumnos que se 
# encuentran en el Gestib
#
#####################################################
class ListaAlumnos:
    def __init__(self):
        self.lista = []
        
    def insertar(self,alumno):
        self.lista.append(alumno)

    def buscarExpediente(self,expediente):
        ret = -1
        for indice in range(len(self.lista)):
            if self.lista[indice].expediente == expediente:
                ret = indice
        return ret
    
    def esExpedienteRepetido(self,expediente):
        cont = 0
        for indice in range(len(self.lista)):
            if self.lista[indice].expediente == expediente:
                cont += 1
        return cont
    
    def buscarNombre(self, nombre, apellidos):
    
        nombre = eliminaEspacios(eliminaSimbolos(eliminaAcentos(nombre.lower())))
        apellidos = eliminaEspacios(eliminaSimbolos(eliminaAcentos(apellidos.lower())))
        ret = -1
        cont = 0
        for indice in range(len(self.lista)):
            n = eliminaEspacios(eliminaSimbolos(eliminaAcentos(self.lista[indice].nombre.lower())))
            a = eliminaEspacios(eliminaSimbolos(eliminaAcentos(self.lista[indice].apellidos.lower())))
            if n == nombre and a == apellidos:
                ret = indice
                cont += 1
        if cont > 1:
            #print ("Alerta! Nombre repetido: ", nombre, apellidos)
            ret = -2
        return ret
    
    def obtenerIndice(self,indice):
        return (self.lista[indice])
    
#####################################################
#             generaEmail(nombre, apellidos)
#____________________________________________________
#
#  Genera el email a partir del nombre y los apellidos
#  Método principal
#
#####################################################
def generaEmail(nombre, apellidos):

    #pasar a miúsculas y quitar acentos
    apellidos = eliminaAcentos(apellidos.lower())
    nombre = eliminaAcentos(nombre.lower())
    
    # si el apellidos mide mas de 12 resumirlo
    apellidos = resumeApellidos(apellidos)
    
    partes_nombre = nombre.split(" ")
    
    nomb = ""
    i = 0
    while i < len(partes_nombre):
        nomb += partes_nombre[i][0]
        i += 1
            
    # Formamos el email añadiendo la inicial del primer nombre    
    email = nomb + apellidos

    #Sustituir ñ y Ç
    email = email.replace("ñ","n")
    email = email.replace("ç","c")

    #Eliminar simbolos
    email = eliminaSimbolos(email)
   
    # Quitamos espacios, tabuladores y \n
    email = eliminaEspacios(email)
    
    # añadimos la @ más el dominio
    email +=  "@" + DOMINIO

    return (email)

#####################################################
#             resumeApellidos(apellidos)
#____________________________________________________
#
#  Acorta los apellidos largos
#  
#
#####################################################
def resumeApellidos(apellidos):
    resumen = ""

    if len(apellidos) > 11:
                
        partes = apellidos.split(" ")
        
        while len(partes) > 3:
            partes.pop()
        
        mas_de_cinco = 0
        for cadena in partes:
            if len(resumen) > 10:
                break
            if len(cadena) > 6 or mas_de_cinco > 0:
                cadena = extraerPrimeraSilaba(cadena)
            elif len(cadena) > 5:
                mas_de_cinco += 1
            resumen += cadena
    else:
        resumen = apellidos
                        
    return (resumen)            

#####################################################
#             generaEmail2(nombre, apellidos)
#____________________________________________________
#
#  Genera el email a partir del nombre y los apellidos
#  Método secundário
#
#####################################################
def generaEmail2(nombre,apellidos):
    # Pasar a miúsculas y quitar acentos
    apellidos = eliminaAcentos(apellidos.lower())
    nombre = eliminaAcentos(nombre.lower())
    
    # Nos quedamos con la primera silaba del primer nombre
    partes = nombre.split(" ")
    nombre = extraerPrimeraSilaba(partes[0])

    # Nos quedamos con las primeras silabas de los apellidos
    partes = apellidos.split(" ")
    apellidos = ""
    for cadena in partes:
        apellidos += extraerPrimeraSilaba(cadena)  
    
    # Formamos el email con las primeras silabas del primer nombre y los apellidos    
    email = nombre + apellidos

    # Sustituir ñ y Ç
    email = email.replace("ñ","n")
    email = email.replace("ç","c")

    # Eliminar simbolos
    email = eliminaSimbolos(email)
   
    # Quitamos espacios, tabuladores y \n
    email = eliminaEspacios(email)
    
    # Añadimos la @ más el dominio
    email +=  "@" + DOMINIO

    return (email)

#####################################################
#             extraerPrimeraSilaba(cadena)
#____________________________________________________
#
#  Extrae la primera (sílaba) de una cadena
#
#####################################################
def extraerPrimeraSilaba(cadena):
    i = 0
    vocales = 0
    new = ""
    while i < len(cadena):
        if cadena[i] in ['a','e','i','o','u']:
            vocales += 1
            if i > 0:
                if cadena[i-1] == 'q' and cadena[i] == 'u':
                    vocales -= 1
                if cadena[i-1] == 'g' and cadena[i] == 'u':
                    vocales -= 1
        if vocales < 2:
            new += cadena[i]
        else:
            break
        i += 1
    return(new)


#####################################################
#             generaEmail3(nombre, apellidos)
#____________________________________________________
#
#  Genera el email a partir del nombre y los apellidos
#  Tercer método
#
#####################################################
def generaEmail3(nombre,apellidos):
    # Pasar a miúsculas y quitar acentos
    apellidos = eliminaAcentos(apellidos.lower())
    nombre = eliminaAcentos(nombre.lower())
    
    # Nos quedamos con la inicial de cada nombre
    partes = nombre.split(" ")
    nombre = partes[0][0]
    if len(partes) > 1:
        nombre += partes[1][0]
        
    # Nos quedamos con el primer apellido
    partes = apellidos.split(" ")
    apellidos = partes[0]
    
    # Formamos el email con las iniciales del nombre y el primer apellido    
    email =  nombre + apellidos

    #Sustituir ñ y Ç
    email = email.replace("ñ","n")
    email = email.replace("ç","c")

    #Eliminar simbolos
    email = eliminaSimbolos(email)
   
    # Quitamos espacios, tabuladores y \n
    email = eliminaEspacios(email)
    
    # añadimos la @ más el dominio
    email +=  "@" + DOMINIO

    return (email)

#####################################################
#             eliminaEspacios(cadena)
#____________________________________________________
#
# Elimina los espacios, tabuladores y retorno de carrro
# de una cadena
#
#####################################################
def eliminaEspacios(cadena):
    cadena = cadena.replace(" ","")
    cadena = cadena.replace("\t","")
    cadena = cadena.replace("\n","")
    cadena = cadena.replace("\r","")
    return (cadena)
    
#####################################################
#             eliminaSimbolos(cadena)
#____________________________________________________
#
# Elimina los símbolos de una cadena
#
#####################################################
def eliminaSimbolos(cadena):
    cadena = cadena.replace("-","")
    cadena = cadena.replace("_","")
    cadena = cadena.replace("{","")
    cadena = cadena.replace("}","")
    cadena = cadena.replace("[","")
    cadena = cadena.replace("]","")
    cadena = cadena.replace("+","")
    cadena = cadena.replace("¿","")
    cadena = cadena.replace("?","")
    cadena = cadena.replace("=","")
    cadena = cadena.replace("€","")
    cadena = cadena.replace("'","")
    cadena = cadena.replace(".","")
    cadena = cadena.replace(",","")
    cadena = cadena.replace(";","")
    cadena = cadena.replace(":","")
    cadena = cadena.replace("/","")
    cadena = cadena.replace("\\","")
    cadena = cadena.replace("&","")
    cadena = cadena.replace("%","")
    cadena = cadena.replace("$","")
    cadena = cadena.replace("·","")
    cadena = cadena.replace("!","")
    cadena = cadena.replace("¡","")
    cadena = cadena.replace("@","")
    cadena = cadena.replace("º","")
    cadena = cadena.replace("ª","")
    cadena = cadena.replace("<","")
    cadena = cadena.replace(">","")
    
    return(cadena)

#####################################################
#             eliminaAcentos(cadena)
#____________________________________________________
#
# Elimina los acentos de una cadena ( MINÚSCULAS ),
# abiertos y cerrados
#
#####################################################
def eliminaAcentos(cadena):

    cadena = cadena.replace("á","a")
    cadena = cadena.replace("é","e")
    cadena = cadena.replace("í","i")
    cadena = cadena.replace("ó","o")
    cadena = cadena.replace("ú","u")
    cadena = cadena.replace("à","a")
    cadena = cadena.replace("è","e")
    cadena = cadena.replace("ì","i")
    cadena = cadena.replace("ò","o")
    cadena = cadena.replace("ù","u")
    cadena = cadena.replace("ä","a")
    cadena = cadena.replace("ë","e")
    cadena = cadena.replace("ï","i")
    cadena = cadena.replace("ö","o")
    cadena = cadena.replace("ü","u")
    cadena = cadena.replace("â","a")
    cadena = cadena.replace("ê","e")
    cadena = cadena.replace("î","i")
    cadena = cadena.replace("ô","o")
    cadena = cadena.replace("û","u")
    
    return (cadena)

#####################################################
#  generaUnidadOrganizativa(estudios,curso,grupo)
#____________________________________________________
#
# Forma el nombre de la unidad organizativa
#
#####################################################
def generaUnidadOrganizativa(estudios,curso,grupo):
    
    uorg = "/"+ UNIDAD_ORGANIZATIVA_PADRE +"/{0}/{1}{2}"
    uorg = uorg.format(estudios, curso, grupo.upper())
    #uorg = uorg.replace(".","") # quita el punto de batx.
    return uorg

#####################################################
#           cargarUsuariosGoogle(con)
#____________________________________________________
#
#  Carga la información de los usuarios de la 
#  consola de Google que se encuentran en el 
#  fichero users.cvs en la lista usuarios_google
#
#####################################################
def cargarUsuariosGoogle():
    if not path.exists('users.csv'):
        print("ERROR: No existe el fichero users.csv (usuarios consola Google)")
        exit(0)
    with open('users.csv') as f:
        for linea in f:
            aux_user=linea.split(',');
            if aux_user[0] == "First Name [Required]":
                continue
            usuario = User(aux_user[0],aux_user[1],aux_user[2],
                           aux_user[5], 0, aux_user[16] ) #16 expediente
            usuarios_google.insertar(usuario)            
        
#####################################################
#         generaPassword()
#____________________________________________________
#
#  Genera un password alfanumerico de 8 caracteres
#
#####################################################
def generaPassword():
    caract=string.ascii_letters
    password = ("").join(random.choice(caract)for i in range(2))

    caract= string.ascii_letters + string.digits
    password += ("").join(random.choice(caract)for i in range(3))

    caract=  string.digits
    password += ("").join(random.choice(caract)for i in range(1))

    caract=string.ascii_letters
    password += ("").join(random.choice(caract)for i in range(2))

    return(password)

#####################################################
#         escribeUsuarioFichero(alumno)
#____________________________________________________
#
#  Escribe el nuevo usuario o actualización en el 
#  fichero de salida usuarios_bloque.csv
#
#####################################################
def escribeUsuarioFichero(alumno, fichero):

    # Formatear la línea
    linea = "{0},{1},{2},{3},,{4},,,,,,,,,,,{5},,,,,,,,,{6},"
    linea = linea.format(alumno.nombre ,alumno.apellidos, alumno.email,
                         alumno.password, alumno.uorg, alumno.expediente,
                         FORZAR_CAMBIAR_PASSWORD)

    # Añadir al fichero
    f= open(fichero,"a")
    f.write(linea+"\n")
    f.close()

#####################################################
#          escribeMiembroGrupo(alumno)
#____________________________________________________
#
#  Escribe una entrada de miembro de grupo en el fichero
#  grupos_bloque.cvs
#
#####################################################
def escribeMiembroGrupo(alumno):

    #formatear email de grupo
    email_grupo = "{0}{1}@iesisidormacabich.es"
    email_grupo = email_grupo.format(alumno.curso.replace(".",""),alumno.grupo) #quita a curso el . de batxl.

    #quitar espacios y pasar a minusculas
    email_grupo = email_grupo.replace(" ","").lower()

    #formatear la linea del fichero de grupos
    linea = "{0},{1},{2} {3},MEMBER,USER"
    linea = linea.format(email_grupo,alumno.email,alumno.nombre,alumno.apellidos)

    f= open("grupos_bloque.csv","a")
    f.write(linea+"\n")
    f.close()

#####################################################
#          escribeInformacionNuevos(alumno)
#____________________________________________________
#
#  Escribe una entrada de usuario y contraseña en el 
#  fichero correspondiente dentro del directorio 
#  Información
#
#####################################################
def escribeInformacionNuevos(fichero, alumno):

    #formatear informacion
    nombre = alumno.nombre+" "+ alumno.apellidos
    linea = "{0:40}{1:35}{2:10}{3:8}{4:2}"
    linea = linea.format(nombre,alumno.email, alumno.password,alumno.curso,alumno.grupo)

    f= open(DIRECTORIO_INFORMACION+ "/" + fichero,"a")
    f.write(linea+"\n")
    f.close()

#####################################################
#          escribeContacto(alumno)
#____________________________________________________
#
#  genera una entrada de contacto en el fichero
#  cvs correspondiente
#
#####################################################
def escribeContacto( alumno):

    #formatear la etiqueta de contacto
    etiqueta = "{0} {1}{2}"
    etiqueta = etiqueta.format( alumno.estudios,alumno.curso, alumno.grupo)
    #etiqueta = etiqueta.replace(".","").upper()

    linea = "{0} {1},{0},,{1},,,,,,,,,,,,,,,,,,,,,,,,,{2} ::: * myContacts,* ,{3}"
    linea = linea.format(alumno.nombre,alumno.apellidos,etiqueta,alumno.email)

    fichero = alumno.curso+alumno.grupo[0].upper()+".csv"

    f= open(DIRECTORIO_CONTACTOS+ "/" + fichero,"a")
    f.write(linea+"\n")
    f.close()

#####################################################
#              borrarArchivos()
#____________________________________________________
#
#  Borrar archivos de de salida de ejecuciones anteriores
#
#####################################################
def borrarArchivos():

    archivos = [ 'usuarios_bloque.csv', 'grupos_bloque.csv', 'nuevos_contactos.csv',
                 'usuarios_repetidos.csv','listado_uorg.txt', 'listado_grupos.txt',
                 'usuarios_baja.txt']

    for file in archivos:
        if path.exists(file):
            remove(file)

    # Borrar el directorio de contactos y su contenido
    if path.exists(DIRECTORIO_CONTACTOS):
        rmtree(DIRECTORIO_CONTACTOS)

    # Borrar el directorio de información y su contenido
    if path.exists(DIRECTORIO_INFORMACION):
        rmtree(DIRECTORIO_INFORMACION)


#####################################################
#              generaCabeceraUsuarios()
#____________________________________________________
#
#  Escribe la cabecera del archivo usuarios_bloque.csv
#
#####################################################
def generaCabeceraUsuarios(fichero):

    linea = "First Name [Required],Last Name [Required],Email Address [Required],Password [Required],Password Hash Function [UPLOAD ONLY],Org Unit Path [Required],New Primary Email [UPLOAD ONLY],Recovery Email,Home Secondary Email,Work Secondary Email,Recovery Phone [MUST BE IN THE E.164 FORMAT],Work Phone,Home Phone,Mobile Phone,Work Address,Home Address,Employee ID,Employee Type,Employee Title,Manager Email,Department,Cost Center,Building ID,Floor Name,Floor Section,Change Password at Next Sign-In,New Status [UPLOAD ONLY]"
    f= open(fichero,"a")
    f.write(linea+"\n")
    f.close()

#####################################################
#              generaCabeceraGrupos()
#____________________________________________________
#
#  Escribe la cabecera del archivo grupos_bloque.csv
#
#####################################################
def generaCabeceraGrupos():
 
    linea = "Group Email [Required],Member Email,Member Name,Member Role,Member Type"
    f= open("grupos_bloque.csv","a")
    f.write(linea+"\n")
    f.close()

#####################################################
#              generaCabeceraContactos()
#____________________________________________________
#
#  Escribe la cabecera del archivo de contactos
#  el nombre de este archivo coincide con el nombre
#  del curso + .csv
#
#####################################################
def generaCabeceraContactos():
    
    linea = "Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Language,Photo,Group Membership,E-mail 1 - Type,E-mail 1 - Value"
        
    for curso in lista_cursos:
        cursocsv = curso + ".csv"
        f= open(DIRECTORIO_CONTACTOS+"/"+cursocsv,"a")
        f.write(linea+"\n")
        f.close()

#####################################################
#              generaListadoUorg()
#____________________________________________________
#
#  Escribe un listado de unidades organizativas en el 
#  fichero listado_uorg.txt   
#
#####################################################
def generaListadoUorg():
    
    l = sorted(lista_uorg)    
    for uo in l:
        f= open("listado_uorg.txt","a")
        f.write(uo+"\n")
        f.close()

#####################################################
#              generaListadoGrupos()()
#____________________________________________________
#
# Escribe un listado de los grupos en el fichero
# listado_grupos.txt 
#
#####################################################
def generaListadoGrupos():
    
    l = sorted(lista_cursos)    
    cont = 1
    for curso in l:
        f= open("listado_grupos.txt","a")
        f.write(curso+"\n")
        f.close()

#####################################################
#              cargaFicheroGestib
#____________________________________________________
#
# Carga el fichero cvs que contiene los datos del  
# Gestib a la lista_alumnos_gestib 
# 
#####################################################
def cargaFicheroGestib( dades_gestib):
    cont = 0
    error = 0
    
    with open(dades_gestib) as f:
        for linea in f:
            
            cont += 1 
            
            # Quitar el \n del final de la línea
            linea = linea.replace("\n","")

            # Separamos los campos por comas
            aux_user = linea.split(',');
            
            # Se deben leer 7 campos por línea
            if len(aux_user) != 7:
               print("Error de formato. Línea: {:15} NO SE PROCESA".format(cont))
               error += 1
               continue #no se procesa la línea
            # El primer y último campo deben ser dígitos 
            elif not(aux_user[0].isdigit()) or not(aux_user[6].isdigit()):
               print ("Error de formato. Línea: {:15} NO SE PROCESA (Dígitos)".format(cont))
               error += 1
               continue  #no se procesa la línea
    
            # Crear el alumno con los datos leídos
            alumno = ClassAlumno(aux_user[0],aux_user[1],aux_user[2],aux_user[3],
                                 aux_user[4],aux_user[5], aux_user[6] )

            # Controlar expedientes repetidos 
            if lista_alumnos_gestib.esExpedienteRepetido(alumno.expediente) > 0:
                print("Error expediente {} repetido. Línea: {:15} NO SE PROCESA".format(alumno.expediente, cont))
                error += 1
                continue
                
            # Añadir a la lista de alumnos gestib
            lista_alumnos_gestib.insertar(alumno)
            
    if error > 0:
        print ("ALERTA! Se han descartado {} líneas erroneas del fichero {}".format(error,dades_gestib))
        #exit()                

#####################################################
#   muestrasGeneracionEmail([tipo lista de alumnos])
#____________________________________________________
#   Muestra las tres combinaciones de email que
#    se pueden generar
#####################################################
def muestrasGeneracionEmail():

    for alumno in lista_alumnos_gestib.lista:

        # No tratar datos de alumnos que no se encuentren en la lista de estudios
        if alumno.estudios not in LISTA_DE_ESTUDIOS_ACOTADOS:
            continue

        encontrado = 0
        print("-------------")
        print( alumno.nombre, alumno.apellidos)
        print("{:4} Versión 1\t\t{:30}".format(len(alumno.email)-21,alumno.email))
        
        email = generaEmail2(alumno.nombre,alumno.apellidos)
        print("{:4} Versión 2\t\t{:30}".format(len(email)-21, email))
        
        email = generaEmail3(alumno.nombre,alumno.apellidos)
        print("{:4} Versión 3\t\t{:30}".format(len(email)-21, email))
        
        indice_encontrado = usuarios_google.buscarExpediente(alumno.expediente)
        if  indice_encontrado != -1:
            print("Actual Workspace\t{:30}".format(usuarios_google.obtenerIndice(indice_encontrado).email))        


#####################################################
#              generarDatosFalsos(fichero)
#____________________________________________________
#
#  Para pruebas y demos públicas
#  Genera un ficheo de gestib ficticio combinando
#  aleatoriamente nombres, apellidos, y demás informació
#  del fichero de gestib.
#
#####################################################
def generarDatosFalsos():

    cont = 0
    for alumno in lista_alumnos_gestib.lista:

        # No tratar datos de alumnos que no se encuentren en la lista de estudios
        if alumno.estudios not in LISTA_DE_ESTUDIOS_ACOTADOS:
            continue

        encontrado = 0
                    
        tam_lista = len(lista_alumnos_gestib.lista)
        
        nombre = lista_alumnos_gestib.obtenerIndice(randint(1,tam_lista-1)).nombre
        
        partes = nombre.split(" ")
        
        if len(partes) > 1:
        
            alumno.nombre = partes[randint(0,1)]
            nombre2 = lista_alumnos_gestib.obtenerIndice(randint(1,tam_lista-1)).nombre
            partes2 = nombre2.split(" ")
        
            if len(partes2) > 1:
                alumno.nombre += " " + partes2[randint(0,1)]
            else: 
                alumno.nombre += " " + nombre2
                
        else:
            alumno.nombre = nombre
                               
        apellidos = lista_alumnos_gestib.obtenerIndice(randint(1,tam_lista-1)).apellidos
        
        partes = apellidos.split(" ")
        
        if len(partes) > 1:
        
            alumno.apellidos = partes[0]
            apellidos2 = lista_alumnos_gestib.obtenerIndice(randint(1,tam_lista-1)).apellidos
            partes2 = apellidos2.split(" ")
            aux = ""
            if len(partes2) == 1: 
                aux += apellidos2
            
            if len(partes2) > 1:
                aux += partes2[1]
            if len(partes2) > 2:
                aux += " " + partes2[2]
            if len(partes2) > 3:
                aux += " " + partes2[3]
            
            alumno.apellidos = alumno.apellidos + " " + aux
                
        else:
            alumno.apellidos = apellidos
        
        indice_aleatorio= randint(1,tam_lista-1)
        
        alumno.estudios = lista_alumnos_gestib.obtenerIndice(indice_aleatorio).estudios
        alumno.curso = lista_alumnos_gestib.obtenerIndice(indice_aleatorio).curso
        alumno.grupo = lista_alumnos_gestib.obtenerIndice(indice_aleatorio).grupo
           
        alumno.expediente = "099" + alumno.expediente
        linea = "{0},{1},{2},{3},{4},{5},{6}"
        linea = linea.format( cont, alumno.apellidos, alumno.nombre,
                             alumno.estudios,alumno.curso, alumno.grupo, alumno.expediente)

        f= open("gestib.csv","a")
        f.write(linea+"\n")
        f.close()
        cont += 1
            

#####################################################
#              actualizarExpedientes(fichero)
#____________________________________________________
#
#  Lee el fichero dadesGestib.cvs, busca por nombre
#  y actualiza los numeros de expediente en el fichero
#  de salida usuarios_bloque.csv
#
#####################################################
def actualizarExpedientes():

    generaCabeceraUsuarios("usuarios_bloque.csv")
    
    actualizados = 0
    for alumno in lista_alumnos_gestib.lista:

        # No tratar datos de alumnos que no se encuentren en la lista de estudios
        if alumno.estudios not in LISTA_DE_ESTUDIOS_ACOTADOS:
            continue

        # Buscar por nombre
        indice_encontrado = usuarios_google.buscarNombre(alumno.nombre,alumno.apellidos)

        if indice_encontrado > 0:

            usuario = usuarios_google.obtenerIndice(indice_encontrado)
              
            if usuario.expediente == "":
                
                actualizados += 1    
                alumno.email = usuario.email #conservamos el email
                alumno.password = "****" # nos aseguramos que no se cambie la password
                # Escribimos la actualizacion de los datos en el fichero
                escribeUsuarioFichero(alumno,"usuarios_bloque.csv")
       
        elif indice_encontrado == -2:
            print("Nombre repetido {} {} {} - NO SE PROCESA".format(
                   alumno.nombre, alumno.apellidos, alumno.email))
       
    print ("Se han actualizado {} expedientes".format(actualizados))
    
#####################################################
#              generaGrupos()
#____________________________________________________
#
#   Genera todos los grupos y contactos
#
#####################################################
def generaGrupos():

    generaCabeceraGrupos()
    
    if not path.exists(DIRECTORIO_CONTACTOS):
        mkdir(DIRECTORIO_CONTACTOS)
        
    generaCabeceraContactos()
    
    for alumno in lista_alumnos_gestib.lista:

        # No tratar datos de alumnos que no se encuentren en la lista de estudios
        if alumno.estudios not in LISTA_DE_ESTUDIOS_ACOTADOS:
            continue

        encontrado = 0
        #buscar por Expediente
        indice_encontrado = usuarios_google.buscarExpediente(alumno.expediente)
        
        if indice_encontrado > 0:
            
            #print ("Encontrado por nombre", alumno.nombre, alumno.apellidos)

            usuario = usuarios_google.obtenerIndice(indice_encontrado)
          
            #actualizar la información grupos
            alumno.email = usuario.email # Conserbar el email de workspace
            
            # Escribir el fichero de grupos
            escribeMiembroGrupo(alumno)
            # Escribir el fichero de contactos
            escribeContacto(alumno)
        
#####################################################
#              actualizarUsuarios()
#____________________________________________________
#
#  Lee el fichero dadesGestib.cvs y procesa la información.
#  Si encuentra usuarios nuevos se añaden.
#  Se actualiza la unidad organizativa, por ejemplo cambio de curso.
#  NO SE REGENERAN TODOS LOS GRUPOS, pero sí se escriben las entradas
#  __sólo__ de los nuevos usuarios en el fichero de grupos_bloque.csv
#
#####################################################
def actualizarUsuarios():

    global cont_validados
    global cont_nuevos
    global cont_actualizados
    
    #generar las cabeceras
    generaCabeceraUsuarios("usuarios_bloque.csv")
    generaCabeceraUsuarios("usuarios_repetidos.csv")    
    generaCabeceraGrupos()

    if not path.exists(DIRECTORIO_INFORMACION):
        mkdir(DIRECTORIO_INFORMACION)
    
    for alumno in lista_alumnos_gestib.lista:

        # No tratar datos de alumnos que no se encuentren en la lista de estudios
        if alumno.estudios not in LISTA_DE_ESTUDIOS_ACOTADOS:
            continue

        # Añadir a la lista de cursos(grupos) para luego poder crear las cabeceras        
        lista_cursos.add(alumno.curso+alumno.grupo[0].upper())
        # Añadir al listado de unidades organizativas  
        lista_uorg.add(alumno.uorg)
           
        encontrado = 0
        #buscar por Expediente
        indice_encontrado = usuarios_google.buscarExpediente(alumno.expediente)
            
        if indice_encontrado == -1: # no se ha encontrado el usuario. Se añade al fichero usuarios_bloque,
                            # grupos_bloque y a la lista_usuarios en memoria

            cont_nuevos += 1
            #generamos la nueva contraseña
            alumno.password = generaPassword()

            # Comprobar que el email no está repetido
            if usuarios_google.buscarEmail(alumno.email) > 0: #el email lo usa otro usuario
                # se genera un nuevo email con la segunda función
                alumno.email = generaEmail2(alumno.nombre, alumno.apellidos)
                #print(alumno.nombre, alumno.apellidos) 
            # Se vuelve a buscar por si el segundo email también está usado
            if usuarios_google.buscarEmail(alumno.email) == -1: # se puede usar este email
            
                # Se escribe la entrada en el fichero
                escribeUsuarioFichero(alumno, "usuarios_bloque.csv")

                # Se escribe la entrada en el fichero
                escribeMiembroGrupo(alumno)

                # Insertar en la lista de usuarios_google
                us = User(alumno.nombre, alumno.apellidos, alumno.email,
                          alumno.uorg,1,alumno.expediente) # validado
                usuarios_google.insertar(us)   

                # Generar una entrada en el fichero de información para los tutores
                n_archivo = alumno.curso+alumno.grupo[0].upper()+".txt"
                escribeInformacionNuevos(n_archivo,alumno)
                
            else:
                print("Error, email repetido: {} {} {} {} NO SE PROCESA".format( alumno.nombre,alumno.apellidos,
                      alumno.curso, alumno.expediente))
                                      
                #Se escribe en el fichero de repetidos para su revisión
                escribeUsuarioFichero(alumno, "usuarios_repetidos.csv")

        else:  # El nombre o expediente sí existen

            #usuario = usuarios_google.lista[indice_encontrado]
            usuario = usuarios_google.obtenerIndice(indice_encontrado)
            
            # Confirmar el usuario
            usuarios_google.validar(indice_encontrado)
            cont_validados += 1

            # Actualizar la información
            if(alumno.uorg != usuario.uorg or  #Si ha cambiado de curso hay que cambiar la unidad organizativa
               alumno.nombre != usuario.nombre or   #Corrige nombre y apellidos
               alumno.apellidos != usuario.apellidos):  
                                                               
                cont_actualizados += 1
                # Alumno ya tiene calculada la nueva unidad organizativa 

                #Escribimos el alumno al fichero de nuevos para actualizar la uorg
                alumno.email = usuario.email # Cnserbamos el email de workspace
                
                alumno.password = "****" # nos aseguramos que no se cambie la password

                #escribimos la actualización en el fichero
                escribeUsuarioFichero(alumno, "usuarios_bloque.csv")

#####################################################
#                   noValidados()
# Escribe un fichero de usuarios(usuarios_baja.txt) que
# ya no figuran en el gestib. Sólo se escriben usuarios
# que pertenecen a unidades organizativas procesadas
#
#####################################################
def noValidados():
    n = 0
    for usuario in usuarios_google._lista:
        if usuario.uorg in lista_uorg:
            if usuario.validado == 0:
                n += 1
                #if usuario.expediente != "":
                #formatear informacion
                nombre = usuario.nombre+" "+ usuario.apellidos
                linea = "{0:30}{1:35}{2:15}"
                linea = linea.format(nombre,usuario.email,usuario.uorg)
                f= open("usuarios_baja.txt","a")
                f.write(linea+"\n")
                f.close()

                #print(linea)

#####################################################
#                         
#
#                      MAIN
#
#
#####################################################
cont_nuevos = 0
cont_actualizados = 0
cont_validados = 0

#lista de usuarios consola
usuarios_google = ListaUsers()
#lista de alumnos getib
lista_alumnos_gestib = ListaAlumnos()

# Lista cursos para generar las cabeceras de los ficheros de contactos y nombres de grupos
# Se crea en la lectura del fichero de datos del getib
lista_cursos = set()
# Lista de unidades organizativas para generar un listado de todas
# Se crea en la lectura del fichero de datos del getib
lista_uorg = set()

if not path.exists("config.ini"):
    print("No exixte el fichero config.ini")
    print("\n")
    exit()

# Cargar las configuraciones del fichero config.ini
config = configparser.ConfigParser()
config.read('config.ini')

DOMINIO = config['MAIN']['DOMINIO']
est = config['MAIN']['LISTA_ESTUDIOS'] 
LISTA_DE_ESTUDIOS_ACOTADOS= est.split(",")

FORZAR_CAMBIAR_PASSWORD = config['MAIN']['CAMBIAR_PASSWD']
DIRECTORIO_CONTACTOS = config['MAIN']['DIRECTORIO_CONTACTOS']
DIRECTORIO_INFORMACION = config['MAIN']['DIRECTORIO_INFORMACION']
UNIDAD_ORGANIZATIVA_PADRE = config['MAIN']['UNIDAD_ORGANIZATIVA_PADRE']

print("\n")

# Borrar los archivos de ejecuciones anteriores
borrarArchivos()

if sys.argv[1] == "-b":
    exit()

if len(sys.argv) != 3:
    print("Uso: \n -a actualizar usuarios \n -g regenerar grupos \n -e regenera expedientes\n")
    exit()

# Comprobar que existe el fichero de datos del gestib
dades_gestib = sys.argv[2]
if not path.exists(dades_gestib):
    print("No exixte el fichero: ",dades_gestib)
    print("\n")
    exit()

# Opción actualizar usuarios
if sys.argv[1] == "-a":
    cargarUsuariosGoogle()
    cargaFicheroGestib(dades_gestib)    
    actualizarUsuarios()
    generaListadoUorg()
    generaListadoGrupos()
    noValidados()
    print("\n\nResumen:")
    print("Se han añadido {} usuarios nuevos al fichero usuarios_bloque.csv".format( cont_nuevos ))
    print("Se han añadido {} actualizaciones al fichero usuarios_bloque.csv".format(cont_actualizados))
# Opción generar grupos
elif sys.argv[1] == "-g":
    cargarUsuariosGoogle()
    cargaFicheroGestib(dades_gestib)
    generaGrupos()
# Opcion regenerar expedientes
elif sys.argv[1] == "-e":
    cargarUsuariosGoogle()
    cargaFicheroGestib(dades_gestib)
    actualizarExpedientes()
# Opcion regenerar informacion
elif sys.argv[1] == "-i":
    cargarUsuariosGoogle()
    cargaFicheroGestib(dades_gestib)
    actualizarInformacionEmail()

elif sys.argv[1] == "-p":
    cargarUsuariosGoogle()
    cargaFicheroGestib(dades_gestib)
    muestrasGeneracionEmail()

elif sys.argv[1] == "-d":
    cargarUsuariosGoogle()
    cargaFicheroGestib(dades_gestib)
    generarDatosFalsos()

#Opcion incorrecta
else:
    print("Parámetros incorrectos")
    print("Uso: \n -a actualizar usuarios \n -g regenerar grupos \n -e regenera expedientes\n")
    exit()
