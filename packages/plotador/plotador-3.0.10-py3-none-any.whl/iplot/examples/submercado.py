class GeraSubmercado():

    def __init__(self,iplot, submercado, title):
        iplot.figure(submercado)
        iplot.add_frame(submercado, "gH_SBM", 1 , 1, submercado)
        iplot.add_frame(submercado, "gT_SBM", 1 , 2, submercado)
        iplot.add_frame(submercado, "cmo_SBM", 1 , 3, submercado)
        iplot.add_frame(submercado, "eARM_SBM", 2 , 1, submercado)
        iplot.add_frame(submercado, "eVER_SBM", 2 , 2, submercado)
        iplot.add_frame(submercado, "eAFL_SBM", 2 , 3, submercado)
        iplot.show(submercado, title)


