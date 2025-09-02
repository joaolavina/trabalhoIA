import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

linhas, colunas = len(grid), len(grid[0])

G = nx.Graph()
direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

for i in range(linhas):
    for j in range(colunas):
        G.add_node((i, j))
        for di, dj in direcoes:
            ni, nj = i + di, j + dj
            if 0 <= ni < linhas and 0 <= nj < colunas:
                G.add_edge((i, j), (ni, nj))

posicao_valida = [(i, j) for i in range(linhas) for j in range(colunas)]
inicio = random.choice(posicao_valida)

def percorrer(G, inicio):

    for direcao in random.sample(direcoes, len(direcoes)):
        yield inicio
        ni, nj = inicio[0] + direcao[0], inicio[1] + direcao[1]

        while 0 <= ni < linhas and 0 <= nj < colunas:
            yield (ni, nj)
            inicio = (ni, nj)
            ni, nj = inicio[0] + direcao[0], inicio[1] + direcao[1]

caminho = percorrer(G, inicio)

# Animação

fig, ax = plt.subplots(figsize=(6, 6))

for i in range(linhas):
    for j in range(colunas):
        y = linhas - 1 - i
        ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor="white", edgecolor="gray", linewidth=0.5))

ax.text(inicio[1] + 0.5, linhas - 1 - inicio[0] + 0.5, "I", ha="center", va="center", fontsize=10, weight="bold")
line, = ax.plot([], [], 'o-', color='red', linewidth=2)
cursor_dot = ax.scatter([], [], s=100, color='black', zorder=3)

def update(frame):
    global line, cursor_dot
    try:
        current_node = next(caminho)
        x_coords = list(line.get_xdata())
        y_coords = list(line.get_ydata())

        x_coords.append(current_node[1] + 0.5)
        y_coords.append(linhas - 1 - current_node[0] + 0.5)

        line.set_xdata(x_coords)
        line.set_ydata(y_coords)

        cursor_dot.set_offsets([[current_node[1] + 0.5, linhas - 1 - current_node[0] + 0.5]])

    except StopIteration:
        ani.event_source.stop()

    return line, cursor_dot

ax.set_xlim(0, colunas)
ax.set_ylim(0, linhas)
ax.set_aspect("equal") 
ax.axis("off") 

ani = animation.FuncAnimation(fig, update, frames=G.number_of_nodes() * 2,
                                  interval=100, blit=True, repeat=False)
plt.show()