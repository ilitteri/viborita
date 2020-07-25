from pygraphviz import AGraph

def crear(datos):

    g = AGraph(directed=True)
    
    for funcion in datos:
        g.add_node(funcion)
        
        for i in datos[funcion]["invocaciones"]:
            g.add_edge((funcion, i))
            
    g.draw('grafo.svg', prog='dot')
    g.draw('grafo.png', prog='dot')