# -*- coding: cp1252 -*-
#Simulación de ventilación de una mina.
#El programa en resumen lo que hace es tomar los datos entregados por el
#usuario para poder hacer una distribución eficiente haciendo uso del método Iterativo
#de Hardy Cross para el cálculo del caudal en cada resistencia.
#La salida corresponde a el caudal distribuido para cada resistencia del
#sistema de ventilación a considerar-
#27 de noviembre, 2017

#Bloque de definición.

#Módulos a importar.
import numpy as np
import os.path as path
import copy

#Definición de funciones.

#Entrada: Archivo de texto
#Verificamos si pasa la compatibilidad, en caso contrario volverá a reiniciar automáticamente.
#Denominamos en este programa como switch a aquellos parametros con contenido no relevante,
#pero que sirven para poder ejecutar funciones.
def reinicioAutomatico(switch):
    global listaResistencias
    global listaGalerias
    global puntoEntradas
    global puntoSalidas
    global nombreDeArchivo
    i=0
    while i==0:
        nombreDeArchivo=raw_input("Ingrese nombre de archivo, agregar extensión de formato:")
        if path.exists(nombreDeArchivo)==True:
            listaResistencias=[]
            listaGalerias=[]
            archivo=open(nombreDeArchivo,"r")
            verificador1=ordenarDatos(archivo)
            if verificador1=="Verdadero":
                verificador2=verificarCompatibilidad(listaResistencias,listaGalerias)
                if verificador2=="Verdadero":
                    archivo.close()
                    i+=1
        else:
            print ("Nombre de archivo inubicable.")
            continue
#Salida:Datos ordenados en listas de no haber error en el formato del archivo.
    
#Entrada: Cada línea del archivo.
#Tomar el texto e ingresarlo a dos listas.
def ordenarDatos(archivo):
    global listaResistencias
    global listaGalerias
    for linea in archivo:
        linea=linea.strip("\n")
        if len(linea)==2 and linea!="":
            listaGalerias.append(linea)
        elif len(linea)>=11:
            if "," in linea:
                linea=linea.split(" ")
                if len(linea)==3:
                    linea.append(linea[2].split(",")[0])
                    linea.append(linea[2].split(",")[1])
                    linea.pop(2)
                    listaResistencias.append(linea)
        elif len(linea)==0:
            continue
        else:
            print ("Error en Resistencias y/o Galerias:")
            print ("El archivo debe tener por contenido: R(Mayuscula)-Numero,")
            print ("Valor R, Letra separado por coma de Numero.")
            return "Reiniciar"
            break        
    return "Verdadero"
#Salida: Listas con el contenido del archivo separado según si son galerías o
#las resistencias entre ellas. En el segundo caso, serán listas de listas.

 
#Entrada: Archivo 
def verificarCompatibilidad(listaResistencias,listaGalerias):
#Comparación de strings para ver si el texto ingresado tiene el formato correcto
#para ejecutar el programa y si tiene los datos necesarios.
    letraInicial=listaGalerias[0][0]
    i=0
    while i<len(listaGalerias):
        valorVerificar=listaGalerias[i]
        if valorVerificar[0]==letraInicial and valorVerificar[1].isdigit()==True:
            i+=1
        else:
            print ("Error en Galerias:")
            print ("El archivo debe seguir un formato LETRA - todas iguales - unido a un NUMERO")
            return "Reiniciar"
            break
    i=0
    while i<len(listaResistencias):
        primeraCadena=listaResistencias[i][0]
        segundaCadena=listaResistencias[i][1]
        terceraCadena=listaResistencias[i][2]
        cuartaCadena=listaResistencias[i][3]
        if (primeraCadena[0]=="R" and primeraCadena[1].isdigit()==True) and (segundaCadena.isdigit()==True and float(segundaCadena)>0) and (terceraCadena[0]==letraInicial and terceraCadena[1].isdigit()==True) and (cuartaCadena[0]==letraInicial and cuartaCadena[1].isdigit()==True):
            i+=1
        else:
            print ("Error en Resistencias y/o Galerias:")
            print ("El archivo debe tener por contenido: R(Mayuscula)-Numero,")
            print ("Valor R, Letra separado por coma de Numero.")
            return "Reiniciar"
            break
    return "Verdadero"
