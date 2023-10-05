from iplot.source.go.goBox import goBox 
from iplot.source.go.goDado import goDado
from iplot.source.go.goMaximo import goMaximo 
from iplot.source.go.goMinimo import goMinimo
class buscaSubmercado():

    def __init__(self):
        pass

    def interpreta(self, classe, legenda, mneumonico, cor, string):
        if(mneumonico == "gh_sbm"):
            return goDado(classe.geracaoHidreletricaSubmercado(string), classe.estagio, "MW", None, cor, legenda)
        elif(mneumonico == "gt_sbm"):
            return goDado(classe.geracaoTermicaSubmercado(string), classe.estagio, "MW", None, cor, legenda)
        elif(mneumonico == "cmo_sbm"):
            return goDado(classe.cmoSubmercado(string), classe.estagio, "MW", None, cor, legenda)
        elif(mneumonico == "earm_sbm"):
            return goDado(classe.earmSubmercado(string), classe.estagio, "MW", None, cor, legenda)
        elif(mneumonico == "ever_sbm"):
            return goDado(classe.enevertSubmercado(string), classe.estagio, "MW", None, cor, legenda)
        elif(mneumonico == "eafl_sbm"):
            return goDado(classe.enafluSubmercado(string), classe.estagio, "MW", None, cor, legenda)
            #ADICIONAR MNEUMONICO DE VVER_SBM, VFIM_SBM, VAFL_SBM, VDEF_SBM
        elif(mneumonico == "enaflu_sbm_cen"):
            return goBox(classe.enafluSubmercado_Serie(string), None, "MW", None, cor, legenda)
        else:
            return 0
    