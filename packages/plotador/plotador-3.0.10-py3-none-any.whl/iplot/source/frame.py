
class frame():
    def __init__(self, chave, identificador, linha, coluna):
       self.chave = chave
       self.identificador = identificador
       self.linha = linha
       self.coluna = coluna
       self.listaGO = []
       self.titulo = None

    def addListaGO(self, GO):
        self.listaGO.append(GO)
    
    def setListaGO(self, listaGO):
        self.listaGO = listaGO

    def getListaGO(self):
        return self.listaGO
        
    def getTitulo(self):
        tituloIdentificador = "_" if self.identificador is None else self.identificador
        self.titulo = self.chave+"_"+tituloIdentificador
        return self.titulo

    #def 