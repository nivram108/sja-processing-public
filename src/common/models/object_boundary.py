class ObjectBoundary:
    """
    Boundary holds the coordinates of position and the boundaries

    ----

    Attributes:

    center_x: int
      center coordinate of x-axis
    center_y: int
      center coordinate of y-axis
    x_min: int
      left coordinate of x-axis
    y_min: int
      top coordinate of y-axis
    x_max: int
      right coordinate of x-axis
    y_max: int
      bottom coordinate of y-axis
    """

    center_x: int
    center_y: int
    x_min: int
    y_min: int
    x_max: int
    y_max: int

    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.center_x = int((x_min + x_max) / 2)
        self.center_y = int((y_min + y_max) / 2)

    def get_area(self) -> int:
        return (self.x_max - self.x_min) * (self.y_max - self.y_min)

    def get_coords(self) -> tuple[int, int, int, int]:
        return self.x_min, self.y_min, self.x_max, self.y_max

    def is_including(self, other) -> bool:

        return (
                self.x_min <= other.x_min
                and self.x_max >= other.x_max
                and self.y_min <= other.y_min
                and self.y_max >= other.y_max)
