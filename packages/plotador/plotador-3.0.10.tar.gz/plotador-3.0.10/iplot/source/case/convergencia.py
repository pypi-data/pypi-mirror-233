from iplot.source.go.goBox import goBox 
from iplot.source.go.goDado import goDado
from iplot.source.go.goMaximo import goMaximo 
from iplot.source.go.goMinimo import goMinimo
class buscaConvergencia():

    def __init__(self):
        pass

    def interpreta(self, classe, legenda, mneumonico, cor):
        if(mneumonico == "zinf"):
            return goDado(classe.zinf, classe.iter, "1000R$", None, cor, legenda)
        else:
            return 0
    