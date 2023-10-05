from iplot.source.go.goBox import goBox 
from iplot.source.go.goDado import goDado
from iplot.source.go.goMaximo import goMaximo 
from iplot.source.go.goMinimo import goMinimo
class buscaIntercambio():

    def __init__(self):
        pass

    def interpreta(self, classe, legenda, mneumonico, cor, string):
        if(mneumonico == "interc"):
            if(len(string.split('-')) == 2):
                sbmDE = string.split('-')[0]
                sbmPARA = string.split('-')[1]
                return goDado(classe.intercambio(sbmDE, sbmPARA), classe.estagio, "MW", None, cor, legenda)
            elif(len(string.split('-')) == 1):
                return goDado(classe.intercambioTotalSubmercado(string), classe.estagio, "MW", None, cor, legenda)

        else:
            return 0
    