#Salida: Listas aprobadas con el contenido del archivo separado según si son galerías o
#las resistencias entre ellas.

#Entrada: lista_Resistencias, la cual nos servirá de guía para recorrer la lista_Resistencia.
def formarMallas(lista):
#Ya la lista creada, se ordenan según a que malla de ventilación pertenece cada resistencia
#para esto crearemos una lista que las contenga.
    global listaMallas
    global listaResistencias
    global listaGalerias
    global resistenciasPorNodos
#Calcularemos el total de mallas que debemos de obtener.
    totalMallas=int(len(listaResistencias))-(int(len(listaGalerias))-1)
#Elegiremos un nodo de la listaGalerias, él nos servirá para recorrer la listaResistencias.
#Duplicamos lista para conservar información.
    listaGalerias2=listaGalerias[:]
    listaResistencias2=listaResistencias[:]
    while len(listaMallas)!=totalMallas:
        for nodo in listaGalerias2:
#Agregaremos a lista vacía inicio todos las resistencias que contengan la galería elegida. 
            inicio=[]
            for resistencia in listaResistencias2:
                if nodo in resistencia:
                    inicio.append(resistencia)
#Procederemos a verificar primero si el nodo inicial puede formar mallas de tres o cuatro nodos.
#Esto para mallas ubicadas en esquinas.            
            if len(inicio)==2:
#Crearemos una lista con todos los nodos que sean diferentes al nodo elegido y que estén en inicio.
#Esto para tener valores más al alcance para efectuar condiciones. Por esto será una lista de strings.           
                inicioNodos=[]
                for nodosIniciales in inicio:
                    for galeria in nodosIniciales[2:4]:
                        if galeria!=nodo:
                            inicioNodos.append(galeria)
                mallaInicial=[]        
#Ahora veremos para todas las resistencias que no están en inicio y que tengan un nodo en común
#con la resistencia, siendo diferente al elegido en principio.                
                for elemento in inicio:
                    mallaInicial.append(elemento)
                for resistencia in inicioNodos:
                    for otraResistencia in listaResistencias2:
                        if resistencia in otraResistencia[2:4] and nodo not in otraResistencia[2:4]:
                            mallaInicial.append(otraResistencia)
#Estamos listos con esta información para poder obtener mallas de tres resistencias.
#Escogemos los nodos diferentes respecto del nodo inicial,luego buscamos una resistencia
#que los contenga a ambos. Esta será nuestra primera malla.
                for restoResistencias in listaResistencias2:
                    for elemento in inicioNodos:
                        for otroElemento in inicioNodos:
                            if otroElemento!=elemento and elemento in restoResistencias and otroElemento in restoResistencias:
                                for elemento in inicio:
                                    listaResistencias2.remove(elemento)
                                inicio.append(restoResistencias)
                                listaMallas.append(inicio)
                                mallaInicial=[]
                                inicioNodos=[]
                                inicio=[]
#Si no se realizó el proceso anterior, el contenido debe de mantenerse intacto.
                if len(inicio)==2:                
#Sabemos que una malla en sus esquinas, por nodo tendrá sólo dos uniones. Podríamos realizar
#este análisis para verificar que existan mallas de 4 nodos y que se ubiquen en esquinas.
#Escogeremos una resistencia en mallaInicial que no esté en inicio.
                    for restoResistencias in listaResistencias2:
                        if inicioNodos[0] in restoResistencias and restoResistencias not in inicio:
                            for nodos in restoResistencias[2:4]:
                                if nodos!=inicioNodos[0]:
                                    for restoResistencias2 in listaResistencias2:
                                        if restoResistencias2!=restoResistencias and inicioNodos[1] in restoResistencias2 and nodos in restoResistencias2:
                                            for elemento in inicio:
                                                listaResistencias2.remove(elemento)
                                            inicio.append(restoResistencias2)
                                            inicio.append(restoResistencias)
                                            listaMallas.append(inicio)
                                            mallaInicial=[]
                                            inicio=[]
