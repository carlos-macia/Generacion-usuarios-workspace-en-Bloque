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
from os import listdir
from shutil import copy
from shutil import rmtree
from random import randint
from datetime import datetime
from datetime import timedelta
from time import ctime
class User:
    """
    Clase para guardar los datos de usuario que se 
    encuentran en el fichero que descargamos de la
    consola de Workspace
    """
    def __init__(self, nombre,apellidos, email, uorg,
                 validado, expediente):
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.uorg = uorg
        self.password = "****"
        self.validado = validado
        self.expediente = expediente

class ListaUsers:
    """
    Clase para manejar una lista de usuarios(Class User) 
    """
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
            #log.imprimir ("Alerta! Nombre repetido: ", nombre, apellidos)
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

class ClassAlumno:
    """
    Clase para guardar los datos del alumno que se 
    encuentran en el Gestib
    """
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


class ListaAlumnos:
    """
    Clase para construir una lista de alumnos que se 
    encuentran en el Gestib
    """
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
            #log.imprimir ("Alerta! Nombre repetido: ", nombre, apellidos)
            ret = -2
        return ret
    
    def obtenerIndice(self,indice):
        return (self.lista[indice])

class Log:    
    def __init__(self):
        self.fichero_log = "genera.log"
        
    def imprimir(self,linea):
       # Añadir al fichero
        f= open(self.fichero_log,"a")
        f.write(linea+"\n")
        print(linea)
        f.close()

def generaEmail(nombre, apellidos):
    """
    Seleciona la función generadora de email según el método
    """
    if METODO_GENERA_EMAIL == "1":
        return generaEmail1(nombre,apellidos)
        print (METODO_GENERA_EMAIL)
    else:
        return generaEmail3(nombre, apellidos)


def generaEmail1(nombre, apellidos):
    """
    Genera el email a partir del nombre y los apellidos
    Método principal
    """
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

def resumeApellidos(apellidos):
    """
    Acorta los apellidos largos
    """
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

def generaEmail2(nombre,apellidos):
    """
    Genera el email a partir del nombre y los apellidos
    Método secundário del método 1
    """
    
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

def extraerPrimeraSilaba(cadena):
    """
    Extrae la primera (sílaba) de una cadena
    """
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

def generaEmail3(nombre,apellidos):
    """
    Genera el email a partir del nombre y los apellidos
    método 2 de config
    """
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
    email =  "a" + nombre + apellidos

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

def generaEmail4(nombre,apellidos):
    """
    Genera el email a partir del nombre y los apellidos
    Cuarto  método. Complementa al 3 cuando hay repetidos 
    """
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
    if len(partes)>1:    
        email =  "a" + nombre + apellidos + partes[1][0]
    else:
        email =  "a" + nombre + apellidos + "2"

        
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


def eliminaEspacios(cadena):
    """
    Elimina los espacios, tabuladores y retorno de carrro
    de una cadena
    """
    cadena = cadena.replace(" ","")
    cadena = cadena.replace("\t","")
    cadena = cadena.replace("\n","")
    cadena = cadena.replace("\r","")
    return (cadena)
    
def eliminaSimbolos(cadena):
    """
    Elimina los símbolos de una cadena
    """
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

def eliminaAcentos(cadena):
    """
    Elimina los acentos de una cadena ( MINÚSCULAS ),
    abiertos y cerrados
    """
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

def generaUnidadOrganizativa(estudios,curso,grupo):
    """
    Forma el nombre de la unidad organizativa
    """  
    uorg = "/"+ UNIDAD_ORGANIZATIVA_PADRE +"/{0}/{1}{2}"
    uorg = uorg.format(estudios, curso, grupo.upper())
    #uorg = uorg.replace(".","") # quita el punto de batx.
    return uorg


def cargarUsuariosGoogle():
    """
    Carga la información de los usuarios de la 
   consola de Google que se encuentran en el 
   fichero users.cvs en la lista usuarios_google
    """
    with open('users.csv', encoding="utf8") as f:
        for linea in f:
            aux_user=linea.split(',');
            if aux_user[0] == "First Name [Required]":
                continue
            usuario = User(aux_user[0],aux_user[1],aux_user[2],
                           aux_user[5], 0, aux_user[16] ) #16 expediente
            usuarios_google.insertar(usuario)            
        
