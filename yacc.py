from numpy import isin
from sly import Parser
from lexer import LexerBasico

class ParserBasico(Parser):
    # Pega a lista de tokens do Lexer
    tokens = LexerBasico.tokens
    
    precedence = (
        ('left', MAIS, MENOS),
        ('left', VEZES, DIVIDIDO),
        ('right', EXP)
    )
    
    def __init__(self):
        self.env = {}
    
    # Regras Gramaticais e Ações
    
    # STATEMENT
    @_('')
    def statement(self, p):
        pass
        
    @_('var_assign')
    def statement(self, p):
        return p.var_assign
    
    @_('comparison')
    def statement(self, p):
        return p.comparison
        
    @_('expr')
    def statement(self, p):
        return p.expr

    @_('PRINT expr')
    def statement(self, p):
        return 'mostre', p.expr
    
    @_('PARA var_assign ATE expr ENTAO statement')
    def statement(self, p):
        return 'for', ('for_loop_setup', p.var_assign, p.expr), p.statement
    
    @_('SE expr ENTAO statement ELSE statement')
    def statement(self, p):
        return 'se', p.expr, ('branch', p.statement0, p.statement1)
    
    # ----------------------------------------------------------------------
    
    # VAR_ASSIGN
    @_('ID ATRIBUICAO expr')
    def var_assign(self, p):
        return 'var_assign', p.ID, p.expr
        
    # ----------------------------------------------------------------------
    
    # COMPARISON
    @_('expr OR expr')
    def comparison(self, p):
        return 'or', p.expr0, p.expr1

    @_('expr AND expr')
    def comparison(self, p):
        return 'and', p.expr0, p.expr1

    @_('expr XOR expr')
    def comparison(self, p):
        return 'xor', p.expr0, p.expr1
    
    @_('expr IGUAL expr')
    def comparison(self, p):
        return 'eq', p.expr0, p.expr1
    
    @_('expr DIFERENTE expr')
    def comparison(self, p):
        return 'diff', p.expr0, p.expr1
    
    @_('expr LE expr')
    def comparison(self, p):
        return 'le', p.expr0, p.expr1
    
    @_('expr LT expr')
    def comparison(self, p):
        return 'lt', p.expr0, p.expr1
    
    @_('expr GE expr')
    def comparison(self, p):
        return 'ge', p.expr0, p.expr1
    
    @_('expr GT expr')
    def comparison(self, p):
        return 'gt', p.expr0, p.expr1
    
    # ----------------------------------------------------------------------

    # EXPR
    @_('term MAIS expr')
    def expr(self, p):
        return 'add', p.expr, p.term
    
    @_('term MENOS expr')
    def expr(self, p):
        return 'sub', p.expr, p.term
    
    @_('term')
    def expr(self, p):
        return p.term
    
    # ----------------------------------------------------------------------
    
    # TERM
    @_('midexp')
    def term(self, p):
        return p.midexp
    
    @_('midexp VEZES term')
    def term(self, p):
        return 'mul', p.term, p.midexp
    
    @_('midexp DIVIDIDO term')
    def term(self, p):
        return 'div', p.term, p.midexp
    
    # ----------------------------------------------------------------------
    
    # MIDEXP
    @_('factor EXP midexp')
    def midexp(self, p):
        return 'exp', p.factor, p.midexp
    
    @_('factor')
    def midexp(self, p):
        return p.factor
    
    # ----------------------------------------------------------------------
    
    # FACTOR
    @_('NUMERO')
    def factor(self, p):
        return p.NUMERO
    
    @_('STRING')
    def factor(self, p):
        return p.STRING
    
    @_('ID')
    def factor(self, p):
        return 'var', p.ID
    
    @_('TRUE')
    def factor(self, p):
        return True
    
    @_('FALSE')
    def factor(self, p):
        return False
    
    @_('PARENESQ statement PARENDIR')
    def factor(self, p):
        return p.statement


# Classe de execução dos comandos lidos, para percorrimento da árvore
class ExecuteJeantugol:
    def __init__(self, tree, variables):
        self.variables = variables
        result = self.walkTree(tree)
        if result is None:
            pass
        elif result is not None and type(result) in [int, float]:
            print(result)
        elif isinstance(result, str):
            print(result)
        elif isinstance(result, bool):
            if result is True:
                print('verdadeiro')
            else:
                print('falso')

    # Caminha pelos nós da árvore, realizando as operações, sempre dos das folhas até a raiz
    def walkTree(self, node):
        if isinstance(node, int) or isinstance(node, str):
            return node
        
        if node is None:
            return None
        
        if node[0] == 'mostre':
            return self.walkTree(node[1])
        if node[0] == 'num':
            return node[1]
        if node[0] == 'str':
            return node[1]
        if node[0] == 'eq':
            return self.walkTree(node[1]) == self.walkTree(node[2])
        if node[0] == 'gt':
            return self.walkTree(node[1]) > self.walkTree(node[2])
        if node[0] == 'or':
            return self.walkTree(node[1]) or self.walkTree(node[2])
        if node[0] == 'and':
            return self.walkTree(node[1]) and self.walkTree(node[2])
        if node[0] == 'xor':
            return self.walkTree(node[1]) ^ self.walkTree(node[2])
        if node[0] == 'le':
            return self.walkTree(node[1]) <= self.walkTree(node[2])
        if node[0] == 'lt':
            return self.walkTree(node[1]) < self.walkTree(node[2])
        if node[0] == 'ge':
            return self.walkTree(node[1]) >= self.walkTree(node[2])
        if node[0] == 'gt':
            return self.walkTree(node[1]) > self.walkTree(node[2])
        if node[0] == 'diff':
            return self.walkTree(node[1]) != self.walkTree(node[2])
        if node[0] == 'se':
            resultado = self.walkTree(node[1])
            if resultado:
                return self.walkTree(node[2][1])
            else:
                return self.walkTree(node[2][2])
        if node[0] == 'for':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])
                
                loop_count = loop_setup[0]
                loop_limit = loop_setup[1]
                
                for i in range(loop_count + 1, loop_limit + 1):
                    resultado = self.walkTree(node[2])
                    if resultado is not None:
                        if isinstance(resultado, bool):
                            if resultado == True:
                                print('verdadeiro')
                            elif resultado == False:
                                print('falso')
                        else:
                            print(resultado)
                    self.variables[loop_setup[0]] = i
                    self.variables[node[1][1][1]] += 1
                del self.variables[loop_setup[0]]
                
        if node[0] == 'for_loop_setup':
            return self.walkTree(node[1]), self.walkTree(node[2])
        
        
        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])
        elif node[0] == 'exp':
            return self.walkTree(node[1]) ** self.walkTree(node[2])
        
        if node[0] == 'var_assign':
            self.variables[node[1]] = self.walkTree(node[2])
            return node[2]
        
        if node[0] == 'var':
            try:
                return self.variables[node[1]]
            except LookupError:
                print(f'Nome não definido: '.format(node[1]))
                return 0


# Parte inicial, que lê os comandos e realiza os procedimentos adequados
if __name__ == '__main__':
    lexer = LexerBasico()
    parser = ParserBasico()
    env = {}
    while True:
        try:
            text = input('JEANTUGOL > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            ExecuteJeantugol(tree, env)
