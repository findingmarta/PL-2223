import ply.lex as lex

total_idents = 0
total_dedents = 0

states = (
    ('pointState','exclusive'),
    ('barState','exclusive'),
    ('atributeState', 'exclusive'),
    ('conditionalState', 'exclusive'),
    ('dedent', 'exclusive')
)


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
    'MENOS',
    'MAIOR',
    'MENOR',
    'DIF',
    'MULT',
    'DIV',
    'CONJ',
    'DIJ',
    'NEG',
    'EQUIVALENCIA',
    'MAIORIGUAL',
    'MENORIGUAL',
    'MODULO',
    'VAR_COND',
    'VALUE_COND',
    'WHILE',
    'INDENT',
    'DEDENT'
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

def t_ANY_EQUIVALENCIA(t):
    r'=='
    return t

def t_ANY_EQUALS(t):
    r'='
    return t

def t_ANY_PLUS(t):
    r'\+'
    return t
def t_ANY_DIJ(t):
    r'\|\|'
    return t

def t_ANY_DIF(t):
    r'!='
    return t


def t_ANY_DIV(t):
    r'\/'
    return t

def t_ANY_MULT(t):
    r'\*'
    return t

def t_ANY_CONJ(t):
    r'&&'
    return t

def t_ANY_MAIORIGUAL(t):
    r'>='
    return t

def t_ANY_MENORIGUAL(t):
    r'<='
    return t

def t_ANY_MAIOR(t):
    r'\>'
    return t

def t_ANY_MENOR(t):
    r'\<'
    return t

def t_ANY_NEG(t):
    r'\!'
    return t

def t_ANY_MODULO(t):
    r'\%'
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

def t_ANY_MENOS(t):
    r'\-'
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

    global total_indents, total_dedents
    if tabs_count > t.lexer.tabs:
        t.type = 'INDENT'
        t.value = tabs_count - t.lexer.tabs
        t.lexer.tabs = tabs_count
        return t
    elif tabs_count < t.lexer.tabs:
        total_dedents = (t.lexer.tabs - tabs_count) / 4
        t.lexer.push_state('dedent')
        t.lexer.tabs = tabs_count


def t_dedent_DEDENT(t):
    r'(.|\n)'
    global total_dedents
    t.lexer.lexpos -= 1
    if total_dedents > 0:
        total_dedents -= 1
        t.value = 4
        return t
    else:
        t.lexer.pop_state()


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

		-url = 'https://example.com/'
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

lexer.input(pug)

while tok := lexer.token():
    print(tok)