def generaPassword():
    """
    Genera un password alfanumerico de 8 caracteres
    """
    #caract=string.ascii_letters
    caract="ABCDEFGHJKNMPQRSTUVWXYZabcdefghjknmpqrstuvxyz"
    digitos = "23456789"
    
    password = ("").join(random.choice(caract+digitos)for i in range(2))

    #caract= string.ascii_letters + string.digits
    
    password += ("").join(random.choice(caract+digitos+digitos+digitos)for i in range(3))

    #caract=  string.digits
    
    password += ("").join(random.choice(digitos)for i in range(1))

    #caract=string.ascii_letters
    password += ("").join(random.choice(caract+digitos+digitos)for i in range(2))

    return(password)

def escribeUsuarioFichero(alumno, fichero):
    """
    Escribe el nuevo usuario o actualización en el 
   fichero de salida usuarios_bloque.csv
    """
    # Formatear la línea
    linea = "{0},{1},{2},{3},,{4},,,,,,,,,,,{5},,,,,,,,,{6},"
    linea = linea.format(alumno.nombre ,alumno.apellidos, alumno.email,
                         alumno.password, alumno.uorg, alumno.expediente,
                         FORZAR_CAMBIAR_PASSWORD)

    # Añadir al fichero
    f= open(fichero,"a")
    f.write(linea+"\n")
    f.close()

def escribeMiembroGrupo(alumno):
    """
    Escribe una entrada de miembro de grupo en el fichero
    grupos_bloque.cvs
    """
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

def escribeInformacionNuevos(fichero, alumno):
    """
    Escribe una entrada de usuario y contraseña en el 
    fichero correspondiente dentro del directorio 
    Información
    """
    #formatear informacion
    nombre = alumno.nombre+" "+ alumno.apellidos
    #linea = "{0:40}{1:35}{2:10}{3:8}{4:2}"
    linea = "{0},{1},{2},{3},{4}"
    
    linea = linea.format(nombre,alumno.email, alumno.password,alumno.curso,alumno.grupo)

    f= open(DIRECTORIO_INFORMACION+ "/" + fichero,"a")
    f.write(linea+"\n")
    f.close()

def escribeContacto( alumno):
    """
    genera una entrada de contacto en el fichero
    cvs correspondiente
    """
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

def escribeContactoProfessor( nombre, apellidos, email):
    """
    genera una entrada de contacto en el fichero
    cvs correspondiente
    """
    #formatear la etiqueta de contacto
    etiqueta = "Claustre"

    linea = "{0} {1},{0},,{1},,,,,,,,,,,,,,,,,,,,,,,,,{2} ::: * myContacts,* ,{3}"
    linea = linea.format(nombre,apellidos,etiqueta,email)

    fichero = "contactos_claustre.csv"

    #f= open(DIRECTORIO_CONTACTOS+ "/" + fichero,"a")
    
    f= open( fichero,"a")
    
    f.write(linea+"\n")
    f.close()

def GeneraContactosProfessors():
    """
    """
    with open('users.csv', encoding="utf8") as f:
        for linea in f:
            aux_user=linea.split(',')
            if aux_user[0] == "First Name [Required]":
                continue
            
            uorg= aux_user[5]
            uorg_split = uorg.split('/')
            if uorg_split[1] == "claustre":
                if uorg != "/claustre/antic professorat centre":     
                    nombre = aux_user[0]
                    apellidos = aux_user[1]
                    email = aux_user[2]
                    escribeContactoProfessor(nombre, apellidos, email)

