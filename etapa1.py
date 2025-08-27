import random
import time

class Grid:
    def __init__(self, grid_size = 10):
        self.grid_size = grid_size
        self.create_grid()

    def create_grid(self):
            x = random.randrange(self.grid_size)
            y = random.randrange(self.grid_size)
            self.collisions = {"N": 0, "S": 0, "W": 0, "E": 0}
            self.bot = (x, y)   

    def render_grid(self):
        grid = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        ax, ay = self.bot
        grid[ax][ay] = "R"
        print("\n".join(" ".join(row) for row in grid))
        print()

    def move_bot(self, direction):
        x,y = self.bot

        if direction == "N":
            if x == 0:
                self.collisions["N"] = 1
            else:
                x -= 1
        elif direction == "S":
            if x == self.grid_size - 1:
                self.collisions["S"] = 1
            else:
                x += 1
        elif direction == "W":
            if y == 0:
                self.collisions["W"] = 1
            else:
                y -= 1
        elif direction == "E":
            if y == self.grid_size - 1:
                self.collisions["E"] = 1
            else:
                y += 1
        
        self.bot = (x, y)
        self.render_grid()

        done = all(value == 1 for value in self.collisions.values())
        return done
    
def run():
        grid = Grid()
        grid.render_grid()
        directions = ["N", "S", "W", "E"]
        done = False

        while not done:
            direction = random.choice(directions)
            print(f"Movendo para {direction}")
            done = grid.move_bot(direction)
            time.sleep(0.5) 

        print("Todas direções exploradas!")
run()


