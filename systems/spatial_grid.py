import pygame
from typing import List, Set, Dict, Tuple
from entities.circleshape import CircleShape


class SpatialGrid:
    """Otimização de colisão usando grid espacial."""

    def __init__(self, cell_size: float = 100.0):
        self.cell_size = cell_size
        self.grid: Dict[Tuple[int, int], List[CircleShape]] = {}
        self.object_cells: Dict[int, Set[Tuple[int, int]]] = {}

    def _get_cell(self, position: pygame.Vector2) -> Tuple[int, int]:
        return (
            int(position.x // self.cell_size),
            int(position.y // self.cell_size),
        )

    def insert(self, obj: CircleShape) -> None:
        cell = self._get_cell(obj.position)
        obj_id = id(obj)

        if cell not in self.grid:
            self.grid[cell] = []
        self.grid[cell].append(obj)

        if obj_id not in self.object_cells:
            self.object_cells[obj_id] = set()
        self.object_cells[obj_id].add(cell)

    def insert_all(self, objects: List[CircleShape]) -> None:
        for obj in objects:
            self.insert(obj)

    def clear(self) -> None:
        self.grid.clear()
        self.object_cells.clear()

    def get_nearby(
        self, position: pygame.Vector2, radius: float
    ) -> List[CircleShape]:
        center_cell = self._get_cell(position)
        radius_in_cells = int(radius // self.cell_size) + 1

        nearby = []
        for dx in range(-radius_in_cells, radius_in_cells + 1):
            for dy in range(-radius_in_cells, radius_in_cells + 1):
                cell = (center_cell[0] + dx, center_cell[1] + dy)
                if cell in self.grid:
                    nearby.extend(self.grid[cell])

        return nearby

    def get_potential_collisions(self, obj: CircleShape) -> List[CircleShape]:
        obj_id = id(obj)
        if obj_id not in self.object_cells:
            return []

        potential = []
        cells = self.object_cells[obj_id]

        for cell in cells:
            if cell in self.grid:
                for other in self.grid[cell]:
                    if other is not obj:
                        potential.append(other)

        return list(set(potential))
