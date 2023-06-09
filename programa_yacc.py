import ply.yacc as yacc

from programa_lex import tokens

variaveis = {}
self_closing_tags = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]


precedence = (
    ('left', 'DIJ'),
    ('left', 'CONJ'),
    ('left', 'MAIORIGUAL'),
    ('left', 'MENORIGUAL'),
    ('left', 'EQUIVALENCIA'),
    ('left', 'DIF'),
    ('left', 'NEG'),
    ('left', 'MAIOR'),
    ('left', 'MENOR'),
    ('left', 'MULT'),
    ('left', 'DIV'),
    ('left', 'MODULO'),
    ('left', 'PLUS'),
    ('left', 'MENOS'),
)

# Regras de produção da gramática
def p_pug(p):
    'pug : elemList'
    p[0] = p[1]


def p_elemList(p):
    """elemList : elemList elem
                | elem
    """
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]


def p_elem_tag_atr_text(p):
    """
    elem : TAG PA atributos PF TEXT INDENT elemList DEDENT
         | TAG PA atributos PF TEXT INDENT elemList
    """
    p[0] = f"<{p[1]} {p[3]}> {p[5]} {p[7]} </{p[1]}>"


def p_elem_tag_text(p):
    """
    elem : TAG TEXT INDENT elemList DEDENT
         | TAG TEXT INDENT elemList
    """
    p[0] = f"<{p[1]}> {p[2]} {p[4]} </{p[1]}>"                 


def p_elem_tag_atr(p):
    """
    elem : TAG PA atributos PF INDENT elemList DEDENT
         | TAG PA atributos PF INDENT elemList
    """
    p[0] = f"<{p[1]} {p[3]}> {p[6]} </{p[1]}>"

def p_elem_tag_atr_btext(p):
    '''
    elem : TAG PA atributos PF INDENT blocks DEDENT
         | TAG PA atributos PF INDENT blocks
    '''
    p[0] = f"<{p[1]} {p[3]}> {p[6]} </{p[1]}>"


def p_elem_tag(p):
    """
    elem : TAG INDENT elemList DEDENT
         | TAG INDENT elemList
    """
    p[0] = f"<{p[1]}> {p[3]} </{p[1]}>"


def p_elem_tag_btext(p):
    '''
    elem : TAG INDENT blocks DEDENT
         | TAG INDENT blocks
    '''
    p[0] = f"<{p[1]}> {p[3]} </{p[1]}>"


def p_elem_tag_text_sem_in(p):
    """
    elem : TAG PA atributos PF TEXT 
         | TAG TEXT
    """
    if len(p) == 6:
        p[0] = f"<{p[1]} {p[3]}> {p[5]} </{p[1]}>"
    else:
        p[0] = f"<{p[1]}> {p[2]} </{p[1]}>"


def p_elem_tag_atr_sem_in(p):
    """
    elem : TAG PA atributos PF
         | TAG
    """
    if len(p) == 5:
        p[0] = f"<{p[1]} {p[3]}"
        if p[1] in self_closing_tags:
            p[0] += "/>"
        else:
            p[0] += f"> </{p[1]}>"
    else:
        p[0] = f"<{p[1]}"
        if p[1] in self_closing_tags:
            p[0] += "/>"
        else:
            p[0] += f"> </{p[1]}>"


def p_elem_tag_literals(p):
    """
    elem : TAG literals INDENT elemList DEDENT
         | TAG literals INDENT elemList
         | TAG literals 
    """
    if len(p) == 6:
        p[0] = f"<{p[1]} {p[2]}> {p[4]} </{p[1]}>" 
    if len(p) == 5:
        p[0] = f"<{p[1]} {p[2]}> {p[4]} </{p[1]}>"
    if len(p) == 3:
        p[0] = f"<{p[1]} {p[2]}"
        if p[1] in self_closing_tags:
            p[0] += "/>"
        else:
            p[0] += f"> </{p[1]}>"

