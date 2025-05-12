import math
import matplotlib.pyplot as plt

class Point:
    def __init__(self, input1, input2):
        self.x = input1
        self.y = input2

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other_point):
        dx = self.x - other_point.x
        dy = self.y - other_point.y
        return math.sqrt(dx**2 + dy**2)

    def draw_vector(self, color='blue'):
        plt.figure()
        plt.axhline(0, color='gray', linewidth=0.5)
        plt.axvline(0, color='gray', linewidth=0.5)
        plt.quiver(0, 0, self.x, self.y, angles='xy', scale_units='xy', scale=1, color=color)
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.grid(True)
        plt.title(f"Vector from (0,0) to ({self.x}, {self.y})")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()