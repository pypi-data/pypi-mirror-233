from iplot.layout.Layout_Plot_Simples import LayoutPlotSimples
class GeraPlotSimples():

    def __init__(self, iplot, key , sameGraph, id, title):
        id = " " if id is None else id
        title = " " if title is None else title
        if(sameGraph is None):
            name = key+"_"+id+"_"+title
            iplot.figure(name)
            iplot.add_frame(name, key, 1 , 1, id)
            iplot.show(name)
        elif(sameGraph == False):
            Gera = LayoutPlotSimples(key, id, iplot.interpretador, title)


