
import plotly.graph_objects as go
class goMaximo():
    def __init__(self, y, x, yaxis, xaxis, cor, legenda):
       self.y = y
       self.x = x
       self.yaxis = yaxis
       self.xaxis = xaxis
       self.cor  = cor
       self.legenda = legenda

    def returnGoObject(self, show = False): #MAXIMO
        return go.Scatter(x = self.x, y = self.y, name = self.legenda, legendgroup=self.legenda, mode = "markers", marker=dict(color=self.cor, size = 3), showlegend=False)
