from sys import stdin

def calc_vec(point1, point2, other):
    return (point1[0] - other[0]) * (point2[1] - other[1]) - (point2[0] - other[0]) * (point1[1] - other[1])


def if_intersect(object1, object2):
    for i in object1.point1, object1.point2, object1.point3:
        flag = True
        tmp = calc_vec(object2.point1, object2.point2, i)
        if tmp * calc_vec(object2.point2, object2.point3, i) < 0:
            flag = False
        if tmp * calc_vec(object2.point3, object2.point1, i) < 0:
            flag = False
        if flag:
            return True
    return False


class Triangle:
    def __init__(self, point1, point2, point3):
        self.point1 = tuple(point1)
        self.point2 = tuple(point2)
        self.point3 = tuple(point3)

    def __abs__(self):

        return abs((self.point1[0] * (self.point2[1] - self.point3[1]) + self.point2[0] * (
                self.point3[1] - self.point1[1]) + self.point3[0] * (self.point1[1] - self.point2[1]))) / 2

    def __bool__(self):
        return bool(abs(self))

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __contains__(self, item):
        if not abs(item):
            return True
        if not abs(self):
            return False
        for i in item.point1, item.point2, item.point3:
            tmp = calc_vec(self.point1, self.point2, i)
            if tmp * calc_vec(self.point2, self.point3, i) < 0:
                return False
            if tmp * calc_vec(self.point3, self.point1, i) < 0:
                return False
        return True

    def __and__(self, item):
        if not abs(self) or not abs(item):
            return False

        return if_intersect(self, item) or if_intersect(item, self)


exec(stdin.read())
