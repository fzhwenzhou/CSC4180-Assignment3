 # type: ignore
from sys import argv
from scanner import Scanner, reserved, literal_tokens
import pydot

other_tokens = {
    'id': 'ID',
    'intliteral': 'INTLITERAL',
    'stringliteral': 'STRINGLITERAL'
}

tokens = {
    **reserved,
    **literal_tokens,
    **other_tokens
}


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



class Parser:
    def __init__(self, grammar):
        self.start = None
        self.first = {}
        self.follow = {}
        self.terminals = set()
        self.nullable = []
        self.productions = {}
        self.table = {}
        grammar = grammar.split('\n')
        for line in grammar:
            # Check empty line
            line = line.strip()
            if not line:
                continue
            left, right = line.split('::=')
            left, right = f'<{left.strip()}>', right.strip()
            right = right.split() if right != '\'\'' else []
            right = list(map(lambda x: tokens.get(x, f'<{x}>'), right))
            if not self.start:
                self.start = left
            if left not in self.productions:
                self.productions[left] = [right]
            else:
                self.productions[left].append(right)
            
        for productions in self.productions.values():
            for production in productions:
                for symbol in production:
                    if symbol not in self.productions:
                        self.terminals.add(symbol)
        self.terminals.add('$') # End symbol
        
        self.compute_nullable()
        self.compute_first()
        self.compute_follow()
        self.compute_table()
    
    # Helper function
    def first_of_sequence(self, symbols):
        first = set()
        for symbol in symbols:
            if symbol in self.terminals:
                first.add(symbol)
                break
            else:
                first.update(self.first[symbol] - {'ε'})
                if symbol not in self.nullable:
                    break
        else:
            first.add('ε')
        return first        
    
    def compute_first(self):
        changed = True
        while changed:
            changed = False
            for non_terminal in self.productions.keys():
                if non_terminal not in self.first:
                    self.first[non_terminal] = set()
                original_first = self.first[non_terminal].copy()
                for production in self.productions[non_terminal]:
                    first = set()
                    for symbol in production:
                        if symbol == '':
                            pass
                        elif symbol in self.terminals:
                            first.add(symbol)
                            break
                        else:
                            first.update(self.first.get(symbol, set()))
                            if symbol not in self.nullable:
                                break
                    self.first[non_terminal].update(first)
                if self.first[non_terminal] != original_first:
                    changed = True
    
    
    def compute_follow(self):
        self.follow[self.start] = {'$'}
        changed = True
        while changed:
            changed = False
            for non_terminal in self.productions:
                for production in self.productions[non_terminal]:
                    trailer = self.follow.get(non_terminal, set()).copy()
                    for symbol in reversed(production):
                        if symbol in self.productions:
                            if symbol not in self.follow:
                                self.follow[symbol] = set()
                            original_follow = self.follow[symbol].copy()
                            self.follow[symbol].update(trailer)
                            if self.follow[symbol] != original_follow:
                                changed = True
                            if symbol in self.nullable:
                                trailer.update(self.first.get(symbol, set()) - {'ε'})
                            else:
                                trailer = self.first.get(symbol, set()) - {'ε'}
                        else:
                            trailer = {symbol}
                            
            
    def compute_nullable(self):
        self.nullable = []
        changed = True
        while changed:
            changed = False
            for non_terminal in self.productions:
                for production in self.productions[non_terminal]:
                    if all(symbol in self.nullable or symbol == 'ε' for symbol in production):
                        if non_terminal not in self.nullable:
                            self.nullable.append(non_terminal)
                            changed = True
    
    def compute_table(self):
        for non_terminal, productions in self.productions.items():
            for production in productions:
                first_production = self.first_of_sequence(production)
                for i in first_production - {'ε'}:
                    self.table[(non_terminal, i)] = production
                if 'ε' in first_production:
                    for i in self.follow[non_terminal]:
                        self.table[(non_terminal, i)] = production
        
    
    def parse(self, file):
        '''
        Parse the inputs
        The result will be represented as a list of lists
        '''
        inputs = [tok[0] for tok in Scanner().scan(file)] + ['$']
        stack = [self.start]
        parse_tree = [self.start]
        index = 0 
        tree_stack = [(parse_tree, index)]
        
        while stack:
            symbol = stack.pop()
            current_node, current_idx = tree_stack.pop()
            if symbol in self.terminals:
                if symbol == inputs[index]:
                    current_node[current_idx] = symbol
                    index += 1
                else:
                    raise RuntimeError('Unexpected end of symbol.')
            else:
                key = (symbol, inputs[index])
                if key not in self.table:
                    raise RuntimeError(f'No such production rule {key} in parse table.')
                production = self.table[key]
                subtree = [symbol] + production
                current_node[current_idx] = subtree
                for i, p in reversed(list(enumerate(production))):
                    if p != 'ε':
                        stack.append(p)
                        tree_stack.append((subtree, i + 1))
                
        
        return parse_tree[0]     


if len(argv) != 4:
    print('Usage: python3 yacc.py <grammar file> <input file> <output png file>')
    exit(1)

with open(argv[1], 'r') as f:
    parser = Parser(f.read())

tree = tree_to_dot(parser.parse(argv[2]))
tree.write_png(argv[3])