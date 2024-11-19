class Sender:
    flag = False

    @classmethod
    def report(cls):
        if not cls.flag:
            print("Greetings!")
            cls.flag = True
        else:
            print("Get away!")


class Asker:
    @staticmethod
    def askall(lst):
        for i in lst:
            i.report()


lst = [Sender() for i in range(5)]
a = Asker()
a.askall(lst)

