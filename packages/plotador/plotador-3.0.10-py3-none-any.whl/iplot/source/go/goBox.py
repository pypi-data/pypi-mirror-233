
import plotly.graph_objects as go
class goBox():
    def __init__(self, y, x, yaxis, xaxis, cor, legenda):
       self.y = y
       self.x = x
       self.yaxis = yaxis
       self.xaxis = xaxis
       self.cor  = cor
       self.legenda = legenda

    def returnGoObject(self, show = False):
        return go.Box(x = self.x, y = self.y, text=self.y,     boxpoints= False, name = self.legenda, legendgroup = self.legenda, fillcolor = self.cor, marker_color = self.cor, showlegend=show) #, mode='lines+markers+text'
    