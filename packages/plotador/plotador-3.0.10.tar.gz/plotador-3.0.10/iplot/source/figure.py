
from iplot.source.frame import frame
from iplot.source.interpretador import interpretador
class Figura():
    def __init__(self, nome):
       self.nome = nome
       self.__listaFrames = []
       self.__mapaTitulos = {}
       self.titulo = self.nome
       
    def createFrame(self,key, identificator, lin, col, gerenciadorArquivos):
        Frame = frame(key, identificator, lin, col)
        Frame.setListaGO(interpretador().retornaListasGO(Frame, gerenciadorArquivos))
        self.__listaFrames.append(Frame)

    def addFrame(self, Frame):
        self.__listaFrames.append(Frame)



    
    @property
    def max_linha(self):
        linhas = []
        for Frame in self.__listaFrames:
            linhas.append(Frame.linha)
        return max(linhas)
    
    @property
    def max_coluna(self):
        colunas = []
        for Frame in self.__listaFrames:
            colunas.append(Frame.coluna)
        return max(colunas)


    @property
    def listaFrames(self):
        contadorTemporario = 0
        for linha in range(1,self.max_linha+1):
            for coluna in range(1,self.max_coluna+1):
                self.__mapaTitulos[(linha,coluna)] = contadorTemporario
                contadorTemporario += 1
        return self.__listaFrames

    def getPosicaoTitulo(self, linha, coluna):
        return self.__mapaTitulos[(linha, coluna)]
    



    
        
