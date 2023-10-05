
import plotly.graph_objects as go
class goMinimo():
    def __init__(self, y, x, yaxis, xaxis, cor, legenda):
       self.y = y
       self.x = x
       self.yaxis = yaxis
       self.xaxis = xaxis
       self.cor  = cor
       self.legenda = legenda

    def returnGoObject(self, show = False): #MINIMO
        return go.Scatter(x = self.x, y = self.y, name = self.legenda, legendgroup=self.legenda,line=dict(color=self.cor, width = 1, dash = 'dash'), showlegend=False)
