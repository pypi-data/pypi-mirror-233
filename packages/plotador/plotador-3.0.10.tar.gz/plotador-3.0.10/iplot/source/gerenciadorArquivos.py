from iplot.modelo.SDDP import dadosSDDP
from iplot.modelo.Newave import dadosNewave
import os
class gerenciadorArquivos():

    def __init__(self):
        self.__mapaCasos = {}
        self.bancoCores = [ "#ffa600", "#0c255c", "#f76047", "#4b335b" , "red", "black", "blue" , "gray", "green", "magenta"] 
        self.__mapaCores = {} # #fc3a52
        self.listaCasosNewave = []
        self.listaCasosSDDP = [] #"#870A28", "#00613C", 
        self.contador = 0
          
    def add(self, path, color = None):
        if(os.path.exists(path+"/SIN")):
            caso = dadosSDDP(path)
            self.listaCasosSDDP.append(path)
        else:
            caso = dadosNewave(path)
            self.listaCasosNewave.append(path)
        self.__mapaCasos[path] = caso
        self.configuracao(path,color)
        
    def configuracao(self, caminhoCompletoCaso,cor):
        idCor = self.bancoCores[self.contador] if cor is None else cor
        self.__mapaCores[caminhoCompletoCaso] = idCor
        if cor is None: self.contador += 1
        return cor
    

    @property
    def mapaCores(self):
        return self.__mapaCores
    
    @property
    def mapaCasos(self):
        return self.__mapaCasos
    
    def getClasse(self, caso):
        return self.__mapaCasos[caso]