def existeArchivosEntrada(dades_gestib):
    existe = 1
    # Comprobar que existe el fichero de datos del gestib
    dades_gestib = sys.argv[2]
    if not path.exists(dades_gestib):
        linea = "No exixte el fichero " + dades_gestib
        log.imprimir(linea)
        log.imprimir("\n")
        existe = 0
    # Comprobar que tiene extensión csv
    elif dades_gestib[-3:] != "csv":
        linea = "\nEl archivo {} debe conversitrse a formato csv, ".format(dades_gestib)
        log.imprimir(linea)
        log.imprimir("\n")
        existe = 0
    else:
        fecha_archivo = datetime.strptime(ctime(path.getctime(dades_gestib)),"%a %b %d %H:%M:%S %Y")
        limite_anterior = datetime.now()-timedelta(hours=1)
        if fecha_archivo < limite_anterior:
            log.imprimir("ALERTA! El archivo {} está caducado".format(dades_gestib))
            log.imprimir("Debe bajar el archivo de nuevo desde Gestib\n")
            #existe = 0

    # Comprobar que existe el fichero users.csv
    if not path.exists("users.csv"):
        log.imprimir("No exixte el fichero users.csv\n")
        existe = 0
    else:
        fecha_archivo = datetime.strptime(ctime(path.getctime("users.csv")),"%a %b %d %H:%M:%S %Y")
        limite_anterior = datetime.now()-timedelta(hours=1)
        if fecha_archivo < limite_anterior:
            log.imprimir("ALERTA! El archivo users.csv está caducado")
            log.imprimir("Debe bajar el archivo de nuevo desde Workspace\n")
            #existe = 0        
                
    return existe

def borrarArchivos():
    """
    Borrar archivos de de salida de ejecuciones anteriores
    """

    archivos = [ 'usuarios_bloque.csv', 'grupos_bloque.csv', 'nuevos_contactos.csv',
                 'usuarios_repetidos.csv','listado_uorg.txt', 'listado_grupos.txt',
                 'usuarios_baja.txt', 'genera.log']

    # Borrar archivos
    for file in archivos:
        if path.exists(file):
            remove(file)

    # Borrar el directorio de contactos y su contenido
    if path.exists(DIRECTORIO_CONTACTOS):
        rmtree(DIRECTORIO_CONTACTOS)

    # Borrar el directorio de información y su contenido
    if path.exists(DIRECTORIO_INFORMACION):
        rmtree(DIRECTORIO_INFORMACION)

def archivar():
    
    ruta = "Archivo/Ficheros_"
    
    fecha = datetime.now()
    ruta += fecha.strftime('%d-%m-%Y_%H-%M')
    
    if not path.exists("Archivo"):
        mkdir("Archivo")
    
    if not path.exists(ruta):
        mkdir(ruta)
    
    if path.exists(DIRECTORIO_CONTACTOS):
        dir_destino = ruta+"/"+DIRECTORIO_CONTACTOS
        if not path.exists(dir_destino):
            mkdir(dir_destino)
        lista_ficheros = listdir(DIRECTORIO_CONTACTOS)
        for fichero in lista_ficheros:
            full_file_name = path.join(DIRECTORIO_CONTACTOS, fichero)
            copy(full_file_name , dir_destino)
    
    if path.exists(DIRECTORIO_INFORMACION):
        dir_destino = ruta+"/"+DIRECTORIO_INFORMACION
        if not path.exists(dir_destino):
            mkdir(dir_destino)
        lista_ficheros = listdir(DIRECTORIO_INFORMACION)
        for fichero in lista_ficheros:
            full_file_name = path.join(DIRECTORIO_INFORMACION, fichero)
            copy(full_file_name , dir_destino)
    """
    archivos = [ 'usuarios_bloque.csv', 'grupos_bloque.csv', 'nuevos_contactos.csv',
                 'usuarios_repetidos.csv','listado_uorg.txt', 'listado_grupos.txt',
                 'usuarios_baja.txt', 'genera.log']
    """
    excluir = ['genera.py','README.txt','LICENSE']
    
    archivos = listdir(".")

    for fichero in archivos:
        if fichero in excluir:
            continue
        if path.isfile(fichero):
            copy(fichero , ruta)

    
def generaCabeceraUsuarios(fichero):
    """
    Escribe la cabecera del archivo usuarios_bloque.csv
    """

    linea = "First Name [Required],Last Name [Required],Email Address [Required],Password [Required],Password Hash Function [UPLOAD ONLY],Org Unit Path [Required],New Primary Email [UPLOAD ONLY],Recovery Email,Home Secondary Email,Work Secondary Email,Recovery Phone [MUST BE IN THE E.164 FORMAT],Work Phone,Home Phone,Mobile Phone,Work Address,Home Address,Employee ID,Employee Type,Employee Title,Manager Email,Department,Cost Center,Building ID,Floor Name,Floor Section,Change Password at Next Sign-In,New Status [UPLOAD ONLY]"
    f= open(fichero,"a")
    f.write(linea+"\n")
    f.close()