#Salida:Resistencias agrupadas en mallas (lista de listas).

#Entrada: puntosEntradas y puntosSalidas, lista vacía.
def ingresarDatos(switch):
#Ingrearemos datos de entrada para valores de caudal así como de salida.
    global caudalEntrantes
    global puntoInicios
    i=0
    while i==0:
        valor=raw_input("Agregue punto donde ingresa caudal:")
        valor2=raw_input("Señale valor de caudal, volumen por cada segundo:")
        if valor in listaGalerias:
            if any(elemento.isalpha()==True for elemento in valor2):
                print ("Ingrese valor numero con o sin decimales para caudal.")
                continue
            elif valor2=="":
                print ("Ingrese valor numérico.")
                continue
            else:
                caudalEntrantes=float(valor2)
                puntoInicios.append(valor)
                break
        else:
            print ("Verifique que su valor para nodos exista.")
            continue
            
#Salida:Lista con nodo de entrada de caudal y valor. 
        
#Entrada: listaMallas
def cambioDeSignoYSuponerDistribucionDelCaudal(listaMallas):
#Función que supone diferentes valores de caudales distribuidos por ramal o resistencia.
    global listaGalerias
    global listaResistencias
    global caudalEntrantes
    global puntoInicios
    global matrizCaudalesSupuestos
    global matrizSignos
    global valoresResistencias
    global interseccion
#En inicio, recuperaremos los valores de resistencia de listaMallas en un array como flotantes.
    valoresResistencias=[]
    arrayMalla=np.array(listaMallas)
    for fila in arrayMalla:
        valoresResistencias.append(fila.flat[1::4])
    valoresResistencias=np.array(valoresResistencias)
    valoresResistencias=valoresResistencias.astype(float)
#Necesitamos conocer las intersecciones, para lo que las tendremos en una lista.
    intersecciones=[]
    for elemento in listaMallas:
        for resistencia in elemento:
            for otroElemento in listaMallas:
                if resistencia in otroElemento and ([resistencia[2],resistencia[3]] not in intersecciones and [resistencia[3],resistencia[2]] not in intersecciones) and otroElemento!=elemento:
                    intersecciones.append(resistencia[2:4])
#Crearemos un diccionario a partir con la cantidad de recurrencia de estas intersecciones.
    diccionarioIntersecciones=dict()
    for elemento in intersecciones:
        contador=0
        for elemento2 in listaMallas:
            for resistencias in elemento2:
                if elemento==resistencias[2:4]:
                    contador+=1
        diccionarioIntersecciones[tuple(elemento)]=contador
#Ahora crearemos una matriz para cambiar los signos.
    matrizSignos=np.ones(valoresResistencias.shape)
#Necesitamos conocer las posiciones de las intersecciones. Esto para el análisis matricial.
#A partir de esto modificaremos la matriz uno de modo que se obtenga una matriz cambio de signo.
#El cambio de signo será en lo posible alternado para los elementos de un vector, cuidando
#que para las intersecciones en cada malla se presente de signo diferente.
    diccionarioIntersecciones2=diccionarioIntersecciones.copy()
    i=0
    constante=1
    while i<len(listaMallas):              
        j=0
        while j<len(listaMallas[i]):
            if tuple(listaMallas[i][j][2:4]) in diccionarioIntersecciones2:
                if diccionarioIntersecciones2[tuple(listaMallas[i][j][2:4])]%2==0:
                    diccionarioIntersecciones2[tuple(listaMallas[i][j][2:4])]-=1
                    matrizSignos[i][j]=1
                    j+=1
                else:
                    matrizSignos[i][j]=-1
                    diccionarioIntersecciones2[tuple(listaMallas[i][j][2:4])]-=1
                    j+=1
            else:
                matrizSignos[i][j]*=constante
                constante*=-1
                j+=1
        i+=1
#Ahora debemos centrarnos en la suposición de los valores.Materia fundamental de esta función.
#Para listas más pequeñas la conservación del flujo es fácil de asegurar.
#Elegiremos un nodo de la listaGalerias, él nos servirá para recorrer la listaResistencias.
    resistenciasPorNodos=dict()
    for nodo in listaGalerias:
