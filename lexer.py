from lib2to3.pgen2 import literals
from sly import Lexer

# from yacc import CalcParser

class LexerBasico(Lexer):
    
    # Declaração de todos os tokens envolvidos na criação
    tokens = { ID, SE, ELSE, PRINT, ENTAO, PARA, ATE, OR, AND, XOR, TRUE, FALSE, NUMERO, MAIS, MENOS, VEZES, DIVIDIDO, EXP, IGUAL, DIFERENTE, ATRIBUICAO, PARENESQ, PARENDIR, LT, LE,
              GT, GE, STRING }
    
    ignore = ' \t'
    ignore_comment = r'\#.*'
    
    # Regex para ID's em geral: ID tem que iniciar com pelo menos uma letra minúscula, maiúscula ou _. 
    # Pode conter letras, números e _ para os próximos caracteres
    ID      = r'[a-zA-Z_]+[a-zA-Z0-9_]*'

    # ID's reservados da minha linguagem    
    ID['se'] = SE
    ID['igual'] = IGUAL
    ID['diferente'] = DIFERENTE
    ID['menor_igual'] = LE
    ID['menor'] = LT
    ID['maior_igual'] = GE
    ID['maior'] = GT
    ID['caso_contrario'] = ELSE
    ID['mostre'] = PRINT
    ID['para'] = FOR
    ID['ou'] = OR
    ID['e'] = AND
    ID['ouexc'] = XOR
    ID['verdadeiro'] = TRUE
    ID['falso'] = FALSE
    ID['para'] = PARA
    ID['ate'] = ATE
    ID['entao'] = ENTAO
    ID['elevado'] = EXP
    
    NUMERO  = r'\d+'
    STRING = r'\".*?\"'
    MAIS    = r'\+'
    MENOS   = r'\-'
    EXP = r'\*\*'
    VEZES   = r'\*'
    DIVIDIDO  = r'\/'
    ATRIBUICAO  = r'='
    PARENESQ  = r'\('
    PARENDIR  = r'\)'
    
    # Caracteres literais
    literals = { '{', '}' }
    
    # Aprofundamento de camada, quando a chave de abertura é utilizada
    @_(r'\{')
    def lbrace(self, t):
        t.type = '{'
        self.nesting_level += 1
        return t
    
    # @ serve para realizar comentários no código
    @_(r'@.*')
    def COMMENT(self, t):
        pass
    
    # Desaprofundamento de camada, quando a chave de fechamento é utilizada
    @_(r'\}')
    def rbrace(self, t):
        t.type = '}'
        self.nesting_level -= 1
        return t
    
    # Ignora novas linhas
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
    
    # Caso haja erro em algum comando
    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
    
    # Realiza a conversão do input dado para valor numérico
    @_(r'\d+')
    def NUMERO(self, t):
        t.value = int(t.value)
        return t
    
        

if __name__ == '__main__':
    data = input('Digite a expressão a ser analisada:\n')
    lexer = LexerBasico()
    
    for tok in lexer.tokenize(data):
        print(tok)