def p_elem_literals(p):
    """
    elem : literals INDENT elemList DEDENT
         | literals INDENT elemList
         | literals 
    """
    if len(p) == 5:
        p[0] = f"<div {p[1]}> {p[3]} </div>" 
    elif len(p) == 4:
        p[0] = f"<div {p[1]}> {p[3]} </div>"
    else:
        p[0] = f"<div {p[1]}></div>"


def p_elem_tag_literals_text(p):
    """
        elem : TAG literals TEXT INDENT elemList DEDENT
             | TAG literals TEXT INDENT elemList
             | TAG literals TEXT
        """
    if len(p) == 7:
        p[0] = f"<{p[1]} {p[2]}> {p[3]} {p[5]} </{p[1]}> " 
    if len(p) == 6:
        p[0] = f"<{p[1]} {p[2]}> {p[3]} {p[5]} </{p[1]}>"
    if len (p) == 4:
        p[0] = f"<{p[1]} {p[2]}> {p[3]} </{p[1]}>"


def p_elem_literals_text(p):
    """
    elem : literals TEXT INDENT elemList DEDENT
         | literals TEXT INDENT elemList
         | literals TEXT
    """
    if len(p) == 6:
        p[0] = f"<div {p[1]}> {p[2]} {p[4]} </div> " 
    if len(p) == 5:
        p[0] = f"<div {p[1]}> {p[2]} {p[4]} </div> " 
    if len (p) == 3:
        p[0] = f"<div {p[1]}> {p[2]} </div> "
    

def p_elem_condition(p):
    """
    elem : IF cond INDENT elemList DEDENT else_if ELSE INDENT elemList DEDENT
         | IF cond INDENT elemList DEDENT ELSE INDENT elemList DEDENT
         | IF cond INDENT elemList DEDENT
         | WHILE cond INDENT elemList DEDENT
    """
    if len(p) == 11:
        if p[2]:
            p[0] = p[4]
        elif p[6][0]:
            p[0] = p[6][1]
        else:
            p[0] = p[9]   
    elif len(p) == 10:
        if p[2]:
            p[0] = p[4]
        else:
            p[0] = p[8]
    if len(p) == 6:
        if p[2]:
            if p.slice[1] == "IF":
                p[0] = p[4]
            else:
                p[0] = ""
                while p[2]:
                    p[0]+=p[4]

def p_else_if(p):
    '''
    else_if : else_if ELSE IF cond INDENT elemList DEDENT
            | ELSE IF cond INDENT elemList DEDENT
    '''
    if len(p) == 8:
        if p[1][0]:
            p[0] = p[1]
        elif p[4]: 
            p[0] = [True, p[6]]
        else:
            p[0] = [False, ""]
    else:
        if p[3]:
            p[0] = [True, p[5]]
        else:
            p[0] = [False, ""]


def p_elem_var(p):
    """
    elem : VAR_JS VAR_NAME EQUALS VAR_VALUE 
         | TAG EQUALS VAR_VALUE
    """
    if len(p) == 5:
        if p[4] == "true":
            p[4] = True
        elif p[4] == "false":
            p[4] = False
        else:
            try:
                p[4] = float(p[4])                                        
            except:
                p[4] = p[4].replace("'","")
                p[4] = p[4].replace('"',"")
        p[0] = ""
        variaveis[p[2]] = p[4]
    if len(p) == 4:
        p[0] = f"<{p[1]}></{p[1]}>"
    

def p_blocks(p):
    """
    blocks : blocks INDENT BLOCK_TEXT DEDENT
           | blocks INDENT BLOCK_TEXT
           | blocks BLOCK_TEXT 
           | BLOCK_TEXT
    """
    if len(p) == 3:
        p[0] = p[1] + '\n' + p[2]
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + '\n' + p[3]


def p_literals(p):
    """
    literals : HASHTAG ID POINT CLASS
             | HASHTAG ID
             | POINT CLASS
    """
    if len(p) == 5:
        p[0] = " class=" + '"' + p[4] + '"' + " id=" + '"' + p[2] + '"'
    elif len(p) == 3:
        p[0] = p.slice[2].type.lower() + "=" + '"' + p[2] + '"'


