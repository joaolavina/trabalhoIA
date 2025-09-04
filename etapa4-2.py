import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Geração da grid com custos de caminhada

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

# Teste de limites da grid

def dentro_grid(i, j):
    return 0 <= i < linhas and 0 <= j < colunas

# Busca com conhecimento local

def busca_gulosa_local(inicio, fim):
    # Inicia a lista de caminho com a posição inicial
    caminho = [inicio]
    atual = inicio
    
    # Cria um conjunto para armazenar casas já visitadas
    visitado = set()
    visitado.add(atual)
    
    # Enquanto não chegar na casa alvo
    while atual != fim:
        ci, cj = atual  
        vizinhos = []
        
        # Percorre as direções possíveis
        for di, dj in direcoes:
            ni, nj = ci + di, cj + dj   # calcula nova posição
            
            # Verifica se a posição está dentro da grid e ainda não foi visitada
            if dentro_grid(ni, nj) and (ni, nj) not in visitado: 
                custo = grid[ni][nj] 
                distancia = abs(ni - fim[0]) + abs(nj - fim[1])  
                # Armazena custo, distância e coordenadas do vizinho
                vizinhos.append((custo, distancia, (ni, nj)))
        
        # Se não houver vizinhos válidos, encerra a busca
        if not vizinhos:
            break
        
        # Ordena os vizinhos pelo menor custo e menor distância
        vizinhos.sort()
        
        # Escolhe a melhor próxima casa
        proxima_casa = vizinhos[0][2]
        
        # Adiciona ao caminho e marca como visitado
        caminho.append(proxima_casa)
        visitado.add(proxima_casa)
        
        # Atualiza a posição atual
        atual = proxima_casa

    return caminho

def calcular_custo(caminho, grid_map):
    # Se o caminho for vazio, o custo é zero
    if not caminho:
        return 0
    # Soma o custo de todas as posições visitadas no caminho
    return sum(grid_map[i][j] for (i, j) in caminho)

# Executa a busca gulosa do ponto inicial até o final

caminho = busca_gulosa_local(inicio, fim)

# Calcula o custo total do caminho encontrado

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
