class GeraIntercambios():

    def __init__(self, iplot, title):
        #listaIntercambios = [("SUDESTE","SUL"), ("SUDESTE","NORDESTE"), ("SUDESTE","NORTE"), ("SUDESTE","NOFICT1"), ("NORDESTE","NOFICT1"), ("NORTE","NOFICT1")]
        iplot.figure("intercambios")
        iplot.add_frame("intercambios", "interc", 1 , 1,"SUDESTE-SUL")
        iplot.add_frame("intercambios", "interc", 1 , 2,"SUDESTE-NORDESTE")
        iplot.add_frame("intercambios", "interc", 1 , 3,"SUDESTE-NORTE")
        iplot.add_frame("intercambios", "interc", 2 , 1,"SUDESTE-NOFICT1")
        iplot.add_frame("intercambios", "interc", 2 , 2,"NORDESTE-NOFICT1")
        iplot.add_frame("intercambios", "interc", 2 , 3,"NORTE-NOFICT1")
        iplot.show("intercambios", title)


