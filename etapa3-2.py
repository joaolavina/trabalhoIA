import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
from collections import deque

grid = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
]

linhas, colunas = len(grid), len(grid[0])
start_node = (0, 0)
end_node = (7, 7)
csv_file_path = 'caminho_et2-2.csv'

def get_shortest_path(file_path, start, end):
    explored_graph = nx.Graph()
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            previous_node = None
            for row in reader:
                node = (int(row[1]), int(row[2]))
                if previous_node is not None:
                    explored_graph.add_edge(previous_node, node)
                previous_node = node
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return None

    if explored_graph.has_node(start) and explored_graph.has_node(end):
        try:
            shortest_path = nx.shortest_path(explored_graph, source=start, target=end)
            return shortest_path
        except nx.NetworkXNoPath:
            print("Não foi possível encontrar um caminho entre os nós no grafo explorado.")
            return None
    else:
        print("Os nós de início ou fim não foram encontrados no grafo explorado.")
        return None

shortest_path = get_shortest_path(csv_file_path, start_node, end_node)

if not shortest_path:
    print("Erro: Não foi possível encontrar o caminho. Verifica se o CSV tem os pontos de início e fim, tchê!")
else:
    def path_generator():
        for node in shortest_path:
            yield node

    fig, ax = plt.subplots(figsize=(6, 6))

    for i in range(linhas):
        for j in range(colunas):
            y = linhas - 1 - i
            if grid[i][j] == 1:
                ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor="tab:blue", edgecolor="black", linewidth=0.5))
            else:
                ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor="white", edgecolor="gray", linewidth=0.5))

    ax.text(start_node[1] + 0.5, linhas - 1 - start_node[0] + 0.5, "I", ha="center", va="center", fontsize=10, weight="bold")
    ax.text(end_node[1] + 0.5, linhas - 1 - end_node[0] + 0.5, "F", ha="center", va="center", fontsize=10, weight="bold", color="green")

    line, = ax.plot([], [], 'o-', color='red', linewidth=2)
    path_gen = path_generator()

    def update(frame):
        global line
        try:
            current_node = next(path_gen)
            x_coords = list(line.get_xdata())
            y_coords = list(line.get_ydata())
            x_coords.append(current_node[1] + 0.5)
            y_coords.append(linhas - 1 - current_node[0] + 0.5)
            line.set_xdata(x_coords)
            line.set_ydata(y_coords)
        except StopIteration:
            ani.event_source.stop()
        return line,

    ax.set_xlim(0, colunas)
    ax.set_ylim(0, linhas)
    ax.set_aspect("equal")
    ax.axis("off")

    ani = animation.FuncAnimation(fig, update, frames=len(shortest_path),
                                  interval=100, blit=True, repeat=False)

    plt.show()