import ply.lex as lex

# Definição dos tokens
tokens = (
    'TAG',
    'ID',
    'CLASS',
    'TEXT',
    'ATTRIBUTE',
)

# Expressões regulares para cada token
t_TAG = r'[a-zA-Z][a-zA-Z0-9]*'
t_ID = r'\#[a-zA-Z][a-zA-Z0-9]*'
t_CLASS = r'\.[a-zA-Z][a-zA-Z0-9]*'
t_TEXT = r'([^#\.\{\}])+'
t_ATTRIBUTE = r'\([a-zA-Z][a-zA-Z0-9]*(=("[^"]*"|\'[^\']*\'))?\)'

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
