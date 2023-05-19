import ply.lex as lex

states = (
    ('pointState','exclusive'),
    ('barState','exclusive'),
    ('atributeState', 'exclusive'),
    ('conditionalState', 'exclusive'),
)

literals = ['-', '*', '/', '%', '&', '|', '<', '>']

# FALTA AS SELF CLOSING TAGS (ver no yacc se calhar)

# Definição dos tokens
tokens = (
    'ATTRIBUTE',
    'QUESTION_MARK',
    'COMMA',
    'TWO_POINTS',
    'ATTRIBUTE_VALUE',
    'ATTRIBUTE_VAR',
    'PA',
    'PF',
    'TAG',
    'HASHTAG',
    'ID',
    'POINT',
    'BAR',
    'CLASS',
    'TEXT',
    'BLOCK_TEXT',
    'IF',
    'ELSE',
    'VAR_JS',
    'VAR_NAME',
    'VAR_VALUE',
    'EQUALS',
    'PLUS',
    'VAR_COND',
    'VALUE_COND',
    'OP_COND',
    'WHILE',
    'INDENT'
)

# Expressões regulares para cada token
def t_ANY_enter_pointState(t):
    r'\.(?=\n)'
    t.lexer.block_indent = True
    t.lexer.push_state('pointState')

def t_ANY_enter_barState(t):
    r'(?<=\t)\|'
    if(t.lexer.current_state() == 'INITIAL'):
        t.lexer.push_state('barState')

def t_pointState_barState_BLOCK_TEXT(t):   
    r'[^\t\n]+'
    return t

def t_HASHTAG(t):
    r'\#'
    return t

def t_ID(t):
    r'(?<=\#)[a-zA-Z0-9\-]+'
    return t

def t_POINT(t):
    r'\.'
    return t

def t_BAR(t):
    r'\|'
    return t

def t_CLASS(t):
    r'(?<=\.)\w+'
    return t

def t_IF(t):
    r'if'
    t.lexer.push_state('conditionalState')
    return t

def t_WHILE(t):
    r'while'
    t.lexer.push_state('conditionalState')
    return t

def t_ELSE(t):
    r'else'
    return t

def t_ANY_EQUALS(t):
    r'='
    return t

def t_ANY_PLUS(t):
    r'\+'
    return t

def t_atributeState_ATTRIBUTE(t):
    r'(?<=[, \t\(])[ ]?\w+=[ ]?'
    return t

def t_atributeState_ATTRIBUTE_VALUE(t):
    r"(?<=[= ,?:])['\"][^\n ]+['\"]"
    return t

def t_atributeState_ATTRIBUTE_VAR(t):
    r"(?<=[= ,?:])[\w\-']+"
    return t

def t_VAR_JS(t):
    r'-[ ]?var(?=\s)|-'
    return t

def t_VAR_NAME(t):
    r'(?<=\bvar\s)\w+|(?<=-\s)\w+|(?<=-)\w+|(?<=\bif\s)\w+'
    return t

def t_VAR_VALUE(t):
    r"((?<=\=)|(?<==\s))['\"]?[^\n\t\+\-\*\&\|]+[\"']?"
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

def t_conditionalState_INITIAL_PA(t):
    r'\('
    if t.lexer.current_state() == 'INITIAL':    
        t.lexer.begin('atributeState')
    return t

def t_atributeState_conditionalState_PF(t):
    r'\)'
    if t.lexer.current_state() == 'atributeState':
        t.lexer.begin('INITIAL')
    return t

def t_conditionalState_VAR_COND(t):
    r'[a-z]\w*'
    return t

def t_conditionalState_VALUE_COND(t):
    r'\d+'
    return t

def t_conditionalState_OP_COND(t):
    r'\d+'
    return t

def t_TEXT(t):   
    r'((?<= )|(?<=\|))[^\n]+'
    return t  

# Define a rule so we can track line numbers
def t_ANY_newline(t):
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

    if t.lexer.current_state() == 'pointState':
        if t.lexer.block_indent:
            t.lexer.indent = t.lexer.tabs
            t.lexer.block_indent = False
        if tabs_count <= t.lexer.indent:            
            t.lexer.pop_state()
    elif tabs_count != t.lexer.tabs and t.lexer.current_state() == 'barState':
        t.lexer.pop_state()
    elif t.lexer.current_state() == 'conditionalState':
        t.lexer.pop_state()

    t.lexer.tabs = tabs_count
    t.type = "INDENT"
    t.value = tabs_count
    return t


# Ignora espaços em branco e tabulações
t_ANY_ignore = ' \t'

def t_ANY_error(t):
    print('Illegal character: ', t.value[0], ' Line: ', t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()

lexer.tabs = 0
lexer.block_indent = False
lexer.indent = 0

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
		-var authenticated = true
		- var varia = "authed"

		body(class=authenticated ? varia :'anon')
		a: img
		table: h1: h2: a AAAA

		input(
			type='checkbox'
			name='agreement'
		)

		-varia = 'https://example.com/'
		a(href='/' + url) Link
		a(href=url) Another link

        a.button
        .content

        a#main-link
        #content

		- var user = 'foo bar baz'
		- var authorised = false
		#user
			if user
				h2.green Description
				p.description= user
			else if (authorised == 2 && 1 < 3 || 2*(1+2) <= 5)
				h2.blue Description 
				p.description.
				    User has no description,
				    why not add one...
			else
				h2.red Description
				p.description User has no description
		p
			| The pipe always goes at the beginning of its own line,
			| not counting indentation.
			| sada
			| asd
		
		- var n = 0

        script.
            if 1+1 == 2
                title
                BBBBB
            else
                AAAAA

		//just some paragraphs
		ul
			while n < 4
				body(type= n++)
				li= n++
                li exp=sfaew
'''


#with open('datasets/ex1.pug', 'r') as pug:
#    pug.readlines()

lexer.input(pug)


while tok := lexer.token():
    print(tok)