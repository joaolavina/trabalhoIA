import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv

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

for i in range(linhas):
    for j in range(colunas):
        if grid[i][j] == 0:
            G.add_node((i, j))
            for di, dj in dirs4:
                ni, nj = i + di, j + dj
                if 0 <= ni < linhas and 0 <= nj < colunas and grid[ni][nj] == 0:
                    G.add_edge((i, j), (ni, nj))

start = (0, 0)

def dfs_walk_generator(G, start):
    visited = {start}
    yield start
    stack = [(start, iter(sorted(G.neighbors(start))))]

    while stack:
        v, it = stack[-1]
        try:
            w = next(it)
        except StopIteration:
            stack.pop()
            if stack:
                yield stack[-1][0]
            continue

        if w not in visited:
            visited.add(w)
            yield w
            stack.append((w, iter(sorted(G.neighbors(w)))))


path_gen = dfs_walk_generator(G, start)
dfs_path = list(path_gen)

csv_file_path = 'caminho_et2-1.csv'
with open(csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['step', 'node_row', 'node_col'])
    for i, node in enumerate(dfs_path):
        writer.writerow([i, node[0], node[1]])


fig, ax = plt.subplots(figsize=(6, 6))

for i in range(linhas):
    for j in range(colunas):
        y = linhas - 1 - i
        if grid[i][j] == 1:
            ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor="tab:blue", edgecolor="black", linewidth=0.5))
        else:
            ax.add_patch(plt.Rectangle((j, y), 1, 1, facecolor="white", edgecolor="gray", linewidth=0.5))

ax.text(start[1] + 0.5, linhas - 1 - start[0] + 0.5, "I", ha="center", va="center", fontsize=10, weight="bold")

line, = ax.plot([], [], 'o-', color='red', linewidth=2)

path_gen_anim = dfs_walk_generator(G, start)

def update(frame):
    global line
    try:
        current_node = next(path_gen_anim) # Use the new generator
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

ani = animation.FuncAnimation(fig, update, frames=G.number_of_nodes() * 2,
                                  interval=100, blit=True, repeat=False)

plt.show()