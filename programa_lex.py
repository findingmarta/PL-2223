import ply.lex as lex

states = (
    ('dentroPonto','exclusive'),
    ('atributeState', 'exclusive'),
)

#literals = ['.', '=', '+', '-', '*', '/', ',', ':', '#', '|', '"', "'",'(',')']

# FALTA AS SELF CLOSING TAGS (ver no yacc se calhar)

# Definição dos tokens
tokens = (
    'ATTRIBUTE',
    'QUESTION_MARK',
    'COMMA',
    'TWO_POINTS',
    'ATTRIBUTE_THEN',
    'ATTRIBUTE_ELSE',
    'PA',
    'PF',
    'TAG',
    'HASHTAG',
    'ID',
    'POINT',
    'CLASS',
    'TEXT',
    'BLOCK_TEXT',
    'IF',
    'ELSE',
    'VAR'
)

# Expressões regulares para cada token
def t_ANY_enter_dentroPonto(t):
    r'\.(?=\n)'
    t.lexer.push_state('dentroPonto')

def t_dentroPonto_BLOCK_TEXT(t):   
    r'[^\t\n]+'
    return t

def t_HASHTAG(t):
    r'\#'
    return t

def t_ID(t):
    r'(?<=\#)\w+'
    return t

def t_POINT(t):
    r'\.'
    return t

def t_CLASS(t):
    r'(?<=\.)\w+'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_atributeState_ATTRIBUTE_ELSE(t):
    r"['\w ]+(?=\))"
    return t

def t_atributeState_ATTRIBUTE_THEN(t):
    r"['\w ]+(?=:)"
    return t

def t_atributeState_ATTRIBUTE(t):
    r'((?<=\()|(?<=[, ]))[ ]?\w+=[ ]?[^ ,\)\n]+'
    return t

def t_TAG(t): 
    r'[a-z]\w*(?=[\(\.\=:])|(?<=\t)[a-z]\w+|[a-z]\w*'
    return t

def t_atributeState_COMMA(t):
    r','
    return t

def t_atributeState_QUESTION_MARK(t):
    r'\?'
    return t

def t_ANY_TWO_POINTS(t):
    r':'        
    return t

def t_PA(t):
    r'\('
    t.lexer.begin('atributeState')
    return t

def t_atributeState_PF(t):
    r'\)'
    t.lexer.begin('INITIAL')
    return t

def t_VAR(t):
    r'\w*(?<=\()'
    return t

def t_TEXT(t):   
    r'(?<= )[^\n]+'
    return t

def t_dentroPonto_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

    tabs_count = 0
    for char in t.lexer.lexdata[t.lexer.lexpos:]:
        if char == ' ':
            tabs_count += 1
        elif char == '\t':
            tabs_count += 4
        else:
            break

    if tabs_count < t.lexer.tabs:
        t.lexer.pop_state()

    t.lexer.tabs = tabs_count

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignora espaços em branco e tabulações
t_ANY_ignore = ' \t'

def t_ANY_error(t):
    print('Illegal character: ', t.value[0], ' Line: ', t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()

lexer.tabs = 0

pug = '''
html(lang="en")
	head
		title= pageTitle
			script(type='text/javascript').
				if (foo) bar(1 + 5)
	body
		h1 Pug - node template engine
			#container.col
				if youAreUsingPug
					p You are amazing
				else
					p Get on it!
				p.
					Pug is a terse and simple templating language with a
					strong focus on performance and powerful features
		ul
			li Item A
			li Item B
			li Item C
		img(src='./logi?n_icon', alt='login' style='width:100px;height:100px;')
		body(class=authenticated ? authed :'anon')
		a: img
		table: h1: h2: a AAAA
'''

lexer.input(pug)

while tok := lexer.token():
    print(tok)