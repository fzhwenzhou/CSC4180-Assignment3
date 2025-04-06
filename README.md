# CSC4180 Assignment 3
## Name: Fang Zihao, Student ID: 122090106

# Q1. Resolve Ambiguity for Micro Language Grammar
## 1. 
The counter example is like:
```
a + b - c
```  
According to the Context-Free Grammar, this will apply to the Rule 8:
```
<expression> -> <primary> {<add op> <primary>}
```
Thus, the expression will be parsed as:
```
<expression> -> ID PLUOP ID MINUSOP ID
```
However, as for how to generate the parse tree and abstract syntax tree, it depends on the parsing direction. If the parser parses from the left to right, it will generate the following abstract syntax tree:
```
           PLUOP
           /   \
          /     \
         ID   MINUSOP
              /     \
             /       \
            ID       ID
```
If the parser parses from the right to left, it will generate the following abstract syntax tree:
```
           MINUSOP
           /     \
          /       \
        PLUOP     ID
        /   \
       /     \
      ID     ID
```
Both are legal. Therefore, the grammar of Micro Language is ambiguous.
## 2.
### (a)
No. It could mean that the grammar needs more look-ahead tokens, or is not suitable for LL parsing technique, but not necessarily mean that the grammar is ambiguous.
### (b) 
Yes. Since there is no multiply defined entry in the LL(1) parsing table of the grammar, the LL(1) parser is valid. By the definition, if a grammar is parsable by LL(1) parser, then it cannot be ambiguous.

# Q2. Simple LL(1) and LR(0) Parsing Exercises
## LL(1) Grammar
### 1.
Both E and T are multiply defined, because both of them have multiple definitions that share the common prefix. For E, it is T. For T, it is int. Therefore, to resolve the multiply defined entries and eliminate ambiguities, we need to use left factoring to factorize the common prefix, and then define a new non-terminal to represent the rest. The result LL(1) Grammar is as follows:
```
E -> T E'
E' -> + T E'
E' -> ε
T -> F T'
T' -> * F T'
T' -> ε
F -> ( E )
F -> int
```
### 2.
The translated LL(1) Grammar is as follows:
```
E ::= T E'
E' ::= + T E'
E' ::= ''
T ::= F T'
T' ::= * F T'
T' ::= ''
F ::= ( E )
F ::= int
```
The two tables are as follows:
![first_follow](assets/ll1_first_follow.png)
*First, Follow, and Nullable Table*

![parse_table](assets/ll1_parse_table.png)
*Parse Table*

## 3. 
The generated parse tree is as follows:
![parse_tree](assets/ll1_parse_tree.png)
*Parse Tree*

## LR(0) Grammar
## 1. 
The generated LR(0) automaton is as follows:
![automaton_table](assets/lr0_fa_states.png)
*LR(0) Automaton Table*

![automaton_diagram](assets/lr0_fa.png)
*LR(0) DFA Diagram*

# Q3. Implement LL(1) Parser by hand for Oat v.1 
## Usage
To run the hand-written LL(1) Parser, simply follow the usage of the program:
```
Usage: python3 parser.py <grammar file> <input file> <output png file>
```
Where:
- "grammar file" is the path to the grammar file. In this case, it is "Oat-v1-LL1-grammar.txt." Of course, it can be any valid LL(1) grammar, as long as you also modify the Scanner class.
- "input file" is the path to the input source code.
- "output png file" is the path to the output parse tree in PNG format. 


## Explanations
1. The original production rules cannot be used directly for LL(1) parsing, as it contains left recursions and backtracking, which should not appear in valid LL(1) grammar. For example, one of the production rules is `exp ::= exp bop exp`, which contains  left recursion (exp as the left-most non-terminal).
2. 
# Bonus. Implement a Bottom-Up Parser using Yacc for Oat v.1 Language
## Usage
To run the Yacc-based Parser, simply follow the usage of the program:
```
Usage: python3 yacc.py <input file> <output png file>
```
Where:
- "input file" is the path to the input source code.
- "output png file" is the path to the output parse tree in PNG format.

## Explanations