def generaCabeceraGrupos():
    """
    Escribe la cabecera del archivo grupos_bloque.csv
    """
    linea = "Group Email [Required],Member Email,Member Name,Member Role,Member Type"
    f= open("grupos_bloque.csv","a")
    f.write(linea+"\n")
    f.close()

def generaCabeceraContactos():
    """
    Escribe la cabecera del archivo de contactos
    el nombre de este archivo coincide con el nombre
    del curso + .csv
    """
    linea = "Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Language,Photo,Group Membership,E-mail 1 - Type,E-mail 1 - Value"
        
    for curso in lista_cursos:
        cursocsv = curso + ".csv"
        f= open(DIRECTORIO_CONTACTOS+"/"+cursocsv,"a")
        f.write(linea+"\n")
        f.close()

def generaListadoUorg():
    """
    Escribe un listado de unidades organizativas en el 
    fichero listado_uorg.txt   
    """ 
    l = sorted(lista_uorg)    
    for uo in l:
        f= open("listado_uorg.txt","a")
        f.write(uo+"\n")
        f.close()

def generaListadoGrupos():
    """
    Escribe un listado de los grupos en el fichero
    listado_grupos.txt 
    """
    l = sorted(lista_cursos)    
    cont = 1
    for curso in l:
        f= open("listado_grupos.txt","a")
        f.write(curso+"\n")
        f.close()

def cargaFicheroGestib(dades_gestib):
    """
    Carga el fichero cvs que contiene los datos del  
    Gestib a la lista_alumnos_gestib 
    """
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
               log.imprimir("Error de formato. Línea: {:15} NO SE PROCESA".format(cont))
               error += 1
               continue #no se procesa la línea
            # El primer y último campo deben ser dígitos 
            elif not(aux_user[0].isdigit()) or not(aux_user[6].isdigit()):
               log.imprimir("Error de formato. Línea: {:15} NO SE PROCESA (Dígitos)".format(cont))
               error += 1
               continue  #no se procesa la línea
    
            # Crear el alumno con los datos leídos
            alumno = ClassAlumno(aux_user[0],aux_user[1],aux_user[2],aux_user[3],
                                 aux_user[4],aux_user[5], aux_user[6] )

            # Controlar expedientes repetidos 
            if lista_alumnos_gestib.esExpedienteRepetido(alumno.expediente) > 0:
                log.imprimir("Error expediente {} repetido. Línea: {:15} NO SE PROCESA".format(alumno.expediente, cont))
                error += 1
                continue
                
            # Añadir a la lista de alumnos gestib
            lista_alumnos_gestib.insertar(alumno)
            
    if error > 0:
        log.imprimir("\nALERTA! Se han descartado {} líneas erroneas del fichero {}".format(error,dades_gestib))
        #exit()                

def muestrasGeneracionEmail():
    """
    Muestra las tres combinaciones de email que
    se pueden generar
    """
    for alumno in lista_alumnos_gestib.lista:

        # No tratar datos de alumnos que no se encuentren en la lista de estudios
        if alumno.estudios not in LISTA_DE_ESTUDIOS_ACOTADOS:
            continue

        encontrado = 0
        log.imprimir("\n")
        log.imprimir(alumno.nombre + " " + alumno.apellidos)
        log.imprimir("{:4} Versión 1\t\t{:30}".format(len(alumno.email)-21,alumno.email))
        
        email = generaEmail2(alumno.nombre, alumno.apellidos)
        log.imprimir("{:4} Versión 2\t\t{:30}".format(len(email)-21, email))
        
        email = generaEmail3(alumno.nombre, alumno.apellidos)
        log.imprimir("{:4} Versión 3\t\t{:30}".format(len(email)-21, email))
        
        indice_encontrado = usuarios_google.buscarExpediente(alumno.expediente)
        if  indice_encontrado != -1:
            log.imprimir("Actual Workspace\t{:30}".format(usuarios_google.obtenerIndice(indice_encontrado).email))        