#Agregaremos a lista vacía inicio todos las resistencias que contengan la galería elegida. 
        inicio=[]
        for resistencia in listaResistencias:
            if nodo in resistencia:
                for nodos in resistencia[2:4]:
                    if nodos!=nodo:
                        inicio.append(nodos)
            resistenciasPorNodos[nodo]=inicio
#Ahora podemos saber por cuantos puntos se distribuye un caudal.
#Crearemos array con valores supuestos. Partiremos por duplicar un array, por las dimensiones.
    matrizCaudalesSupuestos=copy.copy(valoresResistencias)
#Empezaremos la lógica de la distribución del caudal.
    resistenciasUsadas=[]
    for nodo in puntoInicios:
        if resistenciasPorNodos[nodo]!=[]:
            caudalDistribuido=caudalEntrantes/len(resistenciasPorNodos[nodo])
            k=0
            while k<len(resistenciasPorNodos[nodo]):
                j=0
                while j<len(listaMallas):
                    i=0
                    while i<len(listaMallas[j]):
                        if ([nodo,resistenciasPorNodos[nodo][k]]==listaMallas[j][i][2:4] or [resistenciasPorNodos[nodo][k],nodo]==listaMallas[j][i][2:4]) and listaMallas[j][i] not in resistenciasUsadas:
                            matrizCaudalesSupuestos[j][i]=caudalDistribuido
                            if resistenciasPorNodos[nodo][k] not in puntoInicios:
                                puntoInicios.append(resistenciasPorNodos[nodo][k])
                            if [nodo,resistenciasPorNodos[nodo][k]] in intersecciones or [resistenciasPorNodos[nodo][k],nodo] in intersecciones:
                                l=0
                                while l<len(listaMallas):
                                    m=0
                                    while m<len(listaMallas[l]):
                                        if ([nodo,resistenciasPorNodos[nodo][k]]==listaMallas[l][m][2:4] or [resistenciasPorNodos[nodo][k],nodo]==listaMallas[l][m][2:4]) and listaMallas[l][m] not in resistenciasUsadas and listaMallas[l]!=listaMallas[j]:
                                            matrizCaudalesSupuestos[l][m]=caudalDistribuido        
                                            resistenciasPorNodos[resistenciasPorNodos[nodo][k]].remove(nodo)
                                            resistenciasUsadas.append(listaMallas[j][i])
                                        m+=1
                                    l+=1
                            else:
                                resistenciasPorNodos[resistenciasPorNodos[nodo][k]].remove(nodo)        
                                resistenciasUsadas.append(listaMallas[j][i])
                        i+=1
                    j+=1
                k+=1
            del(resistenciasPorNodos[nodo])
            caudalEntrantes=caudalDistribuido
        else:
            break
    matrizCaudalesSupuestos*=matrizSignos
#Por último guardaremos en un diccionario las ubicaciones de estas intersecciones,
#luego nos será útil.
    interseccion=dict()
    for elemento in intersecciones:
        i=0
        puntos=[]
        while i<len(listaMallas):
            j=0
            while j<len(listaMallas[i]):
                if elemento==listaMallas[i][j][2:4]:
                    puntos.append([i,j])
                j+=1
            i+=1
        interseccion[tuple(elemento)]=puntos
#Salida:matrizCaudalesSupuesto(array).

#A partir de aquí aplicamos los cálculos del método de Hardy Cross.
        
#Entrada: matrizCaudalesSupuestos, valoresResistencias.
def calcularCaidaDePresionLaminar(array1, array2):
    matrizLaminar=array1*array2*2
    return matrizLaminar
#Salida: matrizLaminar(array).
    
#Entrada: matrizCaudalesDistribuidos, valoresResistencias.   
def calcularCaidaDePresion(array1, array2):
    caidaPresion=(array1**2)*array2
    return caidaPresion
#Salida:caidaPresion(array).

