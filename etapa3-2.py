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
inicio = (0, 0)
fim = (7, 7)
arquivo_csv = 'caminho_et2-2.csv'


def caminho_via_arquivo(arquivo, inicio, fim):
    grafo = nx.Graph()
    try:
        with open(arquivo, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            proximo_no = None
            for row in reader:
                no = (int(row[1]), int(row[2]))
                if proximo_no is not None:
                    grafo.add_edge(proximo_no, no)
                proximo_no = no
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não foi encontrado.")
        return None

    if grafo.has_node(inicio) and grafo.has_node(fim):
        try:
            caminho = nx.shortest_path(
                grafo, source=inicio, target=fim)
            return caminho
        except nx.NetworkXNoPath:
            print(
                "Nenhum caminho encontrado.")
            return None


caminho_mais_curto = caminho_via_arquivo(arquivo_csv, inicio, fim)

if caminho_mais_curto:
    def gerador_caminho():
        for no in caminho_mais_curto:
            yield no

# Animação

fig, ax = plt.subplots(figsize=(6, 6))

for i in range(linhas):
    for j in range(colunas):
        y = linhas - 1 - i
        if grid[i][j] == 1:
            ax.add_patch(plt.Rectangle(
                (j, y), 1, 1, facecolor="tab:blue", edgecolor="black", linewidth=0.5))
        else:
            ax.add_patch(plt.Rectangle(
                (j, y), 1, 1, facecolor="white", edgecolor="gray", linewidth=0.5))

ax.text(inicio[1] + 0.5, linhas - 1 - inicio[0] + 0.5,
        "I", ha="center", va="center", fontsize=10, weight="bold")
ax.text(fim[1] + 0.5, linhas - 1 - fim[0] + 0.5, "F",
        ha="center", va="center", fontsize=10, weight="bold", color="green")

line, = ax.plot([], [], 'o-', color='red', linewidth=2)
cursor_dot = ax.scatter([], [], color='black', s=80, zorder=3)
path_gen = gerador_caminho()


def update(frame):
    global line, cursor_dot
    try:
        current_node = next(path_gen)
        x_coords = list(line.get_xdata())
        y_coords = list(line.get_ydata())
        x_coords.append(current_node[1] + 0.5)
        y_coords.append(linhas - 1 - current_node[0] + 0.5)
        line.set_xdata(x_coords)
        line.set_ydata(y_coords)
        cursor_dot.set_offsets(
            [[current_node[1] + 0.5, linhas - 1 - current_node[0] + 0.5]])
    except StopIteration:
        ani.event_source.stop()
    return line, cursor_dot


ax.set_xlim(0, colunas)
ax.set_ylim(0, linhas)
ax.set_aspect("equal")
ax.axis("off")

ani = animation.FuncAnimation(fig, update, frames=len(caminho_mais_curto),
                              interval=100, blit=True, repeat=False)

plt.show()
