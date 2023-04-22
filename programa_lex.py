import ply.lex as lex

states = (
    ('dentroPonto','exclusive'),
)

# Definição dos tokens
tokens = (
    'ATTRIBUTE',
    'ATTRIBUTE_THEN',
    'ATTRIBUTE_ELSE',
    'PA',
    'PF',
    'TAG',
    'HASHTAG',
    'ID',
    'PONTO',
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

def t_PONTO(t):
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

def t_ATTRIBUTE(t):
    r'(?<=\()[^\)]+'
    return t

def t_TAG(t): 
    r'\w+(?=[\(\.\=])|(?<=\t)\w+'
    return t


def t_ATTRIBUTE_THEN(t):
    r"[a-z' ]+(?=:)"
    return t

def t_ATTRIBUTE_ELSE(t):
    r"'[a-z']+(?=\))"
    return t

def t_PA(t):
    r'\('
    return t

def t_PF(t):
    r'\)'
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
t_ANY_ignore = ' \t='

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
'''

lexer.input(pug)

while tok := lexer.token():
    print(tok)