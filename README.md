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
### (b) s valid. By the definition, if a grammar is parsable by LL(1) parser, then it cannot be ambiguous.

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




## 3. 
The generated parse tree is as follows:



## LR(0) Grammar
## 1. 
