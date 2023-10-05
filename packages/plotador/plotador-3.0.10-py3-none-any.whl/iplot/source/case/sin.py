from iplot.source.go.goBox import goBox 
from iplot.source.go.goDado import goDado
from iplot.source.go.goMaximo import goMaximo 
from iplot.source.go.goMinimo import goMinimo
class buscaSIN():

    def __init__(self):
        pass

    def interpreta(self, classe, legenda, mneumonico, cor):
        if(mneumonico == "gh_sin"):
            return goDado(classe.geracaoHidreletricaSIN, classe.estagio, "MW", None, cor, legenda)
        elif(mneumonico == "gt_sin"):
            return goDado(classe.geracaoTermicaSIN, classe.estagio, "MW", None, cor, legenda)
        elif(mneumonico == "earm_sin"):
            return goDado(classe.earmSIN, classe.estagio, "MW", None, cor, legenda)
        elif(mneumonico == "enaflu_sin"):
            return goDado(classe.enafluSIN, classe.estagio, "MW", None, cor, legenda)
        elif(mneumonico == "evert_sin"):
            return goDado(classe.enevertSIN, classe.estagio, "MW", None, cor, legenda)
        elif(mneumonico == "enaflu_sin_cen"):
            return goBox(classe.enafluSIN_Serie, None, "MW", None, cor, legenda)
        else:
            return 0
    