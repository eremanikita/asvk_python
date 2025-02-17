from sys import argv
from glob import iglob
from os.path import basename

match len(argv):
    case 1:
        print("Ошибка ввода параметров. Должен быть передан путь к репозиторию.")
    case 2:
        for i in iglob(argv[1] + "/refs/heads/*"):
            print(basename(i))
