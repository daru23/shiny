# -*- coding: utf-8 -*-
# parser.py 
#########################  English  Version #########################################
#  Transforms the input on a tree branch
#########################  Spanish Version ##########################################
# Transforma la entrada en un árbol de derivación
# Author
# Daniela Ruiz - daru015@gmail.com
# Diego Millan 
#####################################################################################
import ply.yacc as yacc
from lexer import tokens
import sys
import networkx as nx
import matplotlib.pyplot as plt
####################################################################################
# function flatten
######################### English Version ###########################################
#     Flatten a list
# @param  : List
# @return : List
######################## Spanish Version ############################################
#     Aplana una lista
# @param  : List 
# @return : List
#####################################################################################
def flatten(x):
    flat = True
    ans = []
    for i in x:
        if ( i.__class__ is list):
            ans = flatten(i)
        else:
            ans.append(i)
    return ans
#####################################################################################
# Variable Dependency Graph / Grafo de Dependencia de Variables
#####################################################################################
G = nx.DiGraph() 
#####################################################################################
# Precedence / Precedencia
#####################################################################################
precedence = (
    ('left', 'tby'),
    ('right', 'fby'),
    ('left','mayor','menor','mayorigual','menorigual'),
    ('left', 'igual','desigual'),
    ('left','conjunc'),
    ('left','disyunc'),
    ('left','mas','menos'),
    ('left','mult','div','mod'),
    ('left','exp'),
    ('right','umenos','negac'),
    )
#####################################################################################
# Precedence Table / Tabla de Simbolos
#####################################################################################
tab_simb = { }
#####################################################################################
# Initial State / Estado Inicial
#####################################################################################
def p_estados(t):
    '''programa : begin asign end
                | begin expr end
                | begin seleccion end'''
    t[0] = G
    print 'programa : '+ str(t[1])+' '+str(t[2])+' '+str(t[3])
#####################################################################################
# Expressions / Expresiones
#####################################################################################
def p_expresiones2(t):
    '''expr  : expr_num
             | alc_var
             | expr_cad
             | expr_func
             | expr_list
             | expr_tabl'''
    t[0] = t[1]
    print 'expr : '+str(t[1])

def p_expresiones_(t):
    '''expr  : expr mas expr
             | expr menos expr
             | expr mult expr
             | expr div expr
             | expr mod expr
             | expr exp expr'''
    t[0] = [t[1], t[3]] 
    print 'expr : '+str(t[1])+' '+str(t[2])+' '+str(t[3])

def p_alc_var(t):
    ''' alc_var : expr_var
                | expr_var acor expr ccor punto expr_var'''
    t[0] = t[1]
    if len(t)>2 :
        print 'var : '+str(t[1])+' '+str(t[2])+' '+str(t[3])+' '+str(t[4])+' '+str(t[5])+' '+str(t[6])
    else :
        print 'var : '+str(t[1])	  
	
def p_exp_parentizada(t):
    'expr : apar expr cpar'
    t[0] = t[2]
    print 'expr : '+str(t[1])+' '+str(t[2])+' '+str(t[3])
#####################################################################################
# Assignation / Asignacion
#####################################################################################
def p_asignacion(t):
    'asign : variable asignacion algo'
    tab_simb[t[1]] = t[3]
    #print t[3]
    if isinstance(t[3],list):
        var = flatten(t[3])
        for elem in var:
            G.add_node(elem)
            G.add_edge(elem,t[1])
    else:
          G.add_node(t[3])
          G.add_edge(t[3],t[1])
    t[0] = t[1]
    print 'asign : '+str(t[1])+' '+str(t[2])+' '+str(t[3])

def p_algo(t):
    '''algo : expr
            | input'''
    t[0] = t[1]
    print 'algo : '+str(t[1])

def p_asignacion2(t):
    'asign : variable coma asign coma algo'
    G.add_node(t[1])
    G.add_edge(t[5],t[1])    
    tab_simb[t[1]] = t[5]
    t[0] = t[1]
    print 'asign : '+str(t[1])+' '+str(t[2])+' '+str(t[3])+' '+str(t[4])+' '+str(t[5])

def p_declaracion(t):
    'variable : var dosptos tipo'
    t[0] = t[1]
    print 'variable : '+str(t[1])+' '+str(t[2])+' '+str(t[3])

def p_tipo(t):
    '''tipo : int
            | string
            | list of int
            | list of string
            | table'''
    if   t[1] == 'int': t[0] = t[1]
    elif t[1] == 'string': t[0] = t[1]    
    elif t[1] == 'list':
                        if   t[3] == 'int': t[0] = t[1]+' '+t[2]+' '+t[3]
                        elif t[3] == 'string': t[0] = t[1]+' '+t[2]+' '+t[3]
    elif t[1] == 'table': t[0] = t[1]
    if t[1] == 'int':
        t[0] = t[1]
        print 'tipo : '+str(t[1])
    elif t[1] == 'string':
        t[0] = t[1]
        print 'tipo : '+str(t[1])    
    elif t[1] == 'list':
        if  t[3] == 'int':
            t[0] = t[1]+' '+t[2]+' '+t[3]
            print 'tipo : '+str(t[1])+' '+str(t[2])+' '+str(t[3])
        elif t[3] == 'string':
            t[0] = t[1]+' '+t[2]+' '+t[3]
            print 'tipo : '+str(t[1])+' '+str(t[2])+' '+str(t[3])
    elif t[1] == 'table':
        t[0] = t[1]
        print 'tipo : '+str(t[1])