#Entrada: matrizLaminar o caidaPresion, en general, un array.
def calcularSumatoria(arrayDeDatos):
    listaSumatoria=[]
    i=0
    while i<arrayDeDatos.shape[0]:
        suma=0
        for elemento in arrayDeDatos[i]:
            suma+=elemento
        i+=1
        listaSumatoria.append(suma)
    listaSumatoria=np.array(listaSumatoria).reshape(arrayDeDatos.shape[0],1)
    return listaSumatoria
#Salida: listaSumatoria(array).

#Entrada: calcularSumatoria(caidaPresion),calcularSumatoria(matrizLaminar).
def calcularDeltaQ(array1,array2):
    global listaCorreccion
    deltaQ=array1/array2
    arrayDeltaQ=np.ones(matrizCaudalesSupuestos.shape)*deltaQ
    listaCorreccion=[]
    for elemento in deltaQ.flat:
        if elemento not in listaCorreccion:
            listaCorreccion.append(elemento)
    return arrayDeltaQ
#Salida: arrayDeltaQ(array).

#Entrada: matrizCaudalesSupuestos.
def corregirIntersecciones(array1):
    global interseccion
    global listaCorreccion
    for elemento in interseccion:
        i=0
        while i<len(interseccion[elemento]):
            for otroElemento in interseccion[elemento]:
                if otroElemento!=interseccion[elemento][i]:
                    array1[interseccion[elemento][i][0],interseccion[elemento][i][1]]+=listaCorreccion[otroElemento[0]]
            i+=1
    return array1
#Saluda: Valores de intersecciones corregidos(array).

#Entrada: matrizCaudalesSupuestos.
def iterar(array1,array2):
#Realizaremos la iteración para obtener un valor adecuado para el caudal distribuido.
    deltaQ=calcularDeltaQ(calcularSumatoria(calcularCaidaDePresion(array1,array2)),calcularSumatoria(calcularCaidaDePresionLaminar(array1,array2)))
    while all(elemento>0.000001 for elemento in deltaQ.flat):
        array1+=deltaQ
        array1=corregirIntersecciones(array1)
        deltaQ=calcularDeltaQ(calcularSumatoria(calcularCaidaDePresion(array1,array2)),calcularSumatoria(calcularCaidaDePresionLaminar(array1,array2)))
    array1*=matrizSignos
    return array1
#Salida: matrizCaudalesSupuestos con valores de caudales corregidos.

#Entrada:Lista con valores de Resistencias empleadas inicialmente y el último array obtenido.
def tabulacionDeDatos(listaDeResistencias,caudalesNuevos):
    resistencias = listaDeResistencias
    caudales = caudalesNuevos
    listaTabulada = []
    auxiliar = []
    #Se tomaran las listas con resistencias, que estaran del modo [[Resistencia, ..., ...], ...] y se reemplazaran los valores de los caudales con los caudales adecuados
    i = 0
    while i < len(caudales):
        j = 0
        while j < len(caudales[i]):
            auxiliar = []
            auxiliar.append(resistencias[i][j][0])
            auxiliar.append(caudales[i][j])
            listaTabulada.append(auxiliar)
            j += 1
        i += 1
    #Una vez la lista tenga los caudales adecuados, se creara un texto que posea todos los elementos.
    texto = ""
    i= 0
    while i < len(listaTabulada):
        texto += (str(listaTabulada[i][0])) + (" ")+ str(listaTabulada[i][1]) +"\n"          
        i += 1
    return texto
#Tendremos por salida, finalmente, los valores de los datos ordenados de manera tabulada.
    

#Bloque principal

#Entradas

puntoInicios=[]
puntoSalidas=[]
listaGalerias=[]
caudalEntrantes=0
listaResistencias=[]
nombreDeArchivo=""
reinicioAutomatico(nombreDeArchivo)
ingresarDatos(puntoInicios)
listaMallas=[]

#Proceso

formarMallas(listaResistencias)
cambioDeSignoYSuponerDistribucionDelCaudal(listaMallas)
iterar(matrizCaudalesSupuestos,valoresResistencias)

#Salida

print (tabulacionDeDatos(listaMallas,matrizCaudalesSupuestos) )         




