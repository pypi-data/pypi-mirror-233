
import pandas as pd
import sys
#sys.path.append("/home/david/git/isddp")
from isddp.sddp import LeituraPersonalizadaSDDP
from isddp.sddp import Convergencia


class dadosSDDP():

    def __init__(self, caminhoSDDP):
        self.caminhoSDDP = caminhoSDDP
        self.__gHidr = None
        self.mapaAbreviacoes = { "SUDESTE" : "SE", "NORDESTE" : "NE" , "NORTE" : "NO" , "SUL" : "SU", "NOFICT1": "NI" }

        print("Carregou caso SDDP ", self.caminhoSDDP)

    @property
    def caminho(self):
        return self.caminhoSDDP

    @property
    def enafluSIN_Serie(self):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_cen_SIN_enaflu_MW.csv").tabela

    def enafluSubmercado_Serie(self, nomeSubmercado ):
        df = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_cen_sbm_enaflu_MW.csv").tabela
        df_novo = pd.DataFrame()
        df_novo["estagio"] = df["estagio"]
        df_novo["cenario"] = df["cenario"]
        df_novo["valor"] = df[nomeSubmercado]
        return df_novo
    @property
    def zinf(self):
        return Convergencia.read(self.caminhoSDDP+"/sddpconv.csv").tabelaConvergencia["zinf"]/1000
    @property
    def iter(self):
        return Convergencia.read(self.caminhoSDDP+"/sddpconv.csv").tabelaConvergencia["iter"]
    @property
    def cpuTime(self):
        return Convergencia.read(self.caminhoSDDP+"/sddpconv.csv").valorTotalCPUTime

    @property
    def enafluSIN(self, cenario = None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_enaflu_MW.csv").tabela["valor"]


    @property
    def enevertSIN(self):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_enever_MW.csv").tabela["valor"] 
    @property
    def earmSIN(self):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_enearm_MW.csv").tabela["valor"] 
    @property
    def geracaoTermicaSIN(self):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_gerter_MW.csv").tabela["valor"]
    @property
    def geracaoHidreletricaSIN(self):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_gerhid_MW.csv").tabela["valor"]
 
    @property
    def estagio(self):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_gerhid_MW.csv").tabela["estagio"]
    
    def intercambio(self, submercadoDE, submercadoPARA):     
        buscaColuna = self.mapaAbreviacoes[submercadoDE]+"->"+self.mapaAbreviacoes[submercadoPARA]
        print(buscaColuna)
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_intercambio_MW.csv").tabela[buscaColuna]

    def intercambioTotalSubmercado(self, submercado):
        table = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_intercambio_MW.csv").tabela
        estagios = self.estagio.tolist()
        valores = [0]*len(estagios)        
        for subm in self.mapaAbreviacoes:
            abvDE = self.mapaAbreviacoes[submercado]
            abvPARA = self.mapaAbreviacoes[subm]
            buscaColunaPositiva = abvDE+"->"+abvPARA
            buscaColunaNegativa = abvPARA+"->"+abvDE
            if(buscaColunaPositiva in table.columns ):
                lista = table[buscaColunaPositiva].tolist()
                for i in range(0, len(estagios)):
                    valores[i] += lista[i]
                
            if(buscaColunaNegativa in table.columns ):
                lista = table[buscaColunaNegativa].tolist()
                for i in range(0, len(estagios)):
                    valores[i] -= lista[i]

        return valores

    def enafluSubmercado(self, nomeSubmercado):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_enaflu_MW.csv").tabela[nomeSubmercado]
    def enevertSubmercado(self, nomeSubmercado):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_enever_MW.csv").tabela[nomeSubmercado]
    def earmSubmercado(self, nomeSubmercado):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_enearm_MW.csv").tabela[nomeSubmercado]
    def cmoSubmercado(self, nomeSubmercado):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_cmgdem.csv").tabela[nomeSubmercado]
    def geracaoTermicaSubmercado(self, nomeSubmercado):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_gerter_MW.csv").tabela[nomeSubmercado]
    def geracaoHidreletricaSubmercado(self, nomeSubmercado):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_gerhid_MW.csv").tabela[nomeSubmercado]
    


    def vazaoNaturalAfluenteUsina(self, nomeUsina):
        nomeUsina = nomeUsina.replace(" ", "")
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_qafl_m3s.csv").tabela[nomeUsina]
    def volumeMaximoOperativoUsina(self, nomeUsina):
        nomeUsina = nomeUsina.replace(" ", "")
        return LeituraPersonalizadaSDDP.read( self.caminhoSDDP+"/Usina/per_usi_max_volume_operativo_geral_hm3.csv").tabela[nomeUsina]
    def volumeMinimoUsina(self, nomeUsina):
        nomeUsina = nomeUsina.replace(" ", "")
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_min_volume_operativo_geral_hm3.csv").tabela[nomeUsina]
    def vazaoDefluenteMinimaUsina(self, nomeUsina):
        nomeUsina = nomeUsina.replace(" ", "")
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_min_defluencia_geral_m3s.csv").tabela[nomeUsina]
    def vazaoDefluenteUsina(self, nomeUsina):
        nomeUsina = nomeUsina.replace(" ", "")
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_qdef_m3s.csv").tabela[nomeUsina]
    def vazaoTurbinadaUsina(self, nomeUsina):
        nomeUsina = nomeUsina.replace(" ", "")
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_qturb_m3s.csv").tabela[nomeUsina]
    def vazaoVertidaUsina(self, nomeUsina):
        nomeUsina = nomeUsina.replace(" ", "")
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_qvert_m3s.csv").tabela[nomeUsina]
    def volumeFinalUsina(self, nomeUsina):
        nomeUsina = nomeUsina.replace(" ", "")
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_volfin_hm3.csv").tabela[nomeUsina]
    
    def geracaoHidreletricaUsina(self, nomeUsina):
        nomeUsina = nomeUsina.replace(" ", "")
        df = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_gerhid_MW.csv").tabela
        if(nomeUsina in df.columns.tolist()):
            print("Usina existe no dataFrame do SDDP")
            self.__gHidr = df[nomeUsina]
        else:
            print("Usina não existe no dataFrame  do SDDP")
            pd.set_option('display.max_rows', df.shape[0]+1)
            print(df.columns.tolist())
            print(nomeUsina)
            exit(1)
        return self.__gHidr


    def produtibilidade(self, nomeUsina):
        gh = self.geracaoHidreletricaUsina(nomeUsina)
        turb = self.vazaoTurbinadaUsina(nomeUsina)
        print(gh)
        print(turb)
        print(gh/turb)
        return gh/turb













""" 
    def getGeracaoHidreletricaMaximaUsina(self):
        return self.wGHMAX

    def getVazaoTurbinadaMaximaUsina(self):
        return self.qTURBMAX
    
    def getVazaoTurbinadaMinimaUsina(self):
        return self.qTURBMIN """
"""         self.wGHMAX = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Ger_max_disp_usi.csv").tabela[self.nomeUsina]
        self.qTURBMAX = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/turbinamento_maximo_usi.csv").tabela[self.nomeUsina]
        self.qTURBMIN = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/turbinamento_minimo_usi.csv").tabela[self.nomeUsina] """