#####################################################################################
# Expressions for Integers / Expresiones para Enteros
#####################################################################################
def p_binop1(t):
    '''expr_num : num
                | leng'''
    t[0] = t[1]
    print 'expr_num : '+str(t[1])

def p_len(t):
    'leng : len apar expr3 cpar'
    t[0] = t[3]
    print 'leng : '+str(t[1])+' '+str(t[2])+' '+str(t[3])+' '+str(t[4])

def p_expr3(t):
    '''expr3 : expr_cad
             | expr_list
             | expr_tabl'''
    t[0] = t[1]
    print 'expr3 : '+str(t[1])

def p_exp_neg(t):
    'expr : menos expr %prec umenos'
    t[0] = t[2]
    print 'expr : '+str(t[1])+' '+str(t[2])+' '+str(t[3])+' '+str(t[4])

def p_exp_variable2(t):
    'expr_var : var'
    #print 'variable ' + str(t[1])   
    t[0] = t[1]
    G.add_node(t[1])
    print 'expr_var : '+str(t[1])
#####################################################################################
# Expressions for Strings / Expresiones para Cadenas
#####################################################################################
def p_exp_cadenas(t):
    'expr_cad : cadena'
    t[0] = t[1]
    print 'expr_cad : '+str(t[1])
#####################################################################################
# Expressions for Lists / Expresiones para Listas
#####################################################################################
def p_lista(t):
    '''expr_list : lista_simpl
                 | lista_comp'''
    t[0] = t[1] 
    print 'expr_list : '+str(t[1])

def p_lista3(t):
    'lista_simpl : acor contenido ccor'
    t[0] = t[2]
    print 'lista_simpl : '+str(t[1])+' '+str(t[2])+' '+str(t[3])

def p_lista31(t):
    '''contenido : empty
                 | elementos'''
    t[0] = t[1]
    print 'contenido : '+str(t[1])

def p_lista4(t):
    'lista_comp : acor porc definicion porc ccor'
    t[0] = t[3]
    print 'lista_comp : '+str(t[1])+' '+str(t[2])+' '+str(t[3])+' '+str(t[4])+' '+str(t[5])

def p_lista5(t):
    '''definicion : lista_comp2
                  | cuantif'''
    t[0] = t[1]
    print 'definicion : '+str(t[1])

def p_lista_comp(t):
    'lista_comp2 : expr dosptos caso_list dosptos expr'
    t[0] = t[5]
    print 'lista_comp2 : '+str(t[1])+' '+str(t[2])+' '+str(t[3])+' '+str(t[4])+' '+str(t[5])

def p_caso_list(t):
    '''caso_list : expr_list
                 | var'''
    t[0] = t[1]
    print 'caso_list : '+str(t[1])

def p_elementos(t):
    'elementos : elementos coma expr'
    t[0] = t[2]
    print 'elementos : '+str(t[1])+' '+str(t[2])+' '+str(t[3])

def p_elementos2(t):
    'elementos : expr'
    t[0] = t[1]
    print 'elementos : '+str(t[1])

def p_acceso(t):
    'expr_list : expr_list acor expr_num ccor'
    t[0] = t[1]
    print 'expr_list : '+str(t[1])+' '+str(t[2])+' '+str(t[3])

def p_range(t):
    'expr_list : range apar expr coma expr cpar'
    t[0] = t[3]
    print 'expr_list : '+str(t[1])+' '+str(t[2])+' '+str(t[3])+' '+str(t[4])+' '+str(t[5])+' '+str(t[6])
#####################################################################################
# Expressions for Tables / Expresiones para Tablas
#####################################################################################
def p_expr_table(t):
    'expr_tabl : new table acor expr ccor where asignes'
    t[0] = t[4]
    print 'expr_tabl : '+str(t[1])+' '+str(t[2])+' '+str(t[3])+' '+str(t[4])+' '+str(t[5])+' '+str(t[6])+' '+str(t[7])

def p_asignes(t):
    'asignes : variable asignacion algo'
    tab_simb[t[1]] = t[3]
    t[0] = [3]
    print 'asignes : '+str(t[1])+' '+str(t[2])+' '+str(t[3])

def p_asignes2(t):
    'asignes : asignes coma asignes'
    t[0] = t[3]    
    print 'asignes : '+str(t[1])+' '+str(t[2])+' '+str(t[3])
