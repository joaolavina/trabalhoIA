import random
import networkx as nx
import matplotlib.pyplot as plt

class GridGraph:
    def __init__(self, grid_size=random.randrange(4,20)):
        self.grid_size = grid_size
        self.graph = nx.grid_2d_graph(grid_size, grid_size)
        self.bot = (random.randrange(grid_size), random.randrange(grid_size))
        self.pos = {(x, y): (y, -x) for x, y in self.graph.nodes()}
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.render_graph()

    def render_graph(self):
        self.ax.clear()
        nx.draw(
            self.graph, self.pos, ax=self.ax,
            node_size=100, node_color="lightgray", edge_color="lightgray"
        )
        nx.draw_networkx_nodes(
            self.graph, self.pos, nodelist=[self.bot],
            node_color="red", node_size=300, ax=self.ax
        )
        self.ax.set_title("Movimento do Robô na Grid")
        plt.draw()
        plt.pause(0.2)

    def move_until_wall(self, direction):
        x, y = self.bot
        steps = 0
        while True:
            if direction == "N":
                new_pos = (x-1, y)
            elif direction == "S":
                new_pos = (x+1, y)
            elif direction == "W":
                new_pos = (x, y-1)
            elif direction == "E":
                new_pos = (x, y+1)
            else:
                break

            if not self.graph.has_node(new_pos):
                break
            self.bot = new_pos
            x, y = self.bot
            steps += 1
            self.render_graph()
        return steps

def run():
    grid = GridGraph()
    grid.move_until_wall("N")
    grid.move_until_wall("W")
    casas_leste = grid.move_until_wall("E")
    casas_sul = grid.move_until_wall("S")
    largura = grid.grid_size
    altura = grid.grid_size
    print(f"Tamanho da grid: {largura} x {altura}")
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    run()
