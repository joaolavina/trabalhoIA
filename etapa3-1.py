import csv

def read_dfs_path(file_path, start_node, end_node):

    path = []
    found_start = False
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        
        for row in reader:
            step, r, c = row
            node = (int(r), int(c))
            
            if node == start_node:
                found_start = True
            
            if found_start:
                path.append(node)
                
            if node == end_node:
                break
                
    return path

start_node = (0, 0)
end_node = (7, 7)

dfs_path = read_dfs_path('caminho_et2-1.csv', start_node, end_node)

print(f"Path from {start_node} to {end_node}: {dfs_path}")