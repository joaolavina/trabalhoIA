import matplotlib.pyplot as plt
import matplotlib.animation as animation

from heapq import heappush, heappop

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
start_node = (0, 5)
end_node = (10, 5)
dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def in_bounds(i, j):
    return 0 <= i < linhas and 0 <= j < colunas

def passable(i, j):
    return in_bounds(i, j)

def dijkstra_grid(start, goal):
    pq = []
    heappush(pq, (0, start, None))
    came_from = {}
    g_score = {start: 0}

    while pq:
        g, current, parent = heappop(pq)
        if current in came_from:
            continue
        came_from[current] = parent

        if current == goal:
            path = []
            cur = current
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
            return path

        ci, cj = current
        for di, dj in dirs4:
            ni, nj = ci + di, cj + dj
            neighbor = (ni, nj)
            if not passable(ni, nj):
                continue
            tentative_g = g + grid[ni][nj]
            if neighbor in g_score and tentative_g >= g_score[neighbor]:
                continue
            g_score[neighbor] = tentative_g
            heappush(pq, (tentative_g, neighbor, current))

    return None

def calculate_cost(path, grid_map):
    if not path:
        return 0
    return sum(grid_map[i][j] for (i, j) in path)

path = dijkstra_grid(start_node, end_node)
total_cost = calculate_cost(path, grid)

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

ax.text(start_node[1] + 0.5, linhas - 1 - start_node[0] + 0.5, "i", ha="center", va="center", fontsize=12, weight="bold", color="red")
ax.text(end_node[1] + 0.5, linhas - 1 - end_node[0] + 0.5, "f", ha="center", va="center", fontsize=12, weight="bold", color="red")

line, = ax.plot([], [], 'o-', color='red', linewidth=2)

def update_anim(k):
    sub = path[:k+1]
    xs = [c + 0.5 for (_, c) in sub]
    ys = [linhas - 1 - r + 0.5 for (r, _) in sub]
    line.set_data(xs, ys)
    return (line,)

ax.set_xlim(0, colunas)
ax.set_ylim(0, linhas)
ax.set_aspect('equal')
ax.axis('off')

ani = animation.FuncAnimation(fig, update_anim, frames=len(path), interval=200, blit=False, repeat=False)
plt.show()
