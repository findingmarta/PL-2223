import ply.yacc as yacc

from programa_lex import tokens


# Regras de produção da gramática
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
    html_code = ''
    parser.parse(pug_code, tracking=True, debug=False)
    return html_code

if __name__ == '__main__':
    print(pug_to_html('datasets/ex1.pug'))