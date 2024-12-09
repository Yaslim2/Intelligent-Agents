from typing import List


class Environment():
    def __init__(self, width: int, height: int, obstacles: List[List[int]]) -> None:
        self.width = width
        self.height = height
        self.grid: List[List[str]] = [['0' for _ in range(width)] for _ in range(height)]

        # Adicionar obstáculos ('#') ao ambiente
        for row, col in obstacles:
            if 0 <= row < height and 0 <= col < width:  # Verifica os limites
                self.grid[row][col] = '#'

    def addDirt(self, dirt_columns: List, dirt_rows: List) -> None:
        # Adiciona sujeira ('1') às colunas especificadas
        for col in dirt_columns:
            if 0 <= col < self.width:  # Garante que a coluna está nos limites
                for row in range(self.height):
                    if self.grid[row][col] != '#':  # Não sobrescreve obstáculos
                        self.grid[row][col] = '1'

        # Adiciona sujeira ('1') às linhas especificadas
        for row in dirt_rows:
            if 0 <= row < self.height:  # Garante que a linha está nos limites
                for col in range(self.width):
                    if self.grid[row][col] != '#':  # Não sobrescreve obstáculos
                        self.grid[row][col] = '1'
