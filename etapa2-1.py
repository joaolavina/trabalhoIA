import random
import time


class Grid:
    def __init__(self, grid_size = 10):
        self.grid_size = grid_size
        self.create_grid()

    def create_grid(self):
        self.grid = [
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
        ]

        self.bot = (0,0)        

        self.bot = (random.randrange(self.grid_size), random.randrange(self.grid_size))

    def render_grid(self):
        print("\n".join(" ".join(row) for row in self.grid))
        print("\n")
    
    def is_valid_move(self, x, y):
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            return False
        return True

    def move_bot(self, direction):
        old_x, old_y = self.bot
        new_x, new_y = old_x, old_y

        if direction == "N":
            new_x -= 1
        elif direction == "S":
            new_x += 1
        elif direction == "W":
            new_y -= 1
        elif direction == "E":
            new_y += 1
        
        if self.is_valid_move(new_x, new_y):
            self.grid[old_x][old_y] = "V"
            self.grid[new_x][new_y] = "A"
            self.bot = (new_x, new_y)
            return True
        return False

def run_model_based_agent():
    grid = Grid()
    
    steps = 0
    max_steps = 200
        
    grid.grid[grid.bot[0]][grid.bot[1]] = "A"
    grid.render_grid()

    while steps < max_steps:        
        current_x, current_y = grid.bot
        
        possible_moves = []
        directions = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}

        for direction, (dx, dy) in directions.items():
            new_x, new_y = current_x + dx, current_y + dy
            if grid.is_valid_move(new_x, new_y) and grid.grid[new_x][new_y] == ".":
                possible_moves.append(direction)
        
        if possible_moves:
            next_direction = random.choice(possible_moves)
        else:
        
            possible_moves_visited = []
            for direction, (dx, dy) in directions.items():
                new_x, new_y = current_x + dx, current_y + dy
                if grid.is_valid_move(new_x, new_y):
                    possible_moves_visited.append(direction)
            if possible_moves_visited:
                 next_direction = random.choice(possible_moves_visited)
            else:
                break

        grid.move_bot(next_direction)
        grid.render_grid()
        time.sleep(0.5)    
   
run_model_based_agent()
