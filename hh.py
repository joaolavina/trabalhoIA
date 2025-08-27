import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Configuração do Grid ---
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

# --- 1) Constrói o grafo sem diagonais (4 vizinhos) ---
G = nx.Graph()
dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

for i in range(linhas):
    for j in range(colunas):
        if grid[i][j] == 0:
            G.add_node((i, j))
            for di, dj in dirs4:
                ni, nj = i + di, j + dj
                if 0 <= ni < linhas and 0 <= nj < colunas and grid[ni][nj] == 0:
                    G.add_edge((i, j), (ni, nj))

start = (0, 0)
assert grid[start[0]][start[1]] == 0, "Start é um obstáculo!"


# --- 2) DFS walk (gerador passo a passo) com backtracking ---
def dfs_walk_generator(G, start):
    """
    Um gerador que produz cada nó da caminhada,
    permitindo a animação passo a passo.
    """
    visited = {start}
    yield start  # Produz o primeiro nó
    stack = [(start, iter(sorted(G.neighbors(start))))]

    while stack:
        v, it = stack[-1]
        try:
            w = next(it)
        except StopIteration:
            stack.pop()
            if stack:
                # Passo de volta (backtracking) para o pai no topo da pilha
                yield stack[-1][0]
            continue

        if w not in visited:
            visited.add(w)
            yield w  # Passo adiante
            stack.append((w, iter(sorted(G.neighbors(w)))))


# --- 3) Configuração da Animação ---
fig, ax = plt.subplots(figsize=(6, 6))

# Desenha as células estáticas
for i in range(linhas):
    for j in range(colunas):
        y = linhas - 1 - i
        if grid[i][j] == 1:
            ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor="tab:blue", edgecolor="black", linewidth=0.5))
        else:
            ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor="white", edgecolor="gray", linewidth=0.5))

# Desenha marcadores de início e fim
ax.text(start[1] + 0.5, linhas - 1 - start[0] + 0.5, "S", ha="center", va="center", fontsize=10, weight="bold")

# Cria a linha que será animada
line, = ax.plot([], [], 'o-', color='red', linewidth=2)  # 'o-' para mostrar os pontos e a linha

# Cria o gerador do percurso
path_gen = dfs_walk_generator(G, start)


def update(frame):
    """
    Função de atualização para a animação.
    Recebe um novo nó e adiciona à linha do percurso.
    """
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
        # Quando o gerador acaba, a animação para
        ani.event_source.stop()

    return line,


ax.set_xlim(0, colunas)
ax.set_ylim(0, linhas)
ax.set_aspect("equal")
ax.axis("off")
plt.title("Animação da Busca em Profundidade (DFS)")

# Executa a animação
ani = animation.FuncAnimation(fig, update, frames=G.number_of_nodes() * 2,
                                  interval=100, blit=True, repeat=False)

plt.show()