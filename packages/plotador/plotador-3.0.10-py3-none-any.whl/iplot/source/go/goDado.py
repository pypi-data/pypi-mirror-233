
import plotly.graph_objects as go
class goDado():
    def __init__(self, y, x, yaxis, xaxis, cor, legenda):
       self.y = y
       self.x = x
       self.yaxis = yaxis
       self.xaxis = xaxis
       self.cor  = cor
       self.legenda = legenda

    def returnGoObject(self, show = False):
        return go.Scatter(x = self.x, y = self.y , name = self.legenda, legendgroup= self.legenda,line=dict(color=self.cor), showlegend=show)
