# lexer.py
# Daniela Ruiz
# Diego Millan 
#------------------------------------------------------------------------------#
import ply.lex as lex
import sys
sys.path.append("../..")
from ply import *
#------------------------------------------------------------------------------#
# Palabras reservadas
reserved = {	    'int'	: 'int',	
					'string': 'string',
					'list'	: 'list',
                    'of'    : 'of',
					'table'	: 'table',
					'true'	: 'true',
					'false'	: 'false',
					'if'	: 'if',
					'then'	: 'then',
					'else'	: 'else',
					'fby'	: 'fby',
					'tby'	: 'tby',
					'len'	: 'len',
					'input'	: 'input',
					'range'	: 'range',
					'where'	: 'where',
					'new'	: 'new',
					}

# Lista de tokens
tokens = ['var','num','cadena','acor','ccor','apar','cpar',
			'porc','punto','coma','dosptos','conjunc',
			'disyunc','negac','igual','desigual','mayor','menor','mayorigual',
			'menorigual','mas','menos','mult','div','mod','exp',
			'asignacion','begin','end',] + list(reserved.values())

# Expresiones Regulares
t_int				= r'int'
t_acor				= r'\['
t_ccor				= r'\]'
t_apar				= r'\('
t_cpar				= r'\)'
t_porc				= r'%'
t_punto				= r'\.'
t_coma				= r','
t_dosptos			= r':'
t_conjunc			= r'&'
t_disyunc			= r'\|'
t_negac				= r'!'
t_igual				= r'='
t_desigual			= r'!='
t_mayor				= r'>'
t_menor				= r'<'
t_mayorigual		= r'>='
t_menorigual		= r'<='
t_mas				= r'\+'
t_menos				= r'-'
t_mult				= r'\*'
t_div				= r'/'
t_exp				= r'\*\*'
t_asignacion		= r':='
t_begin				= r'{%(=)?'
t_end				= r'%}'

def t_num(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_var(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'var')
    return t

def t_cadena(t):
	r'''(?P<quote>['"])(\w|\d|\W|([ \t\v\r\f]))*?(?P=quote)'''
	t.value = t.value[1:-1]
	return t 

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

#------------------------- Manejador de Errores -------------------------------#
def t_error(t):
	print "Illegal character '%s'" % t.value[0]
	print t.value
	t.lexer.skip(1)
#------------------------- Constructor del Lexer ------------------------------#
lexer = lex.lex()

