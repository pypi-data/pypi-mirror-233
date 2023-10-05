
from iplot.source.interpretador import interpretador
class GeraBoxplot():

    def __init__(self, iplot, key, id, title ):
        nome = key if id is None else key+"_"+id
        iplot.figure(nome)
        iplot.add_frame(nome, key, 1 , 1, id)

        aglutinacoes = [12, 36, 59]
        for frame in iplot.mapaNomeFiguras[nome].listaFrames:
            novaListaElementoGO = []
            for elementoGO in interpretador().retornaListasGO(frame, iplot.gerenciador):
                ylistaPlot = []
                xlistaPlot = []
                for aglut in aglutinacoes:
                    lista = self.mediaPeriodoSerie(elementoGO.y, aglut)
                    ylistaPlot += lista
                    xlistaPlot += [aglut]*len(lista)
                elementoGO.y = ylistaPlot
                elementoGO.x = xlistaPlot
                novaListaElementoGO.append(elementoGO)
            frame.setListaGO(novaListaElementoGO)
        iplot.show(nome, title)


    def mediaPeriodoSerie(self, df, aglut):
        lista = []
        numeroCenarios = max([eval(i) for i in df["cenario"].tolist()]) if isinstance(df["cenario"].tolist()[0], str) else max(df["cenario"].tolist())
        for serie in range(1,(numeroCenarios+1)):
            serie = str(serie) if isinstance(df["cenario"].tolist()[0], str) else serie
            lista.append(df.loc[(df["cenario"]==serie) & (df["estagio"] <= aglut)]["valor"].mean())
        return lista