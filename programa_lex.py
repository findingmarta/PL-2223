import ply.lex as lex

# Definição dos tokens
tokens = (
    'TAG',
    'ID',
    'CLASS',
    'TEXT',
    'ATTRIBUTE',
    'IF',
    'ELSE',
    'PONTO',
    'SCRIPT',
    'VAR'
)

# Expressões regulares para cada token
def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_SCRIPT(t):
    r'script'
    return t

def t_VAR(t):
    r'\w*(?<=\()'
    return t

def t_TAG(t): 
    r'[a-zA-Z]\w*'
    return t

def t_ID(t):
    r'\w+(?<=\#)'
    return t

def t_CLASS(t):
    r'\w+(?<=\.)'
    return t

def t_TEXT(t):
    r'(\w+\s*\w*)+'
    return t

def t_ATTRIBUTE(t):
    r'\(\w*(=("[^"]*"|\'[^\']*\'))?\)'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignora espaços em branco e tabulações
t_ignore = ' \t'

def t_error(t):
    print('Illegal character: ', t.value[0], ' Line: ', t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()

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