import pygame

from core import constants as const


def point_in_triangle(
    point: pygame.Vector2, triangle: list[pygame.Vector2]
) -> bool:
    """Check if point is inside triangle using barycentric technique"""

    def sign(p1, p2, p3):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    d1 = sign(point, triangle[0], triangle[1])
    d2 = sign(point, triangle[1], triangle[2])
    d3 = sign(point, triangle[2], triangle[0])

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)


class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, radius: float):
        if hasattr(self, 'containers'):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface):
        raise NotImplementedError

    def update(self, dt: float):
        raise NotImplementedError

    def wrap_position(self):
        self.position.x %= const.SCREEN_WIDTH
        self.position.y %= const.SCREEN_HEIGHT

    def collides_with(self, other: 'CircleShape') -> bool:
        distance = self.position.distance_to(other.position)
        r1, r2 = self.radius, other.radius
        return distance < (r1 + r2)
