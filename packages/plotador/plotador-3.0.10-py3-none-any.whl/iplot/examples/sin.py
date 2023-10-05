class GeraSIN():

    def __init__(self, iplot, title):
        iplot.figure("SIN")
        iplot.add_frame("SIN", "gH_SIN", 1 , 1, None)
        iplot.add_frame("SIN", "gT_SIN", 1 , 2, None)
        iplot.add_frame("SIN", "eARM_SIN", 1 , 3, None)
        iplot.add_frame("SIN", "eVERT_SIN", 2 , 1, None)
        iplot.add_frame("SIN", "eNAFLU_SIN", 2 , 2, None)
        iplot.show("SIN",title)


