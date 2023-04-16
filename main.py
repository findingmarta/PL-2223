import ply.lex as lex
import ply.yacc as yacc

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
t_ID = r'#[a-zA-Z][a-zA-Z0-9]*'
t_CLASS = r'\.[a-zA-Z][a-zA-Z0-9]*'
t_TEXT = r'([^#\.\{\}])+'
t_ATTRIBUTE = r'\([a-zA-Z][a-zA-Z0-9]*(=("[^"]*"|\'[^\']*\'))?\)'

# Ignora espaços em branco e tabulações
t_ignore = ' \t'

def parse_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

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

def p_attr_with_quoted_value(p):
    'attr : ATTRIBUTE QUOTED_TEXT'
    p[0] = ' {}="{}"'.format(p[1][1:], p[2][1:-1])

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

def p_error(p):
    if p:
        print("Erro de sintaxe na entrada em linha", p.lineno)
    else:
        print("Erro de sintaxe no final da entrada")

lexer = lex.lex()
parser = yacc.yacc()

def pug_to_html(pug_file):
    pug_code = parse_file(pug_file)
    html_code = ''
    parser.parse(pug_code, tracking=True, debug=False)
    return html_code

if __name__ == '__main__':
    #exemplo.pu deve ser substituido pelo nome do ficheiro pug que queremos substituir
    print(pug_to_html('ex1.pug'))