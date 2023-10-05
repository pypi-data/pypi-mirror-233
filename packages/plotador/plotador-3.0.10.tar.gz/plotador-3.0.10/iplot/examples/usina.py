class GeraUsina():

    def __init__(self, iplot, usina, title):
        iplot.figure(usina)
        iplot.add_frame(usina, "gH_USI", 1 , 1, usina)
        iplot.add_frame(usina, "qTUR_USI", 1 , 2, usina)
        iplot.add_frame(usina, "qVER_USI", 1 , 3, usina)
        iplot.add_frame(usina, "vFIM_USI", 2 , 1, usina)
        iplot.add_frame(usina, "qDEF_USI", 2 , 2, usina)
        iplot.add_frame(usina, "qAFL_USI", 2 , 3, usina)
        iplot.show(usina, title)


