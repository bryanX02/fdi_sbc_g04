import pydot

def exportar_grafo(gestor_base, filename):
    # Creamos un grafo con Pydot
    grafo = pydot.Dot(graph_type="graph")

    # Añadimos nodos y relaciones al grafo a partir del contenido de las bases
    contenido = gestor_base.obtener_contenido()
    for linea in contenido:
        if " " in linea:
            sujeto, predicado, objeto = linea.split()[:3]
            nodo_sujeto = pydot.Node(sujeto)
            nodo_objeto = pydot.Node(objeto)
            grafo.add_node(nodo_sujeto)
            grafo.add_node(nodo_objeto)
            grafo.add_edge(pydot.Edge(nodo_sujeto, nodo_objeto, label=predicado))

    # Exportamos el grafo a un archivo de imagen
    grafo.write_png(filename)
    print(f"SBC_P3> Exportando grafo a '{filename}'... OK!")
