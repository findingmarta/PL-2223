import ply.yacc as yacc

from programa_lex import tokens


variaveis = {}


# Regras de produção da gramática
def p_elemList(p):
    """elemList : elemList elem
                | empty
    """
    if len(p) == 2:
        p[0] = p[1] + p[2]
    else:
        pass

def p_elem(p):
    """
    elem : INDENT tag elemList
         | INDENT condition
         | INDENT VAR_JS VAR_NAME EQUALS VAR_VALUE
         | INDENT BLOCK_TEXT
         | TEXT
    """
    if len(p) == 4:
        p[0] = (p[1] * p[1].value) + f"<{p[1]}>" + p[3] + '\n'
    elif len(p) == 6:
        variaveis[p[3]] = p[5]
    elif len(p) == 3:
        p[0] = (p[1] * p[1].value) + p[2]
    elif len(p) == 2:
        p[0] = p[1]

def p_tag(p):
    """
    tag : TAG PA atributos PF
        | TAG HASHTAG ID
        | HASHTAG ID
        | TAG POINT CLASS
        | TAG
    """
    if len(p) == 5:
        p[0] = p[1] + " " + p[3]
    elif len(p) == 4:
        p[0] = p[1] + p[3].type.lower() + "=" + p[3]
    elif len(p) == 3:
        p[0] = "div id=" + p[2]
    elif len(p) == 2:
        p[0] = p[1]

def p_conditon(p):
    """
    condition : IF cond elemList INDENT ELSE elemList
              | IF cond elemList
              | WHILE cond elemList
    """

def p_cond(p):
    """
    cond : cond & & cond 
         | cond | | cond 
         | cond < cond
         | cond <= cond
         | cond > cond
         | cond >= cond
         | cond == cond
         | cond != cond
         | express
    """

def p_express(p):
    """
    express : express PLUS term
            | express - term
            | term
    """

def p_term(p):
    """
    term : term * factor 
         | term / factor
         | factor
    """
    p[0] = p[1]

def p_factor(p):
    """
    factor : PA express PF
           | VAR_COND
           | VALUE_COND
    """

def p_atributos(p):
    """
    atributos : atributos atributo
              | atributos COMMA atributo 
              | atributo 
    """

def p_atributo(p):
    """
    atributo : ATTRIBUTE atr 
             | ATTRIBUTE atr QUESTION_MARK atr TWO_POINTS atr 
    """

def p_atr(p):
    """
    atr : ATTRIBUTE_VALUE
        | ATTRIBUTE_VAR
    """













def p_tag(p):
    'tag : TAG'
    p[0] = '<{}>'.format(p[1])

def p_tag_with_id(p):
    'tag : TAG ID'
    p[0] = '<{} id="{}">'.format(p[1], p[2][1:])

def p_tag_with_class(p):
    'tag : TAG class_list'
    p[0] = '<{}{}>'.format(p[1], ''.join(p[2]))

def p_tag_with_id_and_class(p):
    'tag : TAG ID class_list'
    p[0] = '<{} id="{}"{}>'.format(p[1], p[2][1:], ''.join(p[3]))

def p_tag_with_text(p):
    'tag : TAG TEXT'
    p[0] = '<{}>{}</{}>'.format(p[1], p[2], p[1])

def p_tag_with_attr(p):
    'tag : TAG attr_list'
    p[0] = '<{}{}>'.format(p[1], ''.join(p[2]))

def p_tag_with_id_attr(p):
    'tag : TAG ID attr_list'
    p[0] = '<{} id="{}"{}>'.format(p[1], p[2][1:], ''.join(p[3]))

def p_tag_with_class_attr(p):
    'tag : TAG class_list attr_list'
    p[0] = '<{}{}{}>'.format(p[1], ''.join(p[2]), ''.join(p[3]))

def p_tag_with_id_class_attr(p):
    'tag : TAG ID class_list attr_list'
    p[0] = '<{} id="{}"{}{}>'.format(p[1], p[2][1:], ''.join(p[3]), ''.join(p[4]))

def p_attr(p):
    'attr : ATTRIBUTE'
    p[0] = p[1]

def p_attr_with_value(p):
    'attr : ATTRIBUTE TEXT'
    p[0] = ' {}="{}"'.format(p[1][1:], p[2])

#def p_attr_with_quoted_value(p):
#    'attr : ATTRIBUTE QUOTED_TEXT'
#    p[0] = ' {}="{}"'.format(p[1][1:], p[2][1:-1])

def p_attr_list(p):
    'attr_list : attr'
    p[0] = [p[1]]

def p_attr_list_multiple(p):
    'attr_list : attr_list "," attr'
    p[0] = p[1] + [p[3]]

def p_class(p):
    'class : CLASS'
    p[0] = ' class="{}"'.format(p[1][1:])

def p_class_list_single(p):
    'class_list : class'
    p[0] = [p[1]]

def p_class_list_multiple(p):
    'class_list : class_list class'
    p[0] = p[1] + [p[2]]

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
    
    with open("outputs/output1.html", "w", encoding="utf-8") as f:
        f.write(html_code)

if __name__ == '__main__':
    pug_to_html('datasets/ex1.pug')