def p_atributos(p):
    """
    atributos : atributos atributo
              | atributos COMMA atributo
              | atributo 
    """
    if len(p) == 3:
        p[0] = p[1] + " " + p[2]
    elif len(p) == 4:
        p[0] = p[1] + " " + p[3]
    elif len(p) == 2:
        p[0] = p[1]


def p_atributo(p):
    """
    atributo : ATTRIBUTE atr QUESTION_MARK atr TWO_POINTS atr
             | ATTRIBUTE atr PLUS atr
             | ATTRIBUTE atr  
    """
    if len(p) == 7:
        if p[2] == True:
            p[0] = p[1] + '"' + p[4] + '"'
        else:
            p[0] = p[1] + '"' + p[6] + '"'
    elif len(p) == 5:
        p[0] = p[1] + '"' + p[2] + p[4] + '"'
    elif len(p) == 3:
        p[0] = p[1] + '"' + p[2] + '"'


def p_atr_value(p):
    'atr : ATTRIBUTE_VALUE'
    p[1] = p[1].replace("'","")
    p[1] = p[1].replace('"',"")
    p[0] = p[1]


def p_atr_var(p):
    'atr : ATTRIBUTE_VAR'
    if p[1] in variaveis.keys():
        p[0] = variaveis[p[1]]

def p_cond(p):
    """
    cond : cond CONJ cond
         | NEG cond
         | cond DIJ cond
         | cond EQUIVALENCIA cond
         | cond DIF cond
         | cond MENOR cond
         | cond MENORIGUAL cond
         | cond MAIOR cond
         | cond MAIORIGUAL cond
         | express
    """
    if len(p) == 3:
        p[0] = not p[2]
    if len(p) == 4:
        if p.slice[2].type == 'CONJ':
            p[0] = p[1] and p[3]
        elif p.slice[2].type == 'DIJ':
            p[0] = p[1] or p[3]
        elif p.slice[2].type == "EQUIVALENCIA":
            p[0] = p[1] == p[3]
        elif p.slice[2].type == 'DIF':
            p[0] = p[1] != p[3]
        elif p.slice[2].type == 'MENORIGUAL':
            p[0] = p[1] <= p[3]
        elif p.slice[2].type == 'MAIORIGUAL':
            p[0] = p[1] >= p[3]
        elif p.slice[2].type == 'MENOR':
            p[0] = p[1] < p[3]
        elif p.slice[2].type == 'MAIOR':
            p[0] = p[1] > p[3]
    elif len(p) == 2:
        p[0] = p[1]


def p_express(p):
    """
    express : express PLUS term
            | express MENOS term
            | term
    """

    if len(p) == 4 and p.slice[2].type == "PLUS":
        p[0] = p[1] + p[3]
    elif len(p) == 4 and p.slice[2].type == "MENOS":
        p[0] = p[1] - p[3]
    elif len(p) == 2:    
        p[0] = p[1]


def p_term(p):
    """
    term : term MULT factor
         | term DIV factor
         | factor
    """
    if len(p) == 4 and p.slice[2].type == "MULT":
        p[0] = p[1] * p[3]
    if len(p) == 4 and p.slice[2].type == "DIV":
        p[0] = p[1] / p[3]
    elif len(p) == 2:    
        p[0] = p[1]


def p_factor(p):
    """
    factor : PA express PF
           | VAR_COND
           | VALUE_COND
    """
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 2:
        if p.slice[1].type == "VAR_COND": 
            if p[1] in variaveis.keys():
                p[0] = variaveis[p[1]]
            else:
                p[0] = False                             
        else:
            p[0] = int(p[1])


# Define a rule so we can track line numbers
def p_newline(p):
    p.lineno += len(p.value)

def p_error(p):
    print('Syntax error: ', p, ' Line: ', p.lineno)


#############################################################


parser = yacc.yacc()

def parse_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def pug_to_html(pug_file):
    pug_code = parse_file(pug_file)
    html_code = parser.parse(pug_code, tracking=False, debug=False)
    
    with open("outputs/output3.html", "w", encoding="utf-8") as f:
        f.write(html_code)

pug_to_html('datasets/ex3.pug')