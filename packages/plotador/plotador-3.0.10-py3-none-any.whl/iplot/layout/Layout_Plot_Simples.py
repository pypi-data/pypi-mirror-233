import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
class LayoutPlotSimples():
    def __init__(self, chave, identificador, objeto, tituloGrafico):
        for caso in objeto.mapaCasos:
            fig0 = go.Figure()
            infoplt = objeto.interpreta(objeto.caso(caso), chave, identificador)
            fig0.add_trace(go.Scatter(x = infoplt.x, y = infoplt.y, name = infoplt.legenda, legendgroup=infoplt.legenda,line=dict(color=infoplt.cor)))
            fig0.update_xaxes(title_text=infoplt.xaxis)
            fig0.update_yaxes(title_text=infoplt.yaxis)
            titulo = chave+"_"+infoplt.legenda+"_"+objeto.nomeAnalise if tituloGrafico is None else tituloGrafico
            fig0.update_layout(title=titulo)
            fig0.write_html(titulo+".html")
            print("caso: ", caso, "cor: ", infoplt.cor)
        print("PLOTAGEM CONVERGENCIA CONCLUIDA COM SUCESSO")