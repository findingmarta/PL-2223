import ply.lex as lex

states = (
    ('dentro_ponto','exclusive'),
)

# Definição dos tokens
tokens = (
    'ATTRIBUTE',
    'ATTRIBUTE_NAME',
    'ATTRIBUTE_VALUE',
    'ATTRIBUTE_THEN',
    'ATTRIBUTE_ELSE',
    'VIRG',
    'PA',
    'PF'
    'TAG',
    'ID',
    'CLASS',
    'TEXT',
    'BLOCK_TEXT',
    'IF',
    'ELSE',
    'PONTO',
    'SCRIPT',
    'VAR'
)

# Expressões regulares para cada token

def t_PONTO(t):
    r'\.(?=\n)'
    t.lexer.beggin('dentro_ponto')
    return t

def t_dentro_ponto_BLOCK_TEXT(t):
    tabs += r'^\t+'
    t.lexer.tabs = tabs.count('\t')
    
    print(t.lexer.tabs)

    r'\w[^\n]'
    return t

def t_ATTRIBUTE_NAME(t):
    r'\w+(?==)'
    return t

def t_ATTRIBUTE_VALUE(t):
    r'\w+(?= )'
    return t

def t_ATTRIBUTE_THEN(t):
    r"[a-z' ]+(?=:)"

    return t

def t_ATTRIBUTE_ELSE(t):
    r"'[a-z']+(?=\))"
    return t

def t_ATTRIBUTE(t):
    r'\w+=[^\) ,]*'
    return t

def t_VIRG(t):
    r','
    return t

def t_PA(t):
    r'\('
    return t

def t_PF(t):
    r'\)'
    return t

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
    r'\w+(?<=\t)|\w+(?=\()|^\w+(?=\n)'
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