#####################################################################################
# Expressions for Quantifiers / Expresiones para Cuantificadores 
#####################################################################################
# [% operador variable : lista : expresion %]
def p_cuantif(t):
    'cuantif : op expr_var dosptos expr dosptos expr'
    t[0] = t[2]
    print 'cuantif : '+str(t[1])+' '+str(t[2])+' : '+str(t[4])+' : '+str(t[6])

def p_operador(t):
    '''op : mas
          | menos
          | mult
          | div
          | mod
          | exp
          | negac
          | disyunc
          | conjunc
          | mayor
          | menor
          | mayorigual
          | menorigual
          | igual
          | desigual'''
    t[0] = t[1]
    print 'op : '+str(t[1])
#####################################################################################
# Boolean Operators / Operadores Booleanos 
#####################################################################################
def p_condicion(t): 
    '''condicion : term_b
                 | booleano
                 | cond_parentizada
                 | binop_bool
                 | negacion'''    
    t[0] = t[1]
    print 'condicion : '+str(t[1])

def p_binop_bool(t):
    '''binop_bool : condicion conjunc condicion
                  | condicion disyunc condicion'''
    t[0] = t[3]
    print 'binop_bool : '+str(t[1])+' '+str(t[2])+' '+str(t[3])

def p_negacion(t):
    ' negacion : negac term_b'
    t[0] = not t[2]
    print 'negacion : '+str(t[1])+' '+str(t[2])


def p_terminos_booleanos(t):
    '''term_b : true
              | false'''
    t[0] = t[1]
    print 'term_b : '+str(t[1])	

def p_cond_parentizada(t):
    'cond_parentizada : apar condicion cpar'
    t[0] = t[2]
    print 'cond_parentizada : '+str(t[1])+' '+str(t[2])+' '+str(t[3])

def p_booleano(t):
    '''booleano : booleano igual valor
                | booleano desigual valor
                | booleano mayor valor
                | booleano menor valor
                | booleano mayorigual valor
                | booleano menorigual valor'''
    t[0] = t[3]
    print 'booleano : '+str(t[1])+' '+str(t[2])+' '+str(t[3])
    
def p_booleano2(t):
    '''booleano : valor
                | bool_parentizado'''
    t[0] = t[1]
    print 'booleano : '+str(t[1])

def p_valor(t):
    '''valor : expr_cad
             | expr_num 
             | expr_var'''
    t[0] = t[1]
    print 'valor : '+str(t[1])

def p_booleano_parentizado(t):
    'bool_parentizado : apar booleano cpar'
    t[0] = t[2]
    print 'bool_parentizado : '+str(t[1])+' '+str(t[2])+' '+str(t[3])
#####################################################################################
# Selection / Seleccion
#####################################################################################
def p_seleccion(t):
    'seleccion : if condicion then expr else expr'
    if   t[2]: t[0] = t[4]
    else:      t[0] = t[6]
    print 'seleccion : '+str(t[1])+' '+str(t[2])+' '+str(t[3])+' '+str(t[4])+' '+str(t[5])+' '+str(t[6])
#####################################################################################
# Functions / Funciones
#####################################################################################
def p_func(t):
    '''expr_func : expr_fby
                 | expr_tby'''
    t[0] = t[1]
    print 'expr_func : '+str(t[1])

def p_fby(t):
    'expr_fby : expr fby expr'
    if isinstance(t[3],list):
        var = flatten(t[3])
        for elem in var:
            G.add_node(elem)
            G.add_edge(elem,t[1])
    else:
          G.add_node(t[3])
          G.add_edge(t[3],t[1])
    t[0] = t[3]
    print 'expr_fby : '+str(t[1])+' '+str(t[2])+' '+str(t[3])

def p_tby(t):
    'expr_tby : expr tby varia'
    var = flatten(t[3])
    var1 = flatten(t[1])
    for elem in var:
        for elem2 in var1:
            G.add_node(elem2)
            G.add_edge(elem2,elem)
    t[0] = t[3]
    print 'expr_tby : '+str(t[1])+' '+str(t[2])+' '+str(t[3])

def p_tby2(t):
    '''varia : expr_list
             | expr_var'''
    t[0] = t[1]
    print 'varia : '+str([1])
#------------------------------------------------------------------------------#
def p_empty(p):
    'empty :'
    pass
#####################################################################################
# HANDLER SYNTAX ERRORS / MANEJOR DE ERRORES SINTACTICOS ---------
#####################################################################################
def p_error(t):
    print("Syntax error at '%s'" % t.value)
#####################################################################################
#----------------- Parser Builder / Constructor del Parser -------------------------#
#####################################################################################
parser = yacc.yacc(errorlog=yacc.NullLogger())

#-----------------------------------------------------------------------------------#
#while True:
#   try:
#       s = raw_input('Regla: ')
#   except EOFError:
#       break
#   if not s: continue
#   result = parser.parse(s)
#   print result
#   print 'TABLA DE SIMBOLOS'
#   print tab_simb
#   if result:
#       nx.draw_spring(result)
#       plt.show()
