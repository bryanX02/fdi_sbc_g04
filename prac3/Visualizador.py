import networkx as nx
import matplotlib.pyplot as plt

def exportar_grafo(resultados, filename):
    if not resultados:
        print("No hay resultados de consulta para visualizar.")
        return

    # Creamos un grafo dirigido
    grafo = nx.DiGraph()

    # Convertimos los resultados en nodos y relaciones con etiquetas dinámicas
    for resultado in resultados:
        sujeto = resultado.get("sujeto")
        predicado = resultado.get("predicado")
        objeto = resultado.get("objeto")
        if sujeto and objeto:
            grafo.add_edge(sujeto, objeto, label=predicado)

    # Dibujar el grafo
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(grafo)
    nx.draw(
        grafo, pos,
        with_labels=True,
        node_size=2000,
        node_color="lightblue",
        font_size=10,
        font_weight="bold",
        arrows=True
    )
     # Dibujar etiquetas en las aristas
    edge_labels = {(u, v): d.get("label", "") for u, v, d in grafo.edges(data=True)}
    nx.draw_networkx_edge_labels(
        grafo, pos,
        edge_labels=edge_labels
    )

    # Guardar como imagen
    plt.savefig(filename)
    plt.close()
    print(f"SBC_P3> Exportando grafo a '{filename}'... OK!")


