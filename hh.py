import networkx as nx
import matplotlib.pyplot as plt

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
dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]

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

# --- 2) DFS *walk* (passo a passo) com backtracking ---
def dfs_walk(G, start):
    """Retorna uma sequência de nós onde cada passo é adjacente (inclui backtracking)."""
    visited = {start}
    walk = [start]
    # usar ordem determinística de vizinhos (opcional)
    stack = [(start, iter(sorted(G.neighbors(start))))]

    while stack:
        v, it = stack[-1]
        try:
            w = next(it)
        except StopIteration:
            stack.pop()
            if stack:
                # passo de volta (backtracking) para o pai no topo da pilha
                walk.append(stack[-1][0])
            continue

        if w not in visited:
            visited.add(w)
            walk.append(w)  # passo adiante
            stack.append((w, iter(sorted(G.neighbors(w)))))

    return walk

walk = dfs_walk(G, start)

# Sanidade: todo passo deve ser por aresta do grafo (sem pulo/diagonal)
assert all(G.has_edge(walk[k], walk[k+1]) for k in range(len(walk)-1))

# Métricas (cobertura e repetições por backtracking)
visitados_unicos = []
seen = set()
for v in walk:
    if v not in seen:
        seen.add(v)
        visitados_unicos.append(v)

cobertura = len(seen) / G.number_of_nodes()
passos_redundantes = len(walk) - len(seen)

print(f"Células livres totais: {G.number_of_nodes()}")
print(f"Células visitadas (únicas): {len(seen)}  -> Cobertura: {cobertura:.1%}")
print(f"Passos totais (com backtracking): {len(walk)}")
print(f"Passos redundantes (revisitas): {passos_redundantes}")

# --- 3) Plot do grid + caminho sem teletransporte ---
fig, ax = plt.subplots(figsize=(6,6))

# desenha células
for i in range(linhas):
    for j in range(colunas):
        # y invertido para origem no canto inferior esquerdo do gráfico
        y = linhas - 1 - i
        if grid[i][j] == 1:
            ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor="tab:blue", edgecolor="black", linewidth=0.5))
        else:
            ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor="white", edgecolor="gray", linewidth=0.5))

# desenha a trilha (consecutivos são vizinhos!)
xs = [c[1] + 0.5 for c in walk]
ys = [linhas - 1 - c[0] + 0.5 for c in walk]
ax.plot(xs, ys, linewidth=2)

# marca início e fim
ax.text(start[1]+0.5, linhas-1-start[0]+0.5, "S", ha="center", va="center", fontsize=10)
end = walk[-1]
ax.text(end[1]+0.5, linhas-1-end[0]+0.5, "F", ha="center", va="center", fontsize=10)

ax.set_xlim(0, colunas)
ax.set_ylim(0, linhas)
ax.set_aspect("equal")
ax.axis("off")
plt.show()