def generarDatosAleatorios():
    """
    Para pruebas y demos públicas
    Genera un ficheo de gestib ficticio combinando
    aleatoriamente nombres, apellidos, y demás informació
    del fichero de gestib.
    """
    if path.exists("datos_aleatorios.csv"):
            remove("datos_aleatorios.csv")

    
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
           
        alumno.expediente = "3" + alumno.expediente + str(randint(0,9))
        linea = "{0},{1},{2},{3},{4},{5},{6}"
        linea = linea.format( cont, alumno.apellidos, alumno.nombre,
                             alumno.estudios,alumno.curso, alumno.grupo, alumno.expediente)

        f= open("datos_aleatorios.csv","a")
        f.write(linea+"\n")
        f.close()
        cont += 1
            
def actualizarExpedientes():
    """
    Lee el fichero dadesGestib.cvs, busca por nombre
    y actualiza los numeros de expediente en el fichero
    de salida usuarios_bloque.csv
    """
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
            log.imprimir("Nombre repetido {} {} {} - NO SE PROCESA".format(
                   alumno.nombre, alumno.apellidos, alumno.email))
       
    log.imprimir("Se han actualizado {} expedientes".format(actualizados))
    
def generaGrupos():
    """
    Genera todos los grupos y contactos
    """
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
        
