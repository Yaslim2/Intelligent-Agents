from Environment import Environment
from typing import List
import random


class SimpleReactiveAgent():
    def __init__(self, world: Environment, start_position: List = None) -> None:
        self.world = world
        self.active = False
        if start_position and self.is_within_bounds(start_position) and self.world.grid[start_position[0]][start_position[1]] != "#":
            self.current_position = start_position
        else:
            self.current_position = [
                random.randint(0, world.width - 1),
                random.randint(0, world.height - 1),
            ]
        self.score_1 = 0  # Pontos por tiles limpos
        self.score_2 = 0  # Pontuação considerando limpeza e movimentos
        self.movements = 0  # Número de movimentos realizados

    def is_within_bounds(self, position: List) -> bool:
        return 0 <= position[0] < self.world.width and 0 <= position[1] < self.world.height

    def relocate(self, new_position: List) -> None:
        if self.is_within_bounds(new_position):
            self.current_position = new_position
            self.score_2 -= 1  # Penalidade por movimentação
            self.movements += 1

    def clean_tile(self) -> None:
        if self.world.grid[self.current_position[0]][self.current_position[1]] == "1":
            self.world.grid[self.current_position[0]][self.current_position[1]] = "0"
            self.score_1 += 1
            self.score_2 += 1

    def move_left(self):
        self.relocate([self.current_position[0], self.current_position[1] - 1])

    def move_up_left(self):
        self.relocate([self.current_position[0] - 1, self.current_position[1] - 1])

    def move_up(self):
        self.relocate([self.current_position[0] - 1, self.current_position[1]])

    def move_up_right(self):
        self.relocate([self.current_position[0] - 1, self.current_position[1] + 1])

    def move_right(self):
        self.relocate([self.current_position[0], self.current_position[1] + 1])

    def move_down_right(self):
        self.relocate([self.current_position[0] + 1, self.current_position[1] + 1])

    def move_down(self):
        self.relocate([self.current_position[0] + 1, self.current_position[1]])

    def move_down_left(self):
        self.relocate([self.current_position[0] + 1, self.current_position[1] - 1])

    def get_neighbor_value(self, offset_x: int, offset_y: int):
        neighbor_position = [self.current_position[0] + offset_x, self.current_position[1] + offset_y]
        if self.is_within_bounds(neighbor_position):
            return self.world.grid[neighbor_position[0]][neighbor_position[1]]
        return None

    def inspect_neighbors(self) -> None:
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Up-left, Up, Up-right
            (0, -1),          (0, 1),   # Left, Right
            (1, -1), (1, 0), (1, 1),    # Down-left, Down, Down-right
        ]
        for dx, dy in directions:
            if self.get_neighbor_value(dx, dy) == "1":
                self.relocate([self.current_position[0] + dx, self.current_position[1] + dy])
                return

    def find_empty_spot(self):
        free_moves = []
        potential_moves = [
            (self.move_left, 0, -1),
            (self.move_up_left, -1, -1),
            (self.move_up, -1, 0),
            (self.move_up_right, -1, 1),
            (self.move_right, 0, 1),
            (self.move_down_right, 1, 1),
            (self.move_down, 1, 0),
            (self.move_down_left, 1, -1),
        ]
        for move, dx, dy in potential_moves:
            if self.get_neighbor_value(dx, dy) == "0":
                free_moves.append(move)
        if free_moves:
            random.choice(free_moves)()
        else:
            self.active = False

    def startCleaning(self):
        self.active = True
        self.clean_tile()
        while self.active:
            self.inspect_neighbors()
            self.clean_tile()
            self.find_empty_spot()
        return {
            "tiles_cleaned": self.score_1,
            "efficiency_score": self.score_2,
        }

    def stopCleaning(self):
        self.active = False
