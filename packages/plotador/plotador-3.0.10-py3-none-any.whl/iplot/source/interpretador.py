from iplot.source.case.sin import buscaSIN
from iplot.source.case.usina import buscaUsina
from iplot.source.case.submercado import buscaSubmercado
from iplot.source.case.convergencia import buscaConvergencia
from iplot.source.case.intercambio import buscaIntercambio

class interpretador():

    def __init__(self):
        self.__mneumonicos = ["gh_sin", "gt_sin", "earm_sin", "enaflu_sin", "evert_sin", "qafl_usi",
                "qdef_usi", "qtur_usi", "qver_usi", "vfim_usi", "gh_usi", "enaflu_sin_cen", 
                "gh_sbm", "gt_sbm", "cmo_sbm", "earm_sbm", "ever_sbm", "eafl_sbm",
                "zinf", "interc", "enaflu_sbm_cen"]
        
    def help(self):
        print(self.__mneumonicos)

    
    def retornaListasGO(self, frame, gerenciadorArquivos):
        listaGO = []
        for caso in gerenciadorArquivos.mapaCasos:
            cor = gerenciadorArquivos.mapaCores[caso]
            listaGO.append(self.interpreta(gerenciadorArquivos.getClasse(caso), frame.chave, cor, frame.identificador))
        return listaGO

    def interpreta(self, classe, mneumonico, cor, string = None):
        caminho = classe.caminho
        legenda = self.legenda(caminho)
        mneumonico = mneumonico.lower()
        string = None if string is None else string.upper()
        
        GO = buscaSIN().interpreta(classe, legenda, mneumonico, cor)
        if(GO != 0 ): return GO
        GO = buscaUsina().interpreta(classe, legenda, mneumonico, cor, string)
        if(GO != 0 ): return GO
        GO = buscaSubmercado().interpreta(classe, legenda, mneumonico, cor, string)
        if(GO != 0 ): return GO
        GO = buscaConvergencia().interpreta(classe, legenda, mneumonico, cor)
        if(GO != 0 ): return GO
        GO = buscaIntercambio().interpreta(classe, legenda, mneumonico, cor, string)
        if(GO != 0 ): return GO

        if(GO == 0):
            print("MNEUMONICO ERRADO, TENTEI ALGUNS DOS MNEUMONICOS A SEGUIR:")
            print(self.__mneumonicos)
            exit(1)
            return 0
    
    def legenda(self, caso):
        return caso.split("/")[-1]