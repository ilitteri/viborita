from pygraphviz import AGraph

def crear_grafo_invocaciones(datos):
    '''[Autor: Ivan Litteri]
    [Ayuda: crea grafo.svg y grafo.png]'''

    g = AGraph(directed=True, rankdir='LR')
    
    for funcion in datos:
        g.add_node(funcion)
        
        for i in datos[funcion]["invocaciones"]:
            g.add_edge((funcion, i))
        
    g.layout(prog='dot')
    g.draw('grafo.svg')
    g.draw('grafo.png')