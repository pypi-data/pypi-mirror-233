
import pandas as pd

import sys
sys.path.append("/home/david/git/inewave_teste")
from inewave.newave import Pmo
from inewave.newave import Modif
from inewave.newave.modelos.modif import TURBMAXT
from inewave.newave import Hidr
import numpy as np

class dadosNewave():

    def __init__(self, caminhoNewave):
        self.caminhoNewave = caminhoNewave
        print("Carregou caso Newave ", self.caminhoNewave)
        self.__gHidr = None
        self.__volFIM = None
        self.__qDefluenteMinimo = None
        self.__vMinimo = None
        self.__vMaximoOperativo = None

    @property
    def caminho(self):
        return self.caminhoNewave

    @property
    def enafluSIN_Serie(self):       
        return self.leSINRetornaDataFrameCenariosValidos("ENAA_SIN_EST.parquet.gzip")

    @property
    def zinf(self):
        return pd.read_parquet(self.caminhoNewave+"/CONVERGENCIA.parquet.gzip", engine='pyarrow')["zinf"]
    @property
    def iter(self):
        return pd.read_parquet(self.caminhoNewave+"/CONVERGENCIA.parquet.gzip", engine='pyarrow')["iter"]
    @property
    def cpuTime(self):
        df_Convergencia = pd.read_parquet(self.caminhoNewave+"/CONVERGENCIA.parquet.gzip", engine='pyarrow')
        return df_Convergencia["tempo"].sum()


    def leSINRetornaDataFrameCenariosValidos(self, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df = df_NW.loc[(df_NW["cenario"].apply(lambda x: x.isnumeric()))]
        return df
    
    def enafluSubmercado_Serie(self, nomeSubmercado):       
        return self.leSubmercadoRetornaDataFrameCenariosValidos(nomeSubmercado, "ENAA_SBM_EST.parquet.gzip")
    
    def leSubmercadoRetornaDataFrameCenariosValidos(self, nomeSubmercado, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df = df_NW.loc[(df_NW["submercado"] == nomeSubmercado) & (df_NW["cenario"].apply(lambda x: x.isnumeric()))]
        return df
    



    @property
    def enafluSIN(self):         
        return self.leSINRetornaDataFrameCenarioMedio("ENAA_SIN_EST.parquet.gzip")
    @property
    def enevertSIN(self):        
        return self.leSINRetornaDataFrameCenarioMedio("EVER_SIN_EST.parquet.gzip")
    @property
    def earmSIN(self):        
        return self.leSINRetornaDataFrameCenarioMedio("EARMF_SIN_EST.parquet.gzip")
    @property
    def geracaoTermicaSIN(self):
        return self.leSINRetornaDataFrameCenarioMedio("GTER_SIN_EST.parquet.gzip")
    @property
    def geracaoHidreletricaSIN(self):
        return self.leSINRetornaDataFrameCenarioMedio("GHID_SIN_EST.parquet.gzip")

    @property
    def estagio(self):
        return pd.read_parquet(self.caminhoNewave+'/'+"EST.parquet.gzip", engine='pyarrow')["idEstagio"]

    def leUsinaRetornaDataFrameCenarioMedio(self, nomeUsina, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df = df_NW.loc[(df_NW["usina"] == nomeUsina) & (df_NW["cenario"] == "mean")]["valor"]
        return df
    def leSubmercadoRetornaDataFrameCenarioMedio(self, nomeSubmercado, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df = df_NW.loc[(df_NW["submercado"] == nomeSubmercado) & (df_NW["cenario"] == "mean")]["valor"]
        return df
    


    def leSINRetornaDataFrameCenarioMedio(self, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df = df_NW.loc[(df_NW["cenario"] == "mean")]["valor"]
        return df

    def intercambio(self, submercadoDE, submercadoPARA):
        df = pd.read_parquet(self.caminhoNewave+'/INT_SBP_EST.parquet.gzip', engine='pyarrow')
        df = df.loc[(df["cenario"] == "mean") ]
        dfINTERC = df.loc[(df["submercadoDe"]==submercadoDE) & (df["submercadoPara"]==submercadoPARA)]["valor"]
        return dfINTERC
    
    def intercambioTotalSubmercado(self, submercado):
        df = pd.read_parquet(self.caminhoNewave+'/INT_SBP_EST.parquet.gzip', engine='pyarrow')
        df = df.loc[(df["cenario"] == "mean") ]
        intercDE = df.loc[(df["submercadoDe"] == submercado)]
        intercPARA = df.loc[(df["submercadoPara"] == submercado)]
        totalIntercambio = []
        for periodo in self.estagio.tolist():
            #print(periodo)
            totalIntercambio.append(intercDE.loc[(intercDE["estagio"] == periodo)]["valor"].sum() - intercPARA.loc[(intercPARA["estagio"] == periodo)]["valor"].sum())
        return totalIntercambio

    def enafluSubmercado(self, nomeSubmercado):
        return self.leSubmercadoRetornaDataFrameCenarioMedio(nomeSubmercado, "ENAA_SBM_EST.parquet.gzip")
    def enevertSubmercado(self, nomeSubmercado):
        return self.leSubmercadoRetornaDataFrameCenarioMedio(nomeSubmercado, "EVER_SBM_EST.parquet.gzip")
    def earmSubmercado(self, nomeSubmercado):
        return self.leSubmercadoRetornaDataFrameCenarioMedio(nomeSubmercado, "EARMF_SBM_EST.parquet.gzip")
    def cmoSubmercado(self, nomeSubmercado):
        return self.leSubmercadoRetornaDataFrameCenarioMedio(nomeSubmercado, "CMO_SBM_EST.parquet.gzip")
    def geracaoTermicaSubmercado(self, nomeSubmercado):
        return self.leSubmercadoRetornaDataFrameCenarioMedio(nomeSubmercado, "GTER_SBM_EST.parquet.gzip")
    def geracaoHidreletricaSubmercado(self, nomeSubmercado):
        return self.leSubmercadoRetornaDataFrameCenarioMedio(nomeSubmercado, "GHID_SBM_EST.parquet.gzip")

    def vazaoDefluenteUsina(self, nomeUsina):
        return self.leUsinaRetornaDataFrameCenarioMedio(nomeUsina, "QDEF_UHE_EST.parquet.gzip")
    def vazaoTurbinadaUsina(self, nomeUsina):
        return self.leUsinaRetornaDataFrameCenarioMedio(nomeUsina, "QTUR_UHE_EST.parquet.gzip")
    def vazaoVertidaUsina(self, nomeUsina):
        return self.leUsinaRetornaDataFrameCenarioMedio(nomeUsina, "QVER_UHE_EST.parquet.gzip")
    def vazaoNaturalAfluenteUsina(self, nomeUsina):
        return self.leUsinaRetornaDataFrameCenarioMedio(nomeUsina, "QINC_UHE_EST.parquet.gzip")
    def volumeMaximoOperativoUsina(self, nomeUsina):
        df = Hidr.read(self.caminhoNewave+"/hidr.dat").cadastro
        volume_maximo = df.loc[(df["nome_usina"] == nomeUsina)]["volume_maximo"].tolist()[0]
        self.__vMaximoOperativo =  [volume_maximo]*59
        return self.__vMaximoOperativo
    def volumeMinimoUsina(self, nomeUsina):
        df = Hidr.read(self.caminhoNewave+"/hidr.dat").cadastro
        volume_minimo = df.loc[(df["nome_usina"] == nomeUsina)]["volume_minimo"].tolist()[0]
        self.__vMinimo =  [volume_minimo]*59        
        return self.__vMinimo
    def volumeFinalUsina(self, nomeUsina):
        df = pd.read_parquet(self.caminhoNewave+'/VARMF_UHE_EST.parquet.gzip', engine='pyarrow')
        dataAux = df.loc[(df["usina"] == nomeUsina) & (df["cenario"] == "mean")]["valor"].tolist()
        Vol = []
        volume_minimo_local = self.volumeMinimoUsina(nomeUsina)
        for i in range(len(dataAux)):
            Vol.append(dataAux[i] + volume_minimo_local[i])
        self.__volFIM = Vol
        return self.__volFIM
    def vazaoDefluenteMinimaUsina(self, nomeUsina):
        df = Pmo.read(self.caminhoNewave+"/pmo.dat").vazao_defluente_minima
        #pd.set_option('display.max_rows', df.shape[0]+1)
        defluencia_minima = df.loc[(df["usina"] == nomeUsina)]["valor"].tolist()[0]
        self.__qDefluenteMinimo = [defluencia_minima]*59
        return self.__qDefluenteMinimo
    def geracaoHidreletricaUsina(self, nomeUsina):
        #if self.__gHidr is None:
        df = pd.read_parquet(self.caminhoNewave+'/GHID_UHE_EST.parquet.gzip', engine='pyarrow')
        if(nomeUsina in df["usina"].tolist()):
            print("Usina existe no dataFrame do caso", self.caminhoNewave)
            self.__gHidr = df.loc[(df["usina"] == nomeUsina) & (df["cenario"] == "mean")]["valor"]
        else:
            print("Usina não existe no dataFrame do caso", self.caminhoNewave)
            df = pd.read_parquet(self.caminhoNewave+'/UHE.parquet.gzip', engine='pyarrow')
            pd.set_option('display.max_rows', df.shape[0]+1)
            print(df)
            exit(1)
        return self.__gHidr


    



"""         listaRegistros = Modif.read(self.caminhoNewave+"/modif.dat").modificacoes_usina(34)
        for elemento in listaRegistros:
            if(isinstance(elemento,TURBMAXT)):
                elemento.turbinamento """

    #def getVolumeInicialUsina(self):
    #    return self.vIni.tolist()[0]


    #def getGeracaoHidreletricaMaximaUsina(self):
    #    return self.wGHMAX

    #def getVazaoTurbinadaMaximaUsina(self):
    #    return self.qTURBMAX
    
    #def getVazaoTurbinadaMinimaUsina(self):
    #    return self.qTURBMIN

    #def getVazaoDefluenteMaximaUsina(self):
    #    return self.qDEFMAX