def actualizarUsuarios():
    """
    Lee el fichero dadesGestib.cvs y procesa la información.
    Si encuentra usuarios nuevos se añaden.
    Se actualiza la unidad organizativa, por ejemplo cambio de curso.
    NO SE REGENERAN TODOS LOS GRUPOS, pero sí se escriben las entradas
    sólo!! de los nuevos usuarios en el fichero de grupos_bloque.csv
    """
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
        # No tratar grupos sin letra asignada    
        if alumno.grupo == "-":
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
                # se genera un nuevo email con la segunda función según método
                if METODO_GENERA_EMAIL == "1":
                    alumno.email = generaEmail2(alumno.nombre, alumno.apellidos)
                else:
                    alumno.email = generaEmail4(alumno.nombre, alumno.apellidos)
                    
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
                n_archivo = alumno.curso+alumno.grupo[0].upper()+".csv"
                escribeInformacionNuevos(n_archivo,alumno)
                
            else:
                log.imprimir("Error, email repetido: {} {} {} {} NO SE PROCESA".format( alumno.nombre,alumno.apellidos,
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
            if(alumno.uorg.lower() != usuario.uorg.lower() or  #Si ha cambiado de curso hay que cambiar la unidad organizativa
               alumno.nombre != usuario.nombre or   #Corrige nombre y apellidos
               alumno.apellidos != usuario.apellidos):  
                                                               
                cont_actualizados += 1
                # Alumno ya tiene calculada la nueva unidad organizativa 

                #Escribimos el alumno al fichero de nuevos para actualizar la uorg
                alumno.email = usuario.email # Cnserbamos el email de workspace
                
                alumno.password = "****" # nos aseguramos que no se cambie la password

                #escribimos la actualización en el fichero
                escribeUsuarioFichero(alumno, "usuarios_bloque.csv")

def noValidados():
    """
    Mueve los usuarios que no figuran en el fichero del gestiv
    a la unidad organizativa exalumnes. Sólo se mueven usuarios
    que pertenecen a las unidades organizativas procesadas
    """
    global cont_exalumnes
    cont_exalumnes = 0
    for usuario in usuarios_google._lista:
        partes = usuario.uorg.split("/")
        if len(partes)>3:
            if partes[3] == "Exalumnes":
                estudios = "NoCambiar"
            else:
                estudios = partes[2]
        else:
            estudios = "NoTratar" 
        #if usuario.uorg in lista_uorg: #(ojo los grupos que no tienen alumnos nuevos)
                                       # CAMBIAR POR LISTA ESTUDIOS ACOTADOS
        if estudios in LISTA_DE_ESTUDIOS_ACOTADOS: 
            if usuario.validado == 0:
                cont_exalumnes += 1
                #usuario.uorg = UNIDAD_ORGANIZATIVA_PADRE + "/exalumnes"
                
                partes = usuario.uorg.split("/")
                usuario.uorg = "/" + partes[1] + "/" + partes[2] + "/" + "exalumnes"

                # Escribimos la actualización en el fichero
                # Polimorfismo Alumno, Usuario
                escribeUsuarioFichero(usuario, "usuarios_bloque.csv")
    if cont_exalumnes > 1:
        log.imprimir("ALERTA: Asegurate de tener las SUB-Unidades Organizativas de EXALUMNOS")


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
cont_exalumnes = 0
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

# log para guardar los mensajes de salida en fichero
log = Log()

# Comprobar que existe el fichero config.ini
if not path.exists("config.ini"):
    log.imprimir("No exixte el fichero config.ini")
    log.imprimir("\n")
    exit()

# Cargar las configuraciones del fichero config.ini
config = configparser.ConfigParser()
config.read('config.ini')

DOMINIO = config['MAIN']['DOMINIO']
est = config['MAIN']['LISTA_ESTUDIOS'] 
LISTA_DE_ESTUDIOS_ACOTADOS= est.split(",")

METODO_GENERA_EMAIL = config['MAIN']['METODO_GENERA_MAIL']
FORZAR_CAMBIAR_PASSWORD = config['MAIN']['CAMBIAR_PASSWD']
DIRECTORIO_CONTACTOS = config['MAIN']['DIRECTORIO_CONTACTOS']
DIRECTORIO_INFORMACION = config['MAIN']['DIRECTORIO_INFORMACION']
UNIDAD_ORGANIZATIVA_PADRE = config['MAIN']['UNIDAD_ORGANIZATIVA_PADRE']
AUTOARCHIVAR = config['MAIN']['AUTOARCHIVAR']

print("\n")

ok = 0
if len(sys.argv) > 1:
    # Opción borrar archivos
    if sys.argv[1] == "-b":
        borrarArchivos()
        ok = 1
    # Opción archivar
    elif sys.argv[1] == "-arch":
        ok = 1
        archivar()   
    elif len(sys.argv) > 2:
        dades_gestib = sys.argv[2]
        # Opción actualizar usuarios
        if sys.argv[1] == "-a":
            ok = 1
            if existeArchivosEntrada(dades_gestib) == 1:
                borrarArchivos()
                cargarUsuariosGoogle()
                cargaFicheroGestib(dades_gestib)    
                actualizarUsuarios()
                generaListadoUorg()
                generaListadoGrupos()
                noValidados()
                if AUTOARCHIVAR == "True":
                    archivar()
                log.imprimir("\nResumen:")
                log.imprimir("Se han añadido {} usuarios nuevos al fichero usuarios_bloque.csv".format( cont_nuevos ))
                log.imprimir("Se han añadido {} actualizaciones al fichero usuarios_bloque.csv".format(cont_actualizados))
                log.imprimir("{} usuarios pasaron a la unidad organizativa exalumnes".format(cont_exalumnes))
        # Opción generar grupos
        elif sys.argv[1] == "-g":
            ok = 1
            if existeArchivosEntrada(dades_gestib) == 1:    
                borrarArchivos()
                cargarUsuariosGoogle()
                cargaFicheroGestib(dades_gestib)
                generaGrupos()
        # Opcion regenerar expedientes
        elif sys.argv[1] == "-e":
            ok = 1
            if existeArchivosEntrada(dades_gestib) == 1:
                borrarArchivos()
                cargarUsuariosGoogle()
                cargaFicheroGestib(dades_gestib)
                actualizarExpedientes()
        # Opción muestras email
        elif sys.argv[1] == "-p":
            ok = 1
            if existeArchivosEntrada(dades_gestib) == 1:
                borrarArchivos()
                cargarUsuariosGoogle()
                cargaFicheroGestib(dades_gestib)
                muestrasGeneracionEmail()
        # Opcion Generar datos aleatorios        
        elif sys.argv[1] == "-d":
            ok = 1
            if existeArchivosEntrada(dades_gestib) == 1:
                borrarArchivos()
                cargarUsuariosGoogle()
                cargaFicheroGestib(dades_gestib)
                generarDatosAleatorios()
        # Opcion Generar datos aleatorios        
        elif sys.argv[1] == "-cp":
            ok = 1
            if existeArchivosEntrada(dades_gestib) == 1:
                borrarArchivos()
                GeneraContactosProfessors()
                #cargarUsuariosGoogle()
                #cargaFicheroGestib(dades_gestib)
                #generarDatosAleatorios()

if ok == 0:
    # Imprimir opciones línea de comandos
    log.imprimir("Parámetros incorrectos\n")
    log.imprimir("\t Uso: \n\t     $python genera.py [opcion] <fichero_gestib.csv>")
    log.imprimir("\n\t Opciones: \n\t     -a actualizar usuarios \n\t     -g generar grupos \n")
    