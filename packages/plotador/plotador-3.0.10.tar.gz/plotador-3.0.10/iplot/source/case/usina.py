from iplot.source.go.goBox import goBox 
from iplot.source.go.goDado import goDado
from iplot.source.go.goMaximo import goMaximo 
from iplot.source.go.goMinimo import goMinimo
class buscaUsina():

    def __init__(self):
        pass

    def interpreta(self, classe, legenda, mneumonico, cor, string):

        if(mneumonico == "qafl_usi"):
            return goDado(classe.vazaoNaturalAfluenteUsina(string), classe.estagio, "m3s", "estagios", cor, legenda)
        elif(mneumonico == "qdef_usi"):
            return goDado(classe.vazaoDefluenteUsina(string), classe.estagio, "m3s", "estagios", cor, legenda)
        elif(mneumonico == "qdef_min_usi"):
            return goMinimo(classe.vazaoDefluenteMinimaUsina(string), classe.estagio, "m3s", "estagios", cor, legenda)
        elif(mneumonico == "qtur_usi"):
            return goDado(classe.vazaoTurbinadaUsina(string), classe.estagio, "m3s", "estagios", cor, legenda)
        elif(mneumonico == "qver_usi"):
            return goDado(classe.vazaoVertidaUsina(string), classe.estagio, "m3s", "estagios", cor, legenda)
        elif(mneumonico == "vfim_usi"):
            return goDado(classe.volumeFinalUsina(string), classe.estagio, "hm3", "estagios", cor, legenda)
        elif(mneumonico == "gh_usi"):
            return goDado(classe.geracaoHidreletricaUsina(string), classe.estagio, "MW", "estagios", cor, legenda)
        else:
            return 0
    