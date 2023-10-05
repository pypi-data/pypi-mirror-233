import numpy as np
import plotly.graph_objects as go
class GeraPlotRapido():
    def __init__(self, yaxis, xaxis, legenda, tituloGrafico):
        fig0 = go.Figure()
        legend = " " if legenda is None else legenda
        xaxis_enter = np.linspace(1,len(yaxis.tolist()), len(yaxis.tolist()) ) if xaxis is None else xaxis
        print("YAXIS: ", yaxis)
        fig0.add_trace(go.Scatter(x = xaxis_enter, y = yaxis, name = legend, legendgroup=legend)) #,line=dict(color=cor)
        titulo = " " if tituloGrafico is None else tituloGrafico
        fig0.update_layout(title=titulo)
        fig0.write_html(titulo+".html")
        print("PLOTAGEM CONVERGENCIA CONCLUIDA COM SUCESSO")