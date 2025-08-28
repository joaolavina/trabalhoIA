import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Configuração inicial do grid e do grafo
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
G = nx.Graph()
dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Constrói o grafo a partir do grid
for i in range(linhas):
    for j in range(colunas):
        if grid[i][j] == 0:
            no = (i, j)
            G.add_node(no)
            if j < colunas - 1 and grid[i][j+1] == 0:
                G.add_edge(no, (i, j+1))
            if i < linhas - 1 and grid[i+1][j] == 0:
                G.add_edge(no, (i+1, j))

start = (0, 0)
end = (7, 7)

# Prepara a animação
fig, ax = plt.subplots(figsize=(6, 6))

for i in range(linhas):
    for j in range(colunas):
        y = linhas - 1 - i
        if grid[i][j] == 1:
            ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor="tab:blue", edgecolor="black", linewidth=0.5))
        else:
            ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor="white", edgecolor="gray", linewidth=0.5))

ax.text(start[1] + 0.5, linhas - 1 - start[0] + 0.5, "S", ha="center", va="center", fontsize=10, weight="bold")
ax.text(end[1] + 0.5, linhas - 1 - end[0] + 0.5, "E", ha="center", va="center", fontsize=10, weight="bold", color="red")

line, = ax.plot([], [], 'o-', color='red', linewidth=2, zorder=3)

# Algoritmo de Busca em Largura (BFS) para gerar o caminho passo a passo
def bfs_path_generator(graph, start_node, end_node):
    queue = deque([start_node])
    visited = {start_node}
    parent = {start_node: None}

    path_steps = []

    while queue:
        current_node = queue.popleft()
        path_steps.append(current_node)

        if current_node == end_node:
            # Reconstroi o caminho final
            final_path = []
            while current_node is not None:
                final_path.append(current_node)
                current_node = parent[current_node]
            final_path.reverse()
            yield path_steps, final_path
            return

        for neighbor in sorted(graph.neighbors(current_node)):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current_node
                queue.append(neighbor)
                
        yield path_steps, None # Retorna o caminho parcial e None para o final_path

# Cria o gerador para a animação
bfs_gen = bfs_path_generator(G, start, end)
found_path = None
shortest_path_line, = ax.plot([], [], '-', color='green', linewidth=4, zorder=2)

# Função de atualização da animação
def update(frame):
    global found_path, line, shortest_path_line
    if found_path is not None:
        return line, shortest_path_line

    try:
        current_path_steps, final_path = next(bfs_gen)
        
        # Atualiza a linha de busca
        x_coords_search = [node[1] + 0.5 for node in current_path_steps]
        y_coords_search = [linhas - 1 - node[0] + 0.5 for node in current_path_steps]
        line.set_xdata(x_coords_search)
        line.set_ydata(y_coords_search)

        if final_path:
            found_path = final_path
            print("Caminho mais curto encontrado:")
            print(found_path)
            print(f"Comprimento do caminho: {len(found_path) - 1}")
            
            # Atualiza a linha do caminho final
            x_coords_final = [node[1] + 0.5 for node in found_path]
            y_coords_final = [linhas - 1 - node[0] + 0.5 for node in found_path]
            shortest_path_line.set_xdata(x_coords_final)
            shortest_path_line.set_ydata(y_coords_final)

            ax.set_title("Caminho mais Curto Encontrado! 🏆")
            ani.event_source.stop()

    except StopIteration:
        ax.set_title("Nenhum Caminho Encontrado!")
        ani.event_source.stop()
        
    return line, shortest_path_line

# Configurações finais e exibição da animação
ax.set_xlim(0, colunas)
ax.set_ylim(0, linhas)
ax.set_aspect("equal")
ax.axis("off")
plt.title("Animação da Busca em Largura (BFS)")

ani = animation.FuncAnimation(fig, update, frames=G.number_of_nodes(),
                              interval=100, blit=True, repeat=False)
plt.show()