class GeraCascata():

    def __init__(self, iplot, nomeCascata, key, title = None):
        mapaCascata = {   "SE" : [ "NOVA PONTE", "EMBORCACAO", "SAO SIMAO", "FURNAS", "MARIMBONDO", "A. VERMELHA", "I. SOLTEIRA", "JUPIA", "P. PRIMAVERA"],
            "S" :  ["A.A. LAYDNER", "G.B. MUNHOZ", "MACHADINHO"],
            "NE" : ["TRES MARIAS", "SOBRADINHO", "ITAPARICA", "SERRA MESA", "TUCURUI"]        }
        
        mapaCascataColunaMaxima = {"SE":3, "S":2, "NE":3}

        iplot.figure(nomeCascata)
        cascata = mapaCascata[nomeCascata]
        linha = 1
        coluna = 1
    
        for usina in cascata:
            iplot.add_frame(nomeCascata, key, linha, coluna, usina)
            coluna += 1
            if(coluna > mapaCascataColunaMaxima[nomeCascata]):
                coluna = 1
                linha += 1
        
        iplot.show(nomeCascata, title)


