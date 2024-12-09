from Environment import Environment
from typing import List, Optional, Tuple
import random


class ModelReactiveAgent():
    def __init__(self, world: Environment, start_position: Optional[List[int]] = None) -> None:
        self.world = world
        self.active = False
        self.cleaned_spots = set()
        self.remaining_dirt = 0
        self.score_1 = 0  # Pontuação baseada em quadrados limpos
        self.score_2 = 0  # Pontuação com penalidade por movimento
        self.movements = 0

        self.position = self.initialize_position(start_position)

    def initialize_position(self, start_position: Optional[List[int]]) -> List[int]:
        """Define a posição inicial do agente."""
        if (
            start_position
            and 0 <= start_position[0] < self.world.width
            and 0 <= start_position[1] < self.world.height
            and self.world.grid[start_position[0]][start_position[1]] != "#"
        ):
            return start_position

        position = [
            random.randint(0, self.world.width - 1),
            random.randint(0, self.world.height - 1),
        ]
        while self.world.grid[position[0]][position[1]] == "#":
            position = [
                random.randint(0, self.world.width - 1),
                random.randint(0, self.world.height - 1),
            ]
        return position

    def count_dirt(self) -> int:
        """Conta todas as células sujas no ambiente."""
        return sum(row.count("1") for row in self.world.grid)

    def valid_position(self, pos: List[int]) -> bool:
        """Verifica se uma posição está dentro dos limites e é válida."""
        return 0 <= pos[0] < self.world.width and 0 <= pos[1] < self.world.height

    def move_to(self, new_position: List[int]) -> None:
        """Move o agente para uma nova posição válida."""
        if self.valid_position(new_position):
            self.position = new_position
            self.movements += 1
            self.score_2 -= 1  # Penalidade por movimento

    def clean(self) -> None:
        """Limpa a posição atual se estiver suja."""
        x, y = self.position
        if self.world.grid[x][y] == "1":
            self.world.grid[x][y] = "0"
            self.remaining_dirt -= 1
            self.score_1 += 1
            self.score_2 += 1
            self.cleaned_spots.add(tuple(self.position))

    def get_adjacent_positions(self) -> List[Tuple[str, List[int]]]:
        """Obtém as posições adjacentes e seus conteúdos."""
        directions = [
            (-1, 0),  # Acima
            (1, 0),  # Abaixo
            (0, -1),  # Esquerda
            (0, 1),  # Direita
            (-1, -1),  # Diagonal superior esquerda
            (-1, 1),  # Diagonal superior direita
            (1, -1),  # Diagonal inferior esquerda
            (1, 1),  # Diagonal inferior direita
        ]
        adjacents = []
        for dx, dy in directions:
            new_pos = [self.position[0] + dx, self.position[1] + dy]
            if self.valid_position(new_pos):
                adjacents.append((self.world.grid[new_pos[0]][new_pos[1]], new_pos))
        return adjacents

    def find_dirt(self) -> Optional[List[int]]:
        """Procura por sujeira nas posições adjacentes."""
        for content, position in self.get_adjacent_positions():
            if content == "1":
                return position
        return None

    def find_empty_spot(self) -> Optional[List[int]]:
        """Procura por uma posição limpa adjacente."""
        clean_positions = [
            pos for content, pos in self.get_adjacent_positions() if content == "0"
        ]
        if clean_positions:
            return random.choice(clean_positions)
        return None

    def startCleaning(self) -> None:
        """Inicia o processo de limpeza."""
        self.active = True
        self.remaining_dirt = self.count_dirt()
        print(f"Manchas de sujeira inicial: {self.remaining_dirt}")
        self.clean()

        while self.active and self.remaining_dirt > 0:
            next_dirt = self.find_dirt()
            if next_dirt:
                self.move_to(next_dirt)
            else:
                next_spot = self.find_empty_spot()
                if next_spot:
                    self.move_to(next_spot)
                else:
                    self.active = False  # Sem lugares para ir, agente para
            self.clean()

        print(f"Limpeza concluída. Pontuação 1: {self.score_1}, Pontuação 2: {self.score_2}")

    def stop(self) -> None:
        """Interrompe o processo de limpeza."""
        self.active = False
