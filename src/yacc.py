from ply import yacc
from lex import tokens
from sys import argv
import pydot, warnings

cnt = 0
def convert(dot, lst, head):
    global cnt
    for elem in lst[1:]:
        cnt += 1
        if type(elem) == list:
            if len(elem) > 1:
                node = pydot.Node(f'node{cnt}', label=f'"{elem[0]}"')
                dot.add_node(node)
                convert(dot, elem, node)
        else:
            elem = elem.replace('"', '\\"')
            node = pydot.Node(f'node{cnt}', label=f'"{elem}"')
            dot.add_node(node)
        if 'node' in locals() and len(dot.get_edge(head.get_name(), node.get_name())) == 0:
            dot.add_edge(pydot.Edge(head, node))

def tree_to_dot(tree, name="CST"):
    dot = pydot.Dot(name)
    head = pydot.Node(f'node0', label=f'"{tree[0]}"')
    dot.add_node(head)
    convert(dot, tree, head)
    return dot


# A translation of grammar to ply functions
# It is almost not possible to generate the grammar from the txt
# Otherwise it would require dynamic code generation

def p_prog(p):
    '''
    prog : decl prog
         |
    '''
    p[0] = ['<prog>'] + p[1:]

def p_decl(p):
    '''
    decl : gdecl
         | fdecl
    '''
    p[0] = ['<decl>'] + p[1:]

def p_gdecl(p):
    '''
    gdecl : GLOBAL ID ASSIGN gexp SEMICOLON
    '''
    p[0] = ['<gdecl>'] + p[1:]

def p_fdecl(p):
    '''
    fdecl : t ID LPAREN args RPAREN block
    '''
    p[0] = ['<fdecl>'] + p[1:]

def p_args(p):
    '''
    args : arg args_prime
         |
    '''
    p[0] = ['<args>'] + p[1:]

def p_args_prime(p):
    '''
    args_prime : COMMA arg args_prime
               |
    '''
    p[0] = ['<args\'>'] + p[1:]

def p_arg(p):
    '''
    arg : t ID
    '''
    p[0] = ['<arg>'] + p[1:]

def p_block(p):
    '''
    block : LBRACE stmts RBRACE
    '''
    p[0] = ['<block>'] + p[1:]

def p_t(p):
    '''
    t : primary_t t_arr
    '''
    p[0] = ['<t>'] + p[1:]

def p_t_arr(p):
    '''
    t_arr : LBRACKET RBRACKET
          |
    '''
    p[0] = ['<t_arr>'] + p[1:]

def p_primary_t(p):
    '''
    primary_t : TINT 
              | TBOOL 
              | TSTRING
    '''
    p[0] = ['<primary_t>'] + p[1:]

def p_gexps(p):
    '''
    gexps : gexp gexps_prime
          |
    '''
    p[0] = ['<gexps>'] + p[1:]

def p_gexps_prime(p):
    '''
    gexps_prime : COMMA gexp gexps_prime
                |
    '''
    p[0] = ['<gexps\'>'] + p[1:]

def p_gexp(p):
    '''
    gexp : INTLITERAL
         | STRINGLITERAL
         | t NULL
         | TRUE
         | FALSE
         | NEW t LBRACE gexps RBRACE
    '''
    p[0] = ['<gexp>'] + p[1:]

def p_stmts(p):
    '''
    stmts : stmt stmts
          |
    '''
    p[0] = ['<stmts>'] + p[1:]

def p_stmt_prime(p):
    '''
    stmt_prime : func_call arr_idx assign SEMICOLON
    '''
    p[0] = ['<stmt\'>'] + p[1:]

def p_func_call(p):
    '''
    func_call : LPAREN exps RPAREN
              |
    '''
    p[0] = ['<func_call>'] + p[1:]

def p_arr_idx(p):
    '''
    arr_idx : LBRACKET exp RBRACKET
            |
    '''
    p[0] = ['<arr_idx>'] + p[1:]

def p_assign(p):
    '''
    assign : ASSIGN exp
           |
    '''
    p[0] = ['<assign>'] + p[1:]

def p_stmt(p):
    '''
    stmt : ID stmt_prime
         | vdecl SEMICOLON
         | RETURN exp SEMICOLON
         | if_stmt
         | FOR LPAREN vdecls SEMICOLON exp_opt SEMICOLON stmt_opt RPAREN block
         | WHILE LPAREN exp RPAREN block
    '''
    p[0] = ['<stmt>'] + p[1:]

def p_stmt_opt(p):
    '''
    stmt_opt : stmt
             | 
    '''
    p[0] = ['<stmt_opt>'] + p[1:]

def p_if_stmt(p):
    '''
    if_stmt : IF LPAREN exp RPAREN block else_stmt
    '''
    p[0] = ['<if_stmt>'] + p[1:]

def p_else_stmt(p):
    '''
    else_stmt : ELSE else_body
              | 
    '''
    p[0] = ['<else_stmt>'] + p[1:]

def p_else_body(p):
    '''
    else_body : block
              | if_stmt
    '''
    p[0] = ['<else_body>'] + p[1:]

def p_exp_opt(p):
    '''
    exp_opt : exp
            |
    '''
    p[0] = ['<exp_opt>'] + p[1:]

def p_vdecls(p):
    '''
    vdecls : vdecl vdecls
           |
    '''
    p[0] = ['<vdecls>'] + p[1:]

def p_vdecl(p):
    '''
    vdecl : VAR ID ASSIGN exp
    '''
    p[0] = ['<vdecl>'] + p[1:]

def p_exps(p):
    '''
    exps : exp exps_prime
    '''
    p[0] = ['<exps>'] + p[1:]

def p_exps_prime(p):
    '''
    exps_prime : COMMA exp exps_prime
               |
    '''
    p[0] = ['<exps\'>'] + p[1:]

def p_exp(p):
    '''
    exp : term exp_prime
    ''' 
    p[0] = ['<exp>'] + p[1:]

def p_exp_prime(p):
    '''
    exp_prime : bop term exp_prime
              |
    '''
    p[0] = ['<exp\'>'] + p[1:]

def p_term(p):
    '''
    term : primary
         | uop primary
    '''
    p[0] = ['<term>'] + p[1:]

def p_primary(p):
    '''
    primary : ID func_call arr_idx
            | INTLITERAL
            | STRINGLITERAL
            | t NULL
            | TRUE
            | FALSE
            | LPAREN exp RPAREN
    '''
    p[0] = ['<primary>'] + p[1:]

def p_bop(p):
    '''
    bop : STAR 
        | PLUS
        | MINUS
        | LSHIFT
        | RLSHIFT
        | RASHIFT
        | LESS
        | LESSEQ
        | GREAT
        | GREATEQ
        | EQ
        | NEQ
        | LAND
        | LOR
        | BAND
        | BOR
    '''
    p[0] = ['<bop>'] + p[1:]

def p_uop(p):
    '''
    uop : MINUS
        | NOT
        | TILDE
    '''
    p[0] = ['<uop>'] + p[1:]

def p_error(p):
    print(f'Error: Syntax error at {p}')
 
parser = yacc.yacc(errorlog=yacc.NullLogger())


if len(argv) != 3:
    print('Usage: python3 yacc.py <input file> <output png file>')
    exit(1)
    
with open(argv[1], 'r') as f:
    tree = tree_to_dot(parser.parse(f.read()))
    tree.write_png(argv[2])