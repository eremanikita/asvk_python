import zlib
from sys import argv
from glob import iglob
from os.path import basename
from pathlib import Path


def find_branches(repo_link):
    return iglob(repo_link + "/refs/heads/*")


def get_last_commit_hash(branches_list, branch_name):
    for branch in branches_list:
        if basename(branch) == branch_name:
            required_branch = branch
            break
    else:
        print(f"Не найдено ветки {branch_name}.")
        exit()

    with open(required_branch, "r") as f:
        return f.read().rstrip()


match len(argv):
    case 1:
        print("Ошибка ввода параметров. Должен быть передан путь к репозиторию.")
    case 2:
        for branch in find_branches(argv[1]):
            print(basename(branch))
    case 3:
        last_commit = get_last_commit_hash(find_branches(argv[1]), argv[2])

        commit_object = zlib.decompress(
            Path(argv[1] + f"/objects/{last_commit[:2]}/{last_commit[2:]}").read_bytes())
        head, _, blob = commit_object.partition(b'\x00')
        blob = blob.decode()
        print(blob)
