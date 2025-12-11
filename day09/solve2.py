# Okay this is a pretty significant change from part 1
# Basically, now any tiles that are outside the edge of the polygon disqualify a pair of points from being selectable
# So we need a quick way to test if the rectangle touches any illegal tiles
# There are so many edge cases for potential efficient solutions...

# The assumption I didn't realize held here is that every point provided is part of the polygon outline
# I thought that lines could go through the middle of the polygon and we wouldn't reliably have an outline
# But alas the problem is easier than I thought

# so we can do this: from our set of points, create lines from each pair of adjacent points
# these lines form the outline of the polygon, but we don't actually need to trace it
# instead, we form hypothetical rectangles from each other pair of points
# and we test if any lines on the hypothetical rectangle intersect with the real lines, aka the polygon
# If so, the rectangle fails
# If not, the rectangle passes and we can consider its area
# Edge cases are when endpoints intersect, i.e. at (7, 3) in the example
# In this case, we have to check if intersecting line goes toward the middle of our hypothetical rectangle
# If it does, the rectangle fails
# THis all basically works because the lines are perpendicular and its very easy to compute if they intersect in O(1) time per line

# But wait, there's more! I think we can actually do this even simpler
# Instead of the real rectangle, we can check for any intersections between all the lines 1 cell inside 
# the rectangle. This should handle all cases in one check.

import argparse
from dataclasses import dataclass
from itertools import combinations

TEST_SOLUTION = 24

@dataclass
class Point:
    x: int
    y: int

    def __lt__(self, other: "Point"):
        return (self.x, self.y) < (other.x, other.y)

    def __gt__(self, other: "Point"):
        return (self.x, self.y) > (other.x, other.y)
    
    def __eq__(self, other: "Point"):
        return self.x == other.x and self.y == other.y

@dataclass
class Line:
    a: Point
    b: Point

    def __post_init__(self):
        if self.a > self.b:
            self.a, self.b = self.b, self.a

    def intersects(self, other: "Line") -> bool:
        """Check for any intersection, including single points."""
        return (
            (self.a.x <= other.a.x <= other.b.x <= self.b.x) and (other.a.y <= self.a.y <= self.b.y <= other.b.y)
            or (self.a.y <= other.a.y <= other.b.y <= self.b.y) and (other.a.x <= self.a.x <= self.b.x <= other.b.x)
        )

@dataclass
class Rectangle:
    lower_left: Point
    upper_left: Point
    lower_right: Point
    upper_right: Point

    @classmethod
    def from_corners(cls, corner1: Point, corner2: Point):
        corner3 = Point(corner1.x, corner2.y)
        corner4 = Point(corner2.x, corner1.y)
        return cls(*sorted([corner1, corner2, corner3, corner4]))
    
    def is_valid_by_lines(self, lines: list[Line]):
        """Check if a minimum inscribed rectangle intersects with any lines. If so it is invalid."""
        inscribed_ll = Point(self.lower_left.x+1, self.lower_left.y+1)
        inscribed_ul = Point(self.upper_left.x+1, self.upper_left.y-1)
        inscribed_lr = Point(self.lower_right.x-1, self.lower_right.y+1)
        inscribed_ur = Point(self.upper_right.x-1, self.upper_right.y-1)
        # rectangle was too narrow to compute area
        #if inscribed_ll > inscribed_ul or inscribed_ll > inscribed_lr:
        #    return False
        inscribed_lines = (
            Line(inscribed_ul, inscribed_ur),
            Line(inscribed_ll, inscribed_lr),
            Line(inscribed_ll, inscribed_ul),
            Line(inscribed_lr, inscribed_ur),
        )
        for line in lines:
            for border in inscribed_lines:
                if border.intersects(line):
                    return False
        return True

    @property
    def area(self) -> int:
        return (self.upper_right.x - self.upper_left.x + 1) * (self.upper_left.y - self.lower_left.y + 1)


def prep_input(lines: list[str]) -> list[Point]:
    points = [Point(*(map(int, line.split(",")))) for line in lines]
    return points

def make_lines(points: list[Point]) -> list[Line]:
    """Build a set of lines from the set of points. Each adjacent point forms a line and the list wraps."""
    lines = []
    for i in range(len(points)):
        # sort points to help later
        lines.append(Line(*sorted([points[i-1], points[i]])))
    return lines


def solve(points: list[Point]) -> int:
    lines = make_lines(points)
    print(f"Made {len(lines)} lines from {len(points)} points")
    
    rectangles = [Rectangle.from_corners(p1, p2) for p1, p2 in combinations(points, r=2)]
    print(f"Made {len(rectangles)} rectangles from {len(lines)} lines")

    for rectangle in sorted(rectangles, key=lambda r: r.area, reverse=True):
        if rectangle.is_valid_by_lines(lines):
            print(rectangle, "matches")
            return rectangle.area

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        inf = "test.txt"
    else:
        inf = "input.txt"

    with open(inf, "r") as inf:
        lines = [line.strip() for line in inf.readlines()]
    
    solution = solve(prep_input(lines))

    print(f"Output: {solution}")
    if args.test:
        if solution == TEST_SOLUTION:
            print("Correct!")
        else:
            print(f"Incorrect! Expected {TEST_SOLUTION}")