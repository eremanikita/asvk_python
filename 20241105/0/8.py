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
    
    def value(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1)    

    def __lt__(self, other):
        return self.value() < other.value()

    def __eq__(self, other):
        return self.value()  == value(other)

    def __mul__(self, other):
        return self.__class__(self.x1 * other, self.y1 * other, self.x2 * other, self.y2 * other)

    __rmul__ = __mul__
    
    def __getitem__(self, other):
        return [(self.x1,self.y1), (self.x1,self.y2), (self.x2,self.y2), (self.x2,self.y1)][other]
    
    def __bool__(self):
        return  bool(self.value())
    
    def __del__(self):
        self.__class__.rectcnt -= 1
        print(self.__class__.rectcnt)
