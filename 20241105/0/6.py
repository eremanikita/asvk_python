class Rectangle:
    rectcnt = 0

    def __init__(self, x1, y1, x2, y2):
        self.__class__.rectcnt += 1
        setattr(self, f"rect_<{self.rectcnt}>", self.rectcnt)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    
    def __str__(self):
        return f"({self.x1},{self.y1})({self.x1},{self.y2})({self.x2},{self.y2})({self.x2},{self.y1})"

    def __lt__(self, other):
        return (self.x2 - self.x1) * (self.y2 - self.y1) < (other.x2 - other.x1) * (other.y2 - other.y1)

    def __eq__(self, other):
        return (self.x2 - self.x1) * (self.y2 - self.y1) == (other.x2 - other.x1) * (other.y2 - other.y1)

    def __mul__(self, other):
        return self.__class__(self.x1 * other, self.y1 * other, self.x2 * other, self.y2 * other)

    __rmul__ = __mul__
    
    def __getitem__(self, other):
        return [(self.x1,self.y1), (self.x1,self.y2), (self.x2,self.y2), (self.x2,self.y1)][other]
