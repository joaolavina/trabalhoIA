import matplotlib.pyplot as plt
import matplotlib.animation as animation

grid = [
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 3, 1, 1, 1, 1],
    [1, 1, 2, 2, 1, 3, 3, 2, 1, 1],
    [1, 1, 2, 1, 3, 3, 3, 2, 1, 1],
    [1, 1, 2, 2, 3, 3, 3, 2, 2, 1],
    [1, 1, 1, 2, 3, 1, 2, 2, 1, 1],
    [1, 1, 1, 1, 2, 3, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1]
]

linhas, colunas = len(grid), len(grid[0])
inicio = (0, 5)
fim = (10, 5)
direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def dentro_grid(i, j):
    return 0 <= i < linhas and 0 <= j < colunas

def busca_gulosa_local(inicio, fim):
    caminho = [inicio]
    atual = inicio
    visited = set()
    visited.add(atual)
    while atual != fim:
        ci, cj = atual
        vizinhos = []
        for di, dj in direcoes:
            ni, nj = ci + di, cj + dj
            if dentro_grid(ni, nj) and (ni, nj) not in visited:
                cost = grid[ni][nj]
                dist = abs(ni - fim[0]) + abs(nj - fim[1])
                vizinhos.append((cost, dist, (ni, nj)))
        if not vizinhos:
            break
        vizinhos.sort()
        next_cell = vizinhos[0][2]
        caminho.append(next_cell)
        visited.add(next_cell)
        atual = next_cell

    return caminho


caminho = busca_gulosa_local(inicio, fim)

def calcular_custo(caminho, grid_map):
    if not caminho:
        return 0
    return sum(grid_map[i][j] for (i, j) in caminho)

custo_total = calcular_custo(caminho, grid)

# Animação

fig, ax = plt.subplots(figsize=(6, 6))

for i in range(linhas):
    for j in range(colunas):
        y = linhas - 1 - i
        cost = grid[i][j]
        if cost == 0:
            color = 'white'
            label = "0"
        else:
            color = 'lightgreen' if cost == 1 else 'sandybrown' if cost == 2 else 'dimgray'
            label = str(cost)
        ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor=color, edgecolor="black", linewidth=0.5))
        ax.text(j + 0.5, y + 0.5, label, ha="center", va="center", fontsize=10,
                color='white' if cost == 3 else 'black', weight="bold")

ax.text(inicio[1] + 0.5, linhas - 1 - inicio[0] + 0.5, "i", ha="center", va="center", fontsize=12, weight="bold", color="red")
ax.text(fim[1] + 0.5, linhas - 1 - fim[0] + 0.5, "f", ha="center", va="center", fontsize=12, weight="bold", color="red")

line, = ax.plot([], [], 'o-', color='red', linewidth=2)
cursor_dot = ax.scatter([], [], color='black', s=80, zorder=3)

def update_anim(k):
    sub = caminho[:k+1]
    xs = [c + 0.5 for (_, c) in sub]
    ys = [linhas - 1 - r + 0.5 for (r, _) in sub]
    line.set_data(xs, ys)
    if sub:
        cursor_dot.set_offsets([[xs[-1], ys[-1]]])
    return line, cursor_dot

ax.set_xlim(0, colunas)
ax.set_ylim(0, linhas)
ax.set_aspect('equal')
ax.axis('off')
ax.text(colunas / 2, -0.5, f'Custo total: {custo_total}', ha="center", va="center", fontsize=14, color="blue", weight="bold")

ani = None
if caminho:
    ani = animation.FuncAnimation(fig, update_anim, frames=len(caminho), interval=200, blit=True, repeat=False)

plt.show()
