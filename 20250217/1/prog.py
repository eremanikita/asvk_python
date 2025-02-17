from sys import argv
from glob import iglob
from os.path import basename


def find_branches(repo_link):
    return iglob(repo_link + "/refs/heads/*")


match len(argv):
    case 1:
        print("Ошибка ввода параметров. Должен быть передан путь к репозиторию.")
    case 2:
        for branch in find_branches(argv[1]):
            print(basename(branch))
