# -*- coding: utf-8 -*-
# shinyc.py
# El html intermedio es devuelto en un archivo de texto .sel y es impreso por
# pantalla
# El grafo se muestra generando un archivo grafo.png que se guarda en la carpeta
# Daniela Ruiz
# Diego Millan 
import sys
import re
import os.path
from lexer import lexer
from parser import parser
import sys
import networkx as nx
import matplotlib.pyplot as plt
#------------------------------------------------------------------------------#
# function representacion
#     Funcion que transforma el archivo html de entrada a otra representacion 
#     intermedia del mismo.
# parametros: String: archivo es el archivo html que va en la entrada del
# programa            
# retorna: String: Con la represetacion intermedia del html que entró.
def representacion(archivo):
	archivo_actual = open(archivo,"r")
	contenido = archivo_actual.read()
	print contenido
	resultado = []	
	regex1 = r'((.)*(<head>))'
	regex2 = r'(\{%(?:=)?(?:.)*?%\})'
	regex1 = re.compile(regex1,re.DOTALL)
	regex2 = re.compile(regex2,re.DOTALL)	
	objeto = re.match(regex1,contenido)		
	if objeto:
		primer_elem = objeto.group(0)
			
		resultado = [primer_elem]
		cont_aux = contenido[len(primer_elem):len(contenido)]
		#print cont_aux
		objeto2 = re.split(regex2,cont_aux)
		if objeto2:
			#print len(objeto2)
			resultado = resultado + objeto2
			#print "Archivo en lista"
			#print resultado
	archivo_actual.close()			
	#Ahora comenzamos a construir la representacion intermedia
	outfile = open("resultado.sel",'w')			
	for element in resultado:
		if element == resultado[0]:
			outfile.write(element +"\n\t\t"+ "&&")
		else:
			flag = re.match(regex2,element)
			if (flag):
				outfile.write("&&"+element)
			else:
				outfile.write(element)
	outfile.close()					
	outpantalla = open("resultado.sel","r")
	salida = outpantalla.read() 
	print "Representacion Intermedia:"
	print salida						
#------------------------------------------------------------------------------#
# function tagsForParse
#     Funcion que devuelve los tags ShinyEL que deben ser parseados
# parametros: String: archivo es el archivo html que va en la entrada del
#             programa          
# retorna: Lista con todos los tags que deben ser parseados.		
def tagsForParse(archivo):
	archivo_actual = open(archivo,"r")
	contenido = archivo_actual.read()
	regex = r'(\{%(?:=)?(?:.)*?%\})'
	regex = re.compile(regex,re.DOTALL)
	objeto = re.findall(regex,contenido)
	if objeto:
		shiny = objeto
	archivo_actual.close()	
	return shiny		
#---------------------------------Main-----------------------------------------#
if(len(sys.argv) > 1):	
	if os.path.exists(sys.argv[1]):
		print "Archivo de Entrada.."
		representacion(sys.argv[1])
		print "Tags"
		marcasShiny = tagsForParse(sys.argv[1])
		print marcasShiny
		print "# Marcas ShinyEL = " + str(len(marcasShiny)) + "\n"		
		i = 0	
		for element in marcasShiny:
			i = i + 1
			result = parser.parse(element)
			#print result	
			if result:
				nx.draw_graphviz(result)
				plt.savefig("grafo.png")	
	else:			
		print "El archivo de entrada NO existe"
else:
	print "File Missing ... Exit"

