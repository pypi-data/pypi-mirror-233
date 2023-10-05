from plotly.subplots import make_subplots
class LayoutPlotPersonalizado():
    def __init__(self, figura, tituloGrafico):
        fig0 = make_subplots(rows=figura.max_linha,cols=figura.max_coluna,subplot_titles=(" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " "))
        for frame in figura.listaFrames:
            for go in frame.getListaGO():
                show = True if (frame.linha == 1 and frame.coluna == 1) else False
                fig0.add_trace(go.returnGoObject(show), row=frame.linha,col=frame.coluna)
                fig0.update_xaxes(title_text=go.xaxis)
                fig0.update_yaxes(title_text=go.yaxis)
            fig0.layout.annotations[figura.getPosicaoTitulo(frame.linha,frame.coluna)].update(text=frame.getTitulo())
        fig0.update_layout(title=tituloGrafico, boxmode='group')
        fig0.write_html(tituloGrafico+".html")
        print("PLOTAGEM PERSONALZIADA CONCLUIDA COM SUCESSO")